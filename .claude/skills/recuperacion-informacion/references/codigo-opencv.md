# Recetas de código Python + OpenCV del curso

Extraídas de `Codigos/`: `Anexo 01.2-Ejemplos OpenCV (python)/ejemplo{1,2,3}.py`,
`Anexo 01.3-Procesamiento de imagenes.ipynb`, `Anexo 02.1-Deteccion de bordes en python.ipynb`,
`Anexo 02.2-Ejemplo descriptores globales gris.ipynb`,
`Anexo 03.1-Ejemplo descriptores globales color.ipynb`.

Ambiente: `conda create -n inf3841` + `pip install opencv-contrib-python jupyter scipy
scikit-learn pandas matplotlib PySide6`.

**Recordatorio para las tareas:** se entregan **solo `.py`** ejecutables desde línea de comandos
(los notebooks son material de ejemplo, no formato de entrega), y un evaluador automático las corre.

## 1. Leer imagen, gris, Otsu

```python
import sys, cv2

img_color = cv2.imread(filename, cv2.IMREAD_COLOR)   # siempre 3 canales BGR
if img_color is None:
    sys.exit()
img_gris = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
thresh, img_bin = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imshow("bin", img_bin); cv2.waitKey(0); cv2.destroyAllWindows()
```

## 2. Video o webcam

```python
capture = cv2.VideoCapture(int(arg)) if arg.isdigit() else cv2.VideoCapture(arg)
# en Windows la webcam se abre con cv2.VideoCapture(id, cv2.CAP_DSHOW)
while capture.grab():
    retval, frame = capture.retrieve()
    if not retval:
        continue
    ...
    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:   # q o ESC
        break
capture.release(); cv2.destroyAllWindows()
```

`ejemplo3.py` añade un detector Haar: `cv2.CascadeClassifier`, `detector.load(cv2.data.haarcascades +
xml)`, `detector.detectMultiScale(gris, scale_factor, min_neighbors)` — `scale_factor` 1.01 lento /
1.1 normal / 1.5 rápido; `min_neighbors` 1 ruidoso / 5 confiable / 20 seguro.

## 3. Filtros

```python
imagen_eq       = cv2.equalizeHist(imagen_gris)
imagen_gaussian = cv2.GaussianBlur(imagen_gris, (9, 9), 0)
imagen_median   = cv2.medianBlur(imagen_gris, 9)
kernel          = numpy.ones((3, 3), numpy.float32) / 9
imagen_conv     = cv2.filter2D(imagen_gris, -1, kernel)   # ¡correlación, no convolución!
# para convolución real: kernel = cv2.flip(kernel, flipCode=-1)  (o scipy.signal.convolve2d)
```

## 4. Bordes

```python
sobelX = cv2.Sobel(gris, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=3)
sobelY = cv2.Sobel(gris, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=3)
magnitud = numpy.sqrt(numpy.square(sobelX) + numpy.square(sobelY))
aprox    = numpy.abs(sobelX) + numpy.abs(sobelY)
_, bordes = cv2.threshold(magnitud, thresh=51, maxval=255, type=cv2.THRESH_BINARY)

canny = cv2.Canny(gris, threshold1=51, threshold2=301)

blur1, blur2 = cv2.GaussianBlur(gris, (3,3), 0), cv2.GaussianBlur(gris, (13,13), 0)
dog = cv2.subtract(blur1, blur2)

def normalizarMax255(imagen, valorAbsoluto=False):      # solo para visualizar CV_32F
    if valorAbsoluto:
        imagen = numpy.abs(imagen)
    return cv2.normalize(imagen, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
```

## 5. Esqueleto de comparación de descriptores

El patrón que se repite en todos los notebooks:

```python
def calcular_descriptores(funcion_descriptor, nombres, imagenes_dir):
    matriz = None
    for i, nombre in enumerate(nombres):
        d = funcion_descriptor(nombre, imagenes_dir)
        if matriz is None:
            matriz = numpy.zeros((len(nombres), len(d)), numpy.float32)
        matriz[i] = d
    return matriz

matriz_distancias = scipy.spatial.distance.cdist(descriptores, descriptores, metric='euclidean')
# metric: 'euclidean' (L2) | 'cityblock' (L1) | 'hamming'

numpy.fill_diagonal(matriz_distancias, numpy.inf)     # que el más cercano no sea uno mismo
posiciones = numpy.argmin(matriz_distancias, axis=1)
ok = query[:-5] == mas_cercano[:-5]                   # 'tigre1.jpg' vs 'tigre2.jpg'
```

`cdist(A, B)` con A de `n×d` y B de `m×d` devuelve una matriz `n×m` con la distancia de cada fila de
A contra cada fila de B.

## 6. Descriptores implementados en clase

```python
# vector de intensidades (4x4 = 16 dims), L2
imagen = cv2.imread(archivo, cv2.IMREAD_GRAYSCALE)
descriptor = cv2.resize(imagen, (4, 4), interpolation=cv2.INTER_AREA).flatten()

# OMD, Hamming
posiciones = numpy.argsort(descriptor)
for i in range(len(posiciones)):
    descriptor[posiciones[i]] = i

# histogramas por zona (2x2 zonas x 8 bins = 32 dims), L1
zona = imagen[desde_y:hasta_y, desde_x:hasta_x]
histograma, limites = numpy.histogram(zona, bins=8, range=(0, 255))
histograma = histograma / numpy.sum(histograma)

# HOG (2x2 zonas x 9 bins en [-90,90] = 36 dims), L1
imagenBlur = cv2.GaussianBlur(imagen, (5, 5), 0, 0)
sobelX = cv2.Sobel(imagenBlur, cv2.CV_32F, 1, 0, ksize=3)
sobelY = cv2.Sobel(imagenBlur, cv2.CV_32F, 0, 1, ksize=3)
magnitud = numpy.sqrt(numpy.square(sobelX) + numpy.square(sobelY))
_, imagen_bordes = cv2.threshold(magnitud, 150, 255, cv2.THRESH_BINARY)
mascara = imagen_bordes == 255
angulos = numpy.arctan2(sobelY, sobelX, where=mascara, out=None)
# por zona: grados con math.degrees(), llevar a (-90,90], numpy.histogram(..., range=(-90,90))

# histograma de color 1D por canal (3x1D) — no representa colores
hist = cv2.calcHist([canal], [0], None, [nbins], (0, 256)).flatten()
hist = hist / numpy.sum(hist)

# histograma de color 3D (nbins^3 dims), L1
hist = cv2.calcHist([imagen_zona], [0, 1, 2], None,
                    [nbins, nbins, nbins], [0, 256, 0, 256, 0, 256]).flatten()
hist = hist / numpy.sum(hist)
```

Utilidad para dividir rangos en tramos (bins de histograma o zonas de la imagen):

```python
def calcular_limites(maximo_no_incluido, cantidad):
    lista = [round(maximo_no_incluido * i / cantidad) for i in range(cantidad)]
    lista.append(maximo_no_incluido)
    return lista        # calcular_limites(256, 2) -> [0, 128, 256]
```

## 7. Notas prácticas
- Todos los notebooks tienen una bandera `mostrar_imagenes = True`; ponerla en `False` para correr
  rápido sin ventanas.
- Los datos de prueba son `Codigos/imagenes/*.jpg`: pares `estatua`, `luna`, `mano`, `palmas`, `puc`,
  `tigre`, `torres` (la respuesta correcta de cada imagen es su par).
- Ejercicios propuestos por el profesor: ajustar el número de zonas y de bins de cada descriptor y
  ver cuál mejora el porcentaje de aciertos; revisar con qué descriptor cada imagen encuentra a su
  par.
