# Clase 2 — Detección de Bordes

Fuente: `Slides 02.1-Detección de bordes.pdf`, `Anexo 02.1-Deteccion de bordes en python.ipynb`.

## 1. Derivadas por convolución

La pregunta que abre el capítulo: *¿qué sucede al convolucionar una imagen con este kernel?*

```
-1  0  1
-1  0  1        →  derivada parcial en el eje x  (Ix = ∂I/∂x)
-1  0  1
```

```
-1 -1 -1
 0  0  0        →  derivada parcial en el eje y  (Iy = ∂I/∂y)
 1  1  1
```

## 2. Gradiente

- **Magnitud:** `|∇I| = √(Ix² + Iy²)`, con la aproximación barata `|Ix| + |Iy|`.
- **Orientación:** `θ = atan2(Iy, Ix)`, en el rango `[-180°, 180°]`.

`atan2` recibe **primero y, luego x** (`numpy.arctan2(Iy, Ix)`) y devuelve radianes en `[-π, π]`.
Tabla del curso (diapositiva 6) para fijar signos:

| Ix | Iy | ángulo |
|----|----|--------|
| 100 | 100 | 45° |
| -100 | 0 | 180° o -180° |
| -100 | 100 | 135° |
| 0 | -100 | -90° |
| 0 | 0 | indefinido (un punto no tiene ángulo) |

Nunca se evalúa `atan2(0,0)`: el ángulo solo se calcula donde la magnitud supera el umbral.

## 3. Operadores de primera derivada

**Prewitt** — los kernels de arriba (ejes x, y) y sus versiones diagonales.

**Sobel** — pondera más la fila/columna central:
```
Sx =  -1  0  1        Sy =  -1 -2 -1
      -2  0  2               0  0  0
      -1  0  1               1  2  1
```
Sobel es **separable**: `Sx = [1 2 1]ᵀ * [-1 0 1]` → un suavizado 1D perpendicular más una derivada
1D.

**Scharr** — más preciso en la rotación:
```
Sx =  -3   0   3        Sy =  -3 -10 -3
     -10   0  10               0   0   0
      -3   0   3               3  10   3
```

En OpenCV: `cv2.Sobel(img, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=3)`. Usar `CV_32F` (no `uint8`)
porque las derivadas son negativas; para visualizar, normalizar con
`cv2.normalize(..., 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)` sobre el valor absoluto.

Flujo típico: imagen → `Ix`, `Iy` → magnitud del gradiente → **umbral** sobre la magnitud → imagen
binaria de bordes.

## 4. Segunda derivada: Laplaciano

```
0  1  0
1 -4  1        →  Laplaciano  (∇²I = Ixx + Iyy)
0  1  0
```
Variantes con las diagonales (`1 1 1 / 1 -8 1 / 1 1 1`) y con signos invertidos.

Uso clásico de *sharpening*: `A + cte · Laplaciano(A)`.

**El Laplaciano es muy susceptible al ruido** → se suaviza primero con un Gaussiano. La combinación
de ambos es el **LoG (Laplaciano de Gaussiana)**:

```
LoG(x,y,σ) = Gxx(x,y,σ) + Gyy(x,y,σ)
```

## 5. Canny

Detector de bordes **delgados**, basado en criterios de primera y segunda derivada:
1. Suavizar con distintos filtros gaussianos para obtener bordes a distintas escalas y unirlos.
2. Descartar los pixeles cuya magnitud del gradiente **no sea máximo local** en una vecindad 3×3
   (*non-maximum suppression*).
3. Seleccionar pixeles de borde en forma **incremental siguiendo la dirección perpendicular al
   gradiente**.
4. **Histéresis con dos umbrales** `Tsup` y `Tinf` (se recomienda `Tsup` entre 2 y 3 veces `Tinf`):
   - gradiente ≥ `Tsup` → **semilla**, se selecciona y se recorren sus vecinos perpendiculares al
     gradiente;
   - gradiente < `Tinf` → rechazado;
   - `Tinf` ≤ gradiente < `Tsup` → se selecciona **solo si** tiene al menos un vecino ya seleccionado.

Efecto de los parámetros (ejemplo de las slides con `Tsup=500`): con `Tinf=10` aparecen muchísimos
bordes propagados; con `Tinf=400` casi solo quedan las semillas.

En OpenCV: `cv2.Canny(gris, threshold1=51, threshold2=301)`.

## 6. Diferencia de Gaussianas (DoG)

El blur afecta principalmente las zonas con gran variación de intensidad. Al **restar** la imagen
borrosa de la original se localizan esas zonas. Se usan **dos filtros gaussianos**: uno pequeño
(σ₁, para quitar ruido) y uno más grande (σ₂, para restar y detectar bordes).

```
DoG = G(x,y,σ₁) − G(x,y,σ₂)      (con σ₂ = k·σ₁)
```

DoG **aproxima** el LoG y es mucho más barato de calcular. En el notebook: `sigma1=3`, `sigma2=13`,
`cv2.subtract(blur1, blur2)` y luego umbral.

## 7. Bibliografía del capítulo
- Gonzalez & Woods, cap. 3 (filtrado espacial) y cap. 10 (segmentación).
- Bovik, cap. 19 (Gradient and Laplacian Edge Detection).
- Kaehler & Bradski, *Learning OpenCV 3*, cap. 10.
