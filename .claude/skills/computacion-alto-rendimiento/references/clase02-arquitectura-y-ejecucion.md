# Clase 02 — Arquitectura de computadores y modelo de ejecución

**IMT3870**, Prof. Ignacio Labarca. Fuente: `Presentaciones/clase02.pdf` (35 láminas).

**Agenda:** ¿Cómo corre un computador un cálculo? (¿cómo ejecuta las instrucciones?, ¿cómo transfiere
los datos?) ¿Cómo correr múltiples procesos?

**Motivación:** para **diseñar algoritmos eficientes** es importante entender la arquitectura de un
procesador. Recordar que un **clúster o supercomputador es un conjunto de muchos procesadores
'normales'** — entender uno es entender la base de todos.

> **Advertencia metodológica de la clase:** se estudian *modelos básicos* del funcionamiento de un
> computador. **Un modelo es siempre una simplificación de la realidad** que nos permite entender *lo
> suficiente* para un propósito específico (mejorar la eficiencia). Al usar un modelo, nombra sus
> supuestos.

---

## 1. La arquitectura de Von Neumann

Antiguamente los computadores se programaban **a mano** (recableando). Von Neumann introduce dos
principios:

**Principio 1 — programa almacenado (*stored-program architecture*):**
- **las instrucciones se manejan como datos**;
- esto permite el diseño de **compiladores y editores** (un programa puede leer y escribir otro
  programa).

**Principio 2 — las instrucciones se manejan como la secuencia:**
1. **fetch** (buscar, traer),
2. **execute** (ejecutar, calcular),
3. **store** (almacenar, guardar).

Vocabulario asociado:
- La parte del procesador que ejecuta instrucciones se llama **CPU** (*Central Processing Unit*).
- Los datos están guardados en la **memoria** del procesador: **RAM** (*Random Access Memory*).
- El **almacenamiento** (*storage*) es **distinto** y es parte del **disco duro**. En este curso
  "memoria" significa RAM, no disco.

---

## 2. Velocidad de reloj

El procesador opera sincronizado por un **reloj** (*clock*):

- **Frecuencia f**: número de **ciclos por segundo**. Se mide en **GHz**.
- **Período de ciclo τ = 1/f**: duración de un ciclo. Se mide en **ns**.

**Ejemplo:** un procesador a **3,5 GHz** tiene **τ ≈ 0,286 ns** por ciclo.

Cada operación tarda un número fijo de ciclos. La **velocidad real** depende de:

- la **frecuencia** del reloj,
- el número de **instrucciones completadas por ciclo (IPC)**.

**Máximo teórico:**

```
FLOPS ~ f × #FPUs
```

Es una cota superior: supone que todas las FPUs están ocupadas en cada ciclo, es decir, que los datos
llegan siempre a tiempo — justo el supuesto que la sección siguiente derriba.

---

## 3. Movimiento de datos: RAM → procesador

El procesador **no accede directamente a la RAM**: los datos viajan por un **bus de memoria** a
través de los niveles de la jerarquía.

```
   RAM <---> L3 <---> L2 <---> L1 <---> Registros
                    (bus)
```

El rendimiento de ese viaje se describe con **dos métricas**:

- **Latencia**: ¿cuánto tarda en llegar el **primer byte**?
- **Ancho de banda**: ¿a qué **tasa** llegan los bytes siguientes?

### Buses
Los cables que mueven datos a través de los niveles de memoria y hacia la CPU se llaman **"buses"**.

- **Frecuencia**: número de ciclos de bus por segundo — **alrededor de 1 GHz**. (Recordar que la
  velocidad de reloj de la CPU es alrededor de **3 GHz**: el bus corre ~3× más lento que la CPU.)
- **Capacidad**: número de **bits por ciclo de bus** — el **ancho del bus** es típicamente de **64 o
  128 bits**.
- **Ancho de banda** (*bandwidth*): número de **bytes por segundo**.

### Latencia (α)
Tiempo desde que se **solicita** un dato hasta que llega el primero. Se mide en **ciclos** o en
**nanosegundos**.

**Ejemplo típico (procesador a 3,5 GHz, 1 ciclo ≈ 0,3 ns):**

| Nivel | Latencia (ciclos) | Latencia (ns) |
|---|---|---|
| L1 cache | ~4 | ~1 |
| L2 cache | ~12 | ~3 |
| L3 cache | ~40 | ~11 |
| RAM | ~200 | ~60 |

**Durante la latencia el procesador queda bloqueado** (*memory stall*). Ir a RAM cuesta ~200 ciclos
en los que no se calcula nada: ahí está el costo real de un acceso mal planificado.

### Ancho de banda (BW)
Tasa a la que llegan los datos **después** de la latencia inicial. Se mide en **GB/s** o en
**Byte/ciclo**. Depende del bus de memoria:

- velocidad del bus (*bus speed*),
- ancho del bus (bits por transferencia),
- número de **canales** (dual-channel, quad-channel).

### Modelo de tiempo de transferencia

El tiempo total de transferir **n bytes** es:

```
T(n) = α + β n
```

- **α**: latencia (tiempo de inicio),
- **β**: inverso del ancho de banda, **β = 1/BW** (tiempo por byte).

**Lectura del modelo:** para n pequeño domina α (conviene agrupar accesos en transferencias grandes);
para n grande domina βn (conviene reducir el volumen total de datos movidos).

### Concurrencia

El **máximo nivel de concurrencia** se obtiene cuando **todo el ancho de banda está en uso**:

```
   RAM  ==[ d1 d2 d3 d4 d5 d6 d7 d8 ]==>  CPU
        BW bytes/s          tiempo de viaje: α
   Concurrencia = BW × α   (bytes simultáneamente en tránsito)
```

**Ejemplo:** si **BW = 50 GB/s** y **α = 60 ns**, entonces hay
**BW × α = 3.000 bytes** en tránsito simultáneamente.

Interpretación: para saturar el canal el programa debe tener ~3.000 bytes de peticiones *en vuelo* al
mismo tiempo. Si pide un dato, espera, y recién entonces pide el siguiente, usa una fracción mínima
del ancho de banda disponible.

### El muro de la memoria

La **transferencia de datos es a menudo (mucho) más lenta que la ejecución de operaciones de punto
flotante**. ¿Cómo acelerar el flujo de datos entre memoria y CPU? → **considerando las limitaciones
del hardware del procesador** (y en consecuencia diseñando algoritmos que reutilicen datos en lugar
de volver a buscarlos).

---

## 4. cpu-bound vs. memory-bound

**La velocidad del procesador no siempre es el cuello de botella.**

- Algoritmos **cpu-bound**: limitados por la **velocidad de procesamiento**. La memoria entrega datos
  a tiempo, pero el procesador no puede calcular más rápido.
- Algoritmos **memory-bound**: limitados por la **velocidad de acceso a memoria**. El procesador
  queda **ocioso esperando datos**.

¿Cómo distinguirlos? Mediante la **Intensidad Aritmética**.

### Intensidad Aritmética (AI)

Mide cuánto cómputo se realiza por cada byte transferido:

```
AI = N° de operaciones (FLOP) / Bytes transferidos desde memoria
```

- **AI alta**: muchos FLOP por byte → el programa es **cpu-bound**.
- **AI baja**: pocos FLOP por byte → el programa es **memory-bound**.

### Ejemplo cpu-bound: GEMM

Multiplicación de matrices **C ← A · B + C**, con A, B, C ∈ ℝ^{n×n}.

| | |
|---|---|
| **Cómputo** | **2n³** operaciones (cada elemento de C requiere n multiplicaciones y n sumas) |
| **Datos** | **3 × 8n²** bytes (3 matrices de n × n *doubles*) |

```
AI = 2n³ / 24n² = n/12   FLOP/Byte
```

Con **n = 1000**: **AI ≈ 83 FLOP/Byte** → es **cpu-bound**.

> **Supuestos del cálculo** (explícitos en la lámina): que cada dato se carga **una sola vez** (las
> matrices caben en caché) y que el procesador ejecuta las operaciones de punto flotante **sin cuello
> de botella interno**.

Observación: la AI **crece con n** — a mayor tamaño, más favorable al cómputo. Por eso GEMM es el
núcleo del benchmark Linpack y el caso ideal del hardware.

### Ejemplo memory-bound: DAXPY

Operación vectorial **y ← a · x + y**, con x, y ∈ ℝⁿ, a escalar.

| | |
|---|---|
| **Cómputo** | **2n** operaciones (una multiplicación y una suma por elemento) |
| **Datos** | **3 × 8n** bytes (leer x, leer y, escribir y) |

```
AI = 2n / 24n = 1/12 ≈ 0,083   FLOP/Byte
```

**AI no depende de n y es muy baja** → es **memory-bound**. Agrandar el problema no ayuda: cada
elemento se usa para una sola multiplicación-suma y se descarta.

### Cómo usar esto en un ejercicio
1. Cuenta los **FLOP** del algoritmo.
2. Cuenta los **bytes** que hay que traer de memoria (y escribir), × 8 por *double*.
3. Divide → AI.
4. Compara con el hardware: la AI de equilibrio de una máquina es ≈ (FLOPS pico)/(BW). Si la AI del
   algoritmo está por debajo, es memory-bound y optimizar aritmética no sirve: hay que reducir
   tráfico de datos o aumentar reutilización.

---

## 5. Jerarquía de memoria

Existen diferentes tipos de dispositivos de memoria:
- de **gran capacidad** de almacenamiento pero **lentos** para leer y escribir,
- de **lectura y escritura rápidas** pero **pequeña** capacidad.

Y existen diferentes **buses** (latencia, ancho de banda). **Idea:** usar una **jerarquía de niveles**
y almacenar los datos de **uso frecuente** en los dispositivos de lectura rápida. Niveles: memoria
principal (**RAM**), **cachés** y **registros**.

### Tabla de la jerarquía (cifras de la clase)

| Nivel | Latencia | Tamaño |
|---|---|---|
| **Registros** | ~1 ciclo | ~1 KB |
| **L1** | ~4 ciclos | ~32 KB |
| **L2** | ~8 ciclos | ~256 KB |
| **L3** | ~28 ciclos | ~8–32 MB |
| **RAM** | ~160 ciclos | ~16–128 GB |

Hacia abajo: **menor latencia**. Hacia arriba: **mayor tamaño**.

> **El objetivo es maximizar la reutilización de datos en los niveles cercanos al procesador.** Esta
> es la frase operativa del curso para diseñar algoritmos (blocking/tiling, recorrer arrays en el
> orden en que están en memoria, etc.).

### Memoria principal (RAM)
- El nivel **más alto** de la jerarquía.
- Con 'memoria' normalmente se entiende la **RAM**, no el almacenamiento en disco duro.
- **Gran** cantidad de almacenamiento (p. ej. 16 GB).
- Relativamente **barata** de producir.
- **Volátil**: necesita fuente de alimentación.

### Registros
- Memoria de nivel **más bajo**.
- Es **parte de la CPU**, por lo que la **latencia es despreciable**.
- Hay espacio para **solo 16 a 32 números de punto flotante**.

### Caché
- Memoria de nivel **intermedio**, normalmente **tres niveles (L1, L2, L3)**.
- **Todos los datos deben pasar por los niveles de caché.**
- Cada nivel **guarda una copia**, como un *checkpoint*.
- Si necesitas **nuevamente** el dato, **no hace falta ir a buscarlo a la RAM** — de ahí el valor de
  la reutilización.

### Caché y múltiples núcleos

```
   Un núcleo                        Dos núcleos
   +---------------+                +---------------+  +---------------+
   | Núcleo        |                | Núcleo        |  | Núcleo        |
   | Registros     |                | Registros     |  | Registros     |
   | Caché L1      |                | Caché L1      |  | Caché L1      |
   +---------------+                +---------------+--+---------------+
   | Caché L2      |                |      Caché L2 (compartida)      |
   +---------------+                +---------------------------------+
   | Memoria (RAM) |                |          Memoria (RAM)          |
   +---------------+                +---------------------------------+
```

Cada núcleo tiene su **L1 propia** y comparte niveles superiores. Si dos núcleos tienen copias del
mismo dato en sus cachés privadas y uno lo modifica, ¿cómo asegurar que **las copias son correctas**?
→ **Coherencia** (de caché). Es el costo oculto del multithreading sobre datos compartidos.

---

## 6. Procesos e hilos

**Procesos**
- un **programa** que ejecuta tareas a través de la **creación de threads**;
- cada proceso tiene un identificador (**PID**: *process ID*).

**Threads (hilos, subprocesos)**
- un **flujo secuencial de instrucciones de bajo nivel**;
- son parte de un **único proceso**.

**Paralelismo:** múltiples procesos en paralelo.

### Tres modelos a no confundir

| Modelo | Qué hace | Dataspace |
|---|---|---|
| **Multiprocessing** | un programa que crea **otros programas** | cada programa tiene **su propio** dataspace |
| **Multithreading** | un programa que crea **threads** que corren simultáneamente | **todos los threads comparten** el mismo dataspace |
| **Hyperthreading** | cada **núcleo físico** se presenta como **dos núcleos lógicos** (virtuales) | los dos threads **comparten las unidades de ejecución** del núcleo |

Consecuencias prácticas: multithreading necesita menos memoria y comunica gratis (dataspace
compartido) pero expone a condiciones de carrera y al problema de coherencia; multiprocessing aísla
(más robusto) a costa de duplicar datos y comunicar explícitamente. Hyperthreading **no** duplica
capacidad de cómputo — solo ayuda a llenar huecos (p. ej. *memory stalls*).

---

## 7. Lenguajes de programación

**Lenguajes interpretados (*scripted*)**
- el código se ejecuta **línea por línea**,
- instrucciones de **alto nivel**,
- **Python, R, MATLAB**, etc.

**Lenguajes compilados**
- el código es convertido en un **programa ejecutable**,
- **dos pasos**: compilar y ejecutar,
- **Fortran, C, C++, Java, Rust**, etc.

### Python y el GIL

Python tiene un bloqueo: el **GIL** (*Global Interpreter Lock*).

- **solo un thread a la vez** puede ejecutar código Python;
- **impide el paralelismo entre threads que ejecutan código Python**;
- **permite el paralelismo en rutinas externas** — por ejemplo, **NumPy utiliza LAPACK y BLAS**;
- desde **Python 3.13** existe una versión **sin GIL** (*free-threaded*), con **soporte oficial desde
  3.14**.

Python tiene además una variedad de librerías para programación paralela, **cada una con sus alcances
y limitaciones**.

**Regla práctica para las tareas:** si el trabajo pesado ocurre dentro de NumPy (álgebra lineal,
operaciones vectorizadas), ya hay paralelismo disponible vía BLAS/LAPACK y el GIL no estorba. Si el
trabajo pesado es un bucle en Python puro, multithreading **no** acelera: hay que vectorizar o usar
**multiprocessing**.

---

## 8. Estructura y ejecución de un programa

### Estructura

```
   programa.py
     ├── tarea 1 ──> función a ──> instrucciones
     │              función b
     └── tarea 2 ──> función c
```

### Ejecución línea por línea + multithreading

```
   programa.py
     x = leer_datos("datos.csv")
     y = 2 * x          <-- misma instrucción, para cada dato
     z = suma(y)
     print(z)

   inicio ──> 2·x1  2·x2   (thread 1)
          ──> 2·x3  2·x4   (thread 2)      multithreading
```

El caso natural del multithreading: **la misma instrucción aplicada a cada dato** (paralelismo de
datos), dentro de un mismo programa y dataspace.

### Múltiples procesos

```
   datos_1.csv ──> programa.py ──> proceso 1
   datos_2.csv ──> programa.py ──> proceso 2      multiprocessing
   datos_3.csv ──> programa.py ──> proceso 3
```

El caso natural del multiprocessing: **el mismo programa sobre datasets independientes**, sin
necesidad de compartir memoria.

---

## 9. Resumen de la clase

**¿Cómo se ejecutan instrucciones en un computador?**
- arquitectura de **Von Neumann**:
  - las instrucciones se manejan como datos,
  - secuencias de **fetch, execute, store**;
- **procesos e hilos**.

**¿Cómo fluyen los datos en un computador?**
- **jerarquía de memoria** con niveles de caché (y el modelo T(n) = α + βn para el costo del viaje).

**Próxima semana:** ¿cómo correr **instrucciones** en paralelo? ¿cómo correr **procesos** en paralelo?
