---
name: aprendizaje-supervisado
description: >
  Expert knowledge base for the EPG4001 Aprendizaje Supervisado course (Magíster en IA, PUC Chile,
  Prof. Jorge Luis Bazán). Covers supervised learning: linear and logistic regression, model
  selection, regularization (Ridge, Lasso, Elastic Net), diagnostics, k-NN, classification metrics
  and ROC curves, cross-validation and bootstrap, bias-variance, LDA/QDA, Naive Bayes, decision
  trees and Random Forest, SVM/kernels, imbalanced classification (SMOTE, under/oversampling), and
  R programming. Use for any EPG4001 question — homework, labs, controls (Q1, Q2), project, syllabus.
  Also trigger on regresión lineal/logística, ANOVA, AIC, BIC, VIF, multicolinealidad, curva ROC,
  matriz de confusión, validación cruzada, K-Fold, sesgo-varianza, F1, análisis discriminante,
  árboles de decisión, índice de Gini, entropía, hiperplano, margen, kernel, clases desbalanceadas,
  Tomek, or course datasets (Default, PimaIndiansDiabetes, Smarket, Vehicle, globwarm, Advertising).
  Respond in Spanish when the user writes in Spanish.
---

# EPG4001 Aprendizaje Supervisado — Knowledge Base

You are an expert tutor for the EPG4001 Aprendizaje Supervisado course. Answer questions accurately
using the knowledge below. When solving exercises, show step-by-step work. When writing R code,
follow the conventions and packages used in the course. Respond in the same language the user uses.

For detailed R code examples and additional reference material, read `references/r-code-examples.md`.

---

## 1. Course Overview

- **Code**: EPG4001
- **Name**: Aprendizaje Supervisado
- **Program**: Magíster en Inteligencia Artificial, Pontificia Universidad Católica de Chile
- **Professor**: Dr. Jorge Luis Bazán (jlbazan@uc.cl)
- **Period**: Segundo Bimestre 2026

### Learning Outcomes
1. Analizar los conceptos fundamentales del aprendizaje supervisado.
2. Distinguir los problemas y desafíos del aprendizaje supervisado.
3. Aplicar métodos para predicción en problemas de clasificación y regresión.
4. Identificar ventajas y desventajas de los métodos según la tarea.
5. Aplicar métricas de evaluación y rendimiento.
6. Seleccionar el algoritmo adecuado dependiendo de la tarea.
7. Resolver problemas reales mediante programas computacionales en R.

### Course Topics
1. Conceptos fundamentales de aprendizaje supervisado
2. Regresión Lineal
3. Regresión Logística
4. Métricas de Desempeño
5. Análisis Discriminante y Naive Bayes
6. Árboles de Decisión y Random Forest
7. Support Vector Machine (SVM) y Vecinos cercanos

### Evaluations
- **Nota Final**: NF = 0.30·Q + 0.30·L + 0.40·P
- **Controles (Q)**: Evaluaciones online en Canvas (conceptos teóricos + ejemplos pedagógicos)
  - Q1: 8 de Junio
  - Q2: 1 de Julio
- **Laboratorios (L)**: Problemas prácticos en R, subida de archivo .R en Canvas
  - Lab1: 15 de Junio
  - Lab2: 6 de Julio
- **Proyecto (P)**: Estudio de caso, informe + presentación, grupos de 4-5 personas
  - Informe: 17 de Julio
  - Presentación: 20 de Julio

### Bibliography

**Mínima:**
1. Kelleher, J., Namee, B.M., D'Arcy, A. "Fundamentals of Machine Learning for Predictive Data Analytics", MIT Press, 2015.
2. Murphy, K. "Machine Learning: A Probabilistic Perspective", MIT Press, 2012.
3. Flach, P. "Machine Learning: The Art and Science of Algorithms that Make Sense of Data", Cambridge University Press, 2012.

**Complementaria:**
1. Gérón, A. "Hands-On Machine Learning with Scikit-Learn and TensorFlow", O'Reilly, 2017.
2. Bishop, C. "Pattern Recognition and Machine Learning", Springer, 2006/2011.
3. Hastie, T., Tibshirani, R. and Friedman, J. "The Elements of Statistical Learning" (2nd Ed.), Springer, 2009.
4. Faraway, J. "Extending the Linear Model with R", Chapman Hall/CRC, 2016.
5. James, G., Witten, D., Hastie, T., Tibshirani, R. "An Introduction to Statistical Learning with Applications in R" (ISLR), Springer, 2013.

---

## 2. Conceptos Fundamentales (Clase 1)

### Definiciones Clave
- **Aprendizaje Supervisado**: Dado un conjunto de datos de entrenamiento donde conocemos tanto las características (X) como el resultado (Y), construimos un modelo de predicción que permite predecir Y para nuevas observaciones. Se llama "supervisado" por la presencia de Y para guiar el aprendizaje.
- **Regresión**: Cuando Y es continua (predicción numérica).
- **Clasificación**: Cuando Y es categórica (asignación a clases).

### Terminología Equivalente
- **X**: Entrada = Características = Regresores = Predictores = Variables Independientes
- **Y**: Salida = Respuesta = Variable Dependiente

### Formulación General
Las técnicas de predicción/clasificación surgen de resolver:
```
mín E[(Y - Ŷ)² | X]  →  Ŷ = E[Y | X]  es el óptimo
```

- En modelos lineales: E[Y|X] = Xβ
- En GLMs: μ = E[Y|X], g(μ) = Xβ
- En clasificación binaria: E[Y|X] = P[Y=1|X], cuando Rec(Y) = {0,1}

### Método k-NN (k-Nearest Neighbors)

**Para regresión**: Dado x₀, encontrar los k vecinos más cercanos N_k(x₀) y estimar:
```
Ŷ_k(x) = (1/k) Σ_{j ∈ N*_k} Y_j
```
Es decir, el promedio de los valores Y de los k vecinos.

**Para clasificación**: Igual búsqueda de vecinos, pero se usa la **moda** de Y en el grupo de vecinos.

**Distancia**: Típicamente distancia euclidiana al cuadrado: d²(xᵢ, x) = Σ(xᵢⱼ - xⱼ)²

**Ejemplo resuelto (Regresión):**
Datos: y=[13,3,0,6,5,6,14,6,5,3], x₁=[9,6,1,3,3,1,9,9,4,6], x₂=[6,2,6,9,7,9,8,2,6,4]
Para x=(5,2):
- Distancias d²: [32,1,32,53,29,65,52,16,17,5]
- 1-NN: N*={2} → Ŷ=3
- 2-NN: N*={2,10} → Ŷ=(3+3)/2=3
- 3-NN: N*={2,10,8} → Ŷ=(3+3+6)/3=4

**Ejemplo resuelto (Clasificación):**
Mismas x, pero y=[a,a,a,a,a,b,b,b,b,b]:
- 1-NN: N*={2} → Ŷ=a
- 2-NN: N*={2,10} → moda{a,b}=empate, se agrega vecino
- 3-NN: N*={2,10,8} → moda{a,b,b}=b

**Nota**: Resultados dependen de k y de la distancia utilizada. Extensión natural: Nadaraya-Watson (promedio ponderado).

---

## 3. Regresión Lineal (Clase 2)

### 3.1 Modelización
```
Yᵢ = β₀ + β₁x_{i1} + β₂x_{i2} + ... + βₚx_{ip} + εᵢ
```
Forma matricial: **Y = Xβ + ε**, donde X es la matriz de diseño (n×(p+1) con columna de 1s).

### 3.2 Estimación por Mínimos Cuadrados
```
β̂ = (X'X)⁻¹X'Y
```

**Caso simple** (un regresor):
- β̂₁ = S_XY / S²_X = Σ(xᵢ-x̄)(yᵢ-ȳ) / Σ(xᵢ-x̄)²
- β̂₀ = ȳ - β̂₁·x̄

**Propiedades** (bajo E[εᵢ]=0, V[εᵢ]=σ²):
- E[β̂] = β (insesgado)
- V[β̂] = σ²(X'X)⁻¹

**Valores ajustados**: Ŷ = Xβ̂
**Residuos**: e = Y - Ŷ
**Estimador de σ²**: S²_e = e'e/(n-p-1) = Σ(Yᵢ-Ŷᵢ)²/(n-p-1)

### 3.3 Bondad de Ajuste
- **SCT** = Σ(Yᵢ - Ȳ)² (Suma de Cuadrados Total)
- **SCR** = Σ(Ŷᵢ - Ȳ)² (Suma de Cuadrados Regresión)
- **SCE** = Σ(Yᵢ - Ŷᵢ)² (Suma de Cuadrados Error)
- **SCT = SCR + SCE**
- **R²** = SCR/SCT = 1 - SCE/SCT (crece con p → problema)
- **R²_adj** = 1 - (SCE/(n-p-1))/(SCT/(n-1)) (penaliza por p)

### 3.4 Predicción
Sea x₀ un vector con valores de covariables:

**Valor Medio** (intervalo de confianza para E[Y₀]):
- Ŷ₀ = x₀β̂
- S²_{E[Y₀]} = S²_e · x₀(X'X)⁻¹x₀'

**Valor Individual** (intervalo de predicción para Y₀):
- Ŷ₀ = x₀β̂ + ε₀
- S²_{Y₀} = S²_e · [x₀(X'X)⁻¹x₀' + 1]

**Ejemplo resuelto**: Inversión vs Rendimiento (n=12)
- β̂₀ = -1.68, β̂₁ = 0.45, R² = 0.382
- Ecuación: Ŷ = -1.68 + 0.45X
- Para X=8: Ŷ = 1.94
- S²_e = 4.24
- IC₉₅%(E[Y₀]) = 1.94 ∓ 3.60
- IC₉₅%(Y₀) = 1.94 ∓ 5.83

### 3.5 Inferencia
Bajo **ε ~ N(0, σ²I)**:
- β̂ ~ N_{p+1}(β, σ²(X'X)⁻¹)
- Estadístico t: T_j = β̂_j / √[S²_β]_{j+1,j+1} ~ t_{n-p-1}

**Tabla ANOVA**:
| Fuente    | Suma² | G.L.    | Cuadrados Medios | Razón F       |
|-----------|-------|---------|------------------|---------------|
| Regresión | SCR   | p       | MCR = SCR/p      | F = MCR/MCE   |
| Error     | SCE   | n-p-1   | MCE = SCE/(n-p-1)|               |
| Total     | SCT   | n-1     |                  |               |

F ~ F_{p, n-p-1} → test global de calidad de ajuste.

### 3.6 Criterios de Selección de Variables
1. **p-valor**: Quitar variables con p > α.
2. **R²_adj**: Eliminar variables que no aporten mejora significativa.
3. **Tabla ANOVA / Deviance**: Test para modelos anidados (H₀: modelo reducido ≈ modelo completo).
4. **Criterios de Información**:
   - AIC = -2ℓ(θ̂) + 2p
   - BIC = -2ℓ(θ̂) + log(n)·p
   - Elegir modelo con menor AIC o BIC.
5. **Stepwise**: Backward, Forward, Both → función `step()` en R.

**Ejemplo Calentamiento Global** (globwarm, 1880-2000):
- M1 (lineal): R²_adj=0.6178, AIC=-113.94, BIC=-105.55
- M2 (cuadrático): R²_adj=0.6385, AIC=-119.68, BIC=-108.49
- M3 (cúbico): R²_adj=0.6383, AIC=-118.65, BIC=-104.67
- Conclusión: M2 es el mejor (ANOVA: F=7.79, p=0.006 entre M1-M2; no significativo M2-M3).

### 3.7 Métodos de Contracción (Regularización)

**Regresión Ridge (L₂)**:
```
mín { ε'ε + (λ/2)Σβ²_j }  ⟺  mín{ε'ε} s.a. Σβ²_j ≤ t
```
Solución (covariables centradas): β̂₀ = Ȳ, β̂ = (X'X + λI_p)⁻¹X'Y

**Regresión Lasso (L₁)**:
```
mín { (1/2)ε'ε + λΣ|β_j| }  ⟺  mín{ε'ε} s.a. Σ|β_j| ≤ t
```
Solución numérica. Puede hacer coeficientes exactamente cero → selección continua de subconjuntos.

**Elastic Net** (combinación Ridge + Lasso):
```
mín { (1/2)ε'ε + λ[αΣ|β_j| + ((1-α)/2)Σβ²_j] }
```

λ se determina por **validación cruzada** o grados de libertad. En R: `glmnet()` del paquete `glmnet`.

### 3.8 Multicolinealidad
- Si columnas de X son colineales → det(X'X) ≈ 0 → varianza inflada de β̂.
- **VIF_j** = 1/(1 - R²_j), donde R²_j es el R² de modelar x_j con las demás covariables.
- **Criterio**: Descartar variable con VIF_j ≥ 10.

### 3.9 Diagnóstico del Modelo
**Supuestos** (deben cumplirse obligatoriamente):
1. **Independencia** de errores
2. **Homocedasticidad** de errores
3. **Normalidad** de errores
4. Variables predictoras **linealmente independientes**

**Tests de autocorrelación**: Durbin-Watson (`dwtest`), Breusch-Godfrey (`bgtest`), Ljung-Box/Box-Pierce (`Box.test`)

**Tests de homocedasticidad**: Gráfica Ŷ vs e, Goldfeld-Quandt (`gqtest`), Breusch-Pagan (`bptest`)

**Tests de normalidad**: QQ-plot (`qqnorm`, `qqline`), Kolmogorov-Smirnov (`ks.test`), Shapiro-Wilk (`shapiro.test`), Lilliefors (`lillie.test`), Anderson-Darling (`ad.test`), Jarque-Bera (`jarque.bera.test`)

---

## 4. Regresión Logística (Complemento 3)

### Modelo
Para Y binaria (0/1), con enlace logit:
```
P(Y=1|X) = e^(β₀+β₁x) / (1 + e^(β₀+β₁x))
```

### Funciones de Enlace
- **Logit**: plogis(x) — simétrica, colas un poco más pesadas
- **Probit**: pnorm(x) — simétrica, centrada en (0, 0.5)
- **CLogLog**: 1 - exp(-exp(x)) — asimétrica, alcanza valores positivos más rápido

### Odds Ratio
```
odd = e^(β₀) · e^(β₁·x)
odd(x+1)/odd(x) = e^(β₁)
```
- Si e^β₁ > 1: riesgo mayor
- Si e^β₁ < 1: riesgo menor

### Ejemplo: chd ~ cigs (wcgs data)
- β̂₀ = -2.742, β̂₁ = 0.023 (p ≈ 9.22e-09)
- OR = e^0.023 = 1.0235 → por cada cigarro adicional, riesgo 2.35% mayor

### Ejemplo: Default data
**Modelo simple** (default ~ income):
- income significativo (p=0.0471), AIC=2920.7

**Modelo múltiple** (default ~ income + student + balance):
- balance altamente significativo (p<2e-16)
- studentYes significativo (p=0.00619)
- income NO significativo (p=0.7115) al incluir las otras variables
- AIC=1579.5 (mejora sustancial)

### Curva ROC y Punto de Corte
- Punto óptimo: 0.031 con AUC = 0.950
- Funciones: `roc()` y `plot()` del paquete `pROC`

### Matriz de Confusión
```
                Estimado (No)    Estimado (Yes)
Real (No)       Verdadero Neg.   Falso Positivo
Real (Yes)      Falso Negativo   Verdadero Pos.
```
- **Sensibilidad** = VP / (VP + FN) = 0.9039
- **Especificidad** = VN / (VN + FP) = 0.8605
- Función: `confusionMatrix()` del paquete `caret`

---

## 5. Métricas de Desempeño y Validación Cruzada (Clase 4)

### 5.1 Sesgo, Varianza y Complejidad
Función de pérdida L(Y, Ŷ): cuadrática (Y-Ŷ)² o absoluta |Y-Ŷ|.
- **Error de entrenamiento**: err = (1/n)Σ L(yᵢ, f̂(xᵢ)) — optimista, baja al subir complejidad.
- **Error de prueba / generalización**: Err_T = E[L(Y, f̂(X))|T]; Err = E[Err_T] (esperado).
A mayor complejidad: ↓sesgo, ↑varianza. Existe una complejidad intermedia que minimiza el error de prueba.

### 5.2 Descomposición Sesgo-Varianza
Para Y = f(X)+ε, E[ε]=0, V[ε]=σ²:
```
Err(x₀) = σ²_ε + [E[f̂(x₀)] - f(x₀)]² + V[f̂(x₀)]
        = Error Irreducible + Sesgo² + Varianza
```
σ²_ε es irreducible (no se elimina por mejor que se estime f̂).

### 5.3 Pérdida en caso Cualitativo (K clases)
- Modela pₖ(X)=P[Y=k|X] → Ŷ = argmaxₖ p̂ₖ(X).
- **Pérdida 0-1**: L = I{Y≠Ŷ}.
- **Deviance / -2·loglik**: L = -2 log p̂_Y(X).

### 5.4 Métricas de Clasificación
- **Accuracy** = (VP+VN)/n — proporción de aciertos.
- **Sensibilidad/Recall** = VP/(VP+FN); **Especificidad** = VN/(VN+FP).
- **F1-Score** = 2·VP/(2·VP+FP+FN) — penaliza el desbalance de clases (preferir cuando los datos están desbalanceados; accuracy engaña con clases raras).
- **AUC** — área bajo la curva ROC.
- **Regresión**: RMSE = √(mean((y-ŷ)²)), MAE = mean(|y-ŷ|), R².

### 5.5 Validación Cruzada
Estima directamente Err = E[L(Y, f̂(X))]. Objetivos: **selección** (elegir el mejor modelo) y **evaluación** (estimar error del modelo final).
- **Simple (Hold-Out)**: partición Entrenamiento - Validación - Test. Train/Validación seleccionan; Test evalúa el modelo final. Típico 70/30.
- **K-Fold**: dividir en K partes (K=5 ó 10). Entrenar con K-1, medir error en la restante; iterar K veces y promediar: CV(f̂)=(1/K)Σ errₖ.
- **LOOCV** (K=n): para modelos lineales con H=X(X'X)⁻¹X', CV = (1/n)Σ[(yᵢ-ŷᵢ)/(1-hᵢᵢ)]²; GCV usa tr(H)/n en lugar de hᵢᵢ.

### 5.6 Bootstrap
Remuestreo con reemplazo, B muestras del mismo tamaño n.
- Êrr_boot = (1/B)(1/n)ΣΣ L(yᵢ, f̂*ᵇ(xᵢ)) — **sesgado** (train y test comparten observaciones).
- P[obs i ∈ muestra bootstrap] ≈ 1-e⁻¹ = 0.632.
- **Leave-one-out bootstrap** Êrr⁽¹⁾: solo predice con muestras que NO contienen la observación i.
- **Estimador 0.632**: Êrr⁽⁰·⁶³²⁾ = 0.368·err + 0.632·Êrr⁽¹⁾. Existe versión mejorada 0.632+.

**R**: `boot::cv.glm` (K-Fold/LOOCV desde GLM), `caret` (`trainControl` con method "cv"/"boot632"), `Metrics` (RMSE, MAE, F1, precision, recall).

---

## 6. Análisis Discriminante y Naive Bayes (Clase 5)

Objetivo: maximizar la probabilidad posterior P(G=k|X=x) para una clasificación óptima.
Por **teorema de Bayes**, con fₖ(x) densidad condicional de X dado G=k y πₖ=P(G=k):
```
P(G=k|X=x) = fₖ(x)πₖ / Σₗ fₗ(x)πₗ
```
π̂ₖ = nₖ/n. La regla óptima: Ĝ(x) = argmaxₖ δₖ(x), con δₖ(x) = log πₖ + log fₖ(x).

### 6.1 Naive Bayes
Asume independencia condicional de las características dada la clase (apropiado con p grande):
```
fₖ(X) = Πⱼ fₖⱼ(Xⱼ)
```
Marginales fₖⱼ según el tipo de variable:
- **Continua Gaussiana**: N(X̄ₖⱼ, S²ₖⱼ) con media y varianza de Xⱼ restringidas a la clase k.
- **Categórica (L estados)**: Multinomial. EMV p̂ₖᵢ = xᵢ/nₖ; **suavizado de Laplace** p̂ₖᵢ = (xₖᵢ+α)/(nₖ+α·L).
- **Conteos enteros**: Poisson(λ̂=X̄ₖⱼ).
- Densidades continuas también estimables por **kernel** (caja, Gaussiano, Triangular, Epanechnikov).

**Ejemplo resuelto** (n=10, x*=(4,8), marginales Gaussianas):
- f₁(4,8)=0.0133, π₁=0.6; f₂(4,8)=0.0066, π₂=0.4.
- P[G=1|x]=0.0133·0.6/(0.0133·0.6+0.0066·0.4)=0.7517 → clasifica G=1.

### 6.2 LDA y QDA
Asumen fₖ(x) = N(µₖ, Σₖ). Densidad normal multivariada:
fₖ(x) = (2π)^(-p/2)|Σₖ|^(-1/2) exp(-½(x-µₖ)'Σₖ⁻¹(x-µₖ)).

- **LDA**: Σₖ = Σ **iguales** entre grupos → δₖ(x) **lineal**:
  ```
  δₖ(x) = x'Σ⁻¹µₖ - ½µₖ'Σ⁻¹µₖ + log πₖ
  ```
- **QDA**: Σₖ **distintas** → δₖ(x) **cuadrática**:
  ```
  δₖ(x) = -½(x-µₖ)'Σₖ⁻¹(x-µₖ) - ½log|Σₖ| + log πₖ
  ```
Estimadores: µ̂ₖ=media por clase; Σ̂ₖ=covarianza por clase; Σ̂ pooled = (1/(n-K))Σₖ(nₖ-1)Σ̂ₖ.

**Ejemplo LDA** (x*=(4,8)): δ₁=15.59 > δ₂=13.54 → G=1, P[G=1|x]=0.8859.
**Ejemplo QDA** (mismo x*): δ₁=-2.656 > δ₂=-5.770 → G=1, P[G=1|x]=0.9575.

### 6.3 Comparación
| | Naive Bayes | LDA | QDA |
|---|---|---|---|
| fₖ(x) | Πⱼ fₖⱼ(xⱼ) | N(µₖ,Σ) | N(µₖ,Σₖ) |
| Covarianzas | no modela conjunta | Σ compartida | Σₖ distintas |
| Frontera | no lineal (general) | lineal | cuadrática |
| Sesgo / Varianza | alto / bajo | mayor / menor | menor / mayor |

**Regla práctica**: LDA cuando nₖ < 5p (reduce varianza, una sola Σ); QDA con muestras grandes y p moderado, o evidencia de covarianzas distintas. Seleccionar empíricamente por error de test/CV.

**R**: `e1071::naiveBayes`, `naivebayes::naive_bayes`, `MASS::lda`, `MASS::qda`.

---

## 7. Árboles de Decisión y Random Forest (Clase 6)

Método supervisado para clasificación y regresión. Componentes: nodo raíz, nodos de decisión (internos), nodos hoja (terminales con la predicción). Divide el espacio de covariables en rectángulos y ajusta un modelo simple (constante) en cada uno, buscando grupos cada vez más homogéneos.

### 7.1 Árboles de Regresión — Algoritmo
1. Considerar todas las particiones binarias paralelas a un eje (máximo (n-1)p).
2. En cada región usar la media; elegir la partición que minimiza RSS = RSS(part1)+RSS(part2).
3. Recursión hasta criterio de parada (mínimo de datos por nodo o complejidad).

**Ejemplo**: partición x₁<4 vs x₁≥4 → ȳ=4.24 y ȳ=7.33; sub-partición de x₁≥4 por x₂.

### 7.2 Poda (Cost-Complexity Pruning)
Crecer árbol grande T₀, luego podar. Para nodo terminal m (región Rₘ, Nₘ obs):
ĉₘ = media de yᵢ en Rₘ; Qₘ(T) = (1/Nₘ)Σ(yᵢ-ĉₘ)².
```
Cα(T) = Σₘ Nₘ Qₘ(T) + α|T|
```
α≥0 controla tamaño vs ajuste (α=0 → árbol completo T₀). Para cada α hay un único subárbol mínimo Tα, hallado por **poda del eslabón más débil**. α̂ se elige por **validación cruzada k-fold**.

### 7.3 Árboles de Clasificación — Impureza del nodo
p̂ₘₖ = proporción de clase k en el nodo m; se clasifica como k(m)=argmaxₖ p̂ₘₖ. Medidas de impureza Qₘ(T):
- **Error de clasificación**: 1 - p̂ₘ,ₖ(ₘ)
- **Índice de Gini**: Σₖ p̂ₘₖ(1-p̂ₘₖ)
- **Deviance / Entropía cruzada**: -Σₖ p̂ₘₖ ln(p̂ₘₖ)

Para **crecer** el árbol usar Gini o entropía (más sensibles); para **podar** suele usarse el error de clasificación.

### 7.4 Random Forest
Conjunto (ensemble) de árboles sobre submuestras bootstrap (con reemplazo). Cada árbol:
1. Muestra bootstrap de tamaño N del entrenamiento.
2. En cada nodo, seleccionar aleatoriamente M < p variables (M constante en todo el bosque); mejor división entre esas M.
3. Crecer al máximo, **sin poda**.
4. Predicción agregada: **mayoría de votos** (clasificación), **promedio** (regresión).

El bootstrap + selección aleatoria de variables decorrelaciona los árboles y reduce la varianza.

**R**: `rpart` + `rpart.plot` (`method="class"` o `"anova"`), `randomForest(y~., ntree=500, importance=TRUE)`.

---

## 8. SVM, Clases Desbalanceadas y KNN (Clase 7)

### 8.1 Support Vector Machine (SVM)
Construye un **hiperplano de separación óptimo** que maximiza el margen entre clases. Hiperplano: P = {x : x'β + β₀ = 0, ‖β‖=1}; f(x)=x'β+β₀ es la distancia con signo.

**SVM lineal separable** (yᵢ ∈ {-1,1}): regla G(x)=sign(x'β+β₀). El problema
```
máx M  s.a.  ‖β‖=1,  yᵢ(xᵢ'β+β₀) ≥ M
```
es equivalente a **mín ½‖β‖² s.a. yᵢ(xᵢ'β+β₀) ≥ 1** (cuadrático convexo). Del dual (multiplicadores de Lagrange αᵢ) se obtiene β = Σ αᵢyᵢxᵢ; los puntos con αᵢ>0 son los **vectores de soporte**.

**Caso no separable (C-SVM)**: variables de holgura ξᵢ≥0:
```
mín  ½‖β‖² + C·Σξᵢ   s.a.  yᵢ(xᵢ'β+β₀) ≥ 1-ξᵢ
```
Dual con 0 ≤ αᵢ ≤ C. El **parámetro de coste C** regula el trade-off (C=∞ → caso separable). Puntos en el borde: 0<α̂ᵢ<C; dentro del margen: α̂ᵢ=C.

**SVM no lineal (kernel trick)**: el dual depende solo de productos internos xᵢ'xⱼ. Se sustituye por un **kernel** K(u,v)=⟨h(u),h(v)⟩ (simétrico, semidefinido positivo) → fronteras curvas. Solución: f̃(x)=Σ α̂ᵢyᵢK(x,xᵢ)+β̂₀.
- **Polinomial**: K(u,v)=(1+⟨u,v⟩)^d
- **Radial (RBF)**: K(u,v)=exp(-γ‖u-v‖²)
- **Red neuronal (sigmoide)**: K(u,v)=tanh(κ₁⟨u,v⟩+κ₂)

**R**: `e1071::svm(y~., kernel="linear"/"radial"/"polynomial", cost=C, gamma=...)`; ajustar hiperparámetros con `tune()` (CV).

### 8.2 Clasificación con Clases Desbalanceadas
Una clase >90% (mayoritaria); la minoritaria <10% suele ser la de interés (fraude, enfermedades, fuga, spam). Accuracy engaña → usar F1, sensibilidad/especificidad, AUC. **El rebalanceo se aplica solo al conjunto de entrenamiento.**

**Undersampling** (elimina de la clase mayoritaria):
- **Aleatorio**: quita casos al azar.
- **Condensed NN (CNN)**: basado en 1-NN, conserva un prototipo removiendo redundantes.
- **Tomek Links**: elimina pares mutuamente más cercanos de distinta clase (limpia la frontera).
- **Edited NN (ENN)**: basado en 3-NN; elimina el caso mayoritario si ≥2 vecinos difieren. Repetido = RENN.

**Oversampling** (aumenta la clase minoritaria):
- **Aleatorio**: replica casos al azar.
- **SMOTE** (Synthetic Minority Oversampling): genera datos sintéticos entre un caso y sus k-vecinos: Sᵢ = Xⱼ + λ(Xᵢʲ - Xⱼ), λ~U(0,1).

**Híbridas**: SMOTE-Tomek, SMOTE-ENN (exacerban minoritaria + limpian mayoritaria).

**Probabilidad de corte**: en vez de 0.5, elegir el umbral que optimice una métrica variando el corte de 0 a 1:
- Igualar sensibilidad y especificidad.
- Maximizar F-beta para un β fijo.

**R**: `caret`/`themis` (`trainControl(sampling="smote"/"up"/"down")`), `unbalanced`.

### 8.3 KNN (Vecinos más cercanos)
Método **no paramétrico, basado en memoria**: no hay entrenamiento explícito; el costo se paga al predecir. Dado x₀, usar la vecindad Nₖ(x₀) de los k puntos de entrenamiento más cercanos:
- **Regresión**: Ŷ(x₀) = (1/k)Σ yᵢ (promedio de vecinos).
- **Clasificación**: Ĝ(x₀) = moda de las clases de los vecinos.

Distancia euclidiana por defecto; **estandarizar** predictores con escalas distintas. El único parámetro es **k** (trade-off sesgo-varianza):
- **k pequeño (k=1)**: baja sesgo, alta varianza; frontera irregular (Voronoi).
- **k grande**: baja varianza, mayor sesgo; frontera suave.

k óptimo por validación cruzada. Propiedades: consistencia asintótica (si N,k→∞, k/N→0, k-NN → E[Y|X=x]); **maldición de la dimensionalidad** (vecinos lejanos en p alto); Cover-Hart (1967): error de 1-NN ≤ 2× error de Bayes asintóticamente.

**R**: `class::knn(train, test, cl, k)`.

---

## 9. Datasets del Curso

### Default (ISLR)
- 10,000 observaciones, 4 variables
- **default**: factor (No/Yes) — incumplimiento de deuda
- **student**: factor (No/Yes)
- **balance**: saldo promedio tarjeta de crédito
- **income**: ingreso del cliente
- Uso: `datos <- Default`

### PimaIndiansDiabetes (mlbench)
- 768 observaciones, 9 variables
- pregnant, glucose, pressure, triceps, insulin, mass, pedigree, age
- **diabetes**: factor (pos/neg)
- Uso: `data("PimaIndiansDiabetes"); datos <- PimaIndiansDiabetes`
- Nota: requiere `data()` previo (no carga automáticamente)

### Smarket (ISLR)
- 1,250 observaciones, 9 variables
- Rendimientos S&P 500 (2001-2005)
- Year, Lag1-Lag5, Volume, Today
- **Direction**: factor (Down/Up)
- Uso: `datos <- Smarket`

### Vehicle (mlbench)
- 846 observaciones, 19 variables (18 numéricas + 1 categórica)
- Características de siluetas de vehículos
- **Class**: van, saab, bus, opel
- Uso: `data("Vehicle"); datos <- Vehicle`

### globwarm (faraway)
- Temperatura hemisferio norte desde año 1000
- Uso: `data(globwarm)`, filtrar con `subset(globwarm, year >= 1880)`

### Advertising (ISLR / James et al.)
- 200 mercados, gasto publicitario en TV, radio, newspaper
- **sales**: ventas (respuesta continua) — usado en ejemplos de regresión y RMSE/MAE/CV

---

## 10. R Packages & Functions

### Paquetes principales
| Paquete   | Contenido                                              |
|-----------|---------------------------------------------------------|
| ISLR      | Bases de datos (Default, Smarket)                       |
| MASS      | Herramientas estadísticas, regresión                    |
| tree      | Árboles de decisión                                     |
| class     | Clasificación (k-NN)                                    |
| e1071     | SVM, Naive Bayes                                        |
| mlbench   | Bases de datos (PimaIndiansDiabetes, Vehicle)           |
| pROC      | Curvas ROC, AUC                                         |
| caret     | confusionMatrix, train, validación cruzada              |
| car       | VIF (`vif()`), diagnósticos                             |
| nortest   | Tests de normalidad (Lilliefors, Anderson-Darling)      |
| tseries   | Test Jarque-Bera                                        |
| lmtest    | Tests Durbin-Watson, Breusch-Pagan, Goldfeld-Quandt     |
| faraway   | Datos (globwarm, wcgs), funciones auxiliares             |
| glmnet    | Ridge, Lasso, Elastic Net                               |
| boot      | Bootstrap, validación cruzada (`cv.glm`)                |
| Metrics   | RMSE, MAE, MSE, F1, precision, recall                   |
| rpart     | Árboles de decisión (CART)                              |
| rpart.plot| Visualización de árboles                                |
| randomForest | Random Forest                                        |
| naivebayes| Naive Bayes (`naive_bayes`)                             |
| class     | KNN (`knn()`), clasificación                            |
| themis    | SMOTE y rebalanceo de clases (recipes)                  |

### Funciones clave
- `lm()` — Regresión lineal
- `glm(family=binomial(link="logit"))` — Regresión logística
- `summary()` — Coeficientes, SE, significancia, R²
- `anova()` — Tabla ANOVA / comparación de modelos anidados
- `predict(model, newdata, interval="confidence")` — Predicción con IC
- `step()` — Selección stepwise (AIC/BIC)
- `AIC()`, `BIC()` — Criterios de información
- `vif()` (car) — Factor de inflación de varianza
- `roc()`, `plot()` (pROC) — Curva ROC
- `confusionMatrix()` (caret) — Matriz de confusión completa
- `glmnet()` (glmnet) — Regularización Ridge/Lasso/Elastic Net
- `cv.glm()` (boot) — Validación cruzada K-Fold/LOOCV de GLM
- `train()`, `trainControl()` (caret) — CV, bootstrap, ajuste de modelos
- `lda()`, `qda()` (MASS) — Análisis discriminante lineal/cuadrático
- `naiveBayes()` (e1071), `naive_bayes()` (naivebayes) — Naive Bayes
- `rpart()` + `rpart.plot()` — Árboles de decisión (CART)
- `randomForest()` (randomForest) — Random Forest
- `svm()`, `tune()` (e1071) — SVM (kernels lineal/radial/polinomial) y selección de hiperparámetros
- `knn()` (class) — k vecinos más cercanos

---

## 11. Key Formulas Quick Reference

| Concepto | Fórmula |
|----------|---------|
| MCO | β̂ = (X'X)⁻¹X'Y |
| Varianza β̂ | V[β̂] = σ²(X'X)⁻¹ |
| R² | 1 - SCE/SCT |
| R²_adj | 1 - (SCE/(n-p-1))/(SCT/(n-1)) |
| AIC | -2ℓ(θ̂) + 2p |
| BIC | -2ℓ(θ̂) + log(n)·p |
| VIF | 1/(1-R²_j) |
| Logit | P(Y=1|X) = e^(Xβ)/(1+e^(Xβ)) |
| Odds Ratio | e^(β₁) |
| Sensibilidad | VP/(VP+FN) |
| Especificidad | VN/(VN+FP) |
| Ridge | β̂ = (X'X+λI)⁻¹X'Y |
| k-NN (regresión) | Ŷ = (1/k)Σ Y_j (vecinos) |
| k-NN (clasificación) | Ŷ = moda(Y_j) (vecinos) |
| Elastic Net | mín{½ε'ε + λ[αΣ|βⱼ| + ((1-α)/2)Σβⱼ²]} |
| F1-Score | 2·VP/(2·VP+FP+FN) |
| Accuracy | (VP+VN)/n |
| Sesgo-Varianza | Err(x₀) = σ²_ε + Sesgo² + Varianza |
| K-Fold CV | CV(f̂) = (1/K)Σ errₖ |
| Bootstrap 0.632 | Êrr = 0.368·err + 0.632·Êrr⁽¹⁾ |
| Bayes posterior | P(G=k\|X) = fₖ(x)πₖ / Σₗ fₗ(x)πₗ |
| LDA (lineal) | δₖ(x) = x'Σ⁻¹µₖ - ½µₖ'Σ⁻¹µₖ + log πₖ |
| QDA (cuadrática) | δₖ(x) = -½(x-µₖ)'Σₖ⁻¹(x-µₖ) - ½log\|Σₖ\| + log πₖ |
| Naive Bayes | fₖ(X) = Πⱼ fₖⱼ(Xⱼ) |
| Gini | Σₖ p̂ₘₖ(1-p̂ₘₖ) |
| Entropía | -Σₖ p̂ₘₖ ln(p̂ₘₖ) |
| Cost-complexity | Cα(T) = Σₘ Nₘ Qₘ(T) + α\|T\| |
| SVM (margen duro) | mín ½‖β‖² s.a. yᵢ(xᵢ'β+β₀) ≥ 1 |
| C-SVM (holgura) | mín ½‖β‖² + C·Σξᵢ s.a. yᵢ(xᵢ'β+β₀) ≥ 1-ξᵢ |
| SVM kernel | f̃(x) = Σ α̂ᵢyᵢK(x,xᵢ) + β̂₀ |
| Kernel RBF | K(u,v) = exp(-γ‖u-v‖²) |
| SMOTE | Sᵢ = Xⱼ + λ(Xᵢʲ-Xⱼ), λ~U(0,1) |
| KNN (regresión) | Ŷ(x₀) = (1/k)Σ yᵢ (vecinos) |
| KNN (clasificación) | Ĝ(x₀) = moda(yᵢ) (vecinos) |
