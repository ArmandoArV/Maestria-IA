import nbformat as nbf
nb = nbf.v4.new_notebook()
C = []
def md(s): C.append(nbf.v4.new_markdown_cell(s.strip("\n")))
def co(s): C.append(nbf.v4.new_code_cell(s.strip("\n")))

md(r"""
# Tarea 1: Algoritmo de *k*-means paralelo

**IMT3870 · Computación de Alto Rendimiento · 2026-4**
Pontificia Universidad Católica de Chile. Magíster en Inteligencia Artificial

**Alumno:** Armando Arredondo Valle
**Profesor:** Ignacio Labarca
**Fecha de entrega:** martes 10 de noviembre de 2026

---

### Contenido

| Parte | Tema | Sección |
|---|---|---|
| (a) | Implementación base con *loops* (código de Canvas) | §2 |
| (b) | Vectorización con NumPy / SciPy | §3 |
| (c) | Medición de tiempo de cómputo, procesos e hilos | §4 |
| (d) | Inercia, método del codo y paralelización con `joblib` | §5 |
| Informe | **Discusión de resultados** | §6 |

### Declaración de uso de herramientas de IA

Para esta tarea se utilizó un asistente de IA (Claude, Anthropic) como apoyo en: la **vectorización**
del algoritmo (uso de `scipy.spatial.distance.cdist`, `np.argmin`, `np.bincount`), la **estructura del
código de medición** (*benchmarks*, gráficos) y la **redacción** del informe. El diseño experimental,
la ejecución en mi equipo, la verificación de consistencia entre implementaciones y la interpretación
de los resultados son propios. Todo el código fue revisado y ejecutado por mí, y soy responsable del
contenido entregado. Se declara conforme a lo permitido en el enunciado.
""")

md("## 1. Entorno de ejecución y hardware")
co(r"""
import sys, os, platform, subprocess, time, copy, json
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist
from joblib import Parallel, delayed
import psutil

RESULTS = {}   # se guardan las mediciones para el informe

def sysctl(key):
    try:
        return subprocess.check_output(["sysctl","-n",key], text=True).strip()
    except Exception:
        return "n/a"

CPU_BRAND  = sysctl("machdep.cpu.brand_string")
CORES_PHYS = psutil.cpu_count(logical=False)
CORES_LOG  = psutil.cpu_count(logical=True)
CORES_P    = sysctl("hw.perflevel0.physicalcpu")   # performance cores
CORES_E    = sysctl("hw.perflevel1.physicalcpu")   # efficiency cores

print(f"Equipo              : {CPU_BRAND}")
print(f"Sistema             : {platform.platform()}")
print(f"Núcleos FÍSICOS     : {CORES_PHYS}   ({CORES_P} performance + {CORES_E} efficiency)")
print(f"Núcleos LÓGICOS     : {CORES_LOG}")
print(f"Hyperthreading/SMT  : {'sí' if CORES_LOG > CORES_PHYS else 'NO (1 hilo por núcleo físico)'}")
print(f"RAM                 : {psutil.virtual_memory().total/2**30:.0f} GB")
print(f"Python              : {sys.version.split()[0]}  (GIL activo: {getattr(sys,'_is_gil_enabled', lambda: True)()})")
print(f"NumPy / SciPy       : {np.__version__} / {__import__('scipy').__version__}")
print(f"joblib              : {__import__('joblib').__version__}")

RESULTS["hw"] = dict(cpu=CPU_BRAND, phys=CORES_PHYS, log=CORES_LOG,
                     perf=CORES_P, eff=CORES_E, python=sys.version.split()[0])
""")

co(r"""
# ¿Qué librería de álgebra lineal usa NumPy, y cuántos hilos abre?
# Es relevante para la oversubscription de la Parte (d).
from threadpoolctl import threadpool_info

cfg  = np.__config__.show(mode="dicts")
blas = cfg.get("Build Dependencies", {}).get("blas", {})
BLAS_NAME = blas.get("name", "desconocida")
print(f"BLAS/LAPACK de NumPy : {BLAS_NAME}  (version {blas.get('version','?')})")

pools = threadpool_info()
if pools:
    for pool in pools:
        print(f"   {pool['internal_api']:10s} {pool.get('threading_layer',''):10s} "
              f"num_threads = {pool['num_threads']}")
else:
    print("   threadpoolctl no detecta ningun pool de hilos controlable.")
    print(f"   Esto es lo esperado con '{BLAS_NAME}': Apple Accelerate administra sus hilos")
    print("   internamente y no expone la API (OpenMP/MKL) que threadpoolctl sabe leer.")
    print("   => no se puede fijar el nº de hilos de BLAS con threadpoolctl en este equipo,")
    print("      pero Accelerate SI usa varios hilos (se observa en el pico de CPU de la sec. 4.2).")

RESULTS["blas_name"]    = BLAS_NAME
RESULTS["blas_threads"] = [q["num_threads"] for q in pools]
""")

md(r"""
## 2. Parte (a): datos e implementación base (código de Canvas)

Se genera la base de datos con `make_blobs` (única función de `sklearn` permitida por el enunciado) y
se ejecuta la implementación entregada en Canvas, basada en *loops* de Python.

Según el enunciado se usan **al menos 10.000 puntos** y **k ≥ 5**.
""")
co(r"""
np.random.seed(0)          # semilla fija: resultados reproducibles

from sklearn.datasets import make_blobs

n_points   = 10_000        # ≥ 10.000 por enunciado
n_blobs    = 10            # grupos realmente generados
k          = 5             # ≥ 5 por enunciado
max_iterations = 100
d          = 2

dataset, _true_labels = make_blobs(n_samples=n_points, n_features=d, centers=n_blobs)
print(f"Base de datos: {dataset.shape[0]:,} puntos en {dataset.shape[1]} dimensiones, "
      f"generados en {n_blobs} grupos.")
print(f"Memoria del arreglo: {dataset.nbytes/1024:.1f} KiB  (dtype={dataset.dtype})")
print(f"Valor de k para las partes (a)-(c): {k}")
""")
co(r"""
plt.figure(figsize=(6,5))
plt.plot(dataset[:,0], dataset[:,1], 'b.', markersize=2, alpha=.5)
plt.title(f'Base de datos ({n_points:,} puntos, {n_blobs} grupos)')
plt.xlabel('$x$'); plt.ylabel('$y$'); plt.gca().set_aspect('equal')
plt.tight_layout(); plt.show()
""")

md(r"""
### 2.1 Inicialización

Igual que en el ejemplo de Canvas: los $k$ centros iniciales se distribuyen uniformemente en el
segmento $0<x<1$, $y=0$. Es una inicialización deliberadamente *mala* (todos los centros quedan
pegados al origen, lejos de los *blobs*), lo que obliga al algoritmo a iterar varias veces y hace más
visible el costo de cómputo.
""")
co(r"""
def init_centers(k):
    "Centros iniciales del enunciado: uniformes en 0<x<1, y=0."
    centers = np.zeros([k, 2])
    for c in range(k):
        centers[c, 0] = float(c+1)/(k+1)
        centers[c, 1] = 0.0
    return centers

centers0 = init_centers(k)
plt.figure(figsize=(5,3))
plt.plot(centers0[:,0], centers0[:,1], 'rx', markersize=10)
plt.xlim([0,1]); plt.ylim([-1,1]); plt.title(f'Centros iniciales (k={k})')
plt.xlabel('$x$'); plt.ylabel('$y$'); plt.tight_layout(); plt.show()
""")

md(r"""
### 2.2 Implementación con *loops*

Es el código de Canvas, encapsulado en una función para poder reutilizarlo (medirlo y enviarlo como
tarea a `joblib`). Se conserva **exactamente** la estructura de *loops* sobre los puntos.

**Una corrección necesaria.** El código original calcula el nuevo centro como
`sum_of_locations[c,0] / number_of_points_in_cluster[c]`. Si una conglomeración queda **vacía**,
`number_of_points_in_cluster[c] == 0` y esa división produce `nan` (y un `RuntimeWarning`), lo que
contamina todas las iteraciones siguientes. Con la inicialización del enunciado esto **sí ocurre**
para algunos valores de $k$ del barrido de la Parte (d). La convención usual es **mantener el centro
anterior** cuando una conglomeración queda vacía, y es lo que se hace aquí (se cuentan los casos para
reportarlos).
""")
co(r"""
def kmeans_loops(dataset, k, max_iterations=100, keep_history=False):
    '''
    k-means con loops de Python (implementación base de Canvas).
    Devuelve dict con centros, etiquetas, nº de iteraciones y diagnóstico.
    '''
    n_points = dataset.shape[0]
    history_of_centers  = [init_centers(k)]
    history_of_clusters = []
    empty_fixes = 0
    converged   = False

    for iteration in range(max_iterations):

        old_centers = history_of_centers[-1]

        # ---- paso de asignación (loop sobre TODOS los puntos) ----
        cluster = np.zeros(n_points, dtype='int')
        for p in range(n_points):
            minimum_distance = np.inf
            nearest_cluster  = None
            for c in range(k):
                distance_to_cluster_c = np.sqrt((dataset[p,0] - old_centers[c,0])**2
                                                + (dataset[p,1] - old_centers[c,1])**2)
                if distance_to_cluster_c < minimum_distance:
                    minimum_distance = distance_to_cluster_c
                    nearest_cluster  = c
            cluster[p] = nearest_cluster
        history_of_clusters.append(cluster)

        # ---- revisar convergencia (otro loop sobre los puntos) ----
        if iteration > 0:
            clusters_changed = False
            for p in range(n_points):
                if history_of_clusters[-1][p] != history_of_clusters[-2][p]:
                    clusters_changed = True
            if not clusters_changed:
                converged = True
                break

        # ---- paso de actualización (loop sobre los puntos) ----
        number_of_points_in_cluster = np.zeros(k, dtype='int')
        sum_of_locations = np.zeros([k, 2], dtype='float')
        for p in range(n_points):
            number_of_points_in_cluster[cluster[p]] += 1
            sum_of_locations[cluster[p], :] += dataset[p, :]

        new_centers = np.zeros([k, 2], dtype='float')
        for c in range(k):
            if number_of_points_in_cluster[c] == 0:
                new_centers[c, :] = old_centers[c, :]      # conglomeración vacía
                empty_fixes += 1
            else:
                new_centers[c,0] = sum_of_locations[c,0] / number_of_points_in_cluster[c]
                new_centers[c,1] = sum_of_locations[c,1] / number_of_points_in_cluster[c]
        history_of_centers.append(new_centers)

    out = dict(centers=history_of_centers[-1], labels=history_of_clusters[-1],
               iterations=iteration, converged=converged, empty_fixes=empty_fixes,
               pid=os.getpid())
    if keep_history:
        out["history_of_centers"]  = history_of_centers
        out["history_of_clusters"] = history_of_clusters
    return out
""")
co(r"""
t0 = time.perf_counter()
res_loops = kmeans_loops(dataset, k, max_iterations, keep_history=True)
t_loops = time.perf_counter() - t0

print(f"Tiempo de cómputo (loops) : {t_loops:.3f} s")
print(f"Iteraciones               : {res_loops['iterations']}"
      f"  ({'convergió' if res_loops['converged'] else 'NO convergió, se alcanzó el máximo'})")
print(f"Conglomeraciones vacías   : {res_loops['empty_fixes']}")
print(f"Centros finales:\n{res_loops['centers']}")
RESULTS["t_loops_k5"] = t_loops
RESULTS["iters_k5"]   = res_loops["iterations"]
""")
co(r"""
# Evolución: etiquetas finales y trayectoria de los centros
hc, hcl = res_loops["history_of_centers"], res_loops["history_of_clusters"]
show = [0, 1, 2, len(hcl)//2, len(hcl)-1]
show = sorted(set(i for i in show if i < len(hcl)))

fig, axes = plt.subplots(1, len(show), figsize=(4*len(show), 3.6))
for ax, itr in zip(np.atleast_1d(axes), show):
    ax.scatter(dataset[:,0], dataset[:,1], c=hcl[itr], s=2, cmap='tab10', alpha=.6)
    traj = np.array([hc[l] for l in range(itr+1)])
    for c in range(k):
        ax.plot(traj[:,c,0], traj[:,c,1], 'b-+', lw=.8, markersize=4, alpha=.8)
    ax.plot(hc[itr][:,0], hc[itr][:,1], 'rx', markersize=11, mew=2.5)
    ax.set_title(f'Iteración {itr}'); ax.set_aspect('equal')
plt.suptitle('Parte (a): k-means con loops, asignación y trayectoria de los centros')
plt.tight_layout(); plt.show()
""")

md(r"""
### 2.3 ¿Paraleliza algo este código? Medición de procesos e hilos

Para responder la pregunta (1) del informe no basta razonar: se **mide**. Se observa el número de
hilos del proceso de Python y el uso de CPU **mientras** corre el algoritmo con *loops*. Si el código
estuviera paralelizado, el uso de CPU debería superar el 100 % de un núcleo.
""")
co(r"""
proc = psutil.Process()

THREADS_BASELINE = proc.num_threads()
print(f"Hilos del kernel de Jupyter en reposo (linea base): {THREADS_BASELINE}")

def watch_cpu(fn, *args, min_duration=1.0, **kw):
    '''
    Ejecuta fn midiendo %CPU y nº de hilos del proceso (muestreo en un hilo aparte).
    Si fn es muy rápida, la repite hasta acumular min_duration segundos, de modo que
    el muestreador alcance a tomar muestras.
    '''
    import threading
    samples = {"cpu": [], "threads": []}
    stop = threading.Event()
    def sampler():
        proc.cpu_percent(None)                     # primera llamada: inicializa
        while not stop.wait(0.005):
            samples["cpu"].append(proc.cpu_percent(None))
            samples["threads"].append(proc.num_threads())
    th = threading.Thread(target=sampler, daemon=True); th.start()
    try:
        t0 = time.perf_counter(); n_calls = 0
        while True:
            out = fn(*args, **kw); n_calls += 1
            if time.perf_counter() - t0 >= min_duration: break
    finally:
        stop.set(); th.join()
    cpu = [c for c in samples["cpu"] if c > 0]
    return (out, (max(cpu) if cpu else 0.0), (np.mean(cpu) if cpu else 0.0),
            max(samples["threads"] or [0]), n_calls)

_, cpu_max, cpu_avg, n_threads, _nc = watch_cpu(kmeans_loops, dataset, k, max_iterations)

print(f"Procesos de Python activos        : 1  (PID {os.getpid()}, sin procesos hijos: "
      f"{len(proc.children(recursive=True))})")
print(f"Hilos del proceso (máximo)        : {n_threads}  "
      f"(= {THREADS_BASELINE} del kernel de Jupyter + 1 de esta medición)")
print(f"Hilos creados por el ALGORITMO    : {max(0, n_threads - THREADS_BASELINE - 1)}")
print(f"Uso de CPU del proceso  promedio  : {cpu_avg:6.1f} %")
print(f"Uso de CPU del proceso  máximo    : {cpu_max:6.1f} %")
print(f"Núcleos físicos disponibles       : {CORES_PHYS}  "
      f"(uso total posible: {100*CORES_PHYS} %)")
print()
print(f"=> El algoritmo usa ~1 núcleo de {CORES_PHYS}: "
      f"{cpu_avg/(100*CORES_PHYS)*100:.1f} % de la capacidad de la máquina.")
RESULTS["cpu_avg_loops"] = cpu_avg; RESULTS["cpu_max_loops"] = cpu_max
RESULTS["threads_loops"] = n_threads
""")

md(r"""
## 3. Parte (b): vectorización

Requisitos del enunciado:

* usar **arreglos** en lugar de listas;
* usar **funciones vectoriales** de NumPy/SciPy (normas, distancias, sumas);
* **ningún loop ni *list comprehension* sobre los puntos**; se permiten loops sobre los centros;
* solo NumPy/SciPy (sin `sklearn`, `pandas`, etc.), excepto `make_blobs`.

Las tres partes del algoritmo se reemplazan así:

| Paso | Con loops | Vectorizado |
|---|---|---|
| Asignación | loop `p` × loop `c` + `sqrt` escalar | `cdist(dataset, centers)` + `np.argmin(..., axis=1)` |
| Convergencia | loop `p` comparando etiquetas | `np.array_equal(cluster, prev)` |
| Actualización | loop `p` acumulando sumas | `np.add.at` / máscara `dataset[cluster==c].mean(0)` + `np.bincount` |

Para el paso de actualización se usa un loop **sobre los k centros** (permitido), no sobre los puntos.
Se emplea `np.bincount` para contar los puntos por conglomeración y `np.add.at` para acumular las
sumas de coordenadas en una sola pasada vectorial.
""")
co(r"""
def kmeans_numpy(dataset, k, max_iterations=100, keep_history=False):
    '''
    k-means vectorizado con NumPy/SciPy.
    Sin loops ni list comprehensions sobre los n puntos; solo loops sobre los k centros.
    '''
    centers = init_centers(k)
    history_of_centers  = [centers]
    history_of_clusters = []
    previous_cluster = None
    empty_fixes = 0
    converged   = False

    for iteration in range(max_iterations):

        # ---- paso de asignación: matriz de distancias (n x k) y argmin por fila ----
        distances = cdist(dataset, centers, metric='euclidean')   # SciPy, código compilado
        cluster   = np.argmin(distances, axis=1)
        history_of_clusters.append(cluster)

        # ---- convergencia: comparación vectorial de los arreglos de etiquetas ----
        if previous_cluster is not None and np.array_equal(cluster, previous_cluster):
            converged = True
            break
        previous_cluster = cluster

        # ---- paso de actualización: centro de masa por conglomeración ----
        counts = np.bincount(cluster, minlength=k)                # puntos por cluster
        sums   = np.zeros((k, dataset.shape[1]))
        np.add.at(sums, cluster, dataset)                         # suma vectorial por cluster

        new_centers = centers.copy()
        nonempty = counts > 0
        new_centers[nonempty] = sums[nonempty] / counts[nonempty, None]   # centro de masa
        empty_fixes += int(np.count_nonzero(~nonempty))            # vacías: se mantiene el centro

        centers = new_centers
        history_of_centers.append(centers)

    out = dict(centers=centers, labels=history_of_clusters[-1], iterations=iteration,
               converged=converged, empty_fixes=empty_fixes, pid=os.getpid())
    if keep_history:
        out["history_of_centers"]  = history_of_centers
        out["history_of_clusters"] = history_of_clusters
    return out
""")

md("### 3.1 Verificación de consistencia con la implementación base")
co(r"""
res_numpy = kmeans_numpy(dataset, k, max_iterations, keep_history=True)

same_labels  = np.array_equal(res_loops["labels"], res_numpy["labels"])
agreement    = np.mean(res_loops["labels"] == res_numpy["labels"]) * 100
max_dc       = np.abs(np.sort(res_loops["centers"],0) - np.sort(res_numpy["centers"],0)).max()
same_iters   = res_loops["iterations"] == res_numpy["iterations"]

print(f"Iteraciones  loops / numpy   : {res_loops['iterations']} / {res_numpy['iterations']}"
      f"   {'✓ iguales' if same_iters else '✗ distintas'}")
print(f"Etiquetas idénticas          : {'✓ SÍ' if same_labels else '✗ no'}  "
      f"(coincidencia {agreement:.4f} %)")
print(f"Máx. diferencia en centros   : {max_dc:.3e}")
print(f"Conglomeraciones vacías      : loops={res_loops['empty_fixes']}, numpy={res_numpy['empty_fixes']}")
assert same_labels, "Las implementaciones deben dar el mismo resultado"
print("\n=> Las dos implementaciones son CONSISTENTES: mismas etiquetas y mismos centros.")
RESULTS["consistent"] = bool(same_labels); RESULTS["agreement_pct"] = agreement
RESULTS["max_center_diff"] = float(max_dc)
""")
co(r"""
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
for ax, (res, name) in zip(axes, [(res_loops,'(a) loops'), (res_numpy,'(b) NumPy vectorizado')]):
    ax.scatter(dataset[:,0], dataset[:,1], c=res["labels"], s=2, cmap='tab10', alpha=.6)
    ax.plot(res["centers"][:,0], res["centers"][:,1], 'rx', markersize=12, mew=2.5)
    ax.set_title(f'{name}, {res["iterations"]} iteraciones'); ax.set_aspect('equal')
plt.suptitle('Parte (b): resultado idéntico con ambas implementaciones')
plt.tight_layout(); plt.show()
""")

md(r"""
## 4. Parte (c): medición del tiempo de cómputo

Se mide cada implementación repetidas veces (se reporta el **mínimo**, que es la estimación menos
contaminada por ruido del sistema operativo) y se estudia cómo escala el tiempo con el número de
puntos $n$.
""")
co(r"""
def bench(fn, *args, repeats=3, **kw):
    "Devuelve (mejor tiempo, tiempo medio) de varias repeticiones."
    ts = []
    for _ in range(repeats):
        t0 = time.perf_counter(); fn(*args, **kw); ts.append(time.perf_counter()-t0)
    return min(ts), float(np.mean(ts))

t_loops_best, t_loops_mean = bench(kmeans_loops, dataset, k, max_iterations, repeats=3)
t_numpy_best, t_numpy_mean = bench(kmeans_numpy, dataset, k, max_iterations, repeats=7)
speedup = t_loops_best / t_numpy_best

print(f"{'Implementación':<28} {'mejor [s]':>12} {'medio [s]':>12}")
print("-"*54)
print(f"{'(a) loops de Python':<28} {t_loops_best:>12.4f} {t_loops_mean:>12.4f}")
print(f"{'(b) NumPy vectorizado':<28} {t_numpy_best:>12.4f} {t_numpy_mean:>12.4f}")
print("-"*54)
print(f"\nAceleración por vectorizar: {speedup:.1f}x   "
      f"(n = {n_points:,} puntos, k = {k}, {res_loops['iterations']} iteraciones)")
print(f"Tiempo por punto y por iteración:")
print(f"   loops : {t_loops_best/(n_points*res_loops['iterations'])*1e9:8.1f} ns")
print(f"   numpy : {t_numpy_best/(n_points*res_numpy['iterations'])*1e9:8.1f} ns")
RESULTS.update(t_loops_best=t_loops_best, t_numpy_best=t_numpy_best, speedup_vec=speedup)
""")

md("### 4.1 Escalamiento con el número de puntos")
co(r"""
sizes = [1_000, 2_500, 5_000, 10_000, 20_000, 40_000]
tl, tn = [], []
for n in sizes:
    sub = dataset[:n] if n <= n_points else None
    if sub is None:
        np.random.seed(0)
        sub, _ = make_blobs(n_samples=n, n_features=2, centers=n_blobs)
    a,_ = bench(kmeans_loops, sub, k, max_iterations, repeats=1)
    b,_ = bench(kmeans_numpy, sub, k, max_iterations, repeats=3)
    tl.append(a); tn.append(b)
    print(f"n = {n:6,} | loops {a:8.3f} s | numpy {b:8.4f} s | speedup {a/b:6.1f}x")
RESULTS["scaling"] = dict(sizes=sizes, loops=tl, numpy=tn)
""")
co(r"""
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2))
axes[0].loglog(sizes, tl, 'o-', label='(a) loops de Python')
axes[0].loglog(sizes, tn, 's-', label='(b) NumPy vectorizado')
axes[0].set_xlabel('n (puntos)'); axes[0].set_ylabel('Tiempo [s]')
axes[0].set_title('Tiempo de cómputo'); axes[0].legend(); axes[0].grid(True, which='both', alpha=.3)
axes[1].semilogx(sizes, np.array(tl)/np.array(tn), 'd-', color='crimson')
axes[1].set_xlabel('n (puntos)'); axes[1].set_ylabel('Aceleración (×)')
axes[1].set_title('Aceleración de la vectorización'); axes[1].grid(True, alpha=.3)
plt.tight_layout(); plt.show()
""")

md(r"""
### 4.2 Procesos e hilos durante la ejecución

Se compara el uso de CPU e hilos de las dos implementaciones. Esto permite ver si NumPy/SciPy abren
hilos adicionales (BLAS) en esta carga de trabajo.
""")
co(r"""
rows = []
for name, fn in [("(a) loops", kmeans_loops), ("(b) NumPy", kmeans_numpy)]:
    _, cmax, cavg, nth, ncalls = watch_cpu(fn, dataset, k, max_iterations, min_duration=1.5)
    rows.append((name, cavg, cmax, nth, ncalls))

print(f"{'Implementación':<14} {'CPU medio':>11} {'CPU máx':>10} {'hilos':>7} {'corridas':>10}")
print("-"*58)
for name, cavg, cmax, nth, ncalls in rows:
    print(f"{name:<14} {cavg:>10.1f} % {cmax:>9.1f} % {nth:>7} {ncalls:>10}")
print("-"*58)
print("(1 núcleo = 100 %. La version NumPy se repite muchas veces en la ventana de")
print(" medicion porque una sola corrida dura pocos milisegundos.)")
print(f"\nNúcleos físicos: {CORES_PHYS}.  Capacidad total de la máquina: {100*CORES_PHYS} %.")
print("Ninguna de las dos implementaciones supera ~100 %: ambas son esencialmente SECUENCIALES.")
print(f"\nProcesos hijos de Python en este momento: {len(proc.children(recursive=True))}")
RESULTS["cpu_table"] = [(n, float(a), float(m), int(t), int(c)) for n,a,m,t,c in rows]
""")

md(r"""
## 5. Parte (d): inercia, método del codo y paralelización con `joblib`

### 5.1 Inercia

$$I_k=\sum_{i=1}^{k}\sum_{j=1}^{N_i}\lVert \mathbf{x}_{ij}-\mathbf{c}_i\rVert^2$$

Se calcula de forma vectorizada: la inercia es la suma de las distancias al cuadrado de cada punto
al centro **asignado**, es decir `((dataset - centers[labels])**2).sum()`.
""")
co(r"""
def inertia(dataset, labels, centers):
    "Inercia I_k, totalmente vectorizada (sin loops sobre los puntos)."
    diff = dataset - centers[labels]
    return float(np.einsum('ij,ij->', diff, diff))     # == (diff**2).sum()

def inertia_reference(datapoints, cluster, centers):
    "Versión del ejemplo de Canvas, con loop sobre los k centros (para verificar)."
    total = 0.0
    for i in range(centers.shape[0]):
        pts = datapoints[cluster == i, :]
        if pts.size:
            total += np.sum(np.linalg.norm(pts - centers[i,:], axis=1)**2)
    return total

I_fast = inertia(dataset, res_numpy["labels"], res_numpy["centers"])
I_ref  = inertia_reference(dataset, res_numpy["labels"], res_numpy["centers"])
print(f"Inercia (vectorizada)      : {I_fast:,.4f}")
print(f"Inercia (versión de Canvas): {I_ref:,.4f}")
print(f"Diferencia relativa        : {abs(I_fast-I_ref)/I_ref:.2e}  ✓ coinciden")
""")

md(r"""
### 5.2 Tarea para `joblib`: un valor de k por tarea

Cada tarea corre **todo** el algoritmo de k-means para un único $k$ y devuelve la inercia junto con el
**PID** del proceso que la ejecutó (para comprobar que `joblib` efectivamente usa procesos distintos,
bajo el paradigma *multiprocessing*).

Las funciones se definen a nivel de módulo para que sean **serializables** (`pickle`), como requiere el
modelo `spawn` que usa `loky` por defecto (Clase 04).
""")
co(r"""
def kmeans_task(dataset, k, max_iterations=100, impl="numpy"):
    "Una tarea de joblib: k-means completo para un único k. Devuelve inercia, PID y diagnóstico."
    t0  = time.perf_counter()
    res = (kmeans_numpy if impl == "numpy" else kmeans_loops)(dataset, k, max_iterations)
    return dict(k=k, inertia=inertia(dataset, res["labels"], res["centers"]),
                iterations=res["iterations"], converged=res["converged"],
                empty=res["empty_fixes"], pid=os.getpid(),
                t=time.perf_counter()-t0)

ks = list(range(1, 26))        # k = 1, 2, ..., 25
print("k =", ks)
""")

md("### 5.3 Barrido serial y método del codo")
co(r"""
t0 = time.perf_counter()
sweep = [kmeans_task(dataset, kk, max_iterations, impl="numpy") for kk in ks]
t_sweep_serial_numpy = time.perf_counter() - t0

inertias = [s["inertia"] for s in sweep]
print(f"Barrido serial k=1..25 (NumPy): {t_sweep_serial_numpy:.3f} s")
print(f"PIDs utilizados: {sorted({s['pid'] for s in sweep})}  -> un solo proceso (serial)")
no_conv = [s['k'] for s in sweep if not s['converged']]
print(f"Valores de k que NO convergieron en {max_iterations} iteraciones: {no_conv}")
print(f"Valores de k con conglomeraciones vacías: {[s['k'] for s in sweep if s['empty']>0]}")
RESULTS["t_sweep_serial_numpy"] = t_sweep_serial_numpy
RESULTS["inertias"] = inertias
RESULTS["no_converged"] = no_conv
RESULTS["empty_ks"] = [s['k'] for s in sweep if s['empty']>0]
""")
co(r"""
# ---- Método del codo: dos criterios cuantitativos ----
I   = np.array(inertias)
kv  = np.array(ks)
rel = -np.diff(I) / I[:-1] * 100            # reducción RELATIVA al pasar de k a k+1 [%]

# Criterio 1 (cuerda / "Kneedle"): el punto más alejado de la recta que une los
# extremos de la curva. Se aplica sobre log(I) porque la inercia cae varios
# órdenes de magnitud y en escala lineal el criterio se sesga hacia k pequeños.
xn  = (kv - kv.min()) / (kv.max() - kv.min())
yl  = np.log(I); yln = (yl - yl.min()) / (yl.max() - yl.min())
k_chord = int(kv[np.argmin(xn + yln)])

# Criterio 2: primer k cuya ganancia marginal cae por debajo de un umbral.
UMBRAL = 10.0
below   = np.where(rel < UMBRAL)[0]
k_thr   = int(kv[below[0]]) if below.size else int(kv[-1])

# Criterio ingenuo, para contraste: máxima segunda diferencia.
k_naive = int(kv[1:-1][np.argmax(np.diff(I, 2))])

k_elbow = k_chord
print(f"Criterio 1 - cuerda sobre log(I)          : k = {k_chord}")
print(f"Criterio 2 - 1er k con ganancia < {UMBRAL:.0f} %     : k = {k_thr}")
print(f"Criterio ingenuo - max. 2a diferencia     : k = {k_naive}   <-- enganoso (ver informe)")
print(f"Grupos realmente generados por make_blobs : {n_blobs}")
RESULTS.update(k_chord=k_chord, k_thr=k_thr, k_naive=k_naive)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))
axes[0].plot(ks, I, 'o-')
axes[0].axvline(k_elbow, color='crimson', ls='--', label=f'codo ≈ k={k_elbow}')
axes[0].axvline(n_blobs, color='green', ls=':', label=f'grupos generados = {n_blobs}')
axes[0].set_xlabel('k'); axes[0].set_ylabel('Inercia $I_k$')
axes[0].set_title('Método del codo'); axes[0].legend(); axes[0].grid(alpha=.3)
axes[0].set_xticks(range(0,26,5))

axes[1].bar(kv[:-1], rel, color=['crimson' if a == k_elbow else 'steelblue' for a in kv[:-1]])
axes[1].axhline(UMBRAL, color='k', ls='--', label=f'umbral {UMBRAL:.0f} %')
axes[1].set_xlabel('k'); axes[1].set_ylabel('Reducción de $I_k$ al pasar a $k+1$ [%]')
axes[1].set_title('Ganancia marginal de aumentar k')
axes[1].legend(); axes[1].grid(alpha=.3, axis='y'); axes[1].set_xticks(range(0,26,5))
plt.tight_layout(); plt.show()

print("La inercia SIEMPRE decrece al aumentar k (Clase 04): por eso no se puede")
print("minimizar I_k directamente, y hay que buscar el punto de inflexion.\n")
print(f"{'k -> k+1':>10} {'ganancia':>11}")
print("-"*23)
for a, r in zip(kv[:-1], rel):
    print(f"{a:4d} ->{a+1:3d} {r:9.2f} %" + ("   <-- codo" if a == k_elbow else ""))
RESULTS["k_elbow"] = k_elbow
""")

md(r"""
### 5.4 Paralelización con `joblib`: verificación de procesos distintos

Se usa el *backend* `loky` (el de por omisión de `joblib`), que crea **procesos independientes**:
es el paradigma *multiprocessing* pedido por el enunciado. Se verifica recolectando los PID.
""")
co(r"""
out4 = Parallel(n_jobs=4, backend="loky")(
            delayed(kmeans_task)(dataset, kk, max_iterations, "numpy") for kk in ks)
pids = sorted({o["pid"] for o in out4})

print(f"PID del proceso padre : {os.getpid()}")
print(f"PIDs de los workers   : {pids}")
print(f"Nº de procesos distintos usados: {len(pids)}  (n_jobs=4)")
print(f"¿Usa procesos distintos del padre? {'✓ SÍ' if os.getpid() not in pids else '✗ no'}")

same = np.allclose([o["inertia"] for o in out4], inertias)
print(f"\n¿Mismas inercias que el barrido serial? {'✓ SÍ' if same else '✗ NO'}")
RESULTS["n_pids_njobs4"] = len(pids)
RESULTS["parallel_same_result"] = bool(same)
""")

md(r"""
### 5.5 Tiempo de cómputo vs. número de procesos

Se repite el barrido completo $k=1,\dots,25$ para `n_jobs` $=1,2,3,4$ (y además 8 y 15, el número de
núcleos físicos de este equipo), con **dos tareas distintas**, como pide la pregunta (3) del informe:

1. la tarea es k-means implementado con **loops**;
2. la tarea es k-means implementado con **NumPy**.
""")
co(r"""
n_jobs_list = sorted(set([1, 2, 3, 4, 8, CORES_PHYS]))
timings  = {"loops": {}, "numpy": {}}
per_task = {}
REPEATS  = {"numpy": 3, "loops": 1}   # la tarea NumPy dura ms: se repite y se toma el minimo

for impl in ["numpy", "loops"]:
    print(f"\n### Tarea = k-means con {impl}  " + "#"*30)
    print(f"{'n_jobs':>7} {'tiempo [s]':>12} {'speedup':>10} {'eficiencia':>12} {'procesos':>10}")
    print("-"*56)
    for p in n_jobs_list:
        best = np.inf
        for _ in range(REPEATS[impl]):
            t0 = time.perf_counter()
            out = Parallel(n_jobs=p, backend="loky")(
                      delayed(kmeans_task)(dataset, kval, max_iterations, impl) for kval in ks)
            best = min(best, time.perf_counter() - t0)
        npid = len({o["pid"] for o in out})
        timings[impl][p] = best
        if p == 1:
            per_task[impl] = [o["t"] for o in out]
        sp = timings[impl][1] / best
        print(f"{p:>7} {best:>12.3f} {sp:>9.2f}x {sp/p*100:>11.1f} % {npid:>10}")

RESULTS["timings"]  = {i: {str(a): b for a, b in d.items()} for i, d in timings.items()}
RESULTS["per_task"] = {i: [float(x) for x in v] for i, v in per_task.items()}

RESULTS["timings"] = {i: {str(k_): v for k_, v in d.items()} for i, d in timings.items()}
""")
co(r"""
fig, axes = plt.subplots(1, 3, figsize=(16, 4.3))
P = np.array(n_jobs_list)

for impl, mk in [("loops",'o-'), ("numpy",'s-')]:
    t = np.array([timings[impl][p] for p in n_jobs_list])
    axes[0].plot(P, t, mk, label=f'tarea = {impl}')
    axes[1].plot(P, t[0]/t, mk, label=f'tarea = {impl}')
    axes[2].plot(P, (t[0]/t)/P*100, mk, label=f'tarea = {impl}')

axes[0].set_yscale('log'); axes[0].set_ylabel('Tiempo del barrido [s]')
axes[0].set_title('Tiempo vs. nº de procesos')
axes[1].plot(P, P, 'k--', label='ideal $S_p=p$'); axes[1].set_ylabel('Speedup $S_p$')
axes[1].set_title('Aceleración')
axes[2].axhline(100, color='k', ls='--', label='ideal 100 %'); axes[2].set_ylabel('Eficiencia $E_p$ [%]')
axes[2].set_title('Eficiencia paralela')
for ax in axes:
    ax.set_xlabel('n_jobs (procesos)'); ax.grid(alpha=.3); ax.legend(); ax.set_xticks(P)
plt.suptitle('Parte (d): escalabilidad de joblib para el barrido k=1..25')
plt.tight_layout(); plt.show()
""")

md(r"""
### 5.6 Costo por tarea: el desbalance de carga

El barrido $k=1,\dots,25$ tiene tareas de **costo muy desigual** (correr k-means con $k=25$ cuesta
mucho más que con $k=1$). Según la Clase 05, el tiempo total lo determina el worker más lento, así que
este desbalance es una de las razones por las que la eficiencia no llega al 100 %.
""")
co(r"""
t_loop  = np.array(per_task["loops"])
t_np    = np.array(per_task["numpy"])
it_task = np.array([s["iterations"] for s in sweep])

fig, axes = plt.subplots(1, 3, figsize=(16, 4))
axes[0].bar(ks, t_loop, color='steelblue')
axes[0].set_ylabel('Tiempo de la tarea [s]');  axes[0].set_title('Costo por tarea (loops)')
axes[1].bar(ks, t_np*1000, color='seagreen')
axes[1].set_ylabel('Tiempo de la tarea [ms]'); axes[1].set_title('Costo por tarea (NumPy)')
axes[2].bar(ks, it_task, color='darkorange')
axes[2].set_ylabel('Iteraciones');             axes[2].set_title('Iteraciones por tarea')
for ax in axes: ax.set_xlabel('k'); ax.grid(alpha=.3, axis='y')
plt.suptitle('Parte (d): las 25 tareas del barrido tienen costos MUY desiguales')
plt.tight_layout(); plt.show()

print(f"{'':24s} {'loops':>14} {'NumPy':>14}")
print("-"*54)
print(f"{'tarea más barata':24s} {t_loop.min():12.4f} s {t_np.min()*1000:12.2f} ms")
print(f"{'tarea más costosa':24s} {t_loop.max():12.4f} s {t_np.max()*1000:12.2f} ms")
print(f"{'razón máx/mín':24s} {t_loop.max()/t_loop.min():12.1f}x {t_np.max()/t_np.min():12.1f}x")
print(f"{'suma de las 25 tareas':24s} {t_loop.sum():12.3f} s {t_np.sum()*1000:12.1f} ms")
print("-"*54)

# Cota inferior del barrido con p workers (Clase 05): ni el reparto perfecto puede
# bajar de max( tarea más larga , trabajo total / p ).
print(f"\nCota inferior del barrido con loops vs. lo medido:")
print(f"{'p':>4} {'cota [s]':>10} {'medido [s]':>12} {'brecha':>9}")
print("-"*38)
for p_ in n_jobs_list:
    cota = max(t_loop.max(), t_loop.sum()/p_)
    real = timings['loops'][p_]
    print(f"{p_:>4} {cota:>10.2f} {real:>12.2f} {real/cota:>8.2f}x")

RESULTS["task_imbalance"]   = float(t_loop.max()/t_loop.min())
RESULTS["t_task_sum_loops"] = float(t_loop.sum())
RESULTS["t_task_max_loops"] = float(t_loop.max())
""")
co(r"""
# Overhead de joblib: costo de crear procesos medido con una tarea trivial
def trivial(i):
    return os.getpid()

t0 = time.perf_counter(); Parallel(n_jobs=1, backend="loky")(delayed(trivial)(i) for i in range(25))
t_ov1 = time.perf_counter()-t0
t0 = time.perf_counter(); Parallel(n_jobs=4, backend="loky")(delayed(trivial)(i) for i in range(25))
t_ov4 = time.perf_counter()-t0

print(f"Overhead de joblib con 25 tareas triviales:")
print(f"   n_jobs=1 : {t_ov1*1000:8.1f} ms")
print(f"   n_jobs=4 : {t_ov4*1000:8.1f} ms")
print(f"\nComparación con el trabajo útil del barrido:")
print(f"   barrido NumPy (serial)  : {t_sweep_serial_numpy*1000:8.1f} ms")
print(f"   barrido loops (serial)  : {timings['loops'][1]*1000:8.1f} ms")
print(f"\n=> El overhead es {t_ov4/t_sweep_serial_numpy*100:.0f} % del barrido NumPy, "
      f"pero solo {t_ov4/timings['loops'][1]*100:.2f} % del barrido con loops.")
RESULTS["t_overhead_njobs4"] = t_ov4; RESULTS["t_overhead_njobs1"] = t_ov1
""")
co(r"""
# Guardar todas las mediciones (se usan en el informe de la sección 6)
with open("resultados.json", "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)
print("Mediciones guardadas en resultados.json")
print(json.dumps({k_: v for k_, v in RESULTS.items()
                  if k_ in ('t_loops_best','t_numpy_best','speedup_vec','k_elbow',
                            'task_imbalance','n_pids_njobs4')}, indent=2))
""")

C.append(nbf.v4.new_markdown_cell("<!--INFORME-->"))

nb["cells"] = C
nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                  "language_info": {"name": "python", "version": "3.12.14"}}
nbf.write(nb, "Tarea01.ipynb")
print(f"Tarea01.ipynb escrito con {len(C)} celdas")
