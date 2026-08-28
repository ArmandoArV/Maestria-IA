# Clase 1 — Fundamentos de RI y Procesamiento de Imágenes

Fuentes: `Slides 01.1-Introducción a la Recuperación de Información.pdf`,
`Slides 01.2-Procesamiento de imágenes.pdf`, `Slides 01.3-Introducción a OpenCV.pdf`,
`Anexo 01.1-Configurar ambiente Python.md`, `Anexo 01.3-Procesamiento de imagenes.ipynb`.

## 1. Recuperación de Información

**Information Retrieval:** estudia cómo representar, organizar, almacenar y acceder a la información
existente en documentos, y cómo *recuperar* los documentos relevantes a la necesidad de información
del usuario. Documentos clásicos: páginas web, emails, fichas de biblioteca, libros. Consultas:
frases, keywords, preguntas.

Dos conceptos que definen la disciplina:
- **Relevancia** — cuantificar cuán útil es un documento para satisfacer la necesidad del usuario.
- **Ranking** — ordenar los documentos según su relevancia a la consulta.

**Buscador vs. base de datos**

| | Base de datos | Recuperación de Información |
|---|---|---|
| Qué devuelve | *todos* los elementos que cumplen una condición | *los mejores* elementos según la necesidad |
| Cómo se consulta | condición exacta (SQL) | consulta imprecisa, resultado ordenado |
| Garantías | transacciones ACID | relevancia y ranking |

### RI Multimedia (RIM)
Desde 2016 más del 70% del tráfico de Internet son videos: audio, imágenes y video son una "caja
negra" de la que solo se indexan metadatos. RIM estudia cómo recuperar archivos multimedia
relevantes analizando su **contenido** (pixeles, samples de audio, frames), **sin** depender de
metadatos (tags, EXIF, ID3, textos asociados).

Tipos de consulta: por **texto** (keywords/preguntas), **by-example** (buscar algo parecido a un
documento modelo), **by-sketch** (buscar usando un bosquejo).

**Descripción de contenido:** cada documento se representa por uno o más **vectores** mediante
extracción de características. Comparar documentos = comparar vectores con una función de distancia.

**Áreas involucradas:**
1. Análisis de contenido multimedia (imágenes, audio, video, texto).
2. Estructuras de datos: algoritmos eficientes, métodos de búsqueda, **índices** para resolver k-NN
   sobre millones de vectores en espacios vectoriales y métricos.
3. IA y ciencia de datos: clustering, clasificadores, redes neuronales.
4. Interfaces humano-computador: ingresar consultas, mostrar resultados, recibir feedback.

**Casos de estudio vistos en clase**
1. Dada una imagen de consulta, buscar imágenes parecidas en una colección (color, forma, etc.).
2. Reconocer la aparición de un objeto de un catálogo dentro de una foto (impresee.com).
3. Identificar el origen de un trozo de audio en una base de canciones ("Shazam").
4. *Copy detection* de video: determinar de qué escena original proviene cada segmento (P-VCD).
5. Buscar apariciones de un producto o logo en televisión a partir de ejemplos visuales (VGG
   Video Google).
6. Búsqueda semántica por texto en imágenes/videos sin etiquetar ("jirafas comiendo").

## 2. Imágenes

Una imagen es una **señal bidimensional discretizada**. Cada valor es un **pixel** (picture element).
Atributos: ancho (x), alto (y), **canales** (1, 3 ó 4), **profundidad** (usualmente entero de 8 bits
sin signo por canal) y ubicación del origen (usualmente superior izquierda).

Procesamientos comunes: blur/desenfoque, smoothing, sharp, eliminación de ruido, resize, crop,
ajuste de brillo/contraste.

## 3. Operadores punto a punto

`G(i,j) = h( I(i,j) )` — cada pixel se modifica de forma independiente. `h()` depende del valor del
pixel y puede depender globalmente de `I`. Para 8 bits, `h()` se implementa como una **tabla de 256
entradas** calculada una sola vez al inicio.

- **Brillo/contraste:** `G = a·I + b` (ajuste lineal).
- **Corrección gamma:** `G = I^(1/γ)`, típicamente `γ = 2.2` (ajuste no lineal).

### Histograma
Contar cuántos pixeles de la imagen tienen cada valor de intensidad. Cada contador es un **bin**.
Con **normalización** (los bins suman 1) el histograma se interpreta como la **probabilidad** de que
un pixel tenga cierto valor de gris.

Efecto de las operaciones sobre el histograma:
- Aumentar brillo (`b + 60`) → el histograma se **desplaza** hacia la derecha.
- Bajar contraste (`b × 0.75`) → el histograma se **comprime**.
- Invertir (`255 − b`) → el histograma se **refleja**.
- **Ecualización** → reasignar los grises para lograr una distribución cercana a **uniforme**
  (`cv2.equalizeHist`).

### Binarización / umbral (threshold)
Comparar cada pixel contra una constante (umbral). Según sea mayor o menor se asigna un nuevo valor:
blanco, negro, el valor original o el propio umbral → variantes binary, binary inverted, truncate.

**Algoritmo de Otsu** — cómo elegir el umbral automáticamente. Se asume que la imagen tiene pixeles
de fondo y de primer plano, y que en el histograma se distinguen dos conjuntos. Se prueban todos los
umbrales posibles y se elige el que **minimiza la varianza intra-clase**:

```
P_blanco · σ²_blanco  +  P_negro · σ²_negro
```

En OpenCV: `cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)` (devuelve el umbral
elegido como primer valor de retorno).

## 4. Operadores lineales: convolución

El nuevo pixel es la **suma ponderada de una ventana de pixeles**; los pesos son el **kernel** o
**máscara**, de tamaño impar, con un centro definido.

- 2D discreto: `G(x,y) = Σ_i Σ_j K(i,j) · I(x−i, y−j)`.
- **Correlación vs. convolución:** la correlación desliza el kernel tal cual; la convolución lo
  **refleja** primero (180°). Coinciden si el kernel es simétrico. `cv2.filter2D()` implementa
  **correlación**: para convolución hay que reflejar antes con `cv2.flip(kernel, flipCode=-1)`
  (y mover el centro si el kernel es de tamaño par). `scipy.signal.convolve2d()` sí es convolución.
- Propiedades: conmutativa, asociativa, distributiva, lineal; permite descomponer filtros
  (**separabilidad**: un kernel 2D separable = dos convoluciones 1D, mucho más barato).
- **Bordes:** por defecto OpenCV usa `BORDER_REFLECT_101` (`gfedcb | abcdefgh | gfedcba`). Afecta
  pocos pixeles, salvo en imágenes muy pequeñas.

### Blur / smooth (pasa-bajos)
Propiedades deseables del kernel: **normalizado** (suma 1), **simétrico**, **decreciente** hacia los
extremos, que considere todas las celdas, idealmente circular.

- **Promedio:** `ones((n,n))/n²`.
- **Gaussiano** 1D y 2D: `G(x,y,σ) = (1/2πσ²)·exp(−(x²+y²)/2σ²)`. Separable.
  `cv2.GaussianBlur(img, (9,9), 0)`.

Uso típico: blur promedio 15×15 + umbral para eliminar detalle antes de segmentar.

## 5. Operadores no lineales

- **Filtro de mediana:** deslizar una ventana n×n (n impar); el nuevo `I(x,y)` es la **mediana** de
  los n·n valores (ordenarlos y tomar el de la posición `(n·n+1)/2`). Elimina el ruido **sal y
  pimienta**. Siempre selecciona un gris que ya existe en la imagen, rara vez el mínimo o el máximo,
  y tiende a producir regiones planas. `cv2.medianBlur(img, 9)`.
- **Filtro promedio descartando percentiles** menores y mayores.
- **Filtro bilateral:** promedia descartando los pixeles que "difieren mucho" dentro de la ventana
  (suaviza sin borrar bordes).
- **Adaptive threshold:** binarizar con un umbral que es función de la vecindad de cada pixel.

### Filtros morfológicos (sobre imágenes binarias 0/1)
Con un **structuring element** de tamaño S×S lleno de 1:

| Operación | Definición del curso |
|-----------|----------------------|
| **Dilation** | convolución y binarizar con umbral **1** (basta un vecino encendido) |
| **Erosion** | convolución y binarizar con umbral **S** (todas las celdas del elemento) |
| **Majority** | convolución y binarizar con umbral **S/2** |
| **Opening** | `dilate(erode(imagen))` — elimina puntos aislados |
| **Closing** | `erode(dilate(imagen))` — rellena huecos |

## 6. OpenCV

- Software libre (BSD), API para C, C++, Python y Java; multiplataforma. Versión usada en el curso:
  4.13.0 (marzo 2026); el anexo advierte que al instalar hoy puede llegar OpenCV 5.0 con Python 3.14.
- **En C++:** namespace `cv`, tipo `cv::Mat` = encabezado con dimensiones + puntero al buffer de
  pixeles. Acceso `m.at<uchar>(y,x)` (1 canal 8 bits) o `m.at<cv::Vec3b>(y,x)` (3 canales 8 bits).
  **Copiar un `cv::Mat` o seleccionar una región solo duplica el header, no el buffer** → usar
  `.clone()` para duplicar pixeles. Las funciones reciben imagen de entrada y salida; si la salida ya
  tiene buffer se reutiliza, y si es la misma que la entrada el procesamiento es *in-place*.
- **En Python:** las imágenes **son matrices NumPy**; se prefiere NumPy sobre las utilidades de
  matrices de C++. Orden de canales **BGR**, no RGB.
- Instalación del curso:
  ```
  conda create -n inf3841
  conda activate inf3841
  conda install python
  pip install opencv-contrib-python
  pip install jupyter scipy scikit-learn pandas matplotlib PySide6
  ```
  El anexo recomienda **MiniForge** (repositorio `conda-forge`, libre) por sobre Anaconda/MiniConda,
  y bajar a `python=3.11` si hay incompatibilidades. IDEs sugeridos: Spyder, PyCharm CE, VS Code
  (configurar el intérprete al ambiente `inf3841`; formatear con Black / Ctrl+Alt+L).
- Documentación: https://docs.opencv.org/4.13.0/ — módulos `core`, `imgproc_filter`, `videoio`.
