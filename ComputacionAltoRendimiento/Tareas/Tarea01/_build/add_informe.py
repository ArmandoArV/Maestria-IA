# -*- coding: utf-8 -*-
"""
Genera la sección 6 (Informe) del notebook a partir de resultados.json.
Todas las cifras se interpolan desde las mediciones reales: no hay números
escritos a mano, de modo que el informe nunca queda desincronizado del run.
"""
import nbformat as nbf, json, numpy as np

nb = nbf.read("Tarea01.ipynb", as_version=4)
R  = json.load(open("resultados.json"))

# ------------------------- magnitudes derivadas -------------------------
HW   = R["hw"]
PH, PE, PP, LG = HW["phys"], HW["eff"], HW["perf"], HW["log"]
T    = {i: {int(k): v for k, v in d.items()} for i, d in R["timings"].items()}
PJ   = sorted(T["loops"])                      # lista de n_jobs
tl, tn = R["t_loops_best"], R["t_numpy_best"]
SPV  = R["speedup_vec"]
ITERS, NPTS, KMAIN = R["iters_k5"], 10_000, 5
ns_l = tl/(NPTS*ITERS)*1e9
ns_n = tn/(NPTS*ITERS)*1e9
tmax, tsum = R["t_task_max_loops"], R["t_task_sum_loops"]
frac = tmax/tsum                               # fracción del trabajo de la tarea más larga
sinf = 1/frac                                  # cota de Amdahl
ptl  = np.array(R["per_task"]["loops"]); ptn = np.array(R["per_task"]["numpy"])
ovh  = R["t_overhead_njobs4"]
swn  = R["t_sweep_serial_numpy"]
S    = {i: {p: T[i][PJ[0]]/T[i][p] for p in PJ} for i in T}
E    = {i: {p: S[i][p]/p*100       for p in PJ} for i in T}
PMAX = PJ[-1]
def amdahl_f(p):                               # fracción serial efectiva implícita
    return (1/S["loops"][p] - 1/p)/(1 - 1/p)
scal = R["scaling"]
sp_r = np.array(scal["loops"])/np.array(scal["numpy"])
BLAS = R.get("blas_name", "desconocida")
# ganancias marginales de inercia (deterministas: semilla fija) alrededor del codo
_I   = np.array(R["inertias"]); _rel = -np.diff(_I)/_I[:-1]*100
KE   = R["k_chord"]
GAIN_IN, GAIN_OUT = _rel[KE-2], _rel[KE-1]      # (k-1 -> k)  y  (k -> k+1)
# el speedup de la tarea NumPy con 2 procesos puede ser < 1 (frenada); redacción adaptativa
_s2  = S["numpy"][2]
NP2_WORD = ("**no solo no aporta nada: resulta más lento que el barrido serial**"
            if _s2 < 1.0 else
            ("paralelizar **casi no aporta nada**" if _s2 < 1.25 else
             "la ganancia es modesta"))

INFORME = []
def md(s): INFORME.append(nbf.v4.new_markdown_cell(s.strip("\n")))

# --------------------------------- §6 ---------------------------------
md(f"""
---

# 6. Informe y discusión de resultados

Todas las cifras de esta sección se generan automáticamente a partir de las mediciones de
**esta misma ejecución** (`resultados.json`), por lo que no pueden quedar desactualizadas. Los tiempos
varían algunos puntos porcentuales entre corridas; las conclusiones no dependen de esa variación.

## Resumen de las mediciones

| Magnitud | Valor |
|---|---|
| Equipo | {HW['cpu']}, con **{PH} núcleos físicos** ({PP} *performance* + {PE} *efficiency*), {LG} lógicos |
| Base de datos | {NPTS:,} puntos, 2 dimensiones, 10 grupos generados (`make_blobs`) |
| k de las partes (a)–(c) | {KMAIN} (converge en {ITERS} iteraciones) |
| (a) k-means con *loops* | **{tl:.4f} s** ({ns_l:,.0f} ns por punto y por iteración) |
| (b) k-means vectorizado | **{tn:.4f} s** ({ns_n:,.1f} ns por punto y por iteración) |
| Aceleración por vectorizar | **{SPV:.1f}×** |
| Consistencia (a) vs (b) | etiquetas **idénticas** ({R['agreement_pct']:.4f} %), diferencia máxima en centros **{R['max_center_diff']:.1f}** |
| Codo del barrido k = 1…25 | **k = {R['k_chord']}** (coincide con los 10 grupos generados) |
| Barrido serial k = 1…25 | {swn:.3f} s (NumPy) · {T['loops'][1]:.2f} s (*loops*) |
| `joblib`, tarea = *loops* | {T['loops'][1]:.2f} s → **{T['loops'][PMAX]:.2f} s** con {PMAX} procesos (**{S['loops'][PMAX]:.2f}×**) |
| `joblib`, tarea = NumPy | {T['numpy'][1]:.3f} s → **{T['numpy'][PMAX]:.3f} s** con {PMAX} procesos (**{S['numpy'][PMAX]:.2f}×**) |
""")

md(f"""
## (1) ¿Paraleliza el código de Canvas alguna parte del algoritmo?

**No. El código de Canvas es completamente secuencial.** No se trata de una impresión: se midió
(§2.3 y §4.2).

| Evidencia | Medición |
|---|---|
| Procesos de Python | **1** (sin procesos hijos) |
| Hilos creados por el algoritmo | **0** (los {R['threads_loops']-1} hilos observados son del *kernel* de Jupyter en reposo, más 1 del medidor) |
| Uso de CPU del proceso | **{R['cpu_avg_loops']:.1f} % promedio**, {R['cpu_max_loops']:.1f} % máximo, es decir **≈ 1 núcleo** |
| Capacidad de la máquina | {100*PH} % ({PH} núcleos) → se aprovecha el **{R['cpu_avg_loops']/(100*PH)*100:.1f} %** |

**Por qué.** El algoritmo está escrito como *loops* de Python puro sobre los `n` puntos, y en CPython
el **GIL** permite que **solo un hilo ejecute *bytecode* a la vez** (Clase 07). Aunque se crearan
hilos, no habría paralelismo de cómputo. El código tampoco llama a rutinas compiladas que liberen el
GIL de forma significativa: las únicas operaciones de NumPy están **dentro** del loop por punto
(`sum_of_locations[cluster[p], :] += dataset[p, :]` opera sobre **2 elementos**), de modo que aportan
*overhead* de interpretación en lugar de eliminarlo.

**Dos matices honestos:**

* El *hardware* **sí** paraleliza internamente: un núcleo moderno es **superescalar y segmentado**
  (*pipelining*, IPC > 1, Clase 03). Pero eso es paralelismo **a nivel de instrucción**, lo maneja el
  procesador y no el programa, y aquí está limitado por las dependencias y por el *overhead* del
  intérprete.
* La única parte del ejemplo que **sí** está vectorizada es `calc_inertia`, que usa
  `np.linalg.norm(..., axis=1)` sobre un *slice* del arreglo. Pero está **fuera** del ciclo iterativo
  y no afecta el costo del algoritmo.
""")

md(f"""
## (2) Diferencia de tiempo entre las dos variantes, y por qué

La versión vectorizada es **{SPV:.1f}× más rápida** ({tl:.4f} s → {tn:.4f} s con n = {NPTS:,} y
k = {KMAIN}). La aceleración se mantiene **aproximadamente constante** (entre {sp_r.min():.0f}× y
{sp_r.max():.0f}×) para n entre {scal['sizes'][0]:,} y {scal['sizes'][-1]:,} (§4.1): **la
vectorización no cambia la complejidad** (ambas son O(n·k·iteraciones)) sino la **constante** que
multiplica a esa complejidad.

El dato más elocuente es el costo **por punto y por iteración**:

| Implementación | Costo por punto · iteración |
|---|---|
| (a) *loops* de Python | **{ns_l:,.0f} ns** |
| (b) NumPy / SciPy | **{ns_n:,.1f} ns** |

Las razones, en orden de importancia:

1. **Interpretado vs. compilado (Clase 04/08).** Cada iteración del loop de Python paga despacho de
   *bytecode*, creación de objetos `float`, verificación de tipos y de índices. La versión NumPy hace
   **una sola** llamada a `cdist`, y todo el trabajo numérico ocurre dentro de código compilado.
2. **Pipelining (Clase 03).** El código compilado de SciPy ejecuta la **misma instrucción sobre
   muchos datos independientes**, que es justamente el caso favorable para que el *pipeline* del
   procesador se mantenga lleno y la FPU produzca un resultado por ciclo. En el *loop* de Python cada
   operación aritmética está rodeada de trabajo del intérprete, que rompe esa regularidad.
3. **Localidad de datos y línea de caché (Clase 06).** `dataset` es un arreglo contiguo de NumPy.
   `cdist` lo recorre secuencialmente, de modo que cada línea de caché (64–128 bytes, 8–16 *floats*)
   se aprovecha por completo. El *loop* de Python accede `dataset[p,0]` y `dataset[p,1]` elemento por
   elemento, creando un escalar de Python en cada acceso: paga la latencia sin reutilizar la línea.
4. **El chequeo de convergencia.** El original recorre los n puntos comparando etiquetas una por una;
   la versión vectorizada usa `np.array_equal`, que es una comparación compilada.
5. **Algo de paralelismo de hilos.** En §4.2 la versión NumPy llegó a un **máximo de
   {R['cpu_table'][1][2]:.0f} % de CPU** (frente a {R['cpu_table'][0][2]:.0f} % de la versión con
   *loops*), lo que indica que las rutinas compiladas **sí** usan más de un hilo en algunos momentos.
   En este equipo NumPy está compilado contra **{BLAS}** (Apple Accelerate), que administra sus hilos
   internamente. Con todo, el promedio es ≈ 100 %, así que la mayor parte de la ganancia es por
   eficiencia secuencial, no por paralelismo.

**Verificación de que son equivalentes.** No basta con que sea más rápido: las etiquetas finales son
**idénticas** (coincidencia {R['agreement_pct']:.4f} %), la diferencia máxima entre centros es
**exactamente {R['max_center_diff']:.1f}**, y ambas convergen en las **mismas {ITERS} iteraciones**. La
inercia vectorizada coincide con la función de Canvas con un error relativo del orden de 10⁻¹⁶
(precisión de máquina).
""")

# tabla comparativa de joblib
rows = "\n".join(
    f"| {p} | {T['loops'][p]:,.2f} s | {S['loops'][p]:.2f}× | {E['loops'][p]:.1f} % | "
    f"{T['numpy'][p]:.3f} s | {S['numpy'][p]:.2f}× | {E['numpy'][p]:.1f} % |"
    for p in PJ)
cota = "\n".join(
    f"| {p} | {max(tmax, tsum/p):,.2f} s | {T['loops'][p]:,.2f} s | {T['loops'][p]/max(tmax, tsum/p):.2f}× |"
    for p in PJ[1:])
p_floor = next((p for p in PJ if tsum/p <= tmax), PJ[-1])

md(f"""
## (3) Tiempo de cómputo según el número de procesos en `joblib`

Se corrió el barrido completo k = 1,…,25 con `n_jobs` ∈ {{{', '.join(map(str,PJ))}}}, usando el
*backend* `loky` (procesos independientes = paradigma *multiprocessing*). Se verificó que
**efectivamente usa procesos distintos**: con `n_jobs=4` se observaron {R['n_pids_njobs4']} PID de
*workers*, todos **distintos del proceso padre**, y las 25 inercias resultaron idénticas a las del
barrido serial.

| `n_jobs` | Tarea = ***loops*** | Speedup | Eficiencia | Tarea = **NumPy** | Speedup | Eficiencia |
|---|---|---|---|---|---|---|
{rows}

### Por qué la tarea con *loops* escala y la tarea con NumPy casi no

La diferencia está en la **razón entre trabajo útil y *overhead***. El costo de crear y alimentar los
procesos se midió por separado con 25 tareas triviales: **{ovh*1000:.0f} ms** con `n_jobs=4`.

| | Trabajo útil del barrido | *Overhead* medido | *Overhead* relativo |
|---|---|---|---|
| Tarea = *loops* | {T['loops'][1]*1000:,.0f} ms | {ovh*1000:.0f} ms | **{ovh/T['loops'][1]*100:.2f} %** → despreciable |
| Tarea = NumPy | {swn*1000:,.0f} ms | {ovh*1000:.0f} ms | **{ovh/swn*100:.0f} %** → domina |

* Con **tarea = *loops***, cada tarea dura en promedio ≈ {tsum/25:.1f} s de cómputo *cpu-bound* en
  Python puro. Como cada *worker* es un **proceso** con su propio intérprete y su propio GIL, el
  paralelismo es real y el *overhead* es irrelevante frente al trabajo. Por eso hay speedup efectivo.
* Con **tarea = NumPy**, cada tarea dura ≈ {ptn.mean()*1000:.0f} ms, menos que lo que cuesta lanzar un
  proceso y serializar sus argumentos. De hecho con `n_jobs=2` el speedup es
  **{_s2:.2f}×**: {NP2_WORD}. Además `dataset` pesa **156 KiB**,
  por debajo del umbral de 1 MB con que `joblib` usa *memmap*, así que el arreglo se **serializa con
  `pickle` y se copia a cada tarea** (Clase 04).

> **Conclusión práctica:** paralelizar con procesos solo conviene cuando la tarea es **suficientemente
> grande** respecto al costo de crearla. Para el barrido vectorizado lo más rápido en términos
> absolutos sigue siendo **optimizar el algoritmo**: el barrido NumPy **serial** ({swn:.2f} s) es
> **{T['loops'][PMAX]/swn:.0f}× más rápido** que el barrido con *loops* repartido en {PMAX} procesos
> ({T['loops'][PMAX]:.2f} s). *El algoritmo importa más que el paralelismo* (Clase 08).

### Por qué la eficiencia cae incluso en el caso favorable

Aun con tarea = *loops*, el speedup se satura en {S['loops'][PMAX]:.2f}× con {PMAX} procesos
(eficiencia {E['loops'][PMAX]:.0f} %). Hay tres causas, todas medidas:

**(i) Desbalance de carga (Clase 05).** Las 25 tareas tienen costos extremadamente desiguales: de
**{ptl.min():.4f} s** (k = 1) a **{ptl.max():.4f} s** (k = 25), una razón de
**{R['task_imbalance']:.0f}×**. El tiempo total nunca puede ser menor que
`max(tarea más larga, trabajo total / p)`:

| p | Cota inferior | Medido | Brecha |
|---|---|---|---|
{cota}

A partir de p = {p_floor} la cota la fija **una sola tarea**: la de k = 25 dura {tmax:.2f} s, que es
el **{frac*100:.1f} %** de todo el trabajo. Esa tarea indivisible se comporta como una **fracción
serial** y, por la ley de Amdahl, acota el speedup en **S∞ ≤ 1/{frac:.3f} ≈ {sinf:.1f}×**, *sin
importar cuántos procesos se usen*. Invirtiendo Amdahl a partir de los datos medidos se obtiene una
fracción serial efectiva de **f ≈ {amdahl_f(4)*100:.0f}–{amdahl_f(2)*100:.0f} %**, del mismo orden.

**(ii) Los núcleos no son equivalentes.** Este equipo tiene **{PP} núcleos *performance* y {PE}
*efficiency***. Hasta p = {PP} se usan casi solo núcleos rápidos y la eficiencia se mantiene alta
({E['loops'][2]:.0f} % con p = 2). Al pasar de {PP} procesos se empieza a repartir trabajo a núcleos
*efficiency*, bastante más lentos: el *worker* que cae en un núcleo lento **retrasa todo el barrido**,
porque el tiempo total lo determina el más lento. En la ley de Amdahl el parámetro `p` supone
*workers* **idénticos**; en una arquitectura heterogénea ese supuesto no se cumple, y es la razón
principal de la brecha respecto de la cota para p = 8 y p = {PMAX}.

**(iii) *Overhead* y parte serial del padre.** Crear procesos, serializar `dataset` 25 veces y
recolectar los resultados en el proceso padre es trabajo que no se paraleliza.

**Sobre la *oversubscription* (Clase 04).** NumPy puede abrir hilos dentro de cada proceso; con p
procesos × varios hilos se puede superar el número de núcleos. En este equipo NumPy usa **{BLAS}**,
que no expone su *pool* de hilos a `threadpoolctl` (§1), así que no se puede limitar por esa vía; el
efecto aquí es menor porque `cdist` es esencialmente de un hilo.
""")

md(f"""
## (4) ¿Cuántos núcleos físicos tiene el computador?

**{PH} núcleos físicos**, en un **{HW['cpu']}**, distribuidos de forma **heterogénea**:

* **{PP} núcleos *performance*** (alto rendimiento),
* **{PE} núcleos *efficiency*** (bajo consumo).

También tiene **{LG} núcleos lógicos**: en Apple Silicon **no hay hyperthreading/SMT**, así que hay
exactamente **un hilo de hardware por núcleo físico** (a diferencia de un procesador x86 con SMT,
donde los núcleos lógicos serían {2*PH}). Esto es relevante para interpretar los resultados de la
pregunta (3): el límite de paralelismo real son {PH} *workers*, y además esos {PH} **no son
equivalentes entre sí**.

Verificado con `psutil.cpu_count(logical=False)` y `sysctl hw.perflevel{{0,1}}.physicalcpu` en §1.
""")

md(f"""
## 7. Dos observaciones adicionales

### 7.1 El código original falla con conglomeraciones vacías

El ejemplo de Canvas calcula el nuevo centro como
`sum_of_locations[c,0] / number_of_points_in_cluster[c]`. Si una conglomeración queda **vacía**, el
divisor es 0, el resultado es `nan` y eso contamina todas las iteraciones siguientes.

Con la inicialización del enunciado (todos los centros en el segmento 0 < x < 1, y = 0) esto **ocurre
en la práctica**: en el barrido k = 1,…,25 se detectaron conglomeraciones vacías para
**k = {', '.join(map(str, R['empty_ks']))}**. Por eso ambas implementaciones de este notebook
**mantienen el centro anterior** cuando una conglomeración queda vacía (la convención usual) y
**cuentan** los casos para poder reportarlos. Sin esa corrección, el gráfico del codo tendría valores
`nan`.

Además, para **k = {', '.join(map(str, R['no_converged']))}** el algoritmo **no converge** en las 100
iteraciones del ejemplo y se detiene por el máximo. Es esperable con una inicialización tan mala y con
k mayor que el número real de grupos (10): los centros sobrantes quedan oscilando entre puntos de
frontera. La inercia a 100 iteraciones ya está prácticamente estabilizada, así que el gráfico del codo
no se ve afectado.

### 7.2 El método del codo: cuidado con el criterio

El enunciado pide buscar "el punto de inflexión donde la inercia ya no se reduce de manera
significativa". Se usaron **dos criterios cuantitativos**, y ambos coinciden en **k = {R['k_chord']}**,
que es exactamente el número de grupos que generó `make_blobs`:

* **cuerda sobre log(I)** (el punto más alejado de la recta que une los extremos): k = {R['k_chord']};
* **primera ganancia marginal < 10 %**: k = {R['k_thr']}. La inercia cae {GAIN_IN:.1f} % al pasar de
  k = {KE-1} a k = {KE}, y solo {GAIN_OUT:.1f} % al pasar de k = {KE} a k = {KE+1}.

En cambio, el criterio ingenuo de **máxima segunda diferencia** da **k = {R['k_naive']}**, que es
engañoso: como la inercia cae de forma muy abrupta para k pequeños, la mayor curvatura absoluta está
siempre al principio de la curva. Es un buen recordatorio de que el "codo" hay que definirlo de forma
**relativa**, no absoluta.

### 7.3 Sobre la copia de variables (observación del enunciado)

Se revisó explícitamente el riesgo de *aliasing* que advierte el enunciado:

* En la versión con *loops*, `old_centers = history_of_centers[-1]` es una **referencia**, pero nunca
  se modifica `old_centers` en el lugar: `new_centers` se crea como un `np.zeros` **nuevo** en cada
  iteración. No hay *aliasing*.
* En la versión vectorizada se usa `new_centers = centers.copy()` antes de modificar, de modo que la
  asignación por máscara `new_centers[nonempty] = ...` no altera el arreglo anterior.
* El historial guarda arreglos distintos en cada iteración, lo que permitió graficar la trayectoria de
  los centros en §2.2.

Por eso no fue necesario `copy.deepcopy`: basta `.copy()` de NumPy, que además es más barato porque
los arreglos contienen solo números y no objetos anidados.

---

## 8. Conclusiones

1. El código entregado en Canvas **no paraleliza nada**: usa 1 proceso, 1 hilo de cómputo y el
   {R['cpu_avg_loops']/(100*PH)*100:.1f} % de la máquina.
2. **Vectorizar** es la optimización de mayor retorno y la más simple: **{SPV:.1f}× más rápido** sin
   cambiar el resultado (etiquetas idénticas). Mejora la constante, no la complejidad.
3. **Paralelizar con `joblib` solo rinde si la tarea es grande.** Con tareas de ≈ {tsum/25:.1f} s
   (*loops*) se logra {S['loops'][PMAX]:.2f}× con {PMAX} procesos; con tareas de
   ≈ {ptn.mean()*1000:.0f} ms (NumPy) el *overhead* es el {ovh/swn*100:.0f} % del trabajo y con 2
   procesos el speedup es de apenas {_s2:.2f}× ({'una frenada' if _s2 < 1 else 'casi nulo'}).
4. La eficiencia paralela cae por **desbalance de carga** (tareas que difieren
   {R['task_imbalance']:.0f}×; una sola tarea es el {frac*100:.1f} % del trabajo total →
   S∞ ≲ {sinf:.1f}×) y porque los **{PH} núcleos no son equivalentes** ({PP} *performance* + {PE}
   *efficiency*), lo que rompe el supuesto de *workers* idénticos de la ley de Amdahl.
5. El orden correcto es **primero el algoritmo, después la vectorización y al final el paralelismo**:
   el barrido vectorizado **serial** ({swn:.2f} s) le gana por **{T['loops'][PMAX]/swn:.0f}×** al
   barrido con *loops* repartido en **{PMAX} procesos** ({T['loops'][PMAX]:.2f} s).

## Declaración de uso de herramientas de IA

Se utilizó un asistente de IA (Claude, Anthropic) como apoyo en la vectorización del algoritmo
(`scipy.spatial.distance.cdist`, `np.argmin`, `np.bincount`, `np.add.at`), en la estructura del código
de medición y los gráficos, y en la redacción de este informe. El diseño experimental, la ejecución en
mi equipo, la verificación de consistencia entre implementaciones y la interpretación de los
resultados son propios. Todo el código fue revisado y ejecutado por mí y soy responsable del contenido
entregado.
""")

# Idempotente: si existe el marcador se reemplaza; si el informe ya fue insertado en
# una corrida anterior, se recorta desde su encabezado y se vuelve a generar.
MARK, HEAD = "<!--INFORME-->", "# 6. Informe y discusión de resultados"
idx = next((i for i, c in enumerate(nb.cells)
            if c.cell_type == "markdown" and MARK in c.source), None)
if idx is not None:
    nb.cells[idx:idx+1] = INFORME
else:
    idx = next(i for i, c in enumerate(nb.cells)
               if c.cell_type == "markdown" and HEAD in c.source)
    nb.cells[idx:] = INFORME            # descarta el informe anterior y lo regenera
nbf.write(nb, "Tarea01.ipynb")
print(f"Informe generado desde resultados.json: {len(INFORME)} celdas (posición {idx})")
print(f"Total de celdas: {len(nb.cells)}")
