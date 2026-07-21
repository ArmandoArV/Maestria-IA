# Clase 1 — Introducción y Medidas de Similaridad/Disimilaridad

## Introducción al Aprendizaje No Supervisado
- Técnicas descriptivas clásicas analizan variables de a una o por pares (histogramas, tendencia central, correlación, regresión). En problemas modernos hay muchas variables simultáneas.
- Preguntas típicas: ¿Existen grupos naturales? ¿Qué observaciones son similares? ¿Existen anomalías? ¿Cómo resumir la estructura global?
- Aprendizaje "sin profesor": no se conoce la respuesta `Y`; solo se observa `X`.
  - Supervisado: se modela `P(Y|X) = P(X,Y)/P(X)`, interés en `E[Y|X]`; no se discute `P(X)`.
  - No supervisado: el interés está en `P(X)`. Todas las variables son de interés; alta dimensionalidad.
- Baja dimensión (≤3): métodos no paramétricos estiman `P(X)` directamente. Alta dimensión: maldición de la dimensionalidad → solo modelos globales burdos (mezclas gaussianas, descriptivos).
- No hay medida directa del éxito → se recurre a argumentos heurísticos → gran proliferación de métodos.
- Aplicaciones: publicidad segmentada, etc.

## Análisis de clústeres
- Conjunto de técnicas descriptivas para agrupar datos; la cantidad de grupos es **desconocida**.
- Agrupamiento por similitudes/distancias. Dos tipos: **Jerárquico** y **No jerárquico**.
- Idea central: observaciones similares deben ir al mismo grupo → cuantificar qué tan cerca/lejos están dos observaciones. Depende del tipo de variables, escala y contexto. **No existe una medida universalmente correcta.**

## Definiciones formales
Para items `X = (X₁,…,Xₚ)`, `Y = (Y₁,…,Yₚ)`:

**Disimilaridad** `d : ℝᵖ×ℝᵖ → ℝ`:
1. `d(x,y) ≥ 0`
2. `d(x,y) = 0 ⟺ x = y`
3. `d(x,y) = d(y,x)`

**Similitud** `s : ℝᵖ×ℝᵖ → ℝ`:
1. `0 ≤ s(x,y) ≤ 1`
2. `s(x,y) = 1 ⟺ x = y`
3. `s(x,y) = s(y,x)`

Relaciones: `d = 1 − s`, `s = 1/(1+d)`, `s = exp(−d)`.

## Medidas de distancia (cuantitativas)
- **Euclidiana:** `d(x,y) = √(Σ(xᵢ−yᵢ)²) = √((x−y)ᵀ(x−y))`.
- **Euclidiana generalizada / ponderada:** `d_A(x,y) = √((x−y)ᵀA(x−y))`. Si `A = S⁻¹` → **Mahalanobis**.
- **Manhattan:** `d(x,y) = Σ|xᵢ−yᵢ|`.
- **Minkowski:** `d(x,y) = (Σ|xᵢ−yᵢ|^m)^{1/m}`.
- **Canberra:** `d(x,y) = Σ |xᵢ−yᵢ| / (|xᵢ|+|yᵢ|)`.
- **Czekanowski / Sørensen-Dice:** `d(x,y) = 1 − [2·Σ mín{|xᵢ|,|yᵢ|}] / [Σ(|xᵢ|+|yᵢ|)]`.

## Escalas
Algunas distancias son sensibles a la escala. Ej.: Edad ∈ [20,30] vs. Ingreso ∈ [1000,100000]; en Euclidiana/Manhattan el ingreso domina. Por eso se suele **normalizar, estandarizar o ponderar**.

## Correlación y coseno
- Pearson `r` **no** es similaridad, pero define medidas asociadas: `r*(x,y) = |r(x,y)|` ó `r*(x,y) = (1+r(x,y))/2`.
- Si se estandarizan las variables: `d(x,y) = √(2[1−r(x,y)])` (d Euclidiana).
- **Similitud coseno** (variables positivas): `s(x,y) = ⟨x,y⟩/(‖x‖‖y‖)`.
- Categóricas ordinales con M categorías: transformar `(i−0.5)/M`, i=1,…,M, y tratar como continuas.
- Categóricas nominales con M categorías: disimilaridad 0 (coinciden) ó 1 (no coinciden).

## Variables binarias
Tabla de contingencia entre filas `x` (s) y `y` (t):

|        | x=1 | x=0 | Total |
|--------|-----|-----|-------|
| y=1    | a   | b   | a+b   |
| y=0    | c   | d   | c+d   |
| Total  | a+c | b+d | p     |

- **Simple Matching:** `s = (a+d)/(a+b+c+d)`
- **Double Matching:** `s = 2(a+d)/(2(a+d)+c+b)`
- **Jaccard:** `s = a/(a+c+b)`

## Ejemplo de Agresti (datos de 5 individuos)
| Individuo | Peso | Estatura | ColorOjos | ColorPelo | Lateralidad | Sexo |
|-----------|------|----------|-----------|-----------|-------------|------|
| 1 | 68 | 140 | Verde | Rubio | Diestro | F |
| 2 | 73 | 185 | Cafe  | Negro | Diestro | M |
| 3 | 67 | 165 | Azul  | Rubio | Diestro | M |
| 4 | 64 | 120 | Cafe  | Negro | Diestro | F |
| 5 | 76 | 210 | Cafe  | Negro | Zurdo   | M |

Binarización: `Y₁=I(X₁≥72)`, `Y₂=I(X₂≥150)`, `Y₃=I(X₃=Cafe)`, `Y₄=I(X₄=Rubio)`, `Y₅=I(X₅=Diestro)`, `Y₆=I(X₆=F)`.

| Ind | Y₁ | Y₂ | Y₃ | Y₄ | Y₅ | Y₆ |
|-----|----|----|----|----|----|----|
| 1 | 0 | 0 | 0 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 | 0 | 1 | 0 |
| 3 | 0 | 1 | 0 | 1 | 1 | 0 |
| 4 | 0 | 0 | 1 | 0 | 1 | 1 |
| 5 | 1 | 1 | 1 | 0 | 0 | 0 |

Matriz de similitud con **Simple Matching** (triangular inferior, diagonal 1):
```
S =
1
1/6  1
4/6  3/6  1
4/6  3/6  2/6  1
0    5/6  2/6  2/6  1
```
Los más similares: individuos 2 y 5 (`s₂₅ = 5/6`). Los menos: 1 y 5 (`s₁₅ = 0`).

## Comentarios finales
- Binarizar es un primer paso para datos mixtos, pero lo apropiado es usar similitudes/distancias aplicables directamente a datos mixtos.
- El agrupamiento depende críticamente de cómo se define la similitud; distintas métricas → distintos agrupamientos.
- El objetivo es descubrir estructuras útiles, interpretables y coherentes con el contexto, no una única solución "correcta".
