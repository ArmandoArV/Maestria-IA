---
name: aprendizaje-no-supervisado
description: Expert knowledge base for the EPG4002 Aprendizaje No Supervisado course (Magíster en Inteligencia Artificial, Pontificia Universidad Católica de Chile, Prof. Jonathan Acosta, Segundo Bimestre 2026). Covers unsupervised learning fundamentals, similarity/dissimilarity measures, hierarchical clustering (single/complete/average/Ward linkage), non-hierarchical clustering (K-means, K-medoids/PAM, K-modes, K-prototypes), Gower distance for mixed data, choosing the number of clusters (elbow, CH(K), Hartigan H(K), Silhouette, Gap statistic), Principal Component Analysis (PCA), and the Python/R code used in the course. Use this skill whenever the user asks about their Aprendizaje No Supervisado course, homework, labs, controls, project, or any topic from the EPG4002 syllabus. Also trigger when they mention concepts like clustering, agrupamiento, distancia de Gower, distancia euclidiana/Manhattan/Minkowski/Mahalanobis, Jaccard, simple matching, dendrograma, enlace simple/completo/promedio/Ward, K-means/K-medias, K-medoids, PAM, K-prototype, método del codo, Silhouette, Gap statistic, CH(K), Calinski-Harabasz, componentes principales, PCA, valores/vectores propios, or any dataset used in the course (iris, datos mixtos de Agresti). Respond in Spanish when the user writes in Spanish.
---

# Aprendizaje No Supervisado (EPG4002)

Knowledge base for the EPG4002 course at PUC Chile (Magíster en IA, Prof. Jonathan Acosta, Segundo Bimestre 2026). Use it to answer conceptual questions, solve exercises, explain algorithms by hand, and write the Python/R code the course uses.

## How to use this skill

1. **Match the course's notation and conventions.** The course works mostly with worked-by-hand examples (small distance matrices, K-means/K-medoids iterations) and then reproduces them in code. When a student asks for help, prefer the *same* method and notation taught in class over alternative formulations.
2. **Respond in the student's language.** The course is in Spanish; if the user writes in Spanish, answer in Spanish. Keep mathematical notation standard.
3. **For deeper detail on a class, read the matching reference file** in `references/` (listed below). SKILL.md is the map; the reference files hold the worked examples and formulas.
4. **For code tasks, follow the libraries already used in class** (see "Code conventions" below) rather than introducing new dependencies.

## Course map

| Clase | Tema | Reference file |
|-------|------|----------------|
| 1 | Introducción al aprendizaje no supervisado; medidas de similaridad y disimilaridad | `references/clase1-similaridad.md` |
| 2 | Datos mixtos (Gower, k-prototype); métodos jerárquicos aglomerativos | `references/clase2-jerarquico.md` |
| 3 | Métodos no jerárquicos: K-medias y K-medoids (PAM) | `references/clase3-kmeans-kmedoids.md` |
| 4 | Selección del número de clusters; Componentes Principales (PCA) | `references/clase4-numK-pca.md` |

Read the relevant file when a question goes beyond the summary below.

## Core concepts (quick reference)

### What unsupervised learning is
- Learning "without a teacher": only `X` is observed, no response `Y`. Interest is in `P(X)` itself, not `P(Y|X)`.
- All variables are of interest; usually high-dimensional; no direct measure of success, so validity is judged with heuristics.
- Central tasks: find natural groups, identify similar observations, detect anomalies, summarize global structure.

### Similarity & dissimilarity (Clase 1)
- **Dissimilarity** `d`: `d(x,y) ≥ 0`, `d(x,y)=0 ⟺ x=y`, symmetric.
- **Similarity** `s`: `0 ≤ s ≤ 1`, `s=1 ⟺ x=y`, symmetric. Conversions: `d = 1−s`, `s = 1/(1+d)`, `s = exp(−d)`.
- Quantitative distances: **Euclidean**, **weighted/generalized** `d_A` (with `A=S⁻¹` → **Mahalanobis**), **Manhattan**, **Minkowski**, **Canberra**, **Czekanowski/Sørensen-Dice**, **cosine**.
- Standardize/normalize when variables have very different scales (e.g., ingreso vs. edad), or one variable dominates the distance.
- If variables are standardized: `d_euclid(x,y) = √(2[1−r(x,y)])`. Pearson `r` itself is *not* a similarity measure.
- Binary variables (contingency a,b,c,d): **Simple Matching** `(a+d)/(a+b+c+d)`, **Double Matching** `2(a+d)/(2(a+d)+b+c)`, **Jaccard** `a/(a+b+c)`.

### Mixed data (Clase 2)
- **Gower distance**: averages per-variable contributions — for categorical use `I(Xⱼ≠Yⱼ)`, for numeric use `|Xⱼ−Yⱼ|/rangoⱼ`. Then `S_G = 1 − D_G`.
- **k-prototype dissimilarity**: `d = d_euc(num) + λ·d_sm(cat)`, `λ ≥ 0`.

### Hierarchical clustering (Clase 2)
- Two strategies: **aglomerativa** (bottom-up) and **divisiva** (top-down). Must also choose the **linkage**.
- Linkages when merging cluster `(uv)` with `w`:
  - **Simple (single):** `d_{(uv)w} = mín{d_uw, d_vw}` — chaining, large diameter.
  - **Completo (complete):** `d_{(uv)w} = máx{d_uw, d_vw}` — compact clusters, small diameter.
  - **Promedio (average):** `d_{(uv)w} = (d_uw + d_vw)/2` — compromise. *Not invariant* under monotone transforms of dissimilarities (single & complete are invariant).
  - Also: **Ward** (minimum variance, squares dissimilarities before update; common default), WPGMA, WPGMC, UPGMC.
- Result is a **dendrograma**; lets you explore partitions without fixing K beforehand.

### Non-hierarchical clustering (Clase 3)
- **K-means / K-medias**: numeric data, squared Euclidean distance, center = mean. Minimizes within-cluster variance `V_D`. `V_T = V_D + V_E` (total = within + between). Converges to a possibly local optimum; restart with many random seeds (Hartigan & Wong 1979).
- Variants: **K-mode** (categorical), **K-prototype** (mixed), **K-medoids** (any dissimilarity, center is a real data point), **K-mediana**.
- **K-medoids**: change the dissimilarity or the center. Center is an observation; computationally heavier. `T = W(C) + B(C)`; objective `min W(C)` ↔ `max B(C)`.
- **PAM (Partition Around Medoids)**, Kaufman & Rousseeuw 1990: pick K medoids, assign points, then swap medoid↔point while cost decreases; undo swaps that raise total distance.

### Choosing K (Clase 4)
- **Codo (elbow):** plot `W_K` (or `B_K`, or `B_K/T·100`) vs K; pick where it stabilizes, or first K reaching 80–90% of `B_K/T`. Visual/subjective.
- **CH(K)** Calinski-Harabasz (1974): `CH(K) = [B_K/(K−1)] / [W_K/(n−K)]`; `K̂ = argmax CH(K)`, K≥2.
- **H(K)** Hartigan (1975): `H(K) = [W_K/W_{K+1} − 1]/(n−K−1)`; add a cluster while `H(K) > 10`; choose smallest K with `H(K) ≤ 10`.
- **Silhouette** Kaufman & Rousseeuw (1990): `s(i) = (b(i)−a(i))/máx{a(i),b(i)}`; `K̂ = argmax s(K)`, K≥2.
- **Gap statistic** Tibshirani, Walther & Hastie (2001): compare `ln(W_K)` to a reference distribution; `K̂ =` smallest K with `Gap(K) ≥ Gap(K+1) − s_{K+1}`.

### Principal Component Analysis (Clase 4)
- `Y = AX` (linear combos) maximizing variance with orthogonal components; eigenvectors of `Σ` solve it, eigenvalues = variance per component.
- Uses: dimension reduction, outlier detection, visualizing high-dimensional variability.
- `Σ = CΛCᵀ`; `V[cᵢᵀX] = λᵢ`. Proportion of variance of first k components = `(λ₁+…+λ_k)/(λ₁+…+λ_p)` (using `tr(Σ)=Σλᵢ`). Keep k components when proportion ≥ 80%.
- If variables have different units, use the **correlation matrix R** instead of `Σ`.
- Course example: Fisher's **iris** (4 vars); eigenvalues `(4.23, 0.24, 0.08, 0.02)`, first 2 PCs explain 97.77%.

## Code conventions

The course uses **Python** (primary) and **R** (for Gap statistic, since it isn't built into the Python material).

**Python stack** (from the course notebooks):
```python
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from sklearn.preprocessing import scale, StandardScaler
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import linkage
from sklearn.metrics import pairwise_distances, silhouette_score
from sklearn.cluster import AgglomerativeClustering, KMeans
import gower                      # Gower distance for mixed data
from yellowbrick.cluster import SilhouetteVisualizer
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
```

**R stack** (Gap statistic):
```r
library(cluster)   # clusGap, pam, daisy(..., metric="gower")
set.seed(123)
```

Guidance:
- Prefer these already-imported libraries; don't add new dependencies for something a few lines can do.
- Standardize with `scale`/`StandardScaler` when scales differ; note in PCA whether to use covariance or correlation.
- Reproduce the by-hand examples exactly (same data, same `k`, same linkage/metric) when a student is checking their manual work.
- For Gap statistic in Python, point students to R's `cluster::clusGap` (matches the course's `Clase4_..._R_GapStatistic` notebook).

## Bibliography (course references)
- Kaufman & Rousseeuw, *Finding Groups in Data: An Introduction to Cluster Analysis*, Wiley, 2005.
- Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006.
- Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning*, Springer, 2008.
