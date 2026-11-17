# Clase 03 — Pipelining y rendimiento de procesadores

**IMT3870**, Prof. Ignacio Labarca. Fuente: `Presentaciones/clase03.pdf` (36 láminas), lunes 26 de
octubre.

**Agenda:** arquitecturas **secuenciales** de computadores — *¿cómo ejecuta una unidad de
procesamiento las instrucciones?*

**Motivación:** optimizar un código es más fácil cuando se entiende cómo funciona un computador. La
arquitectura del procesador impacta directamente al rendimiento de los códigos ejecutados en
clústeres paralelos.

**Repaso de la clase anterior:** Ley de Moore (el número de transistores aumentó sostenidamente, los
procesadores hacen operaciones cada vez más complejas, pero **la performance de un solo núcleo
eventualmente se estancó**), arquitectura de Von Neumann (stored-program + fetch/execute/store), flujo
de datos RAM → L3 → L2 → L1 → registros por el bus, y la jerarquía de memoria.

---

## 1. La pregunta de partida: ¿qué significa *peak performance*?

En la lista **TOP500**, **R_max** (medido) es **siempre menor** que **R_peak** (teórico). Ejemplo de
clase: **Aurora alcanza solo ~51 % de su R_peak**.

- ¿De dónde sale R_peak?
- ¿Por qué no se alcanza?

Para responder hay que mirar **cómo un procesador ejecuta instrucciones**.

---

## 2. Las cinco etapas de una instrucción

Una instrucción pasa por **cinco etapas**; cada etapa puede tomar varios ciclos:

1. **IF** — *instruction fetch*
2. **ID** — *instruction decode*
3. **MF** — *memory access / memory fetch*
4. **EX** — *execution*
5. **WB** — *write-back*

Es un **modelo más avanzado** construido sobre la arquitectura de Von Neumann: el número de etapas
por instrucción es mayor que el fetch–execute–store de tres pasos.

Recordatorios:
- La **velocidad de reloj** (velocidad del procesador) es el número de **ciclos por segundo**. Es uno
  de los puntos que **se estancó** en el tiempo; hoy ronda los **3 GHz**.
- El dispositivo que realiza un FLOP es la **unidad de punto flotante (FPU)** y es parte de la CPU.

---

## 3. Pipelining (paralelismo a nivel de instrucción)

Analogía de clase: la **línea de ensamblaje**. Es el ejemplo canónico de **instruction level
parallelism (ILP)**.

Con ℓ = 5 etapas y 5 instrucciones, cada etapa trabaja sobre una instrucción **distinta** al mismo
tiempo:

```
        C1  C2  C3  C4  C5  C6  C7  C8  C9
I1      IF  ID  MF  EX  WB
I2          IF  ID  MF  EX  WB
I3              IF  ID  MF  EX  WB
I4                  IF  ID  MF  EX  WB
I5                      IF  ID  MF  EX  WB
```

### 3.1 Rendimiento **sin** pipelining

Ejecutar n instrucciones en un procesador de ℓ etapas, cada etapa toma **τ** segundos. Cada
instrucción **espera** a que termine la anterior:

```
t(n) = n · ℓ · τ
```

En cada momento **solo una** de las ℓ etapas está ocupada. La tasa de resultados es

```
n / t(n) = 1 / (ℓτ)      (constante, aunque n crezca)
```

### 3.2 Rendimiento **con** pipelining

La primera instrucción tarda **ℓτ** en **llenar el pipeline**; luego **termina una instrucción por
ciclo**:

```
t(n) = (ℓ + n − 1) τ
```

Tasa de resultados:

```
n / ((ℓ + n − 1) τ)  →  1/τ   cuando n → ∞
```

**Asintóticamente la tasa es ℓ veces mejor** que sin pipelining. *(Este es el resultado central de la
clase.)*

---

## 4. Procesadores escalares y superescalares

**Procesador escalar:** arquitectura que emite **como máximo una instrucción por ciclo** de reloj,
aunque disponga de recursos ociosos.

**Procesador superescalar:** arquitectura capaz de **emitir y ejecutar varias instrucciones por
ciclo** de reloj:
- utiliza **múltiples unidades funcionales en paralelo**;
- **analiza dependencias** para evitar conflictos.

Características de los superescalares:
- Explotan el **paralelismo a nivel de instrucciones**.
- Completan **más de una instrucción por ciclo** → su **IPC > 1**.
- El **throughput** es la tasa de instrucciones terminadas.
- Hoy **casi toda CPU** de computador personal o celular es superescalar.
- En la práctica el **IPC suele estar entre 1 y 4**.

---

## 5. De dónde sale R_peak

Asintóticamente, las CPU **canalizadas (pipelined)** pueden alcanzar una tasa de resultado **óptima**:
un resultado por ciclo de reloj **en cada unidad funcional**.

- Una **FPU con pipeline produce un FLOP por ciclo**; un núcleo moderno tiene **varias FPUs**, cada
  una operando sobre **varios datos a la vez**.
- A 3 GHz, una **sola FPU escalar** entrega **3 GFLOP/s**; el peak performance de un **núcleo
  moderno** es de **decenas de GFLOP/s**.

**Cálculo de R_peak** (desde las especificaciones del fabricante):

```
R_peak = velocidad de reloj × FLOP por ciclo de cada núcleo × número de núcleos
```

El **rendimiento sostenido R_max** es **medido** por el benchmark (TOP500 publica ambos,
`www.top500.org`).

---

## 6. Medidas de rendimiento y sus límites

- **FLOP**: operación de punto flotante en **precisión doble (8 bytes)**.
- **FLOP/s**: FLOP por segundo. Ejemplo de clase: **LineShine ≈ 2,2 exaFLOP/s**.
- Contar FLOP es **simple** y sigue siendo la medida **más usada**.
- Pero **acceder a memoria suele ser mucho más lento que calcular**.
- **Intensidad aritmética** = FLOP por byte transferido desde memoria → indica si un programa es
  **cpu-bound** o **memory-bound**.

### Limitaciones del conteo de FLOP
- **No considera transferencias de datos.**
- **Ignora latencias y dependencias.**
- **Excluye operaciones no flotantes** (p. ej. conversiones de tipos).
- **Depende del modelo de conteo** (p. ej. si se usa **FMA**, *Fused-Multiply-Add*).
- **No refleja el rendimiento real** — pueden existir otras limitaciones, como memoria.

---

## 7. Cuándo falla el pipeline

Observaciones (supuestos del modelo):
- La **longitud del pipeline depende de la arquitectura** de la máquina.
- El pipelining **requiere que los datos y las instrucciones sean independientes**; verificar las
  dependencias **es costoso**.
- Se **asume que los datos están en los registros** de la CPU → se **ignora la latencia** de traerlos
  de memoria o caché.

### 7.1 Burbujas por dependencia de datos

Si `I2` necesita el resultado de `I1`, el pipeline **se detiene**:

```
I1: LOAD R1        IF  ID  MF  EX  WB
I2: ADD R2, R1         IF  ID  —   MF  EX  WB     ← burbuja (stall)
I3                         IF  —   ID  MF  EX  WB
I4                             —   IF  ID  MF  EX  WB
```

- Una **burbuja (stall)** **se propaga** a todas las instrucciones siguientes.
- El **compilador puede reordenar instrucciones** para evitar dependencias.

---

## 8. Latency hiding

Técnicas para que el procesador **no quede ocioso** durante la latencia:

**Out-of-Order Execution** — el procesador ejecuta **instrucciones independientes** mientras espera
datos, **respetando las dependencias**. Ejemplo de clase:

```c
for (int i = 0; i < N; i++) {
    sum  += a[i];
    prod *= b[i];
    div   = c[i] / d[i];
}
```
Las tres operaciones son **independientes**: mientras la división de la iteración `i` está en curso,
el procesador **adelanta** la suma y la multiplicación de la iteración `i + 1`.

**Prefetching** — el hardware (o el compilador) **anticipa accesos futuros** y solicita los datos por
adelantado. La ejecución fuera de orden **no** oculta la latencia de memoria (~160 ciclos); la
solución es **traer los datos antes de que se necesiten**:
- **Hardware**: detecta **strides constantes** y precarga automáticamente. **Falla con acceso
  irregular.**
- **Software**: el programador emite **prefetch explícitos**. Útil cuando el hardware no detecta el
  patrón.
- **El prefetch excesivo contamina la caché** con datos que no se usarán.

**Multithreading (SMT / HyperThreading)** — cuando un hilo espera por memoria, **otro hilo usa las
unidades de ejecución**. (*SMT: Simultaneous MultiThreading.*)

> Idealmente: **latencia oculta ≈ trabajo útil durante la espera**.

### 8.1 Prefetching en librerías de Python
- **NumPy**: los **arreglos contiguos** permiten precargar datos en caché.
- **scikit-learn**: `pre_dispatch` envía tareas por adelantado.
- **PyTorch**: `DataLoader` carga **lotes** por adelantado.
- **TensorFlow**: `Dataset.prefetch` prepara lotes por adelantado.

---

## 9. Relevancia práctica

- El **compilador y el hardware** del procesador normalmente manejan el **paralelismo de nivel de
  instrucción** (no es algo que el programador escriba a mano).
- Realizar **la misma instrucción muchas veces sobre datos independientes** es beneficioso para el
  rendimiento paralelo.
- **Python puro (sin librerías) no aprovecha esta arquitectura.**
- Librerías como **NumPy** ejecutan las operaciones en **código compilado (vectorización)**, que **sí**
  aprovecha el pipelining.

---

## Resumen de la clase
- Paralelismo a **nivel de instrucciones** → **pipelining**.
- Medidas de rendimiento → **peak performance** vs. **benchmark performance**.

**Próxima clase:** ¿cómo programar distintos procesos en Python?
