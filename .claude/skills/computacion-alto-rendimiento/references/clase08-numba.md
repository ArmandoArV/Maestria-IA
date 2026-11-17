# Clase 08 — Numba en Python (JIT y multithreading)

**IMT3870**, Prof. Ignacio Labarca. Fuente: `Presentaciones/clase08.pdf` (37 láminas), lunes 9 de
noviembre.

**Agenda:** ¿cómo programar la ejecución de **múltiples hilos** en paralelo **desde Python**?

---

## 1. Repaso: interpretados vs. compilados

**Lenguajes interpretados (*scripted*)**
- El código **se ejecuta línea por línea**.
- **Instrucciones de alto nivel.**
- **Python, Julia, R**, etc.

**Lenguajes compilados**
- El código **es convertido en un programa ejecutable**.
- **Dos pasos: compilar y ejecutar.**
- **Fortran, C, C++, Rust**, etc.

**Python tiene el GIL** (*Global Interpreter Lock*):
- Hay un **único *native thread*** en el programa.
- **Prohíbe el paralelismo entre diferentes líneas de código.**

**Estrategia 1** — usar librerías que usan **código compilado** (p. ej. **NumPy**, que utiliza
**LAPACK** y **BLAS**).
**Estrategia 2** — usar librerías para **paralelización** (p. ej. **multiprocessing, joblib,
Numba**).

---

## 2. Numba y la estrategia JIT

**JIT (*just-in-time compilation*):** **compilar y ejecutar un código justo cuando se le necesita**.

**La librería Numba para Python:**
- **Código abierto.**
- **Compilación JIT de código de Python.**
- **Instalación: `conda install numba`** — la **instalación con pip no siempre es estable**.

**El flujo de Numba:**
1. Se escribe **código de Python/NumPy**.
2. **Numba analiza** este código.
3. **Crea código eficiente y optimizado.**
4. **Ejecuta la función compilada.**
5. **Entrega el resultado en formato de Python/NumPy.**

> **Compila en la primera llamada y reutiliza esa compilación.** **Precaución con esto a la hora de
> medir el tiempo de cómputo** (la primera llamada incluye el costo de compilar → hay que "calentar"
> la función antes de cronometrar).

### 2.1 Numba y LLVM
- Numba usa **LLVM (*Low Level Virtual Machine*)** como **motor de compilación**.
- LLVM es una **infraestructura de compilación de propósito general**, usada también por **Clang**
  (C/C++).
- Numba **traduce el código Python a LLVM IR** (*representación intermedia*), que **LLVM compila a
  código máquina nativo**.
- LLVM aplica **optimizaciones avanzadas**: **vectorización, inlining, eliminación de código muerto**,
  etc.
- **Por eso el rendimiento de Numba puede ser cercano al de C o Fortran.**

---

## 3. Uso básico: `@jit` y `@njit`

**Python decorators:** **toman una función y retornan otra función**. Llamado a Numba: **agregar
`@jit` antes de una función**.

Función básica en Python:
```python
def myFunction(x):
    total = 0
    for i in range(len(x)):
        total += x[i] * x[i]
    return total
```

Acelerada con Numba:
```python
@jit
def myFunction(x):
    total = 0
    for i in range(len(x)):
        total += x[i] * x[i]
    return total
```

**`@jit` vs. `@njit`:**
- **Desde Numba 0.59, `@jit` y `@njit` son equivalentes.**
- **Ambos compilan sin usar el intérprete de Python.**
- **Si Numba no puede compilar la función, entrega un error.**

```python
@njit
def myFunction(x):
    total = 0
    for i in range(len(x)):
        total += x[i] * x[i]
    return total
```
**El resultado es una función compilada.**

---

## 4. Paralelizar con `parallel=True` y `prange`

Numba **puede paralelizar código**:
- Con **`@njit(parallel=True)`**, Numba paraleliza el código bajo el **paradigma de multithreading**.
  - **Numba busca oportunidades de paralelizar** el código.
  - **Si no encuentra una manera de paralelizar, corre el código secuencialmente.**
  - **Numba intenta solucionar las condiciones de carrera pero NO hay garantía de consistencia.**
- **Paralelizar ciclos a mano con `prange()`.**

```python
from numba import njit, prange

@njit(parallel=True)
def myFunction(x):
    total = 0
    for i in prange(len(x)):
        total += x[i] * x[i]
    return total
```

**El resultado es una función compilada y paralelizada.**
- **Es posible manejar el número de threads que se crean.**
- **Es capaz de manejar la condición de carrera** (en una reducción como esta).

### 4.1 Benchmark: suma de cuadrados (N = 10 000 000)

| Implementación | Tiempo |
|----------------|--------|
| **Python** | **3,07 s** |
| **`@njit`** | **0,0116 s** (~265× más rápido) |
| **`@njit` + `prange`** | **0,00508 s** (~604×) |

---

## 5. El ejemplo central: suma del producto exterior

Calcular **Σ_{i,j} xᵢxⱼ** con distintas implementaciones:

```python
def slow_function(x):              # Python puro, O(N^2)
    total = 0
    for i in range(len(x)):
        for j in range(len(x)):
            total += x[i] * x[j]
    return total

@njit
def fast_function(x):              # Numba compilado, O(N^2)
    total = 0
    for i in range(len(x)):
        for j in range(len(x)):
            total += x[i] * x[j]
    return total

@njit(parallel=True)
def parallel_function(x):          # Numba paralelo, O(N^2)
    total = 0
    for i in prange(len(x)):
        for j in prange(len(x)):
            total += x[i] * x[j]
    return total

def numpy_fast(x):                 # NumPy, O(N)
    return np.sum(x) ** 2
```

**La nota clave:**

```
Σ_{i,j} xᵢxⱼ = ( Σ_i xᵢ )²
```

**reduciendo el problema de O(N²) a O(N).**

### 5.1 Escalabilidad con `prange` (N = 4000)
Se midió tiempo y speedup con **1, 2, 4 y 8 threads**: el tiempo baja de ~0,016 s a ~0,002–0,004 s,
pero el **speedup real se despega del speedup ideal** al aumentar los threads.

### 5.2 La moraleja de la clase
Comparando **Python, NumPy `outer`, NumPy `sum²`, Numba `@njit` y Numba paralelo** para N de 10² a
10³:

> **El algoritmo importa más que la implementación.**

Es decir: pasar de O(N²) a O(N) (`np.sum(x)**2`) gana **más** que paralelizar el O(N²).

---

## 6. Paralelización automática

**`parallel=True` también paraleliza operaciones vectorizadas.**
- Ejemplos: **`A[i, :] += b`**, **`np.zeros(n)`**, **`np.sum(x)`**.
- **Cada operación crea una región paralela.**
- **Crear una región paralela cuesta unos microsegundos.**
- **`f.parallel_diagnostics(level=1)` muestra qué se paralelizó.**

### 6.1 Tres versiones de "sumar un vector a cada fila"

```python
@njit
def add_rows(A, b):
    for i in range(A.shape[0]):
        A[i, :] += b

@njit(parallel=True)
def add_rows_auto(A, b):
    for i in range(A.shape[0]):
        A[i, :] += b          # una región paralela POR FILA

@njit(parallel=True)
def add_rows_prange(A, b):
    for i in prange(A.shape[0]):
        A[i, :] += b
```

### 6.2 Diagnóstico — paralelización automática

`add_rows_auto.parallel_diagnostics(level=1)`:
```
def add_rows_auto(A, b):              |
    for i in range(A.shape[0]):       |
        A[i, :] += b------------------| #1, 0

-------------------- After Optimisation --------------------
Parallel region 0:
+--1 (parallel, fused with loop(s): 0)
```
**La región paralela es `A[i, :] += b`, dentro del loop secuencial** → se **crea y destruye una región
paralela en cada iteración** (overhead de microsegundos × número de filas).

### 6.3 Diagnóstico — paralelización con `prange`

`add_rows_prange.parallel_diagnostics(level=1)`:
```
def add_rows_prange(A, b):            |
    for i in prange(A.shape[0]):----| #3
        A[i, :] += b----------------| #2

-------------------- After Optimisation --------------------
Parallel region 0:
+--3 (parallel)
   +--2 (serial)
```
**La región paralela es el loop `prange`**; **`A[i, :] += b` corre en serie dentro de cada hilo.**
*(Esta es la versión correcta: una sola región paralela.)*

---

## 7. Caso de estudio: K-means con Numba

**K-means** agrupa **N puntos en K clusters** buscando los centroides que **minimizan la distancia
intra-cluster**. Cada iteración tiene **dos etapas**:
- **Asignación:** cada punto se asigna **al centroide más cercano**.
- **Actualización:** cada centroide se recalcula como **el promedio de los puntos asignados**.

**Implementación base (Python puro)** — paso de asignación:

```python
cluster = np.zeros(n_points, dtype='int')
for p in range(n_points):
    minimum_distance = np.inf
    nearest_cluster = None
    for c in range(k):
        distance_to_cluster_c = np.sqrt(
            (dataset[p,0] - old_centers[c,0])**2
            + (dataset[p,1] - old_centers[c,1])**2)
        if distance_to_cluster_c < minimum_distance:
            minimum_distance = distance_to_cluster_c
            nearest_cluster = c
    cluster[p] = nearest_cluster
```
**Tres for-loops anidados: iteraciones, puntos y centros.**

### Opción 1 — reimplementar con NumPy
- **Reemplazar los for-loops por operaciones vectoriales.**
- Los loops **quedan dentro de NumPy, en código compilado**.
- **Hay que reescribir el algoritmo completo.**
- **Hay que verificar que entregue los mismos resultados.**

### Opción 2 — acelerar con Numba
```python
@njit(error_model='numpy')
def kmeans_numba(dataset, k, max_iterations=100):
    ...                 # mismo código de la Tarea01
    centers = np.zeros((k, 2))
    ...
```
*(Ventaja: **se reutiliza el mismo código**, sin reescribir el algoritmo.)*

### Opción 3 — Numba paralelo
```python
@njit(parallel=True, error_model='numpy')
def kmeans_numba_parallel(dataset, k, max_iterations=100):
    ...
    for p in prange(n_points):   # paso de asignación
        ...
    for p in range(n_points):    # paso de actualización
        number_of_points_in_cluster[cluster[p]] += 1
        sum_of_locations[cluster[p], 0] += dataset[p, 0]
        sum_of_locations[cluster[p], 1] += dataset[p, 1]
```
Con **`parallel=True`**, una **operación con slices lanza hilos** para cada `p`.

> Nota: **el paso de asignación va con `prange`** (independiente por punto), pero **el paso de
> actualización queda con `range`** (escribe en posiciones compartidas → condición de carrera).

### 7.1 Resultados
- **Tiempo vs. N** (k = 5, N de 10³ a 10⁷), comparando **Python puro (Tarea01)**, **NumPy
  (Tarea01)**, **Numba** y **Numba paralelo**.
- **Escalabilidad con `prange`** (N = 10 000 000, k = 5) sobre **1, 2, 4 y 8 threads**: el tiempo baja
  de ~3,2 s a ~1,75 s, y el **speedup real queda muy por debajo del ideal**.

**Las dos razones que da la clase:**
1. **4 núcleos físicos** (los 8 threads son hyperthreading, no núcleos reales).
2. **La actualización y la convergencia son secuenciales** → **fracción serial** (Amdahl, Clase 05).

---

## 8. Límites de Numba

**Del lenguaje:**
- Numba **acelera bien for-loops y estructuras if-else**.
- **A veces es desafiante de debuggear.**
- **Solo interpreta un subconjunto de Python.**
- **Maneja principalmente valores: `int`, `float`, `array`.**
- **No maneja objetos como `dict`.**

**De las librerías externas:**
- **No es compatible con todas las librerías externas.**
- **Maneja gran parte de NumPy y SciPy.**
- **No maneja `pandas`, `scikit-learn`, `tensorflow`**, etc.

---

**Próxima clase:** comunicación y paso de mensajes.
