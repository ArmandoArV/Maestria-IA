---
name: fundamentos-matematicos-ia
description: >
  Expert knowledge base for the course "Fundamentos Matemáticos de Inteligencia Artificial" (IMT3850,
  Prof. Manuel A. Sánchez, Magíster en IA, Pontificia Universidad Católica de Chile). Covers the
  mathematical foundations of AI/ML across 8 class presentations. Use this skill whenever the user asks
  about linear algebra, vector spaces, matrix factorizations, SVD, PCA, least squares, orthogonality,
  eigenvalues/eigenvectors, probability, Bayes theorem, random variables, expectation/variance,
  randomized algorithms, concentration inequalities, limit laws (LLN, CLT), optimization, convexity,
  gradient descent, or Newton's method, or about the IMT3850 course, its homeworks (Tarea1, Tarea2),
  exam, or presentations. Also trigger on terms like álgebra lineal, descomposición matricial, valores
  propios, mínimos cuadrados, desigualdad de concentración, ley de los grandes números, teorema central
  del límite, descenso de gradiente, convexidad. Respond in Spanish when the user writes in Spanish.
---
# Fundamentos Matemáticos de Inteligencia Artificial — Expert Skill

## Description

Expert skill for the course **"Fundamentos Matemáticos de Inteligencia Artificial" (IMT3850)** by Prof. Manuel A. Sánchez. When the user is working inside `D:\Maestria-IA\FundamentosMatematicos`, this skill provides deep knowledge of all course topics drawn from the 8 class presentations in the `Presentaciones/` folder.

Use this skill when the user asks questions about linear algebra, matrix factorizations, SVD, PCA, least squares, probability, Bayes' theorem, randomized algorithms, concentration inequalities, limit laws (LLN, CLT), optimization, convexity, gradient descent, Newton's method, or any mathematical foundation for AI/ML covered in this course.

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

### Clase 6 — Probabilidades Avanzadas (Clase6_IMT3850.pdf)

**Core Topics:**

- **Teorema de Bayes y Naïve Bayes (Repaso):** Bayes' theorem, prior/likelihood/posterior vocabulary. **Naïve Bayes Classifier:** Independence assumption P(x₁,...,xₙ|Cₖ) = ΠP(xᵢ|Cₖ), MAP decision rule, log-trick for numerical stability, Gaussian NB for continuous features. Wine classification example (13 chemical attributes, 3 classes) with scikit-learn implementation.
- **Variables Aleatorias y Distribuciones:**
  - CDF F(x) = P(X ≤ x), PMF f(x) = P(X = x), PDF f(x) ≥ 0, ∫f(x)dx = 1.
  - **Discrete:** Bernoulli, Binomial, Multinomial, Poisson, Geometric, Hypergeometric.
  - **Continuous:** Uniform, Normal, Exponential, Gamma, Beta, Student-t.
  - Binomial approximations: Poisson (rare events, np→λ), Normal (De Moivre-Laplace, np > 5).
  - Exponential distribution: memoryless property P(X > t+s | X > s) = P(X > t). GPU failure time example.
- **Valor Esperado y Varianza:**
  - E[X] = Σx·f(x) / ∫xf(x)dx. Linearity: E[aX + b] = aE[X] + b, E[ΣcᵢXᵢ] = ΣcᵢE[Xᵢ].
  - **Indicator variables technique:** X = ΣXᵢ for counting problems (wardrobe problem, quicksort analysis).
  - **Jensen's Inequality:** φ(E[X]) ≤ E[φ(X)] for convex φ. Foundation of ELBO in EM algorithm.
  - Var[X] = E[X²] − (E[X])². Standard deviation σ = √Var(X).
- **Variables Aleatorias Multivariadas:**
  - Joint distributions F(x₁,...,xₙ), marginals, independence ⟺ joint density factorizes.
  - **Covariance:** Cov(X,Y) = E[XY] − E[X]E[Y]. Pearson correlation ρ = Cov(X,Y)/(σ_X σ_Y).
  - **Multivariate Gaussian:** f(x) = (1/((2π)^(M/2)|Σ|^(1/2))) exp(−½(x−μ)ᵀΣ⁻¹(x−μ)). Connection to PCA and GMM.
  - **SVD–Covariance bridge:** Σ = (1/(N−1))XᵀX = V(S²/(N−1))Vᵀ. Singular vectors = principal axes of Gaussian ellipsoids.
- **Función Generadora de Momentos (FGM):** M(s) = E[eˢˣ]. Derivative property: M⁽ⁿ⁾(0) = E[Xⁿ]. Uniqueness theorem. Examples: Poisson, Gamma, Normal.
- **Algoritmos Aleatorizados:**
  - "Las Vegas" algorithms: always correct, random running time.
  - **Randomized Quicksort:** Indicator variables Xᵢⱼ, P(Xᵢⱼ = 1) = 2/(j−i+1). **E[C] = 2n·ln(n) + O(n)**.
  - **Randomized Median:** Sample R of ⌈n^(3/4)⌉ elements, sort R, compute bounds d and u, filter C = {x ∈ S : d ≤ x ≤ u}. Failure probability ≤ n^(−1/4). Expected time O(n).
- **La Maldición de la Dimensionalidad:** Vol(Bₙ)/Vol(Cube) → 0 exponentially. Data lives in corners of hypercubes. Failure of distance-based methods (k-NN, clustering) in high dimensions.
- **Desigualdades de Concentración:**
  - **Markov:** P(X ≥ a) ≤ E[X]/a (X ≥ 0).
  - **Chebyshev:** P(|X − μ| ≥ a) ≤ σ²/a². Derived from Markov applied to |X − μ|².
  - **Hoeffding:** P(|X̄ₙ − μ| ≥ ε) ≤ 2exp(−2nε²/(b−a)²). Exponential decay. PAC learning foundation.
  - **Kolmogorov:** P(max₁≤k≤n |Sₖ| ≥ ε) ≤ Var(Sₙ)/ε². Controls entire trajectory, not just endpoint.
- **Muestras:** Sample mean X̄ (unbiased, Var = σ²/n). Sample variance S² with Bessel's correction (n−1). Pooled testing example.
- **Leyes Límite:**
  - **Ley Débil (WLLN):** X̄ₙ → μ in probability. Proof via Chebyshev in one line.
  - **Ley Fuerte (SLLN):** X̄ₙ → μ almost surely. Guarantees training stability.
  - **Teorema del Límite Central (CLT):** (X̄ₙ − μ)/(σ/√n) →ᵈ N(0,1). Universal Gaussian convergence regardless of original distribution.
  - **CLT Multivariado:** √n(X̄ₙ − μ) →ᵈ N(0, Σ).
  - **Chebyshev vs CLT for sample size:** Chebyshev gives hard guarantees (conservative n), CLT gives practical approximations (smaller n).

**Applications:** Drug testing (Bayes), wine classification (Gaussian NB), GPU failure time (Exponential), wardrobe problem (indicators), Quicksort analysis, PAC learning bounds, pollster problem (sample size).

---

### Clase 7a — Optimización (Clase7_IMT3850_opti.pdf)

**Core Topics:**

- **Cálculo en una Variable:** Derivatives, differentiability, product/quotient/chain rules. Taylor polynomials Tₙ(x) = Σf⁽ᵏ⁾(a)/k! · (x−a)ᵏ. Examples: cos(x), exp(x).
- **Cálculo Multivariable:**
  - **Gradient:** ∇f(x) = [∂f/∂x₁, ..., ∂f/∂xₙ] ∈ ℝⁿ.
  - **Directional derivative:** Dᵥf(x) = ∇f(x)·v. Steepest ascent in direction of ∇f.
  - **Hessian matrix:** Hᵢⱼ = ∂²f/∂xᵢ∂xⱼ. Second-order Taylor: f(x+δx) ≈ f(x) + δxᵀ∇f(x) + ½δxᵀH(x)δx.
  - **Jacobian matrix:** J ∈ ℝᵐˣⁿ, Jᵢⱼ = ∂fᵢ/∂xⱼ. For f(x) = Ax, J = A.
  - **Chain rule:** (f∘g)'(t) = J_f(g(t)) · J_g(t).
  - **Gradient of least-squares loss:** ∂L/∂θ = −2(y − Φθ)ᵀΦ = 2Φᵀ(Φθ − y).
- **Convexidad:**
  - Convex sets: θx + (1−θ)y ∈ C for all x,y ∈ C, θ ∈ [0,1].
  - **Convex functions:** f(θy + (1−θ)x) ≤ θf(y) + (1−θ)f(x).
  - **First-order condition:** f differentiable ⟹ f convex ⟺ f(y) ≥ f(x) + ∇f(x)ᵀ(y−x) ∀x,y. **Proof provided for D=1 case.**
  - **Second-order condition:** f twice differentiable ⟹ f convex ⟺ H(x) ⪰ 0 (positive semidefinite).
  - **Key theorem:** Every local minimum of a convex function is a global minimum.
  - Composition: g(yᵀx + b) convex if g convex. Sum of convex functions (with aᵢ ≥ 0) is convex. Max of convex functions is convex. Norms are convex.
- **Método de Newton:**
  - Iteration: xₖ₊₁ = xₖ − H(xₖ)⁻¹∇f(xₖ). Equivalent to minimizing T₂(x) at xₖ.
  - **Quadratic convergence:** ‖xₖ₊₁ − x*‖ ≤ C‖xₖ − x*‖².
  - **Backtracking:** Reduce step by β until Armijo condition f(x − γ∇f) ≤ f(x) − αγ‖∇f‖².
- **Método del Descenso del Gradiente:**
  - Iteration: xₖ₊₁ = xₖ − γₖ∇f(xₖ). Ensures f(x₀) ≥ f(x₁) ≥ ... converges to local min.
  - **Exact line search:** γₖ = argmin_γ f(xₖ − γ∇f(xₖ)).
  - **Zig-zag phenomenon:** For f = ½(x₁² + bx₂²), convergence rate depends on condition number b.
  - **Convergence analysis:** For mI ⪯ H ⪯ MI, optimal step γ = 1/M. f(xₖ₊₁) ≤ f(xₖ) − (1/2M)‖∇f(xₖ)‖².
  - **Backtracking algorithm:** Choose α < 1/2, β < 1. While f(x − γ∇f) > f(x) − αγ‖∇f‖², set γ ← βγ.
  - **Gradient descent with momentum:** xₖ₊₁ = xₖ − γzₖ, zₖ = ∇f(xₖ) + βzₖ₋₁. Optimal parameters: γ = (2/(√λ_max + √λ_min))², β = ((√λ_max − √λ_min)/(√λ_max + √λ_min))².
- **Levenberg-Marquardt para NLS:**
  - Nonlinear least squares: E(p) = ‖y − ŷ(p)‖². Gradient: ∇E = 2Jᵀ(y − ŷ(pₖ)).
  - LM iteration: (JᵀJ + λI)(pₖ₊₁ − pₖ) = Jᵀ(y − ŷ(pₖ)). Interpolates between gradient descent (large λ) and Newton/Gauss-Newton (small λ).

**Applications:** Least-squares gradient computation, zig-zag convergence visualization, backtracking line search, momentum optimization, nonlinear curve fitting.

---

### Clase 7b — Probabilidades: Dependencia, FGM, Concentración y Leyes Límite (IMT3850 (27).pdf)

**Core Topics:**

- **Dependencia Multivariada:**
  - Covariance: Cov(X,Y) = E[XY] − E[X]E[Y]. Proof expanding (X−E[X])(Y−E[Y]).
  - Pearson correlation: ρ = Cov(X,Y)/(σ_X σ_Y) ∈ [−1,1]. Only captures linear dependence.
  - Counterexample: X ~ Uniform{−1,0,1}, Y = X² → Cov(X,Y) = 0 but Y = X² (strong nonlinear dependence).
- **Función Generadora de Momentos:** M(s) = E[eˢˣ]. Uniqueness: same MGF ⟺ same distribution. Examples: Poisson M(t) = e^(λ(eᵗ−1)), Normal(0,1) M(t) = e^(t²/2), Exponential M(s) = λ/(λ−s).
- **Desigualdades de Concentración:** Markov, Chebyshev, Hoeffding (exponential decay, PAC), Kolmogorov (trajectory control). Chebyshev vs Hoeffding comparison. Practical example: n ≥ 738 for 95% confidence with ε = 0.05.
- **Leyes Límite:**
  - WLLN: convergence in probability (one-line proof via Chebyshev).
  - SLLN: almost sure convergence (via Kolmogorov + Borel-Cantelli).
  - Weak vs Strong: "Photo" (single snapshot) vs "Movie" (entire trajectory).
  - **CLT:** (X̄ₙ − μ)/(σ/√n) →ᵈ N(0,1). Multivariate CLT: √n(X̄ₙ − μ) →ᵈ N(0,Σ).
  - **Chebyshev vs CLT sample sizes:** Pollster example ε = 0.01, 95% confidence → Chebyshev: n ≥ 50,000 vs CLT: n ≥ 9,604 vs Hoeffding: n ≥ 18,445.
- **Muestras:** Estimators (sample mean, sample variance with Bessel correction). Pooled testing optimization with indicator variables.
- **Estimación de Parámetros:**
  - **Method of Moments (MoM):** Equate theoretical moments E[Xᵏ] with sample moments (1/n)ΣXᵢᵏ. Solve for parameters.
  - Examples: Poisson (λ̂ = X̄), Normal (μ̂ = X̄, σ̂² = (1/n)Σ(Xᵢ − X̄)²).
  - Inverse problem: learning model parameters from data.

**Applications:** Pollster sample size estimation, Chebyshev vs CLT comparison, Hoeffding for PAC bounds, pooled testing, parameter estimation from data.

### Clase 8 — Optimización Avanzada (Clase8_IMT3850.pdf)

**Core Topics:**

- **Método de Newton (Optimization):**
  - Update: x_{k+1} = x_k − [H(x_k)]⁻¹∇F(x_k)
  - Equivalent to minimizing 2nd-order Taylor polynomial around x_k
  - **Convergence:** Quadratic (‖x_{k+1} − x*‖ ≤ C‖x_k − x*‖²) — digits of accuracy double each iteration
  - **Problem:** Only converges if x₀ is close to x* (local convergence)
  - **Backtracking line search:** Control step size t ∈ (0,1]. Armijo condition: F(x_k + tΔx_k) ≤ F(x_k) + αt∇F(x_k)⊤Δx_k. Reduce t → βt until satisfied (β ∈ (0,1), α ∈ (0,0.5))

- **Quasi-Newton Methods:**
  - **Secant equation (multidimensional):** B_k s_k = y_k where s_k = x_k − x_{k-1}, y_k = ∇f(x_k) − ∇f(x_{k-1})
  - **Broyden update (rank-1):** B_k = B_{k-1} + (y_k − B_{k-1}s_k)s_k⊤ / (s_k⊤s_k). Avoids computing Hessian.
  - **BFGS (rank-2):** Preserves symmetry AND positive definiteness (Broyden breaks symmetry). Uses Sherman-Morrison for direct inverse update → O(n²) per iteration.
  - **L-BFGS (Limited memory):** Only stores last m pairs (s_i, y_i) (m ≈ 10). Never builds full matrix. Memory O(mn) instead of O(n²). Essential for large neural networks.

- **Gradient Descent — Analysis:**
  - **Exact line search:** γ_k = argmin_{γ≥0} f(x_k − γ∇f(x_k)). Turns n-dim problem into 1-dim.
  - **Zig-zag example:** f(x₁,x₂) = ½(x₁² + bx₂²). With exact line search: γ_k = 2/(1+b), convergence factor = ((1−b)/(1+b))². When b ≈ 0, convergence is very slow.
  - **Condition number κ = M/m** (ratio of max/min curvature). Convergence: f(x_{k+1}) − f(x*) ≤ (1 − m/M)(f(x_k) − f(x*)). Large κ → slow convergence.
  - **Backtracking (inexact line search):** Same Armijo condition as Newton. Convergence: f(x_{k+1}) ≤ f(x_k) − min{α, βα/M}‖∇f(x_k)‖²

- **Momentum Methods:**
  - **Polyak momentum:** x_{k+1} = x_k − γz_k, z_k = ∇f(x_k) + βz_{k-1}. Direction "remembers" previous step.
  - For quadratic f = ½x⊤Sx: optimal γ = (2/(√λ_max + √λ_min))², β = ((√λ_max − √λ_min)/(√λ_max + √λ_min))²
  - Improvement: ((1−b)/(1+b))² → ((1−√b)/(1+√b))² — dramatic speedup for ill-conditioned problems
  - Example: b=0.01 → GD factor ≈ 0.96, momentum factor ≈ 0.67
  - **Nesterov Accelerated Gradient (NAG):** "Look before you leap" — compute gradient at x_k + βv_k first: v_{k+1} = βv_k + γ∇f(x_k + βv_k), x_{k+1} = x_k − v_{k+1}

- **Subgradients (Non-smooth optimization):**
  - **Definition:** g is a subgradient of convex f at x if f(y) ≥ f(x) + g⊤(y−x) ∀y
  - **Subdifferential ∂f(x):** Set of all subgradients at x
  - |x| at x=0: ∂f(0) = [−1, 1]. ReLU at x=0: ∂f(0) = [0, 1]
  - **Subgradient method:** x_{k+1} = x_k − γ_k g_k, g_k ∈ ∂L(x_k). NOT a descent method — track best value seen.

- **Levenberg-Marquardt (NLS):**
  - **Nonlinear Least Squares:** L(Θ) = ½‖y − ŷ(Θ)‖². Gradient: ∇L = −J⊤(y − ŷ). Gauss-Newton: H ≈ J⊤J.
  - **LM update:** (J⊤J + λI)ΔΘ = J⊤e
  - λ large → gradient descent (safe, slow): ΔΘ ≈ (1/λ)J⊤e
  - λ → 0 → Gauss-Newton (fast, risky): (J⊤J)ΔΘ = J⊤e
  - λ adjusted dynamically — interpolates between GD and Newton

- **Logistic Regression (Derivation):**
  - Model: p_i = P(Y=1|x_i) = exp(w⊤x_i + b)/(1 + exp(w⊤x_i + b)) (sigmoid)
  - Bernoulli trick: P(Y=y_i|x_i) = p_i^{y_i}(1−p_i)^{1−y_i}
  - **Negative log-likelihood (cross-entropy):** L(w,b) = Σ[log(1 + exp(w⊤x_i + b)) − y_i(w⊤x_i + b)]
  - L is strictly convex (Softplus second derivative = p_i(1−p_i) > 0)
  - Gradient: ∂L/∂b = Σ(p_i − y_i), ∇_w L = Σ(p_i − y_i)x_i

- **Stochastic Gradient Descent (SGD):**
  - Full loss: L(Θ) = (1/N)ΣℓΘ_i. SGD: Θ_{k+1} = Θ_k − γ_k ∇ℓ_{i_k}(Θ_k) where i_k random
  - **Unbiased estimator:** E[∇ℓ_j] = ∇L — correct direction on average
  - **Mini-batch SGD:** Average over B samples (typically 32, 64, 256). Reduces variance by 1/√B.
  - **Robbins-Monro conditions:** Σγ_k = ∞ (reach minimum from anywhere), Σγ_k² < ∞ (noise vanishes)
  - Loss functions: Square loss ℓ_i = ½‖y_i − f(x_i;Θ)‖², Cross-entropy, Hinge loss

- **Constrained Optimization:**
  - **General form:** min f(Θ) s.t. h_i(Θ)=0 (equality), g_j(Θ)≤0 (inequality)
  - **SVM example:** min ½‖w‖² s.t. y_i(w⊤x_i + b) ≥ 1
  - **LASSO example:** min ½‖y − Xw‖² s.t. Σ|w_j| ≤ t
  - **Lagrangian:** L(Θ,λ,μ) = f(Θ) + Σλ_i h_i(Θ) + Σμ_j g_j(Θ)
  - **Dual function:** q(λ,μ) = inf_Θ L(Θ,λ,μ). Always concave. Provides lower bound.
  - **Weak duality:** q(λ,μ) ≤ f(Θ) for feasible Θ, μ≥0
  - **Strong duality (Slater):** If problem is convex and ∃Θ with g_j(Θ) < 0 strictly, then p* = d*

- **KKT Conditions (4 conditions for optimality):**
  1. **Stationarity:** ∇f(Θ*) + Σλ_i*∇h_i(Θ*) + Σμ_j*∇g_j(Θ*) = 0
  2. **Primal feasibility:** h_i(Θ*) = 0, g_j(Θ*) ≤ 0
  3. **Dual feasibility:** μ_j* ≥ 0
  4. **Complementary slackness:** μ_j* g_j(Θ*) = 0 (if constraint inactive → multiplier = 0)
  - For convex problems with Slater: KKT necessary AND sufficient
  - KKT identifies support vectors in SVM (μ_j > 0)

- **Quadratic Minimization with Linear Constraints:**
  - Problem: min ½x⊤Sx s.t. A⊤x = b (S symmetric positive definite)
  - KKT system: [S A; A⊤ 0][x; λ] = [0; b]
  - Solution: λ* = −(A⊤S⁻¹A)⁻¹b, x* = S⁻¹A(A⊤S⁻¹A)⁻¹b
  - Optimal cost: F(x*) = ½b⊤(A⊤S⁻¹A)⁻¹b
  - ∂F/∂b = −λ* (sensitivity of optimal cost to constraint level)
  - Saddle point property: max_λ min_x L = min_x max_λ L

**Applications:** SVM formulation, LASSO regularization, neural network training (SGD, momentum, Adam), logistic regression, nonlinear curve fitting (Levenberg-Marquardt), support vectors via KKT.

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
    ↓
Clase 6 → Advanced probability, randomized algorithms (Quicksort, Median),
           concentration inequalities, curse of dimensionality, LLN, CLT
    ↓
Clase 7a → Optimization: calculus review, convexity, Newton's method,
            gradient descent, momentum, Levenberg-Marquardt
    ↓
Clase 7b → Probability: MGF, covariance, Chebyshev/Hoeffding/Kolmogorov,
            LLN/CLT (with proofs), parameter estimation (MoM)
    ↓
Clase 8 → Newton (convergence, backtracking), Quasi-Newton (Broyden, BFGS, L-BFGS),
           GD analysis (zig-zag, condition number), Momentum (Polyak, Nesterov),
           Subgradients, Levenberg-Marquardt, Logistic Regression (full derivation),
           SGD (mini-batch, Robbins-Monro), Constrained optimization (Lagrangian,
           Dual, KKT conditions), Quadratic minimization with linear constraints
```

The course builds from **vector algebra** → **matrix algebra & linear systems** → **advanced factorizations (QR, eigen, SVD)** → **data science applications (PCA, least squares, regularization)** → **probabilistic frameworks (Bayes, MLE, cross-entropy loss)** → **advanced probability (randomized algorithms, concentration inequalities, limit theorems)** → **optimization foundations (convexity, GD, Newton)** → **advanced optimization (quasi-Newton, SGD, constrained optimization, KKT, logistic regression)**.

---

## Behavior Instructions

When this skill is active:

1. **Answer as a subject-matter expert** in the mathematical foundations of AI, drawing directly from the content of these 8 presentations.
2. **Use the same notation** as the course (e.g., ⊤ for transpose, ‖·‖₂ for Euclidean norm, A† for pseudoinverse).
3. **Reference specific classes** when explaining topics (e.g., "As covered in Clase 3, the QR factorization...").
4. **Provide formulas and proofs** at the level presented in the slides — rigorous but applied.
5. **Connect concepts to AI/ML applications** as the course does (K-means, Perceptron, PageRank, recommendation systems, Eigenfaces, Naïve Bayes, cross-entropy loss, randomized algorithms, PAC learning, gradient descent, Levenberg-Marquardt).
6. **When asked to solve exercises**, show step-by-step work using techniques from the relevant class.
7. **If asked about topics beyond the 8 classes**, clearly state that the topic was not covered in the presentations and offer general knowledge with that caveat.
8. **Support both Spanish and English** — the course materials are in Spanish, but answer in whatever language the user writes in.
9. **When reviewing the Presentaciones folder**, read the PDFs to provide specific page references or slide content if needed.

