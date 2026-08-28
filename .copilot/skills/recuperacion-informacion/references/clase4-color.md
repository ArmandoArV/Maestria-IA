# Clase 3 — Sistema visual humano, color y descriptores de color

Fuentes: `Slides 03.1-Sistema visual humano y color.pdf`,
`Slides 03.2-Descriptores globales color (parte 1).pdf`,
`Anexo 03.1-Ejemplo descriptores globales color.ipynb`, y la pregunta de EMD del Control 1.

## 1. Sistema visual humano

- La retina tiene **bastones** (visión en poca luz, sin color) y **conos** (color, alta luminosidad).
- El color es la **longitud de onda** de la luz; existen **tres tipos de conos** con sensibilidades
  distintas → visión tricromática, que es la razón de fondo de los espacios de color de 3 canales.
- El color percibido de un objeto depende de tres cosas: **el color de la luz**, **el material de la
  superficie** y **la sensibilidad de la cámara** (o del ojo).
- *"Las personas vemos con el cerebro"*: ilusiones ópticas y de color (disco de Benham, efecto
  McCollough, *Rotating Snakes* de Kitaoka) muestran que la percepción no es una medición física.
  Consecuencia práctica para RIM: la similitud de color que percibe una persona **no** coincide con
  la distancia en RGB.

Referencia: Gonzalez & Woods, cap. 2 (sistema visual) y cap. 6 (color).

## 2. Espacios de color

- Modelos **aditivo** (RGB, luz) y **sustractivo** (CMY, pigmentos).
- **RGB como tres canales grises:** una imagen color se puede ver como tres imágenes en escala de
  gris superpuestas (en OpenCV el orden es **BGR**). `cv2.split(imagen)` las separa.
- **Cubo RGB:** el espacio de colores es un cubo `[0,255]³`.

## 3. Descriptores de color

### 3.1 Vector de colores
Reducir la imagen a `w × h` pixeles y hacer *flatten* del arreglo `w × h × 3` → vector de
`w · h · 3` dimensiones. Es el análogo directo del vector de intensidades.

### 3.2 Histograma por canal (3 × 1D)
Calcular un histograma **independiente por cada canal** R, G y B y concatenarlos.

**No es adecuado para similitud**, porque cada histograma representa un canal por separado y por lo
tanto **no representa colores**: dos imágenes con las mismas proporciones de rojo, verde y azul por
separado pueden tener colores totalmente distintos. Sí **funciona para buscar duplicados**.

### 3.3 Histograma 3-D de color
Dividir **cada** canal R, G y B en tramos del mismo tamaño; cada **bin** es una combinación de tramos
de los tres canales:
- 6×6×6 → `6³ = 216` bins; 8×8×8 → `512` bins; 16×16×16 → `4096` bins.
- Bin 1 = (tramo1, tramo1, tramo1) → `R=[0,42] G=[0,42] B=[0,42]`; bin 2 = (tramo1, tramo1, tramo2);
  …; bin 216 = (tramo6, tramo6, tramo6).
- Cada color `(r,g,b)` de la imagen **suma 1** al bin que lo contiene. Al final se normaliza.

**Algoritmo de división regular de `[0,255]` en N tramos.** Los 256 tonos se reparten en rangos de
tamaño `256/N`, y el i-ésimo rango puede tener `floor(256/N)` o `ceil(256/N)` tonos. Se espera que la
suma acumulada de tonos hasta el rango i sea `i·256/N`; para cada rango se comparan ambas opciones
contra ese valor esperado y **se elige la que tenga menor error**.

Ejemplo con N = 6 (cada tramo de 42 o 43 tonos):

| Tramo | Rango | Tonos | Suma acumulada | Esperado | Error |
|-------|-------|-------|----------------|----------|-------|
| 1 | [0, 42] | 43 | 43 | 42.66 | +0.33 |
| 2 | [43, 84] | 42 | 85 | 85.33 | -0.33 |
| 3 | [85, 127] | 43 | 128 | 128 | 0 |
| 4 | [128, 170] | 43 | 171 | 170.66 | +0.33 |
| 5 | [171, 212] | 42 | 213 | 213.33 | -0.33 |
| 6 | [213, 255] | 43 | 256 | 256 | 0 |

En código: `calcular_limites(256, N) = [round(256·i/N) for i in range(N)] + [256]`.

**Problema de la división regular:** una división gruesa (3×3×3, 6×6×6) alcanza para representar
imágenes en forma aproximada, pero **no** para buscar colores similares — con 6 tramos por canal, los
colores `(0,0,0)`, `(42,0,0)`, `(0,42,0)` y `(42,42,42)` caen todos en el mismo bin. Y afinar la
división hace explotar el número de bins como **n³** (32 tramos → ~32.000 bins). Por eso se cambia la
forma de representar los colores (parte 2 del capítulo: espacios perceptuales, cuantización no
regular, EMD).

### 3.4 Histograma por zonas
Todo lo anterior se combina con la división en zonas: `descriptor_por_zona_generico()` recorre
`num_zonas_x × num_zonas_y` recortes de la imagen, calcula el histograma de cada zona y concatena.

## 4. Distancias entre histogramas de color

- **Minkowski `Lp`**: `L1` (Manhattan/`cityblock`) es la opción por defecto del curso para
  histogramas; `L2` (euclidiana) para vectores de intensidades/colores.
- **χ²** y **Kullback-Leibler**: tests estadísticos para comparar distribuciones.
- **Hamming**: para descriptores ordinales o de etiquetas (OMD, variante EHD, descriptor de Canny).

### 4.1 Earth Mover's Distance (EMD)
Las distancias bin-a-bin (`L1`, `L2`, χ²) fallan cuando dos histogramas tienen colores *parecidos*
pero en **bins distintos**: para `L1` un rojo en el bin 1 y un rojo casi idéntico en el bin 2 son
totalmente diferentes. La **EMD** resuelve esto permitiendo **transportar masa entre bins**, pagando
un costo proporcional a cuán distintos son los colores que representan.

Ingredientes:
1. **Ground distance** entre los colores representantes de cada par de bins. El curso usa la
   **distancia euclidiana en el espacio CIE LAB** (un espacio perceptualmente uniforme: distancias
   iguales ≈ diferencias percibidas iguales, a diferencia de RGB). Convertir con
   `cv2.cvtColor(color, cv2.COLOR_BGR2LAB)` o con colormine.org.
2. **Matriz de costos** `C = [c_ij]`, con `c_ij` = ground distance entre el bin `i` del histograma 1
   y el bin `j` del histograma 2.
3. **Matriz de flujos** `F = [f_ij]` ≥ 0: cuánta masa se mueve del bin `i` al bin `j`. Es válida si
   `Σ_j f_ij ≤ P_i` (no se saca más masa de la que hay), `Σ_i f_ij ≤ Q_j` (no se llena más de lo que
   cabe) y `Σ_ij f_ij = min(ΣP, ΣQ)` (= 1 si ambos histogramas están normalizados).
4. **EMD** = trabajo mínimo normalizado:

```
EMD(P,Q) = ( Σ_ij c_ij · f_ij ) / ( Σ_ij f_ij )
```

La matriz de flujos **óptima** se obtiene resolviendo un problema de transporte (programación
lineal); para un ejercicio a mano basta una matriz **válida** (que cumpla las restricciones), y con
ella se calcula un EMD que es una cota superior del óptimo.
