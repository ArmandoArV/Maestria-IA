# Clase 04 — Múltiples procesos (multiprocessing y joblib)

**IMT3870**, Prof. Ignacio Labarca. Fuente: `Presentaciones/clase04.pdf` (26 láminas), lunes 26 de
octubre.

**Agenda:** ¿cómo programar **múltiples procesos** en Python?

---

## 1. Procesos

Un **proceso** es un **programa en ejecución**, con su **propio espacio de memoria**.

- Al crearse, el **SO le asigna su propio espacio de memoria**: **stack** y **heap**.
  - **Heap**: memoria **compartida por el proceso completo**.
  - **Stack**: memoria de **uso temporal por hilos**.
- Cada proceso tiene su propia memoria: **no comparte datos con otros procesos**.
- Un proceso **puede tener múltiples hilos**, todos compartiendo su memoria.
- La **comunicación entre procesos requiere mecanismos explícitos**.

```
Sistema operativo
┌─ Proceso 1 ──────────────┐   ┌─ Proceso 2 ──────────────┐
│ Stack hilo 0 │ Stack h.1 │   │ Stack hilo 0 │ Stack h.1 │
│          Heap            │   │          Heap            │
└──────────────────────────┘   └──────────────────────────┘
        ↑ sin acceso directo entre procesos ↑
```

El SO asigna a cada proceso su propio espacio de memoria; **un proceso no puede acceder directamente
a la memoria de otro**.

---

## 2. Hilos (threads)

- Un **hilo** es la **unidad mínima de ejecución** dentro de un proceso.
- Varios hilos **comparten el mismo espacio de memoria** del proceso.
- El **SO los planifica de forma independiente**.
- Permiten ejecutar varias tareas en paralelo **dentro de un mismo programa**.
- **Cada core puede ejecutar un hilo a la vez**: con N cores se pueden ejecutar **N hilos
  simultáneamente**.
- Si hay **más hilos que cores**, el SO **los intercala**.

### Los tres paradigmas (repaso)
- **Multiprocessing** — un programa que **crea otros programas**; cada programa tiene **su propio
  dataspace**.
- **Multithreading** — un programa que crea **threads** que corren simultáneamente; **todos los
  threads comparten el mismo dataspace**.
- **Hyperthreading** — cada **núcleo físico** se presenta como **dos núcleos lógicos (virtuales)**;
  los dos threads **comparten las unidades de ejecución** del núcleo.

---

## 3. El GIL y las dos estrategias

Python tiene un bloqueo: el **GIL (Global Interpreter Lock)**.
- **Solo un thread a la vez** puede ejecutar código Python.
- **Impide el paralelismo entre threads** que ejecutan código Python.
- Desde **Python 3.13** existe una versión **sin GIL (*free-threaded*)**, con **soporte oficial desde
  3.14**.

**Estrategia 1 — usar librerías que usan código compilado.** Por ejemplo, **NumPy** utiliza
**LAPACK** y **BLAS**.

**Estrategia 2 — usar librerías para paralelización.** Por ejemplo, **`multiprocessing`** y
**`joblib`**.

---

## 4. La librería `multiprocessing`

Implementa paralelismo en Python según el paradigma **multiprocessing**:
- **Crea distintos programas de Python.**
- Hay un **overhead** en **crear y terminar procesos** → **el costo de paralelizar**.
- **Sin comunicación automática** entre procesos.
- Sirve para problemas **relativamente sencillos de paralelizar**.

---

## 5. La librería `joblib`

<https://joblib.readthedocs.io> — alternativa a `multiprocessing`, con **más capacidades**:
- Tiene **varios backends**.
- **Funciona en Jupyter Notebooks**.
- **Funciona dentro de clases o funciones**.

**Límites:**
- Es **difícil de generalizar** a cualquier objeto o arquitectura de computador.
- **No siempre es estable.**

### 5.1 Backends de ejecución
- **`loky`** (**por defecto**): procesos independientes, **seguro en Windows y Jupyter**.
- **`multiprocessing`**: usa el módulo estándar, **más rápido en escenarios simples**.
- **`threading`**: usa **hilos**; útil si la carga es **I/O-bound** o si el código **libera el GIL**
  (p. ej. NumPy).

---

## 6. `fork` vs. `spawn`

**`fork`** — el proceso **padre crea una copia de sí mismo** (espacio de memoria y estado) usando
**copy-on-write**:
```
Padre ──fork──> Hijo 1, Hijo 2, Hijo 3
```
- **Muy rápido** para iniciar procesos.
- El hijo puede **leer y escribir en los mismos archivos** que el padre.
- **Riesgo de heredar estado no deseado** (threads, locks, recursos).
- **No disponible en todos los sistemas operativos.**

**`spawn`** — crea un **proceso nuevo desde cero**, cargando el programa indicado (se le envían
**función y datos serializados**):
- **Estado limpio y controlado.**
- **Disponible en cualquier SO moderno.**
- **Inicio más lento**: requiere inicializar memoria y cargar código.
- **Modelo por defecto en joblib.**

---

## 7. Serialización

### ¿Por qué serializar?
- En lenguajes **compilados**, los objetos son **directamente interpretables** como elementos que
  usan un espacio en la memoria.
- En lenguajes **interpretados** como Python, **esto no es directo**.
- Por eso esa interpretación **debe pasar por la serialización**.

**Serializar** = **convertir un objeto en bytes** para enviarlo o guardarlo.

```
Proceso padre  ──serializar──>  bytes  ──deserializar──>  Proceso hijo
(función y argumentos)                        (función y argumentos)
```

- **`pickle`**: módulo estándar de Python para serializar objetos.
- La **documentación de cada librería indica si es *pickleable***.

### 7.1 Recomendaciones para objetos en joblib

**Solo deben enviarse datos serializables:** listas, diccionarios, `numpy.ndarray`, números, etc.

**Debe evitarse el envío de recursos abiertos:**
- Conexiones a base de datos.
- Sockets o puertos de red.
- Archivos abiertos.
- Contextos GPU ya inicializados.

> **Los recursos deben crearse *dentro* de cada proceso** en lugar de ser enviados desde el proceso
> padre.

**Otras limitaciones:** puede fallar con objetos que contienen **recursos no serializables**
(conexiones, dispositivos); hay un **overhead visible cuando las tareas son cortas**.

---

## 8. ¿Cuándo usar joblib?

- **Ejecuciones independientes con distintos parámetros** — probar un algoritmo con distintos valores
  o distintas **semillas aleatorias**.
- **Procesamiento de elementos de una lista o conjunto de datos** — aplicar la misma función a miles
  de imágenes o archivos.
- **Simulaciones repetitivas** — Monte Carlo, barridos de parámetros, simulaciones estocásticas.
- **Entrenamiento o evaluación en lote** — evaluar un modelo sobre múltiples conjuntos de validación.

---

## 9. Ejemplos de código

### 9.1 Patrón básico — estadísticas de muchos CSV

```python
from pathlib import Path
import pandas as pd
from joblib import Parallel, delayed

def process(path):
    df = pd.read_csv(path)
    return df.describe()

files = sorted(Path("data").glob("*.csv"))

# Serial
summaries = [process(f) for f in files]

# Paralelo: 4 procesos
summaries = Parallel(n_jobs=4)(delayed(process)(f) for f in files)
```

- **`delayed(f)(x)` guarda la llamada `f(x)` sin ejecutarla.**
- **`Parallel` reparte las llamadas entre los procesos** y devuelve una lista con los resultados **en
  el mismo orden**.

### 9.2 Calibrar k en k-means (barrido de parámetros)

Repaso de **k-means**: agrupa los datos en **k clusters**; cada punto se asigna al **centroide más
cercano**; los centroides se recalculan como **promedio**, hasta **converger**. La **inercia** es la
**suma de distancias al cuadrado** de cada punto a su centroide.

**¿Cómo elegir k?**
- Se definen **criterios** para juzgar si un parámetro está bien elegido.
- En k-means, la **inercia mide qué tan compactos** son los clusters.
- **La inercia siempre disminuye al aumentar k.**
- **Método del codo:** elegir k **donde la inercia deja de bajar mucho**.
- Evaluar varios k = **barrido de parámetros (*parameter sweep*)**; objetivo: **ajuste de
  hiperparámetros (*hyperparameter tuning*)**.
- Se entrena **un modelo para cada valor de k** y el cálculo para cada k es **totalmente
  independiente** de los demás → **explotar el paralelismo es lo mejor**.

```python
import numpy as np
from joblib import Parallel, delayed
from sklearn.cluster import KMeans

X = np.load("data.npy")

def fit_kmeans(X, k):
    model = KMeans(n_clusters=k, random_state=0)
    return model.fit(X).inertia_

ks = range(2, 11)
inertias = Parallel(n_jobs=-1)(delayed(fit_kmeans)(X, k) for k in ks)
```

---

## 10. Cuidado con la *oversubscription*

**Oversubscription** = **más hilos activos que núcleos**.

- **NumPy (vía BLAS) ya usa varios hilos** en operaciones como `A @ B`.
- **Más procesos dejan menos núcleos** para los hilos de cada proceso.
- **joblib reparte los núcleos**: cada proceso usa **núcleos / n_jobs** hilos.
- **Suele existir un balance** entre número de procesos e hilos.

---

## Resumen de la clase
- **Multiprocessing**: un programa que crea otros programas; cada uno con su propio dataspace.
- En Python usaremos la librería **joblib** (<https://joblib.readthedocs.io>).
- **Ideal para problemas fácilmente paralelizables**: obtener resultados independientes sobre
  distintos parámetros al ejecutar un programa.

**Próxima clase:** ¿cómo analizar el rendimiento de algoritmos paralelos?
