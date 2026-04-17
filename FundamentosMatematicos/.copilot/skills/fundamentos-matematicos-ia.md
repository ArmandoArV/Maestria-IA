# Fundamentos Matemáticos de Inteligencia Artificial — Expert Skill

## Description

Expert skill for the course **"Fundamentos Matemáticos de Inteligencia Artificial" (IMT3850)** by Prof. Manuel A. Sánchez. When the user is working inside `D:\Maestria-IA\FundamentosMatematicos`, this skill provides deep knowledge of all course topics drawn from the 5 class presentations in the `Presentaciones/` folder.

Use this skill when the user asks questions about linear algebra, matrix factorizations, SVD, PCA, least squares, probability, Bayes' theorem, or any mathematical foundation for AI/ML covered in this course.

---

## Course Structure & Knowledge Base

### Clase 1 — Álgebra Lineal: Conceptos Básicos (Clase1.pdf)

**Core Topics:**

- **Espacios Vectoriales (ℝⁿ):** Vector notation (row/column), canonical vectors eₖ, transpose (⊤), 8 axioms of vector spaces.
- **Operaciones Lineales:** Vector addition (x+y), scalar multiplication (αx).
- **Combinaciones Lineales:** Linear combinations, affine combinations (Σβᵢ = 1), convex combinations (βᵢ ≥ 0).
- **Producto Interior:** x⊤y = Σxᵢyᵢ. Properties: commutativity, associativity with scalars, distributivity.
- **Funciones Lineales y Afines:** f(x) = a⊤x (linear), f(x) = a⊤x + b (affine). Superposition: f(αx + βy) = αf(x) + βf(y).
- **Aproximación de Taylor:** f̂(x) = f(z) + ∇f(z)⊤(x − z). Gradient definition ∇f.
- **Regresión Lineal (intro):** ŷ = x⊤β + v. Perceptron connection: f(x) = w⊤x + b.
- **Normas y Distancias:**
  - Norma euclidiana: ‖x‖₂ = √(x⊤x)
  - p-normas: ‖x‖ₚ = (Σ|xᵢ|ᵖ)^(1/p)
  - **Desigualdad de Cauchy-Schwarz:** |x⊤y| ≤ ‖x‖₂ ‖y‖₂
  - **Desigualdad Triangular:** ‖x + y‖₂ ≤ ‖x‖₂ + ‖y‖₂
  - **Desigualdad de Chebyshev:** ‖x‖₂² ≥ ka²
  - Distancia euclidiana: dist(x, y) = ‖x − y‖₂. RMS, std(x).
- **Clustering & K-means:** Objective: minimize J = (1/N)Σ‖xᵢ − z_{cᵢ}‖². Lloyd's algorithm (1957). Curse of dimensionality.
- **Independencia Lineal:** L.I. vs L.D. definitions, span, bases, dimension, coordinates.
- **Bases Ortonormales:** Orthogonality (aᵢ⊤aⱼ = 0), orthonormality, DCT basis, coordinates βᵢ = aᵢ⊤x.

**Applications:** Images as vectors, RGB colors, time series, word counts, FEM deformations, nearest neighbor, document similarity, feature normalization.

---

### Clase 2 — Álgebra Lineal: Sistemas Lineales (Clase2.pdf)

**Core Topics:**

- **Matrices:** A ∈ ℝᵐˣⁿ. Special matrices: identity I, diagonal, triangular, sparse, null, transpose, symmetric.
- **Operaciones Matriciales:** Addition, scalar multiplication, Frobenius norm ‖A‖_F = √(Σaᵢⱼ²).
- **Producto Matriz-Vector:** y = Ax. Column representation: Ax = x₁a₁ + ... + xₙaₙ. Row representation.
- **Transformaciones Lineales:** Rotation matrices, difference matrices. A(x + y) = Ax + Ay.
- **Espacio Nulo e Imagen:** nul(A) = {x : Ax = 0}, im(A) = {Ax : x ∈ ℝⁿ}. **Teorema Rango-Nulidad:** n = dim(nul(A)) + dim(im(A)).
- **Sistemas Dinámicos:** xₜ₊₁ = Axₜ. Population dynamics, epidemic models (SIR).
- **Taylor Multivariable:** f(x) ≈ f(z) + J(z)(x − z). Jacobian matrix J.
- **Producto de Matrices:** C = AB, cᵢⱼ = Σaᵢₖbₖⱼ. Associative, NOT commutative. Outer product ab⊤.
- **Sistemas de Recomendación:** Matrix factorization M ≈ UV⊤ (collaborative filtering).
- **Matriz Inversa:** Left/right inverse. A⁻¹. 2×2 formula: A⁻¹ = (1/det)[a₂₂, −a₁₂; −a₂₁, a₁₁].
- **Clasificación Lineal:** Linear separability, hyperplane w⊤c ≥ w₀.
- **Perceptrón:** ŷ = sgn(w⊤x). Learning rule: w ← w + ηyᵢxᵢ.
- **Sistemas Lineales:** Ax = b. Overdetermined (m > n), underdetermined (m < n), square (m = n).
- **Eliminación Gaussiana:** Forward elimination → upper triangular U. Multipliers ℓᵢⱼ. **LU factorization:** A = LU.
- **Sistemas Triangulares:** Forward substitution (Lx = b), backward substitution (Rx = b).

**Applications:** Image matrices (RGB), precipitation data, purchase history, directed graphs, incidence matrices, Graph Laplacian L = A⊤A (for GNNs), polynomial interpolation (Vandermonde).

---

### Clase 3 — Álgebra Lineal: Factorizaciones y Descomposiciones (Clase3.pdf)

**Core Topics:**

- **Proceso de Gram-Schmidt:** q̃ᵢ = aᵢ − Σ(qⱼ⊤aᵢ)qⱼ, then normalize qᵢ = q̃ᵢ/‖q̃ᵢ‖₂. Linear independence test.
- **Factorización QR:** A = QR. Q ∈ ℝᵐˣⁿ orthogonal, R ∈ ℝⁿˣⁿ upper triangular. **Theorem:** Any full-rank matrix A (m ≥ n) has a QR factorization. Solving: Ax = b ↔ Rx = Q⊤b.
- **Proyección Ortogonal:** P = QQ⊤ (P² = P, P⊤ = P). For non-orthogonal A: P = A(A⊤A)⁻¹A⊤.
- **Pseudoinversa:** A† = (A⊤A)⁻¹A⊤ (left). A† = A⊤(AA⊤)⁻¹ (right). Via QR: A† = R⁻¹Q⊤. Gram matrix: A⊤A invertible ⟺ columns of A are L.I.
- **Valores y Vectores Propios:** Av = λv. Characteristic polynomial: pₐ(λ) = det(A − λI) = 0. At most n eigenvalues. Distinct eigenvalues ⟹ L.I. eigenvectors. **Diagonalization:** A = VΛV⁻¹. Symmetric: A = QΛQ⊤.
- **PageRank:** Web relevance via connectivity matrix; ranking as eigenvector problem.
- **Iteración de Potencia:** Power iteration algorithm to find dominant eigenvalue.
- **SVD (Introduction):** A = UΣV⊤. Singular values σᵢ, left/right singular vectors.
- **Teorema de Eckart-Young:** Best rank-k approximation: Aₖ = Σσᵢuᵢvᵢ⊤ (i = 1..k). ‖A − Aₖ‖_F² = Σσⱼ² (j = k+1..p).
- **PCA (Introduction):** Principal Component Analysis via SVD of centered data.

---

### Clase 4 — SVD, PCA y Mínimos Cuadrados (Clase4_IMT3850.pdf)

**Core Topics:**

- **SVD (Deep Dive):** A = UΣV⊤. Complete vs reduced SVD. **Theorem:** For A ∈ ℝᵐˣⁿ, ∃ orthogonal U, V such that U⊤AV = Σ = diag(σ₁, ..., σₚ), σ₁ ≥ σ₂ ≥ ... ≥ 0. Computation via eigenvalues of AA⊤ and A⊤A → σᵢ = √λᵢ. Geometric interpretation: rotation → scaling → rotation.
- **Aproximación de Bajo Rango:** A = σ₁u₁v₁⊤ + σ₂u₂v₂⊤ + ⋯ + σₙuₙvₙ⊤. **Eckart-Young Theorem:** Aₖ is optimal rank-k approximation in both ‖·‖_F and ‖·‖₂. Image compression application.
- **Moore-Penrose Pseudoinversa:** A† = VΣ⁻¹U⊤ (via SVD). Underdetermined (m ≪ n): minimum norm solution. Overdetermined (m ≫ n): least squares solution. Snapshots method for large m ≫ n.
- **PCA (Full Treatment):**
  - Center data: B = X − 1·x̄⊤
  - Covariance: C = (1/(N−1))B⊤B
  - Principal components: CV = VD → D = V⊤CV; variance Dᵢᵢ = σᵢ²/(N−1)
  - Applications: ovarian cancer gene data (4000 dims → 3 dims), **Eigenfaces** (face recognition).
- **Mínimos Cuadrados Ordinarios (OLS):**
  - Problem: min_x ‖Ax − b‖₂²
  - **Ecuaciones Normales:** A⊤Ax̂ = A⊤b → x̂ = (A⊤A)⁻¹A⊤b = A†b
  - **Principio de Ortogonalidad:** (Az)⊤r̂ = 0 for all z
  - Solving via QR and SVD.
- **Data Fitting:** ŷ = θ₁f₁(x) + ... + θₚfₚ(x). Constant fit (average), linear regression, autoregressive time series.
- **Validación:** Train/test split (80/20), overfitting detection, cross-validation.
- **Regresión Ridge:** min ‖Ax − b‖₂² + λ‖x‖₂² → (A⊤A + λI)x = A⊤b (Tikhonov regularization).
- **Mínimos Cuadrados Multi-objetivo:** J = λ₁‖A₁x − b₁‖² + ... + λₖ‖Aₖx − bₖ‖².
- **Solución de Mínima Norma:** For underdetermined systems.

---

### Clase 5 — Probabilidades (Clase5.pdf)

**Core Topics:**

- **Espacio de Probabilidades (Ω, A, P):** Sample space, event space, probability measure.
  - **Axiomas de Kolmogorov:** Non-negativity, normalization P(Ω) = 1, σ-additivity.
  - Laplace's rule: P(A) = |A|/|Ω|. Union theorem. Boole's inequality. Complement rule.
- **Probabilidad Condicional:** P(E|F) = P(E ∩ F)/P(F).
- **Independencia:** P(E ∩ F) = P(E)P(F). Mutual independence.
- **Ley de Bayes:**
  - Product rule: P[A₁A₂⋯Aₙ] = P[A₁]P[A₂|A₁]⋯P[Aₙ|A₁⋯Aₙ₋₁]
  - **Probabilidad Total:** P(B) = ΣP(B|Eᵢ)P(Eᵢ)
  - **Teorema de Bayes:** P(Eⱼ|B) = P(B|Eⱼ)P(Eⱼ) / ΣP(B|Eᵢ)P(Eᵢ)
  - Applications: loaded coins, spam filter, COVID testing.
- **Clasificador Naïve Bayes:**
  - Naive assumption: P(x₁, ..., xₙ|Cₖ) = ΠP(xᵢ|Cₖ)
  - MAP decision: ŷ = argmax P(Cₖ)ΠP(xᵢ|Cₖ)
  - Training: compute priors P(Cₖ) and likelihoods (categorical or Gaussian).
  - Practical application: wine classification (13 chemical attributes, 3 classes).
- **Variables Aleatorias:**
  - CDF: F(x) = P(X ≤ x). PMF: f(x) = P(X = x). PDF: f(x) ≥ 0, ∫f(x)dx = 1.
  - **Discrete distributions:** Bernoulli, Binomial, Multinomial, Poisson, Geometric, Hypergeometric.
  - **Continuous distributions:** Uniform, Normal, Exponential, Gamma, Beta, Student-t.
- **De Bernoulli a Deep Learning:**
  - Binary classification: P(Y = y|x) = p̂ʸ(1 − p̂)¹⁻ʸ
  - **MLE (Maximum Likelihood):** L(p̂) = Πp̂ᵢʸⁱ(1 − p̂ᵢ)¹⁻ʸⁱ
  - **Cross-Entropy Loss:** Loss = −Σ[yᵢ log(p̂ᵢ) + (1 − yᵢ) log(1 − p̂ᵢ)]
- **Valor Esperado y Varianza:**
  - E[X] = Σx·f(x) (discrete), ∫xf(x)dx (continuous).
  - Linearity: E[aX + b] = aE[X] + b, E[X + Y] = E[X] + E[Y].
  - Var[X] = E[X²] − (E[X])². σ = √Var(X).
- **Función Generadora de Momentos:** M(s) = E[eˢˣ]. M⁽ⁿ⁾(0) = E[Xⁿ].
- **Distribuciones Conjuntas:** F(x₁, ..., xₙ). Marginals. Independence ⟺ f factorizes.
- **Covarianza:** Cov(X, Y) = E[XY] − E[X]E[Y]. Independence ⟹ Cov = 0 (but converse is false).

---

## Course Progression

```
Clase 1 → Vectors, norms, distances, inner products, K-means
    ↓
Clase 2 → Matrices, linear systems, Gaussian elimination, Perceptron, LU
    ↓
Clase 3 → Gram-Schmidt, QR, projections, pseudoinverse, eigenvalues, SVD intro
    ↓
Clase 4 → SVD deep dive, PCA, OLS, normal equations, Ridge regression
    ↓
Clase 5 → Probability, Bayes, Naïve Bayes, distributions, MLE, Cross-Entropy
```

The course builds from **vector algebra** → **matrix algebra & linear systems** → **advanced factorizations (QR, eigen, SVD)** → **data science applications (PCA, least squares, regularization)** → **probabilistic frameworks (Bayes, MLE, cross-entropy loss for deep learning)**.

---

## Behavior Instructions

When this skill is active:

1. **Answer as a subject-matter expert** in the mathematical foundations of AI, drawing directly from the content of these 5 presentations.
2. **Use the same notation** as the course (e.g., ⊤ for transpose, ‖·‖₂ for Euclidean norm, A† for pseudoinverse).
3. **Reference specific classes** when explaining topics (e.g., "As covered in Clase 3, the QR factorization...").
4. **Provide formulas and proofs** at the level presented in the slides — rigorous but applied.
5. **Connect concepts to AI/ML applications** as the course does (K-means, Perceptron, PageRank, recommendation systems, Eigenfaces, Naïve Bayes, cross-entropy loss).
6. **When asked to solve exercises**, show step-by-step work using techniques from the relevant class.
7. **If asked about topics beyond the 5 classes**, clearly state that the topic was not covered in the presentations and offer general knowledge with that caveat.
8. **Support both Spanish and English** — the course materials are in Spanish, but answer in whatever language the user writes in.
9. **When reviewing the Presentaciones folder**, read the PDFs to provide specific page references or slide content if needed.
