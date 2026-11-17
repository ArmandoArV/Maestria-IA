# Clase 07 — Paralelismo y multithreading

**IMT3870**, Prof. Ignacio Labarca. Fuente: `Presentaciones/clase07.pdf` (37 láminas), lunes 9 de
noviembre.

**Agenda:** ¿cómo programar la ejecución de **múltiples hilos** en paralelo? Repaso de arquitectura y
memoria · Tipos de paralelismo y granularidad · Procesos e hilos · Librerías de computación paralela ·
Hilos en Python y el GIL.

---

## 1. Repaso: memoria compartida vs. distribuida

Jerarquía de memoria: Registros (~1 ciclo, ~1 KB) → L1 (~4, ~32 KB) → L2 (~8, ~256 KB) → L3 (~28,
~8–32 MB) → RAM (~160 ciclos, ~16–128 GB). Típicamente **2 o 3 capas de caché**.

- **La memoria es algo físico** en el hardware.
- Un **dataspace** es algo de **software**: una parte de la memoria **reservada para un único proceso**.

**Memoria compartida:**
- Los procesos pueden usar **todos los núcleos de cómputo y toda la memoria** disponible en el sistema.
- **Ejemplo: procesadores multi-core.** Los núcleos **pueden acceder a toda la RAM**. Hay muchas
  variantes (**número de núcleos**, **caché privado o compartido**). Es **la arquitectura más común en
  un computador personal**.

**Memoria distribuida:**
- Los procesos pueden acceder **únicamente a un subconjunto de núcleos** y **una parte de la memoria**.
- **Ejemplos: nube, servidores y clústers.**

### Dónde estamos
Ya se han visto **dos estrategias** para mejorar la eficiencia de un código de Python:
1. **Vectorización con NumPy.**
2. **Multiprocessing con joblib.**

**Vectorización** (consejo general al programar algoritmos):
- **Uso eficiente de memoria y caché.**
- **Normalmente resulta en pipelining.**
- **Oportunidades de hacer multithreading.**
- Estrategia en Python: usar **NumPy arrays en lugar de listas** y **funcionalidad de librerías
  compiladas** (vía NumPy, SciPy, etc.) **en lugar de for-loops de Python**.

---

## 2. Los tres tipos de paralelismo

| Tipo | También llamado | Qué hace |
|------|-----------------|----------|
| **Paralelismo de datos** | **grano fino** | **La misma instrucción** para **muchos elementos de datos** |
| **Paralelismo funcional** | **de instrucción** | **Diferentes instrucciones** sobre elementos de datos **independientes** |
| **Paralelismo de tareas** | — | **Subprogramas independientes** |

### 2.1 Paralelismo de datos — suma de vectores

```c
// Secuencial
for (i = 0; i < n; i++)
    c[i] = a[i] + b[i];
```

**Paralelo:** cada procesador calcula una **porción independiente** (p. ej. `a[0..3]` en P0,
`a[4..7]` en P1). **Cada elemento es independiente ⇒ paralelismo perfecto.**

### 2.2 Paralelismo funcional — ILP / Pipelining
**Distintas instrucciones en distintas etapas del procesador al mismo tiempo**; las etapas (**IF, ID,
MF, EX, WB**) **se solapan** entre instrucciones. *(Ver Clase 03.)*

### 2.3 Paralelismo de tareas — *parameter tuning* en ML
Entrenar un modelo con **distintas configuraciones de hiperparámetros** de forma simultánea:

```
Dataset ──> lr=0.01
        ──> lr=0.001     ──> Mejor modelo
        ──> lr=0.0001
```
**Cada tarea es independiente:** distintos hiperparámetros, **mismos datos**.

---

## 3. Problemas perfectamente paralelos

Un problema es **perfectamente paralelo (*embarrassingly parallel*)** si **se divide en tareas
independientes, sin comunicación entre ellas**.

- **Ejemplos:** simulaciones **Monte Carlo**, **procesar muchas imágenes**, **búsqueda de
  hiperparámetros**.
- **Escalan casi linealmente**: los límites son el **balance de carga** y el **overhead**.
- Se paralelizan con **hilos o con procesos**, por ejemplo con **joblib**.

---

## 4. Granularidad de tareas

La **granularidad** de un algoritmo paralelo está dada por el **número y el tamaño de las tareas** en
que se divide el problema.

- **Paralelismo a nivel de instrucción:** grano **muy fino**, tareas de **una instrucción**.
- **Paralelismo de tareas:** grano **grueso**, tareas del tamaño de un **subprograma**.

| | Grano fino | Grano grueso |
|---|---|---|
| Tareas | **muchas, pequeñas** | **pocas, grandes** |
| Potencial de paralelismo | **mayor** | menor |
| Overhead de sincronización | **mayor** | **menor** |
| Riesgo | overhead domina | **puede dejar recursos ociosos** |

> **La granularidad óptima depende del problema, la arquitectura y el costo de comunicación.**

**Ejemplos de clase:**
- **Grano fino:** cada hilo suma **un único elemento** de un vector (T0→P0, T1→P1, …). Muchas tareas
  pequeñas → **mayor overhead de sincronización**.
- **Grano grueso:** cada procesador trabaja sobre **la mitad** de un dataset (T0–T3→P0, T4–T7→P1).
  *¿Qué pasa si P0 termina antes que P1?* → **P0 queda ocioso.**

---

## 5. Procesos e hilos (detalle)

Un **proceso** es un **programa en ejecución** con su **propio espacio de memoria**. Contiene:
- El **código** del programa (compilado).
- El **heap** con los datos asignados en la memoria.
- El **stack** con la información de **cambio rápido**:
  - **Contador del programa.**
  - **Datos locales.**
  - **Resultados intermedios.**

Un **hilo** es la **unidad mínima de ejecución** dentro de un proceso:
- **Tiene su propio stack** y **comparte el heap** del proceso.

### 5.1 El modelo *fork-join*
- **Fork:** un **hilo principal crea hilos** que trabajan en paralelo.
- **Join:** los hilos **se sincronizan al terminar** y el hilo principal **continúa**.

### 5.2 Datos privados y compartidos
Cuando se usan múltiples hilos, los datos pueden ser **"privados"** o **"compartidos"** (*private* –
*shared*):
- Cuando se crea **dentro de un hilo**, los datos son **privados** → **se eliminarán cuando finalice el
  hilo**.
- Cuando se crea **fuera de un hilo**, los datos **se comparten** → **la memoria compartida puede ser
  utilizada por todos los hilos**.

### 5.3 Consistencia: *thread safety* y condiciones de carrera
Un código es **seguro para hilos (*thread safe*)** si **siempre produce el mismo resultado** cuando se
ejecuta **secuencialmente y en paralelo**.

Una **condición de carrera (*race condition*)**: **el resultado depende de cuál hilo termine primero**.

- **El principal peligro es escribir en datos compartidos.**
- **Se evitan protegiendo el acceso** a datos compartidos con **secciones críticas** o **bloqueos
  (*locks*)**.

---

## 6. Paralelismo en lenguajes compilados

¿Cómo paralelizar código en **C, C++ y Fortran**?
- Los **compiladores son inteligentes**, pero **rara vez paralelizan código automáticamente**.
- **La paralelización sigue siendo principalmente la responsabilidad del programador.**

### 6.1 Librerías de computación científica
Hay librerías que proporcionan **rutinas ya paralelizadas en código compilado**:
- **LAPACK, BLAS, MKL, PETSc, NumPy**, etc.
- **Multiplicación matriz-vector, factorización LU, transformada rápida de Fourier**, etc.

**La mayoría de los lenguajes interpretados tienen capacidades limitadas de paralelización:**
- **Global Interpreter Lock (GIL).**
- Alternativa: **abrir automáticamente varias instancias** con el paradigma de **multiprocessing**.

### 6.2 Las librerías canónicas de HPC

| Librería | Modelo | Memoria |
|----------|--------|---------|
| **OpenMP**, **Pthreads** | **multithreading** | **compartida** |
| **MPI** (*Message Passing Interface*) | **procesos independientes que se comunican con mensajes** | **distribuida** |

Disponibles para **Fortran, C y C++**.
- **Python tiene la librería `MPI4Py`.**
- **Lo más cercano a OpenMP en Python es Numba** (próxima clase).

---

## 7. Paralelismo en Python

¿Cómo hacer **multithreading** en Python?
1. **Utilizando funcionalidad de librerías como NumPy.**
2. **Programar la paralelización explícitamente.**

### 7.1 El módulo `threading`

```python
def download(url, results, idx):
    with urlopen(url) as resp:
        results[idx] = resp.read()

threads = []
for k, url in enumerate(urls):
    t = threading.Thread(target=download,
                         args=(url, results, k))
    threads.append(t)
    t.start()      # fork

for t in threads:
    t.join()       # join
```

- **Crea hilos del sistema operativo.**
- **Mientras un hilo espera la red, otro avanza.**
- **`start()` y `join()` siguen el modelo fork-join.**

### 7.2 Por qué existe el GIL
- **CPython ejecuta el código línea por línea**: lo traduce a **bytecode** y lo interpreta en su
  **máquina virtual**.
- El intérprete mantiene un **estado global** (**conteo de referencias**, memoria).
- **Dos hilos modificando ese estado simultáneamente pueden corromperse.**
- Ante eso, **CPython usa el Global Interpreter Lock (GIL)**.

### 7.3 Qué implica el GIL
- El GIL permite que **solo un hilo ejecute bytecode Python a la vez**, **incluso en sistemas
  multicore**.
- Los **threads de Python son útiles para I/O, pero no para cómputo**.
- **Código CPU-bound con múltiples threads puede ser *más lento* que secuencial.**
- La alternativa es **usar librerías que liberan el GIL o que compilan el código**: **NumPy, Numba**,
  etc.

### 7.4 Concurrencia ≠ paralelismo

```
Hilos de Python con GIL: CONCURRENCIA
Hilo 0  ███░░░███░░░        ███ ejecutando
Hilo 1  ░░░███░░░███        ░░░ esperando el GIL
Hilo 2  ░░░░░░███░░░
Hilo 3  ░░░░░░░░░███   → tiempo

Paralelismo: todos los hilos a la vez
Hilo 0  ████████████
Hilo 1  ████████████
Hilo 2  ████████████
Hilo 3  ████████████   → tiempo
```

### 7.5 Las dos mediciones de la clase

**Tareas de espera** (ocho tareas que esperan 1 s con `time.sleep`, como una descarga):

| Hilos | Tiempo | Speedup |
|-------|--------|---------|
| 1 | 8,00 s | 1,0 |
| 2 | 4,00 s | **2,0** |
| 4 | 2,00 s | **4,0** |
| 8 | 1,00 s | **8,0** |

**Speedup lineal:** **el GIL se libera durante la espera**. Los hilos **esperan en paralelo**, aunque
**no calculen en paralelo**.

**Tareas de cómputo** (ocho tareas en Python puro):

```python
def countdown(n):
    while n > 0:
        n -= 1
```

| Hilos | Tiempo | Speedup |
|-------|--------|---------|
| 1 | 2,25 s | 1,0 |
| 2 | 2,30 s | 1,0 |
| 4 | 2,37 s | 1,0 |
| 8 | 2,44 s | **0,9** |

**Sin speedup:** **los hilos se turnan el GIL** (y con 8 hilos el overhead lo hace *más lento*).

---

## 8. OpenMP en C/C++ (fuera del foco del curso)

- **Directivas `#pragma`** que indican al compilador **qué paralelizar**.
- **Memoria compartida** y **modelo fork-join**.
- Compilar con **`g++ -fopenmp main.cpp`**.

### 8.1 Paralelizar un for-loop (paralelismo de datos)

```cpp
const int N = 100000000;
std::vector<double> a(N), b(N), c(N);
// ... inicializacion ...

#pragma omp parallel for
for (int i = 0; i < N; i++) {
    c[i] = std::sin(a[i]) * std::cos(b[i]);
}
```
**Las iteraciones se reparten entre los hilos**; cada iteración es **independiente**.

### 8.2 Tareas en dividir y conquistar (paralelismo de tareas)

```cpp
void merge_sort(int* a, int n) {
    if (n <= THRESHOLD) { std::sort(a, a+n); return; }

    #pragma omp task
    merge_sort(a, n/2);
    #pragma omp task
    merge_sort(a + n/2, n - n/2);

    #pragma omp taskwait
    merge(a, n);
}
```
**Cada llamada recursiva es una tarea**; **`THRESHOLD` controla la granularidad**.

---

**Próxima clase:** multithreading en Python con la librería **Numba**.
