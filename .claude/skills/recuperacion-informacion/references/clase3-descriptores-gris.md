# Clase 2–3 — Descriptores globales de imágenes en gris

Fuentes: `Slides 02.2-Descriptores globales gris (Intensidades).pdf`,
`Slides 02.3-Descriptores globales gris (Bordes).pdf`,
`Anexo 02.2-Ejemplo descriptores globales gris.ipynb`.

Un **descriptor global** convierte la imagen completa en **un vector** que luego se compara con una
función de distancia. Los de este capítulo usan solo información de grises.

---

## A. Descriptores de intensidades

### A.1 Vector de intensidades
1. Convertir a escala de grises.
2. Dividir la imagen en **w × h zonas** y calcular la **intensidad promedio** de cada zona
   (equivalente: reducir la imagen a w × h pixeles con `cv2.resize(..., cv2.INTER_AREA)`).
3. *Flatten* → vector de largo `w·h`.
4. Comparar con una distancia de **Minkowski (Lp)** — euclidiana (`L2`) o Manhattan (`L1`).

Ejemplos de tamaño: 11×9 → 99 dims; 44×36 → 1.584 dims; 176×144 → 25.344 dims.

*Variante robusta al brillo:* ecualizar el histograma (`cv2.equalizeHist`) antes de reducir.

### A.2 OMD — Ordinal Measurement Descriptor
(Kim et al., 2002/2005 — *content-based image copy detection*.)

1–2. Igual que el vector de intensidades (w × h zonas con su promedio).
3. **Ordenar** las intensidades de menor a mayor.
4. Representar cada zona por **la posición que ocupa** en el arreglo ordenado (su rango).
5. Comparar con **distancia de Hamming**.

Ventaja: invariante a cambios monótonos de brillo/contraste — solo importa el orden relativo.

En NumPy: `posiciones = numpy.argsort(descriptor)` y luego `descriptor[posiciones[i]] = i`.

### A.3 Histograma de intensidades
Calcular un histograma de grises de la imagen. **Parámetros de diseño:**
- cantidad de **bins** (8, 64, 256 → vector de esa dimensión);
- tipo de **asignación**: *hard* (cada pixel suma 1 a un bin) vs. *soft* (reparte entre bins vecinos);
- tipo de **normalización**: norma `L1` o `L2`;
- tipo de dato a guardar (8 bits, 32 bits).

Comparación: Minkowski `Lp`, o un test estadístico como **χ²** o **Kullback-Leibler**.

### A.4 Histograma por zonas y Spatial Pyramid
Un histograma global **descarta la ubicación espacial**. Para conservarla:
1. Dividir la imagen en **w × h zonas** y calcular un histograma independiente de **N bins** por zona
   (asignación *soft* entre zonas → interpolación **tri-lineal**).
2. **Concatenar** → vector de `w · h · N` dimensiones.

Se pueden combinar **varios niveles** de división: 1×1 (global) + 2×2 + 4×4 = **21 zonas** →
estrategia **Spatial Pyramid**.

Ejemplos: 4×4 zonas × 16 bins = 256 dims; 8×8 × 8 bins = 512 dims; 1×3 × 16 bins = 48 dims.

---

## B. Descriptores de bordes

### B.1 HOG — Histogram of Oriented Gradients
1. Convertir a gris y **determinar los pixeles de borde**: aplicar Sobel, calcular
   `magnitud = √(Ix² + Iy²)` y seleccionar los pixeles con magnitud **superior a un umbral mínimo**
   (en el notebook, 150; conviene un `GaussianBlur` previo para quitar ruido).
2. Para cada pixel de borde, calcular el **ángulo del gradiente**:
   - `arctan2(Iy, Ix)` → rango **[-180°, 180°]**, considera el signo de ambas coordenadas y por lo
     tanto **distingue bordes blanco-a-negro de negro-a-blanco** (el *sentido* del borde);
   - `arctan(Iy/Ix)` → rango **(-90°, 90°]** (cuando `Ix = 0` el ángulo es 90°); representa **solo la
     dirección** del borde, no el sentido.
   - Para pasar de `[-180°,180°]` a `(-90°,90°]`: si el ángulo ≤ -90° **sumar** 180°, si es > 90°
     **restar** 180° (p. ej. -135° → 45°).
3. El descriptor es el **histograma de esas orientaciones**, calculado **por zonas**.

Diseño: para representar bien una forma la imagen debe subdividirse en **zonas pequeñas**,
idealmente con una orientación dominante cada una. Los histogramas suelen tener **8 a 18 bins**
(rangos de 10° a 45°). Ejemplo de las slides: 10 zonas × 9 bins = vector de 90 dims.

Mejoras posibles: mejor detección de bordes (segunda derivada), asignación suave y normalización del
histograma.

### B.2 EHD — Edge Histogram Descriptor
(Manjunath et al., *Color and Texture Descriptors*, 2001 — descriptor MPEG-7.)

1. Convertir a gris y ajustar el tamaño a **(4·2·w) × (4·2·h)**.
2. Dividir en **4 × 4 zonas**; cada zona contiene `w × h` **bloques de 2×2 pixeles**.
3. Para cada bloque de 2×2 se mide la **energía** de 5 filtros, correspondientes a 5 orientaciones:
   **vertical, horizontal, 45°, 135° y no-direccional**. Se escoge el filtro con **mayor energía en
   valor absoluto** y se compara con un umbral mínimo `T`:
   - `|energía| < T` → el bloque se **descarta** (no es borde);
   - `|energía| ≥ T` → el bloque tiene esa orientación y **suma 1** al bin correspondiente del
     histograma de su zona.
4. Cada zona queda con un histograma de **5 bins** (fracción de bloques por orientación).
5. El descriptor final es la concatenación: **4 × 4 × 5 = 80 dimensiones**.
6. Comparación con **distancia Manhattan**.

Ejemplo de las slides con `T = 50`:
- energías `(0, -328, -232, -232, -28)` → mayor valor absoluto = -328 (filtro 2), supera `T` → bloque
  "tipo 2", sumar 1 al segundo bin;
- energías `(-41, -3, -31, 27, 2)` → mayor valor absoluto = -41, **no** supera `T` → bloque ignorado.

### B.3 Variante EHD (Iwamoto et al., 2006)
Representar la imagen por **la lista** de la orientación dominante de cada bloque, en vez de
histogramas por zona:
- ajustar el tamaño a `(2w) × (2h)` → `w · h` bloques de 2×2;
- cada bloque → su orientación dominante (entre **10** posibles) o **0 = "No-Edge"** si no supera el
  umbral;
- vector de largo `w · h`, cada dimensión entre 0 y 10;
- comparación con **distancia de Hamming**.

Diseñada para ser robusta a la superposición de subtítulos en video.

### B.4 Descriptor basado en Canny (Hampapur et al., 2001/2002)
1. Calcular los bordes con **Canny**.
2. Dividir la imagen en `w × h` zonas; en cada zona calcular el **centroide de los bordes** y
   **cuantizarlo** en `p × q` posiciones.
3. Vector de `w · h` dimensiones, cada una entre 1 y `p·q`. Parámetros del paper: `w = h = 15`,
   `p = q = 4`.
4. Comparación con **distancia de Hamming**.

---

## C. Ejercicios resueltos de las slides

### C.1 Imagen 1 de 8×8 (mitad negra 0-31, mitad blanca 224-255)
- **Vector de intensidades 2×2:** `(128, 128, 128, 128)` — cada cuadrante mezcla mitad negro y mitad
  blanco, así que el promedio es 128.
- **OMD 2×2:** `(1, 1, 1, 1)` — todas las zonas tienen el mismo valor.
- **Vector de intensidades 4×4:** `(128, 128, …, 128)`.
- **OMD 8×8:** `(1, 33, 1, 33, …)` — alterna posiciones bajas y altas del arreglo ordenado.
- **Histograma global de 8 bins:** `(0.5, 0, 0, 0, 0, 0, 0, 0.5)` — mitad de los pixeles en el bin
  `0-31` y mitad en el bin `224-255`.
- **Histograma de 8 bins por zonas 2×2:** 32 dimensiones, el patrón `(0.5,0,0,0,0,0,0,0.5)` repetido
  4 veces (cada zona tiene la misma proporción).

### C.2 HOG y EHD globales (imagen 5 de 8×8)
El ejercicio pide, para 6 imágenes de 8×8: el **HOG global** (magnitud del gradiente → seleccionar
bordes → histograma de ángulos, p. ej. `0°: 0.32, 45°: 0.32, 90°: 0.35`) y el **EHD global**
(clasificar cada bloque 2×2 en su tipo 1–5 y contar).

Método para hacerlo a mano:
1. Convolucionar con `Sx` y `Sy` **solo donde el kernel cabe completo** en la imagen (o en la zona,
   si la división es estricta).
2. Calcular magnitud `√(Ix²+Iy²)` y descartar los pixeles bajo el umbral.
3. Calcular `atan2(Iy, Ix)` en grados, llevarlo al rango pedido y acumular en el bin correspondiente.
4. Normalizar el histograma (los bins deben sumar 1).
