# Clase 4 — Número de Clusters y Componentes Principales

## Determinación de K
- El problema más difícil en clustering: no hay función de pérdida que cuantifique el ajuste.
- Las técnicas son **independientes del método** de agrupamiento; parten de los grupos ya establecidos.
- Se compara el rendimiento para `K ∈ {1,2,…,K_máx}`, con `K_máx` fijado previamente.

### Método del Codo (Pliegue / Elbow)
- Para cada K calcular `W_K` (within-cluster). Suele ser decreciente en K.
- `K̂` = valor donde la gráfica `W_K` vs K se **estabiliza**.
- Como `W_K + B_K = T` (T fijo), también se grafican:
  - `B_K` vs K
  - `W_K/T · 100` vs K
  - `B_K/T · 100` vs K
- Estos últimos dan el % de explicación de la dispersión total. Estrategia: `K̂` = primer K que alcanza **80% o 90%** de `B_K/T·100`.
- Ventaja: simple y popular. Desventaja: netamente visual → subjetivo.

### CH(K) — Calinski & Harabasz (1974)
```
CH(K) = [B_K / (K−1)] / [W_K / (n−K)]
K̂ = argmax_{K ∈ {2,…,K_máx}} CH(K)
```
`CH(1)` no está definido (valdría 0 porque `B₁=0`). Como `CH(K)>0` para K>1, nunca se escoge K=1.

### H(K) — Hartigan (1975)
```
H(K) = [ W_K/W_{K+1} − 1 ] / (n − K − 1)
```
Inicia con K=1 y añade un cluster mientras `H(K)` sea suficientemente grande. Hartigan sugiere **añadir un cluster si `H(K) > 10`**. El número de clusters es el **menor K tal que `H(K) ≤ 10`**.

### Silhouette — Kaufman & Rousseeuw (1990)
Para cada observación i:
```
a(i) = [1/(|k_i|−1)] Σ_{C(j)=k_i, j≠i} d_ij        (disimilitud media intra-cluster)
b(i) = mín_{l≠i} [ (1/|k_l|) Σ_{C(j)=l} d_ij ]      (al cluster vecino más cercano)
s(i) = [b(i) − a(i)] / máx{a(i), b(i)}
```
`k_i` es el cluster de i, `|k_i|` su cardinalidad.
```
K̂ = argmax_{K ∈ {2,…,K_máx}} s(K)
```
No está definido para K=1.

### Gap Statistic — Tibshirani, Walther & Hastie (2001)
Generar M conjuntos de datos de referencia, obtener `W*_{Km}`, y calcular:
```
Gap(K) = (1/M) Σ_m ln(W*_{Km}) − ln(W_K)
l̄ = (1/M) Σ_m ln(W*_{Km})
sd²_K = (1/M) Σ_m (ln(W*_{Km}) − l̄)²
s_K = sd_K · √(1 + 1/M)
```
Estimar:
```
K̂ = menor K tal que  Gap(K) ≥ Gap(K+1) − s_{K+1}
```
> Nota del curso: el Gap statistic no estaba implementado directamente en el material de Python → se usa **R** (`cluster::clusGap`). Ver notebook `Clase4_EPG4002_2026_R_GapStatistic`.

## Componentes Principales (PCA)

### Resumen
- Sea `X ∼ N_p(μ, Σ)`. Se define `Y = AX` de modo que la combinación lineal **maximice la varianza** de Y con componentes **ortogonales**.
- Se eligen las primeras k componentes para capturar la mayor variabilidad de X.
- **Resultado:** los **vectores propios de Σ** resuelven el problema de optimización; sus **valores propios** (estandarizados) son la fracción de varianza.
- Usos: reducir dimensión, detectar puntos atípicos, visualizar la variabilidad de problemas de alta dimensión.

### Preliminares (resultado clave)
Sea `B` (p×p) simétrica y semidefinida positiva con `λ₁ ≥ λ₂ ≥ … ≥ λ_p ≥ 0` y vectores propios ortonormales `q₁,…,q_p`. Sea `l` unitario (`lᵀl=1`):
1. `máx lᵀBl = λ₁`, alcanzado en `l = q₁`.
2. `mín lᵀBl = λ_p`, alcanzado en `l = q_p`.
3. `máx lᵀBl = λ_j` en `l = q_j`, sujeto a `lᵀqᵢ = 0`, i=1,…,j−1.

Idea (descomposición espectral): `B = QΛQᵀ`. Con `f = Qᵀl` y `fᵀf=1`:
```
lᵀBl = fᵀΛf = Σ λᵢ fᵢ²,    λ_p ≤ lᵀBl ≤ λ₁
```

### Metodología
Sea X vector aleatorio p-dim, `E[X]=0`, `V[X]=Σ` (conocido), `λ₁≥…≥λ_p≥0`, vectores propios ortonormales `c₁,…,c_p`. Con `C=(c₁|…|c_p)` y `Λ=diag(λ)`:
```
Σ = CΛCᵀ
```
Combinaciones lineales `CᵀX` cumplen `V[CᵀX] = CᵀΣC = Λ`, es decir `V[cᵢᵀX] = λᵢ`.

**Varianza generalizada** `g: ℝ^{p×p}→ℝ` (medida global de variabilidad):
1. `g(Σ) = |Σ|`
2. `g(Σ) = tr(Σ)` ← **usada en componentes principales**
3. `g(Σ) = ‖Σ‖₂`

Como `|Σ| = Πλᵢ` y `tr(Σ) = Σλᵢ`:
```
Proporción de varianza de las primeras k componentes = (λ₁+…+λ_k)/(λ₁+…+λ_p)
```
Si `Σ_{i=k+1}^p λᵢ` es pequeño comparado con `Σ_{i=1}^k λᵢ`, usar `Y = AX` con las primeras k.

**Criterio:** si `(λ₁+…+λ_k)/(λ₁+…+λ_p) · 100 ≥ 80`, es razonable usar las primeras k componentes.

**Obs.:** Si las variables tienen unidades diferentes, usar la matriz de **correlación R** en vez de `Σ`.

### Ejemplo: iris (Fisher 1936)
Variables: X₁ longitud sépalo, X₂ ancho sépalo, X₃ longitud pétalo, X₄ ancho pétalo.

Etapas: (1) obtener S de los datos; (2) calcular y ordenar valores/vectores propios; (3) identificar componentes.

Matriz de covarianza:
```
S =
[ 0.69  −0.04   1.27   0.52 ]
[−0.04   0.19  −0.33  −0.12 ]
[ 1.27  −0.33   3.12   1.30 ]
[ 0.52  −0.12   1.30   0.58 ]
```
Valores propios: `(λ₁,λ₂,λ₃,λ₄) = (4.23, 0.24, 0.08, 0.02)`.

Vectores propios (columnas c₁..c₄):
```
C =
[ 0.36  −0.66  −0.58   0.32 ]
[−0.08  −0.73   0.60  −0.32 ]
[ 0.86   0.17   0.08  −0.48 ]
[ 0.36   0.08   0.55   0.75 ]
```
Proporción acumulada: `92.46, 97.77, 99.48, 100.00`. → Con 2 componentes se explica 97.77%.

Componentes:
```
Y₁ = 0.36(X₁−X̄₁) − 0.08(X₂−X̄₂) + 0.86(X₃−X̄₃) + 0.36(X₄−X̄₄)
Y₂ = −0.66(X₁−X̄₁) − 0.73(X₂−X̄₂) + 0.17(X₃−X̄₃) + 0.08(X₄−X̄₄)
```
**Ejercicio:** repetir el análisis con la matriz de **correlación** (en vez de covarianza). Graficar Primera vs Segunda componente.

## Código de referencia

### Python (selección de K + PCA)
```python
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import SilhouetteVisualizer
from sklearn.decomposition import PCA

# Codo
inertias = [KMeans(n_clusters=k, n_init=10, random_state=0).fit(X).inertia_
            for k in range(1, 11)]

# Silhouette
sil = {k: silhouette_score(X, KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X))
       for k in range(2, 11)}

# PCA
pca = PCA().fit(X)
prop = pca.explained_variance_ratio_.cumsum()   # proporción acumulada
```

### R (Gap statistic)
```r
library(cluster)
set.seed(123)
X <- scale(iris[, 1:4])
gap <- clusGap(X, FUN = kmeans, nstart = 25, K.max = 10, B = 50)
print(gap, method = "firstSEmax")   # K̂ por la regla Gap(K) ≥ Gap(K+1) − s_{K+1}
plot(gap)
```
