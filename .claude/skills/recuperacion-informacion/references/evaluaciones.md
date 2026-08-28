# Evaluaciones INF3841 — formato y métodos de cálculo

> **Regla del curso:** los controles y tareas son **individuales**, no se pueden copiar de Internet
> y **no se permite usar ChatGPT ni similares**; si se detecta copia o plagio la nota es 1.0. Usa
> este material para **entender y verificar** el método, no para generar una entrega.

## Formato

| | Controles (C1, C2) | Tareas (T1, T2) |
|---|---|---|
| Qué son | ejercicios/preguntas sobre el contenido | desafíos de programación en Python |
| Cómo se resuelven | papel (foto `.jpg`/`.png`), Excel (`.xlsx`) o PDF | código fuente `.py` |
| Prohibido | subir `.py`, `.ipynb` o links de descarga | subir binarios o `.ipynb` |
| Corrección | manual, con bonus en algunas preguntas | evaluador automático (nota + hasta **+10 décimas** bonus) |
| Falla | — | si no compila, se cae o no cumple el enunciado → **sin entrega** |
| Fechas | C1: 06-sep (sesiones 01–04) · C2: 11-oct (sesiones 05–08) | T1: 30-ago · T2: 04-oct |

Entregas parciales cada domingo con feedback breve; se puede corregir para mejorar la nota. **No se
aceptan entregas atrasadas** (ni por correo ni en los comentarios).

**Ninguna pregunta de control pide programar** — se calcula a mano o en Excel. Herramientas útiles
en Excel: `SUMAPRODUCTO` para la convolución, `MEDIANA`, `RAIZ`, `ATAN2` (ojo: en Excel el orden es
`ATAN2(x; y)`, al revés que `numpy.arctan2(y, x)`), `GRADOS`, `CONTAR.SI` para los histogramas.

## Métodos que se evalúan a mano

### Convolución de una imagen pequeña
1. Reflejar el kernel 180° (convolución ≠ correlación; si el kernel es simétrico da lo mismo).
2. Calcular **solo donde el kernel está completamente contenido** en la imagen: para un kernel 3×3
   sobre una imagen n×n, quedan `(n−2)×(n−2)` valores definidos y el borde vacío.
3. El resultado puede ser negativo o mayor a 255 → se pide profundidad **32f** (floats).

### Función umbral
`U_t(x) = 255 si |x| ≥ t, 0 si no`. Se aplica sobre el resultado de la convolución, en **valor
absoluto** (un borde negativo también es un borde).

### Filtro de mediana
Ventana 3×3, ordenar los 9 valores y tomar el 5º (`(n·n+1)/2`). Igual que la convolución: solo donde
el bloque cabe completo.

### Gradiente
`Ix = I ∗ Sx`, `Iy = I ∗ Sy` (Sobel), luego:
- magnitud `√(Ix²+Iy²)` — celda vacía donde el gradiente no está definido;
- ángulo `atan2(Iy, Ix)` en `[-180°, 180°]` — celda vacía donde no está definido **o la magnitud es
  0**.

### Histogramas
- **Normalizado**: los bins suman 1 → cada altura es una fracción de los pixeles.
- **256 bins** = un bin por tono; hay que decir explícitamente cuántos bins hay, qué representa cada
  bin y cuál es la altura de cada uno.
- **Por zonas 2×2**: cuatro histogramas independientes, cada uno normalizado **dentro de su zona**.
- **Color 4+4+4 (3×1D)**: tres histogramas de 4 bins, uno por canal, concatenados.
- **Color 3D 4×4×4**: 64 bins; hay que indicar qué rango de R, G y B representa cada bin no nulo.
  Los tramos salen de la división regular (`calcular_limites(256, 4)` → `[0,64,128,192,256]`).

### HOG a mano
1. Sobel dentro de **cada zona por separado** si se pide división estricta (no usar pixeles de zonas
   vecinas para calcular el gradiente de una zona).
2. Filtrar por magnitud ≥ umbral.
3. Ángulo → llevarlo al rango pedido (p. ej. `(-90°, 90°]`: sumar 180 si ≤ -90, restar 180 si > 90).
4. Repartir en los bins (9 bins en `(-90,90]` → 20° cada uno) y normalizar.

### EHD a mano
Bloques de 2×2 → energía de los 5 filtros → mayor valor absoluto → comparar con `T` → bin de la zona.

### EMD (Earth Mover's Distance)
1. **Matriz de costos**: ground distance entre los colores representantes de cada par de bins,
   usando la **distancia euclidiana en CIE LAB** (convertir con `cv2.cvtColor` o colormine.org).
2. **Matriz de flujos**: cualquier matriz `f_ij ≥ 0` con `Σ_j f_ij ≤ P_i`, `Σ_i f_ij ≤ Q_j` y
   `Σ f_ij = min(ΣP, ΣQ)`. No tiene que ser la óptima, pero sí válida.
3. `EMD = Σ c_ij·f_ij / Σ f_ij`.

## Audio (sesión 04) — fórmulas que pide el Control 1

Las slides de audio no están en el repo; lo que se evalúa son las relaciones básicas de PCM:

- **Tamaño de un archivo PCM crudo (`.raw`, sin header):**
  `bytes = duración_en_segundos × sample_rate × (profundidad_en_bits / 8) × canales`
  (`s16le` → 2 bytes por sample; `32f` → 4 bytes; mono → 1 canal).
- **Frecuencia máxima audible = Nyquist = sample_rate / 2.** Un archivo a 44.100 Hz llega hasta
  22.050 Hz; uno a 8.192 Hz llega hasta 4.096 Hz.
- **La información perdida no se recupera:** volver a subir el sample rate (o la profundidad) de un
  archivo ya submuestreado produce un archivo **más grande** pero con la **misma** frecuencia máxima
  y la misma calidad audible que el original degradado.
- **Profundidad de bits** → rango dinámico / ruido de cuantización; **sample rate** → ancho de banda
  de frecuencias. Son dos ejes independientes de calidad.
