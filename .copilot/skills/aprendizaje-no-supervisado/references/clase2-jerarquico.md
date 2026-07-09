# Clase 2 — Datos Mixtos y Métodos Jerárquicos

## Datos mixtos (cuantitativos + cualitativos)
Para variables binarias ya vimos simple/double matching y Jaccard. Para datasets **mixtos** dos alternativas: **distancia de Gower** y **k-prototype**.

### Distancia de Gower
Basada en Manhattan + simple matching:
```
d(X,Y) = (1/p) Σⱼ δ(Xⱼ, Yⱼ)
```
donde
```
δ(Xⱼ,Yⱼ) = I(Xⱼ ≠ Yⱼ)             si j es categórico
δ(Xⱼ,Yⱼ) = |Xⱼ − Yⱼ| / rangoⱼ     si j es numérico
```
Similitud asociada: `S_G = 1 − D_G`.

### Disimilaridad k-prototype
Basada en Euclidiana + simple matching:
```
d(x,y) = d_euc(x^num, y^num) + λ · d_sm(x^cat, y^cat),   λ ≥ 0
```
con `x = (x^num, x^cat)`, `y = (y^num, y^cat)`.

## Ejemplo de Gower (datos de Agresti, 5 individuos)
Mismos datos de Clase 1. Rangos: `rango(X₁) = 76−64 = 12`, `rango(X₂) = 210−120 = 90`.

Matriz de similitud `S_G = 1 − D_G` (triangular inferior, diagonal 1):
```
S_G =
1
0.347  1
0.606  0.546  1
0.574  0.588  0.375  1
0.093  0.745  0.292  0.333  1
```
- Con Simple Matching los más similares eran 2 y 5 (`s₂₅ = 0.833`); con Gower también (`s₂₅ = 0.745`).
- Menos similares: 1 y 5 con ambos (Simple `s₁₅ = 0`, Gower `s₁₅ = 0.093`).
- Las magnitudes cambian porque Gower usa la información original de las numéricas, no solo su versión binaria. Las conclusiones coinciden aquí, **pero esto no está garantizado en general**: la representación de los datos puede modificar las relaciones de proximidad.

## Métodos jerárquicos
Asignar jerarquías en las distancias. Dos metodologías:
- **Aglomerativa** (bottom-up): empezar con n clusters e ir uniendo.
- **Divisiva** (top-down).

Además hay que elegir el **tipo de enlace** entre grupos.

### Algoritmo aglomerativo
1. Comenzar con n clusters.
2. Identificar los ítems más próximos.
3. Unir los de mayor similitud.
4. Repetir 2–3, n−1 veces.

Al unir `u` y `v` → `(uv)`, y `w` otro item:

| Enlace | Distancia | Similaridad |
|--------|-----------|-------------|
| Simple | `d_{(uv)w} = mín{d_uw, d_vw}` | `s_{(uv)w} = máx{s_uw, s_vw}` |
| Completo | `d_{(uv)w} = máx{d_uw, d_vw}` | `s_{(uv)w} = mín{s_uw, s_vw}` |
| Promedio | `d_{(uv)w} = (d_uw + d_vw)/2` | `s_{(uv)w} = (s_uw + s_vw)/2` |

### Ejemplo trabajado (matriz de disimilaridad, enlace simple)
```
D =
0
9   0
3   7   0
6   5   9   0
11  10  2   8   0
```
(orden de items: 1,2,3,4,5)

**Paso 1** — mínimo fuera de diagonal es `d₃₅ = 2` → unir (35).
```
d_(35)1 = mín{3,11} = 3
d_(35)2 = mín{7,10} = 7
d_(35)4 = mín{9,8}  = 8
```
Quedan (35), 1, 2, 4:
```
0
3   0
7   9   0
8   6   5   0
```
(orden: (35), 1, 2, 4)

**Paso 2** — mínimo es 3 → unir (35) con 1 → (135).
```
d_(135)2 = mín{7,9} = 7
d_(135)4 = mín{8,6} = 6
```
Quedan (135), 2, 4:
```
0
7   0
6   5   0
```
(orden: (135), 2, 4)

**Paso 3** — mínimo es 5 → unir 2 y 4 → (24). Quedan (135), (24):
```
d_(135)(24) = mín{7,6} = 6
```
**Final:** se grafica el dendrograma. La clase también pide repetir con enlace **completo** y **promedio**.

## Propiedades de los enlaces
- **Simple:** puede violar compacidad (clusters poco homogéneos, *chaining*).
- **Completo:** clusters compactos, pero puede violar cercanía entre clusters.
- **Promedio:** compromiso entre ambos.
- Una transformación monótona estrictamente creciente `h(·)` aplicada a las disimilaridades (`h_ij = h(d_ij)`) puede **cambiar** el resultado del enlace **promedio**; los enlaces simple y completo permanecen **invariantes**.

### Diámetro de un cluster
Mayor disimilitud entre sus miembros.
- Simple → diámetro tiende a ser grande.
- Completo → diámetro tiende a ser pequeño.
- Promedio → punto medio.

## Ejercicio de la clase (Agresti + Gower)
Con la matriz de similitud `S_G` del ejemplo de Gower:
1. Construir dendrogramas con enlaces simple, completo y promedio.
2. Escoger un enlace y obtener 2 grupos.

## Comentarios finales
- El agrupamiento jerárquico usa únicamente una medida de proximidad.
- La elección de la disimilaridad influye, sobre todo con variables de distinta naturaleza.
- El resultado se representa con un **dendrograma**, que permite explorar particiones sin fijar K previamente.
- En métodos no jerárquicos (Clase 3) el número de grupos debe especificarse de antemano.

## Enlaces adicionales (mención, ver Clase 3/4)
Ward (varianza mínima, default frecuente), WPGMA, WPGMC, UPGMC.
