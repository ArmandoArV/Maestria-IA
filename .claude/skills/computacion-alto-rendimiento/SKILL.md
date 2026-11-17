---
name: computacion-alto-rendimiento
description: >
  Expert knowledge base for the IMT3870 Computación de Alto Rendimiento course (Magíster en IA, PUC
  Chile, Instituto de Ingeniería Matemática y Computacional, Prof. Ignacio Labarca). Covers
  high-performance computing from the ground up: qué es HPC y el balance precisión/recursos,
  paralelismo, historia del cómputo (Richardson, ENIAC, supercomputadores), métricas (FLOP, FLOPS,
  Byte, Bit, punto flotante IEEE de doble precisión), la lista TOP500 y el benchmark Linpack, la Ley
  de Moore y sus límites físicos, arquitectura de procesadores (multicore, ALU y FPU, cachés L1/L2/L3,
  CPU+GPU por PCIe, SoC Apple M1/M2); arquitectura de Von Neumann (stored-program, ciclo
  fetch–execute–store), velocidad de reloj (frecuencia f, período τ = 1/f, IPC, FLOPS ≈ f × #FPUs),
  movimiento de datos (buses, latencia α, ancho de banda β = 1/BW, modelo T(n) = α + βn, concurrencia
  = BW × α, memory stall, el muro de la memoria), algoritmos cpu-bound vs. memory-bound e Intensidad
  Aritmética (AI = FLOP / bytes, GEMM con AI = n/12, DAXPY con AI = 1/12), jerarquía de memoria
  (registros, L1, L2, L3, RAM con latencias y tamaños); pipelining y paralelismo a nivel de
  instrucción (las cinco etapas IF/ID/MF/EX/WB, t(n) = nℓτ sin pipeline vs. t(n) = (ℓ+n−1)τ con
  pipeline, procesadores escalares y superescalares, IPC entre 1 y 4, peak performance R_peak vs.
  rendimiento sostenido R_max, limitaciones del conteo de FLOP, FMA, burbujas y stalls por dependencia
  de datos, latency hiding con out-of-order execution, prefetching y SMT); múltiples procesos en
  Python (stack y heap, multiprocessing vs. multithreading vs. hyperthreading, el GIL, la librería
  multiprocessing, joblib con Parallel/delayed y los backends loky/multiprocessing/threading, fork vs.
  spawn con copy-on-write, serialización y pickle, oversubscription); eficiencia paralela (worker,
  speedup S_p = T1/Tp, eficiencia E_p = S_p/p, speedup superlineal, overhead paralelo T0 = pTp − T1,
  cost-optimal, balance de carga, Ley de Amdahl S_p ≤ 1/(f + (1−f)/p) y S_∞ ≤ 1/f, Amdahl con
  comunicación, reducción paralela con sumas parciales y p ≈ √n, Ley de Gustafson S_p = p − (p−1)f,
  escalabilidad fuerte y débil); arquitectura paralela de memoria (memoria compartida vs. distribuida,
  MPI, direcciones de memoria y punteros, row-major vs. column-major, cache hit y cache miss
  compulsory/capacity/conflict, mapeo directo/asociativo/n-asociativo, políticas FIFO y LRU, línea de
  caché de 64–128 bytes, localidad temporal y espacial, vectorización, coherencia de caché y el
  protocolo MESI); tipos de paralelismo y granularidad (paralelismo de datos, funcional y de tareas,
  problemas perfectamente paralelos o embarrassingly parallel, grano fino vs. grueso, modelo
  fork-join, datos privados vs. compartidos, thread safety, condiciones de carrera, locks y secciones
  críticas, OpenMP/Pthreads/MPI/MPI4Py, el módulo threading de Python, concurrencia vs. paralelismo);
  y Numba (compilación JIT, LLVM y LLVM IR, decoradores @jit y @njit, paralelización con
  parallel=True y prange, parallel_diagnostics, paralelización automática de operaciones vectorizadas,
  K-means acelerado, y los límites de Numba con dict/pandas/scikit-learn). Use for any IMT3870
  question — controles semanales, control final, tareas de programación en Python, slides, programa
  del curso — or to reason about performance, bottlenecks and parallelization of numerical code. Also
  trigger on computación de alto rendimiento, HPC, high performance computing, cómputo paralelo,
  programación paralela, paralelismo, FLOP, FLOPS, petaflop, exaflop, TOP500, Linpack,
  supercomputador, Ley de Moore, núcleo, core, multicore, ALU, FPU, punto flotante, doble precisión,
  arquitectura de Von Neumann, fetch execute store, velocidad de reloj, frecuencia, ciclo, IPC, bus,
  latencia, ancho de banda, bandwidth, memory stall, muro de la memoria, memory wall, cpu-bound,
  memory-bound, intensidad aritmética, arithmetic intensity, GEMM, DAXPY, BLAS, LAPACK, MKL, PETSc,
  jerarquía de memoria, caché, cache, L1, L2, L3, registros, RAM, línea de caché, cache line, cache
  hit, cache miss, mapeo de caché, asociatividad, LRU, FIFO, coherencia de caché, MESI, localidad
  temporal, localidad espacial, row-major, column-major, vectorización, pipelining, pipeline,
  burbuja, stall, superescalar, escalar, peak performance, R_peak, R_max, FMA, out-of-order
  execution, prefetching, latency hiding, SMT, proceso, hilo, thread, PID, stack, heap,
  multiprocessing, multithreading, hyperthreading, GIL, global interpreter lock, free-threaded,
  joblib, Parallel, delayed, n_jobs, loky, fork, spawn, copy-on-write, serialización, pickle,
  oversubscription, worker, speedup, eficiencia paralela, overhead paralelo, cost-optimal, balance de
  carga, fracción serial, Ley de Amdahl, Amdahl, Ley de Gustafson, Gustafson, escalabilidad fuerte,
  escalabilidad débil, strong scaling, weak scaling, reducción paralela, sumas parciales, memoria
  compartida, memoria distribuida, MPI, MPI4Py, OpenMP, Pthreads, pragma, paralelismo de datos,
  paralelismo funcional, paralelismo de tareas, granularidad, grano fino, grano grueso, embarrassingly
  parallel, perfectamente paralelo, fork-join, thread safe, condición de carrera, race condition,
  lock, sección crítica, Numba, JIT, just-in-time, LLVM, njit, prange, parallel_diagnostics,
  parameter sweep, hyperparameter tuning, método del codo, k-means, NumPy, Colab, Eijkhout,
  theartofhpc, or the course code (IMT3870).
  Respond in Spanish when the user writes in Spanish.
---

# Computación de Alto Rendimiento (IMT3870)

Knowledge base for **IMT3870 – Computación de Alto Rendimiento**, Pontificia Universidad Católica de
Chile, Instituto de Ingeniería Matemática y Computacional (Facultad de Matemáticas & Escuela de
Ingeniería). Profesor **Ignacio Labarca** (`ignacio.labarca@uc.cl`) — Ingeniero Civil Matemático y
Computacional UC, Doctorado en Matemáticas Aplicadas (ETH Zurich), postdoctorados en Universität
Innsbruck y en el IMC UC.

> *"El HPC se trata del uso eficiente de los recursos computacionales disponibles."* La eficiencia es
> un **balance** entre la precisión de los resultados numéricos y la huella en los recursos
> computacionales.

## Cómo usar esta skill

1. **Lee el archivo de `references/` correspondiente** antes de responder más allá del resumen de
   abajo. SKILL.md es el mapa; las referencias tienen las fórmulas, las cifras y los ejemplos.
2. **Responde en español.** El curso es en español.
3. **Razona siempre desde el cuello de botella.** Es el hilo conductor del curso: antes de optimizar,
   pregunta si el algoritmo es *cpu-bound* o *memory-bound*. La herramienta para decidirlo es la
   **Intensidad Aritmética** (FLOP por byte transferido). Casi toda recomendación de optimización se
   justifica por reducir transferencia de datos o aumentar reutilización en cachés, no por "escribir
   código más rápido".
4. **Un modelo es una simplificación deliberada.** El curso lo dice explícitamente: los modelos de
   arquitectura (Von Neumann, jerarquía de memoria, T(n) = α + βn) se usan porque permiten entender
   *lo suficiente* para mejorar la eficiencia, no porque describan el hardware real al detalle. Al
   responder, nombra los supuestos del modelo que estás usando.
5. **Python, no C/Fortran.** Las tareas son de programación en Python (NumPy, Matplotlib, Jupyter),
   ejecutables en un computador personal o en Google Colab. El curso **no** usa supercomputadores ni
   la nube, aunque los principios sí aplican a ellos.
6. **Cuidado con el GIL** al proponer paralelismo en Python: multithreading no acelera código Python
   puro, sí acelera rutinas externas (NumPy → BLAS/LAPACK). Para código Python puro, usa
   **multiprocessing** (`joblib`) o **compila** (`Numba`). Ver el árbol de decisión abajo.
7. **El algoritmo importa más que la implementación.** Lo dice la clase 08 explícitamente: pasar de
   O(N²) a O(N) gana más que paralelizar el O(N²). Antes de proponer paralelismo, revisa si el
   algoritmo se puede reformular (p. ej. Σᵢⱼ xᵢxⱼ = (Σᵢ xᵢ)²).
8. **Al estimar speedup, nombra el supuesto de tamaño.** Si el tamaño del problema es **fijo** →
   Amdahl (speedup acotado por 1/f, escalabilidad fuerte). Si el tamaño **crece con p** → Gustafson
   (speedup O(p), escalabilidad débil). Son la *misma* medición leída con supuestos distintos.
9. **Mide T₁ con el mejor código secuencial disponible**, si no el speedup sale inflado. Y con Numba,
   **descarta la primera llamada** al cronometrar (incluye la compilación JIT).
10. **Integridad académica:** rige el **Código de Honor UC**. Los controles son individuales y de
    libro abierto; las tareas son de entrega individual y **no se comparte código** entre compañeros.
    El curso **permite usar aplicaciones basadas en IA** en las tareas, pero la evaluación pone
    énfasis en la **discusión de los resultados** y el alumno es totalmente responsable de lo que
    entrega. Usa esta skill para explicar, resolver ejemplos análogos y revisar razonamiento; no para
    entregar respuestas de un control.

## Mapa del curso

| Clase | Tema | Reference |
|-------|------|-----------|
| 01 | Introducción: programa del curso + fundamentos de HPC | `references/clase01-introduccion-hpc.md` |
| 02 | Arquitectura de computadores y modelo de ejecución | `references/clase02-arquitectura-y-ejecucion.md` |
| 03 | Pipelining y rendimiento de procesadores (ILP, superescalares, R_peak vs. R_max) | `references/clase03-pipelining.md` |
| 04 | Múltiples procesos: `multiprocessing`, `joblib`, fork/spawn, serialización | `references/clase04-multiples-procesos.md` |
| 05 | Eficiencia paralela: speedup, Amdahl, Gustafson, escalabilidad | `references/clase05-eficiencia-paralela.md` |
| 06 | Arquitectura paralela: memoria, mapeo de caché, localidad, coherencia (MESI) | `references/clase06-arquitectura-paralela.md` |
| 07 | Paralelismo y multithreading: tipos, granularidad, `threading`, GIL, OpenMP | `references/clase07-paralelismo-multithreading.md` |
| 08 | Numba en Python: JIT, LLVM, `@njit`, `prange`, paralelización automática | `references/clase08-numba.md` |
| 09 | *(anunciada)* Comunicación y paso de mensajes | — |

> Material disponible hasta la fecha: `Presentaciones/clase01.pdf` … `clase08.pdf`. Las clases se
> dictan **en pares** (dos presentaciones por sesión del lunes): 01–02, 03–04 (26-oct), 05–06
> (02-nov), 07–08 (09-nov). La **clase 09 (comunicación y paso de mensajes, MPI)** está anunciada pero
> aún no está en el repositorio — dilo si alguien la pide.

## El programa en breve

- **Formato híbrido.** Clases los lunes en sala C403, 18:50–20:00 y 20:15–21:20 h. Plataforma
  **Canvas** (programa, anuncios, material, evaluaciones).
- **Evaluación y ponderación:**
  - **8 controles semanales** — preguntas de alternativas, pestaña *Tareas* en Canvas, nota en escala
    lineal del puntaje total → **20 %** del total.
  - **4 tareas** de programación en Python, entrega por Canvas → **15 % cada una** (60 % en total).
  - **1 control final** → **20 %**.
- **Libro guía:** Victor Eijkhout, *The Science of Computing*, University of Texas, 3ª ed., 2022 —
  disponible en <https://theartofhpc.com>.
- **Conocimiento previo:** álgebra lineal (vectores, matrices) y programación en Python (for-loops,
  if-statements, arrays, funciones, NumPy, Matplotlib, Jupyter). Recomendación de entorno: Google
  Colab o Anaconda.
- **Objetivos:** aprender los fundamentos de la computación de alto rendimiento y los fundamentos de
  la programación paralela en Python.
- **Contenido en tres preguntas:** arquitectura de computadores (*¿cómo funciona un computador?*),
  algoritmos paralelos (*¿cómo diseñar un algoritmo eficiente?*) y programación paralela (*¿cómo
  programar un algoritmo paralelo?*). Combinación de teoría (matemática e ingeniería computacional) y
  práctica (Python).
- **Consultas:** correo `ignacio.labarca@uc.cl`, Canvas, u horario de clase.

## Resumen de conceptos

### Qué es HPC
**Computación de alto rendimiento** = uso eficiente de los recursos computacionales disponibles,
balanceando precisión numérica y huella de recursos. **Paralelismo** = uso simultáneo de distintos
dispositivos de cómputo.

### Métricas
**FLOP** (operación de punto flotante en doble precisión, 8 byte), **FLOPS** = FLOP/s, **Byte**
(doble precisión 8 byte, simple 4 byte), **Bit** (1 Byte = 8 Bit). Doble precisión IEEE: 1 bit de
signo + 11 bit de exponente + 52 bit de fracción = 64 bit. La **FPU** es la unidad relevante en HPC
porque el rendimiento se mide en FLOP/s.

### Ley de Moore y el giro al paralelismo
"El número de transistores en un chip se duplicará cada dos años aproximadamente" (Gordon Moore,
co-fundador de Intel, 1975). Limitantes observadas: el **tamaño** de los chips y la **temperatura**
del chip. De ahí la respuesta de la industria: más núcleos en lugar de más frecuencia → el
paralelismo pasa de ser opcional a obligatorio.

### Modelo de ejecución
**Von Neumann**: (1) las instrucciones se manejan como datos — programa almacenado
(*stored-program*), lo que habilita compiladores y editores; (2) las instrucciones se ejecutan en la
secuencia **fetch → execute → store**. La **CPU** ejecuta; los datos viven en la **RAM**; el
*storage* (disco duro) es otra cosa.

### Movimiento de datos
Los datos viajan RAM → L3 → L2 → L1 → registros por **buses**. Dos métricas: **latencia** α (cuánto
tarda el primer byte) y **ancho de banda** BW (a qué tasa llegan los siguientes). Transferencia de n
bytes: **T(n) = α + βn** con β = 1/BW. **Concurrencia = BW × α** bytes en tránsito simultáneo.
Durante la latencia el procesador se bloquea (**memory stall**) → el **muro de la memoria**: mover
datos suele ser mucho más lento que calcular.

### cpu-bound vs. memory-bound
**Intensidad Aritmética** AI = FLOP / bytes transferidos desde memoria. AI alta → cpu-bound; AI baja
→ memory-bound (procesador ocioso esperando datos). Ejemplos canónicos del curso: **GEMM**
(C ← A·B + C) con AI = n/12 ≈ 83 FLOP/Byte para n = 1000 → cpu-bound; **DAXPY** (y ← a·x + y) con
AI = 1/12 ≈ 0,083 FLOP/Byte, independiente de n → memory-bound.

### Jerarquía de memoria
Registros (~1 ciclo, ~1 KB) → L1 (~4 ciclos, ~32 KB) → L2 (~8 ciclos, ~256 KB) → L3 (~28 ciclos,
~8–32 MB) → RAM (~160 ciclos, ~16–128 GB). Más cerca del procesador = más rápido y más pequeño. El
objetivo del diseño de algoritmos es **maximizar la reutilización de datos en los niveles cercanos**.
Con múltiples núcleos cada core tiene L1 propia y comparte niveles superiores → problema de
**coherencia** de caché.

### Procesos e hilos
**Proceso**: programa que ejecuta tareas creando threads; tiene un **PID**. **Thread**: flujo
secuencial de instrucciones de bajo nivel dentro de un proceso. **Multiprocessing**: un programa crea
otros programas, cada uno con su propio *dataspace*. **Multithreading**: threads simultáneos que
**comparten** el dataspace. **Hyperthreading**: cada núcleo físico se presenta como dos núcleos
lógicos que comparten las unidades de ejecución.

### Python y el GIL
Lenguajes **interpretados** (Python, R, MATLAB) ejecutan línea por línea con instrucciones de alto
nivel; **compilados** (Fortran, C, C++, Java, Rust) convierten el código en un ejecutable (compilar +
ejecutar). El **GIL** (Global Interpreter Lock) permite que solo un thread a la vez ejecute código
Python → impide el paralelismo entre threads de código Python, pero **permite** paralelismo en
rutinas externas (NumPy usa **LAPACK** y **BLAS**). Desde Python 3.13 existe una versión sin GIL
(*free-threaded*), con soporte oficial desde 3.14.

### Pipelining y peak performance (Clase 03)
Una instrucción pasa por **cinco etapas**: IF (*instruction fetch*) → ID (*decode*) → MF (*memory
fetch*) → EX (*execute*) → WB (*write-back*). **Sin pipelining**, n instrucciones en ℓ etapas de τ
segundos toman **t(n) = nℓτ** (tasa constante 1/(ℓτ), una sola etapa ocupada a la vez). **Con
pipelining**, la primera instrucción llena el pipeline en ℓτ y luego termina una por ciclo:
**t(n) = (ℓ + n − 1)τ**, con tasa → **1/τ** — **asintóticamente ℓ veces mejor**. Un procesador
**escalar** emite ≤1 instrucción por ciclo; un **superescalar** emite y ejecuta varias usando múltiples
unidades funcionales en paralelo → **IPC > 1** (en la práctica **entre 1 y 4**). De ahí **R_peak =
reloj × FLOP por ciclo por núcleo × núcleos** (teórico, desde las especificaciones) vs. **R_max**
(sostenido, medido por el benchmark). Nunca se alcanza R_peak: **burbujas (*stalls*)** por dependencia
de datos se propagan a todas las instrucciones siguientes. **Latency hiding**: *out-of-order
execution* (ejecutar instrucciones independientes mientras se espera), *prefetching* (hardware detecta
*strides* constantes; falla con acceso irregular, y el exceso contamina la caché) y *multithreading*
SMT/HyperThreading. **Limitaciones del conteo de FLOP:** ignora transferencias, latencias y
dependencias, excluye operaciones no flotantes, y depende del modelo de conteo (p. ej. **FMA**).

### Múltiples procesos en Python (Clase 04)
Un **proceso** tiene su propio espacio de memoria asignado por el SO: **heap** (compartido por el
proceso completo) y **stack** (temporal, por hilo). **Un proceso no puede acceder directamente a la
memoria de otro** → la comunicación requiere mecanismos explícitos. Cada **core ejecuta un hilo a la
vez**; con más hilos que cores el SO **los intercala**. En Python: **`multiprocessing`** crea distintos
programas de Python (hay **overhead** de crear/terminar procesos = el costo de paralelizar, sin
comunicación automática); **`joblib`** es la alternativa del curso — backends **`loky`** (por defecto,
seguro en Windows y Jupyter), **`multiprocessing`** y **`threading`** (útil si la carga es I/O-bound o
el código libera el GIL). Patrón: **`Parallel(n_jobs=4)(delayed(f)(x) for x in items)`** —
`delayed(f)(x)` guarda la llamada sin ejecutarla y `Parallel` devuelve los resultados **en el mismo
orden**. **`fork`** copia el padre con *copy-on-write* (rápido, pero puede heredar estado no deseado y
no existe en todos los SO) vs. **`spawn`** que arranca limpio (más lento, portable, **default en
joblib**). Como Python es interpretado, los objetos deben **serializarse** (**`pickle`**) para viajar
entre procesos: enviar solo datos serializables (listas, dicts, `ndarray`, números) y **crear los
recursos abiertos dentro de cada proceso** (conexiones, sockets, archivos, contextos GPU). Cuidado con
la **oversubscription** (más hilos activos que núcleos): NumPy ya usa varios hilos vía BLAS, y joblib
reparte **núcleos / n_jobs** hilos por proceso.

### Eficiencia paralela: Amdahl y Gustafson (Clase 05)
Un **worker** es la unidad de ejecución paralela (proceso, hilo o nodo; en joblib **p = `n_jobs`**).
**Speedup S_p = T₁/T_p**; **eficiencia E_p = S_p/p = T₁/(p·T_p)** = fracción del tiempo en que cada
worker hace trabajo útil. En general **S_p ≤ p**, salvo el **speedup superlineal** (con p workers cada
subproblema cabe en caché). **Overhead paralelo T₀ = p·T_p − T₁ ≥ 0**; un algoritmo es
**cost-optimal** si p·T_p = O(T₁). Lo que limita el speedup: la **parte serial** (impone un techo), la
**comunicación/sincronización** (crece con p) y el **desbalance de carga** (el tiempo total lo fija el
worker más lento). **Ley de Amdahl** (tamaño **fijo**, fracción serial f): **S_p ≤ 1/(f + (1−f)/p)**,
y **S_∞ ≤ 1/f** — con f = 5 %, S_1000 ≈ 19,6: **nunca supera 20×**. Con comunicación,
T_p = T₁(f + (1−f)/p) + T_com y como T_com crece con p **existe un número óptimo de procesadores**.
Ejemplo canónico de la **reducción paralela**: cada worker suma n/p elementos y uno acumula los p
parciales → T₁ = n, **T_p = n/p + (p − 1)**, E_p = 1/(1 + p(p−1)/n) → **eficiencia constante cuando
p ≈ √n**. **Ley de Gustafson** (el tamaño **crece con p**): **S_p = p − (p − 1)f** → S_p = O(p),
E_p = O(1); con f = 5 % y p = 100 da **≈ 95** frente a los **≈ 16,8** de Amdahl. Amdahl = **escalabilidad
fuerte** (N fijo, p → ∞ ⇒ E_p ≈ const); Gustafson = **escalabilidad débil** (N/p fijo). En la práctica
se mide **E_débil = T₁(N/p) / T_p(N) ≈ 1**.

### Arquitectura paralela de memoria (Clase 06)
**Memoria compartida** (procesadores **multi-core**): mismo *dataspace*, todos los núcleos acceden a
toda la RAM, el compilador se hace cargo de buscar los datos. **Memoria distribuida** (**clústers**,
nube, servidores): acceso explícito por paso de mensajes (**MPI**) — **la mejor arquitectura para
escalar**, pero **más difícil de programar**. Los compiladores ubican los elementos de un array
**consecutivamente** — en Python **solo los arrays de NumPy, no las listas**; las matrices se
linealizan en **row-major** (C, Python) o **column-major** (Fortran, MATLAB). **Cache miss** de tres
tipos: **compulsory** (primera referencia), **capacity** (se borró por tamaño) y **conflict** (uso
múltiple de la misma ubicación). **Mapeo directo** (ubicación módulo el tamaño: rápido — módulo 2ⁿ son
los últimos n bits — pero con riesgo de *conflict*), **asociativo** (cualquier ubicación; requiere
tablas de búsqueda → overhead) y **n-asociativo** (combina ambos: flexibilidad y velocidad), con
políticas de reemplazo **FIFO** o **LRU** y **asociatividad típica de hasta 8** — por eso **la
localidad sigue importando**. El transporte entre niveles es siempre por **línea de caché** de **64 o
128 bytes (8 o 16 floats)**: cada acceso trae gratis a los vecinos contiguos. Dos localidades:
**temporal** (lo usado recientemente aún está en caché → *localizar el uso de datos en pocas líneas de
código*) y **espacial** (el mapeo directo preserva secuencias → *operar sobre elementos vecinos*).
Recomendaciones en Python: **arrays de NumPy en lugar de listas**, **recorrer con paso 1**,
**reutilizar datos mientras siguen en caché** y **dividir el problema en bloques que quepan en caché**.
La **vectorización** (NumPy arrays + funciones de NumPy en vez de for-loops) gana las cuatro cosas a la
vez: pipelining, reutilización de caché, localidad y múltiples hilos. **Coherencia**: garantía de que
las copias en caché son consistentes con la memoria principal; se rompe cuando un núcleo modifica su
copia privada y otro lee un valor obsoleto. El protocolo **MESI** da a cada línea uno de cuatro
estados: **M**odificada (cambiada aquí, única copia), **E**xclusiva (igual a memoria, única copia),
**S**hared/compartida (igual a memoria, en varios cachés), **I**nválida (ya no sirve).

### Tipos de paralelismo, granularidad e hilos (Clase 07)
Tres tipos: **paralelismo de datos** (= grano fino; la *misma* instrucción sobre muchos elementos —
suma de vectores, paralelismo perfecto), **paralelismo funcional o de instrucción** (instrucciones
*distintas* sobre datos independientes — ILP/pipelining) y **paralelismo de tareas** (subprogramas
independientes — *parameter tuning* en ML). Un problema es **perfectamente paralelo (*embarrassingly
parallel*)** si se divide en tareas independientes sin comunicación (Monte Carlo, procesar muchas
imágenes, búsqueda de hiperparámetros): escala casi linealmente y sus límites son el **balance de
carga** y el **overhead**. **Granularidad** = número y tamaño de las tareas: **grano fino** = muchas
tareas pequeñas (mayor potencial, **mayor overhead de sincronización**); **grano grueso** = pocas
tareas grandes (menor overhead, pero **puede dejar recursos ociosos**). La óptima **depende del
problema, la arquitectura y el costo de comunicación**. Modelo **fork-join**: un hilo principal crea
hilos (*fork*) que se sincronizan al terminar (*join*). Datos creados **dentro** de un hilo son
**privados** (mueren con el hilo); creados **fuera**, **compartidos**. Un código es **thread safe** si
da el mismo resultado secuencial y en paralelo; una **condición de carrera** ocurre cuando el resultado
depende de cuál hilo termine primero — **el peligro es escribir en datos compartidos** y se evita con
**secciones críticas o locks**. Librerías canónicas: **OpenMP** y **Pthreads** (multithreading, memoria
compartida) y **MPI** (procesos que se comunican, memoria distribuida); en Python existe **MPI4Py**, y
**lo más cercano a OpenMP es Numba**. En Python el módulo **`threading`** crea hilos del SO con
`start()`/`join()`, pero el **GIL** (necesario porque CPython mantiene un estado global —conteo de
referencias, memoria— que dos hilos podrían corromper) permite **solo un hilo ejecutando bytecode a la
vez**: los hilos de Python dan **concurrencia, no paralelismo**. Las dos mediciones de la clase lo
muestran: con 8 tareas de **espera** (`time.sleep`) el speedup es **lineal** (8 hilos → 8,0×, el GIL se
libera durante la espera), y con 8 tareas de **cómputo** en Python puro **no hay speedup** (8 hilos →
**0,9×**, más lento que secuencial).

### Numba (Clase 08)
**JIT (*just-in-time*)**: compilar y ejecutar justo cuando se necesita. **Numba** hace compilación JIT
de código Python/NumPy usando **LLVM** como motor: traduce a **LLVM IR** y LLVM compila a código
máquina nativo aplicando vectorización, *inlining* y eliminación de código muerto — por eso su
rendimiento **puede ser cercano al de C o Fortran**. Instalación: **`conda install numba`** (pip no
siempre es estable). **Compila en la primera llamada y reutiliza esa compilación** → **precaución al
medir tiempos**. Se usa como **decorador**: desde Numba 0.59 **`@jit` y `@njit` son equivalentes**
(ambos compilan sin el intérprete; si Numba no puede compilar, **da error**). Para paralelizar:
**`@njit(parallel=True)`** usa el paradigma de **multithreading** — Numba **busca oportunidades**, y si
no encuentra ninguna **corre secuencialmente**; **intenta resolver las condiciones de carrera pero no
garantiza consistencia**. Los ciclos se paralelizan a mano con **`prange()`**. Benchmark de la clase
(suma de cuadrados, N = 10⁷): Python **3,07 s** → `@njit` **0,0116 s** → `@njit`+`prange`
**0,00508 s**. `parallel=True` **también paraleliza operaciones vectorizadas** (`A[i,:] += b`,
`np.zeros(n)`, `np.sum(x)`), y **cada operación crea una región paralela** que cuesta microsegundos —
de ahí que poner `prange` en el loop externo sea mejor que dejar que Numba paralelice el slice en cada
iteración; **`f.parallel_diagnostics(level=1)`** muestra qué se paralelizó. En el caso de estudio de
**K-means**, el paso de **asignación** va con `prange` (independiente por punto) pero el de
**actualización** queda en `range` (escribe en posiciones compartidas); el speedup real queda lejos del
ideal por **4 núcleos físicos** (los 8 threads son hyperthreading) y porque **la actualización y la
convergencia son secuenciales** (Amdahl). **Límites:** acelera bien for-loops e if-else, pero es
**difícil de debuggear**, **solo interpreta un subconjunto de Python**, maneja principalmente `int`,
`float` y `array` (**no `dict`**), cubre gran parte de **NumPy y SciPy** pero **no `pandas`,
`scikit-learn` ni `tensorflow`**.

## Árbol de decisión: ¿cómo acelero este código Python?

1. **¿El algoritmo es el correcto?** Revisa la complejidad antes que todo — *el algoritmo importa más
   que la implementación* (Clase 08).
2. **¿Es cpu-bound o memory-bound?** Calcula la **Intensidad Aritmética**. Si es memory-bound, no
   sirve agregar FLOPS: hay que **reducir transferencia** y **aumentar reutilización de caché**.
3. **¿Se puede vectorizar?** NumPy arrays + funciones de NumPy en lugar de for-loops. Es la primera
   opción: gana pipelining, caché, localidad y múltiples hilos de una vez, y evita el GIL.
4. **¿Son tareas independientes** (barrido de parámetros, muchos archivos, Monte Carlo)? →
   **`joblib`** con `Parallel`/`delayed` (*embarrassingly parallel*, grano grueso).
5. **¿Es un for-loop numérico que NumPy no cubre?** → **Numba** `@njit`, y luego `prange` si las
   iteraciones son independientes.
6. **¿Es I/O-bound** (red, disco)? → **`threading`** sirve: el GIL se libera durante la espera.
7. **Nunca:** `threading` para cómputo en Python puro — con el GIL puede salir **más lento** que
   secuencial.
8. **Al medir:** T₁ con el mejor código secuencial, descarta la primera llamada en Numba, y vigila la
   **oversubscription** (NumPy ya usa hilos vía BLAS).

## Referencias bibliográficas

- Victor Eijkhout, *The Science of Computing*, 3ª ed., University of Texas, 2022 —
  <https://theartofhpc.com> (libro guía).
- Lista TOP500 de supercomputadores — <https://top500.org/> (rendimiento medido con un benchmark
  basado en un algoritmo de la librería **Linpack**).
- Lewis Fry Richardson, *Weather Prediction by Numerical Process*, 1922 (el "cómputo paralelo humano").
- Película *Hidden Figures* (2016), referida en clase sobre los computadores humanos.
- **joblib** — <https://joblib.readthedocs.io> (librería de paralelización usada en el curso).
- **Numba** — compilación JIT de Python sobre LLVM (`conda install numba`).
- **OpenMP**, **MPI** / **MPI4Py** — referidas en clase 07; MPI queda para la clase de comunicación.
