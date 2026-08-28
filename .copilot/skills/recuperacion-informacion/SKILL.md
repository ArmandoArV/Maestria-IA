---
name: recuperacion-informacion
description: >
  Expert knowledge base for the INF3841 Recuperación de Información course (Magíster en IA, PUC Chile,
  Prof. Juan Manuel Barrios). Covers multimedia information retrieval: IR vs. databases, relevance and
  ranking, image processing (point operators, histograms, equalization, Otsu thresholding, convolution,
  Gaussian/median/bilateral filters, morphology), edge detection (Prewitt, Sobel, Scharr, Laplacian,
  LoG, DoG, Canny), global grayscale descriptors (intensity vector, OMD, histograms by zone, spatial
  pyramid, HOG, EHD), color (human visual system, RGB cube, per-channel 3x1D vs 3D color histograms,
  regular bin division, CIE LAB, Earth Mover's Distance), similarity search, and the Python/OpenCV code
  used in class. Use for any INF3841 question — controles, tareas de programación, slides, syllabus.
  Also trigger on recuperación de información, information retrieval, RIM, multimedia retrieval,
  descriptores de imágenes, procesamiento de imágenes, convolución, kernel, máscara, umbral, Otsu,
  ecualización, histograma, filtro de mediana, morfología, detección de bordes, gradiente, Sobel,
  Prewitt, Scharr, Laplaciano, LoG, DoG, Canny, HOG, EHD, OMD, spatial pyramid, histograma de color,
  espacio de color, CIE LAB, EMD, Earth Mover's Distance, búsqueda por similitud, k-NN, OpenCV, cv2,
  or the course code (INF3841). Respond in Spanish when the user writes in Spanish.
---

# Recuperación de Información (INF3841)

Knowledge base for INF3841 at PUC Chile (Magíster en IA, Prof. Juan Manuel Barrios,
03-ago-2026 → 05-oct-2026). The course is about **Recuperación de Información Multimedia (RIM)**:
how to represent, index and search content — images, audio, text — *by similarity of the content
itself*, not by metadata.

## How to use this skill

1. **Read the matching reference file** in `references/` before answering anything beyond the summary
   below. SKILL.md is the map; the reference files hold formulas, kernels and worked examples.
2. **Respond in the student's language.** The course is in Spanish → answer in Spanish.
3. **Follow the course's conventions**: images as NumPy matrices via `cv2`, descriptors as rows of a
   matrix, comparison with `scipy.spatial.distance.cdist`. Don't introduce new dependencies for
   something the course already solves with `cv2` + `numpy` + `scipy`.
4. **Academic-integrity note:** the syllabus states that controles and tareas are individual and
   explicitly forbids solving them with ChatGPT or similar. Use this skill to *explain* methods, work
   through analogous examples, and check reasoning — not to hand over answers to be submitted. Say so
   plainly once if the request is literally "resuelve el Control X por mí", then help them learn it.

## Course map

| Sesión | Fecha | Tema | Reference |
|--------|-------|------|-----------|
| 01 | 03-ago | Introducción a la RI + Procesamiento de imágenes + OpenCV | `references/clase1-fundamentos-imagenes.md` |
| 02 | 10-ago | Detección de bordes + Descriptores globales gris (intensidades, bordes) | `references/clase2-bordes.md`, `references/clase3-descriptores-gris.md` |
| 03 | 17-ago | Sistema visual humano y color + Descriptores globales color | `references/clase4-color.md` |
| 04 | 24-ago | Descriptores de audio | (slides no están en el repo; ver `references/evaluaciones.md` §audio) |
| 05 | 31-ago | Descriptores de texto | (pendiente) |
| 06 | 07-sep | Búsquedas por similitud e índices multidimensionales | (pendiente) |
| 07 | 21-sep | Evaluación de efectividad y alta dimensionalidad | (pendiente) |
| 08 | 28-sep | Deep features de imágenes | (pendiente) |
| 09 | 05-oct | Deep features de texto y combinación | (pendiente) |

Código y datos: `RecuperacionDeInformacion/Codigos/` (anexos y notebooks),
`RecuperacionDeInformacion/Presentaciones/` (slides), `RecuperacionDeInformacion/Controles/`.
Code recipes: `references/codigo-opencv.md`. Evaluación y ejercicios: `references/evaluaciones.md`.

## Core concepts (quick reference)

### Qué es RI y en qué se diferencia de una base de datos
- **Base de datos:** obtiene *eficientemente todos* los elementos que cumplen una condición exacta
  (SQL), con transacciones ACID.
- **Recuperación de Información:** obtiene *los mejores* elementos que satisfacen una necesidad de
  información. Dos conceptos clave: **relevancia** (cuán útil es un documento) y **ranking**
  (ordenar por relevancia).
- **RIM (multimedia):** los documentos son audio, imagen, video, 3D, grafos. La búsqueda analiza el
  **contenido** (pixeles, samples, frames) y **no** requiere metadatos (tags, EXIF, ID3). Consultas
  por texto, *by-example* (algo parecido a este documento) o *by-sketch*.
- El contenido de cada documento se representa por **uno o más vectores** (extracción de
  características) → luego la búsqueda es un **k-NN** en un espacio vectorial o métrico.
- Áreas involucradas: análisis de contenido, estructuras de datos e índices, IA/ciencia de datos,
  interfaces humano-computador.

### Procesamiento de imágenes (tres familias de operadores)
1. **Punto a punto** `G(i,j) = h(I(i,j))` — brillo/contraste `aI+b`, gamma `I^(1/γ)`, histograma,
   ecualización, umbral (Otsu).
2. **Lineales (convolución)** — suma ponderada de una ventana por un **kernel/máscara**: blur
   promedio, Gaussiano (separable), derivadas.
3. **No lineales** — mediana (ruido sal y pimienta), bilateral, adaptive threshold, morfológicos.

### Detección de bordes
Gradiente por convolución con derivadas parciales; **magnitud** `√(Ix²+Iy²)` (aprox. `|Ix|+|Iy|`) y
**orientación** `atan2(Iy, Ix)`. Operadores **Prewitt / Sobel / Scharr**; segunda derivada
**Laplaciano** → **LoG**; **DoG** como aproximación; **Canny** (máximos locales + histéresis con
`Tsup` y `Tinf`, con `Tsup ≈ 2–3 · Tinf`).

### Descriptores globales (imagen → vector)
| Descriptor | Idea | Distancia típica |
|------------|------|------------------|
| Vector de intensidades | reducir a w×h zonas (promedio) y *flatten* | Minkowski `Lp` |
| OMD | reemplazar cada zona por su **rango** al ordenar | Hamming |
| Histograma de intensidades | distribución de grises, N bins normalizados | `Lp`, χ², KL |
| Histograma por zonas / Spatial Pyramid | un histograma por zona, concatenados (1×1+2×2+4×4 = 21 zonas) | `L1` |
| HOG | histograma de orientaciones del gradiente en pixeles de borde, por zonas | `L1` |
| EHD | 4×4 zonas × 5 orientaciones dominantes de bloques 2×2 = **80 dims** | Manhattan |
| Variante EHD | lista de orientación dominante por bloque (0 = No-Edge) | Hamming |
| Descriptor basado en Canny | centroide de bordes por zona cuantizado en p×q | Hamming |
| Vector / histograma de color | 3×1D por canal (no representa colores) vs. histograma 3D RGB | `L1`, EMD |

### Flujo de trabajo del curso (siempre el mismo)
1. Leer todas las imágenes de una carpeta.
2. Calcular un vector por imagen → **matriz de descriptores** (`n_imágenes × largo_descriptor`).
3. Comparar todos contra todos con `cdist` → **matriz de distancias**.
4. Poner `inf` en la diagonal y para cada fila reportar el **más cercano**; medir % de aciertos
   (la respuesta correcta es la imagen con el mismo nombre y distinto número final: `tigre1.jpg` ↔
   `tigre2.jpg`).

## Evaluación

- **NF = (C1 + C2 + T1 + T2) / 4**, aprueba con **NF ≥ 4.0**. Todo individual.
- **Tareas (T1, T2)** en Python: solo `.py` (no `.ipynb`, no binarios). Hay datos de prueba y un
  **evaluador automático** que asigna la nota y puede dar hasta **+10 décimas de bonus**. Si no
  compila, se cae o no cumple el enunciado → sin entrega.
  - T1: domingo 30-ago 23:59 · T2: domingo 04-oct 23:59.
- **Controles (C1, C2)**: ejercicios a mano/Excel/PDF — **ninguna pregunta pide programar**; subir
  foto `.jpg`/`.png`, `.xlsx` o PDF. C1 cubre sesiones 01–04 (entrega 06-sep), C2 sesiones 05–08
  (entrega 11-oct).
- **Entregas parciales** cada domingo con feedback breve; se puede corregir y mejorar la nota. No hay
  descuento por atraso: simplemente **no se aceptan entregas atrasadas**.

## Bibliografía del curso
- Gonzalez & Woods, *Digital Image Processing*, 3rd ed., 2008 — cap. 3 (filtrado espacial), 6 (color),
  10 (segmentación).
- Baeza-Yates & Ribeiro-Neto, *Modern Information Retrieval*, 2011.
- Knees et al., *Music Similarity and Retrieval*, 2016.
- Chollet, *Deep Learning with Python*, 2nd ed., 2021.
- Bovik, *The Essential Guide to Image Processing*, 2009 — cap. 3 (histogramas), 19 (bordes).
- Kaehler & Bradski, *Learning OpenCV 3*, 2017 — cap. 10 (filtros y convolución).
- Szeliski, *Computer Vision: Algorithms and Applications*, 2011 — cap. 3.
- Papers: Kim et al. (OMD, 2002/2005), Manjunath et al. (EHD, 2001), Iwamoto et al. (variante EHD,
  2006), Hampapur et al. (descriptor Canny, 2001/2002).
