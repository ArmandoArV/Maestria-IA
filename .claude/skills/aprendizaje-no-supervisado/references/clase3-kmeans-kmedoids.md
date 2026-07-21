# Clase 3 — K-medias y K-medoids

## Enlaces jerárquicos adicionales
Desde lo aglomerativo también existen: **Ward, WPGMA, WPGMC, UPGMC**.
- **Ward** (criterio de varianza mínima, Ward 1963) es default en varios programas. Evalúa una función objetivo en cada etapa: une los clústeres que **minimizan la varianza dentro** (del error). Mismo principio que K-medias.
- En Ward las disimilitudes **se elevan al cuadrado** antes de actualizar el clúster.

## Método de K-medias (K-means)
- Método de agrupación por descenso iterativo, muy popular.
- Pensado para variables **cuantitativas**; usa **distancia euclidiana al cuadrado** como disimilaridad.
- Divide una muestra de tamaño n en K clases.

**Rutina:**
1. Escoger K centros de forma aleatoria.
2. Agrupar cada dato al centro más cercano.
3. Recalcular el centro (promedio) de cada grupo.
4. Iterar (2)–(3) hasta criterio de parada.

### Descomposición de la variabilidad
```
V_T = Σⱼ Σᵢ ‖X_ij − X̄‖²        (variabilidad total; X̄ = promedio total por variable)
V_D = Σⱼ Σᵢ ‖X_ij − X̄ⱼ‖²       (varianza DENTRO)
V_E = Σⱼ nⱼ ‖X̄ⱼ − X̄‖²          (varianza ENTRE)
```
`V_T = V_D + V_E`. La función objetivo es **minimizar la variabilidad dentro `V_D`**.

### Criterios de parada
- Iterar hasta que no se reduzca la varianza dentro (convergencia asegurada, posible **óptimo local**).
- Hartigan & Wong (1979): iniciar con muchas opciones aleatorias de medias iniciales y elegir la de menor función objetivo.
- Si se exige parar cuando ninguna observación cambia de grupo, podría no converger → detener en un número máximo de iteraciones.

### Ejemplo K-medias (k=2, sin escalar)
Observaciones:
| i | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| x | 10 | 8 | 34 | 9 | 46 | 68 |
| y | 4 | 99 | 44 | 50 | 77 | 30 |

Centros iniciales al azar: `C₁=(15,20)`, `C₂=(50,50)`. Distancias **al cuadrado**:

| obs | a C₁ | a C₂ | Asignar |
|-----|------|------|---------|
| 1 | 281 | 3716 | G1 |
| 2 | 6290 | 4165 | G2 |
| 3 | 937 | 292 | G2 |
| 4 | 936 | 1681 | G1 |
| 5 | 4210 | 745 | G2 |
| 6 | 2909 | 724 | G2 |

→ `G₁ = {1,4}`, `G₂ = {2,3,5,6}`. Nuevos centros: `C₁=(9.5, 27.0)`, `C₂=(39.0, 62.5)`.

Segunda iteración:
| obs | a C₁ | a C₂ | Asignar |
|-----|------|------|---------|
| 1 | 529.25 | 4263.25 | G1 |
| 2 | 5186.25 | 2293.25 | G2 |
| 3 | 889.25 | 367.25 | G2 |
| 4 | 529.25 | 1056.25 | G1 |
| 5 | 3832.25 | 259.25 | G2 |
| 6 | 3431.25 | 1897.25 | G2 |

→ `G₁ = {1,4}`, `G₂ = {2,3,5,6}` (se mantienen) → converge.

> ¿Cuándo conviene escalar? Cuando las variables tienen escalas/unidades muy distintas y una dominaría la distancia.

## Generalizaciones del K-medias
La restricción principal es que solo sirve para datos numéricos (distancia euclidiana). Variantes:
- **K-mode:** datos categóricos.
- **K-prototype:** datos mixtos (mezcla de K-means y K-mode).
- **K-medoids:** cualquier tipo de dato (con disimilaridad apropiada); cambia la forma de buscar el centro.
- **K-mediana:** como K-medias pero el centro es la mediana.

## Método de K-medoids
- Adaptación del K-means: cambiar la medida de disimilaridad **o** el centro.
- A diferencia de K-means, el centro (**medoid**) es un **punto de la muestra**.
- Requiere optimización en cada etapa (al cambiar la distancia no se conoce el óptimo del centro) → más intensivo computacionalmente.

### Formalización
Con codificador `C(i)=k` (asigna obs i al cluster k) y `d_ij = d(xᵢ,xⱼ)`:
```
T = (1/2) Σ_k Σ_{C(i)=k} [ Σ_{C(j)=k} d_ij + Σ_{C(j)≠k} d_ij ]   (constante para datos fijos)
W(C) = (1/2) Σ_k Σ_{C(i)=k} Σ_{C(j)=k} d_ij     (Within-Cluster)
B(C) = (1/2) Σ_k Σ_{C(i)=k} Σ_{C(j)≠k} d_ij     (Between-Cluster)
```
`T = W(C) + B(C)`. Objetivo: `min W(C)` ↔ `max B(C)`. (En K-means, `W(C)` se minimiza en el promedio.)

### Algoritmo (búsqueda exhaustiva)
1. Para una asignación C, encontrar en cada cluster la observación que minimiza la distancia total a los demás:
   `i*_k = argmin_{C(i)=k} Σ_{C(j)=k} d_ij`. Entonces `m_k = x_{i*_k}` son los centros.
2. Dados los centros `{m₁,…,m_K}`, asignar cada obs al centro más cercano: `C(i) = argmin_k d(xᵢ, m_k)`.
3. Repetir 1–2 hasta que las asignaciones no cambien.

### Algoritmo PAM (Partición Alrededor de Medoids)
Kaufman & Rousseeuw (1990) — la búsqueda exhaustiva es costosa:
1. Seleccionar K de los n puntos como medoids.
2. Asociar cada punto al medoid más cercano.
3. Mientras el costo disminuya: intercambiar un medoid con otro punto y recalcular distancias. Si la distancia total **aumentó**, deshacer el intercambio.

### Ejemplo K-medoids (k=2, distancia de Manhattan, sin escalar)
Mismas 6 observaciones del ejemplo de K-medias.

Centros iniciales (de los datos): `C₁=(10,4)` [obs 1], `C₂=(46,77)` [obs 5]. Distancias Manhattan:
| obs | a C₁ | a C₂ | Asignar | d(xᵢ,m_k) |
|-----|------|------|---------|-----------|
| 1 | – | – | – | – |
| 2 | 97 | 60 | G2 | 60 |
| 3 | 64 | 45 | G2 | 45 |
| 4 | 47 | 64 | G1 | 47 |
| 5 | – | – | – | – |
| 6 | 84 | 69 | G2 | 69 |

→ `G₁ = {1,4}`, `G₂ = {2,3,5,6}`, **costo = 221**.

Probar nuevo medoid: `C₁=(10,4)`, `C₂=(68,30)` [obs 6]:
| obs | a C₁ | a C₂ | Asignar | d(xᵢ,m_k) |
|-----|------|------|---------|-----------|
| 1 | – | – | – | – |
| 2 | 97 | 129 | G1 | 97 |
| 3 | 64 | 48 | G2 | 48 |
| 4 | 47 | 79 | G1 | 47 |
| 5 | 109 | 69 | G2 | 69 |
| 6 | – | – | – | – |

→ `G₁ = {1,2,4}`, `G₂ = {3,5,6}`, **costo = 261** (aumenta) → **deshacer el cambio**.
