# Clase 01 — Introducción a la Computación de Alto Rendimiento

**IMT3870**, Prof. Ignacio Labarca. Fuente: `Presentaciones/clase01.pdf` (39 láminas).
Agenda: programa del curso + introducción a la computación de alto rendimiento.

---

## 1. Qué es HPC

> **El HPC se trata del uso eficiente de los recursos computacionales disponibles.**

La **eficiencia** es un balance entre dos cosas en tensión:

- la **precisión** de los resultados numéricos,
- la **huella** en los recursos computacionales (tiempo, memoria, energía).

Subir precisión cuesta recursos (doble precisión = 8 byte por número vs. 4 en simple); bajar la
huella suele costar precisión. HPC es administrar ese trade-off, no "hacer todo lo más exacto
posible".

**Computación en paralelo:** *paralelismo* es el **uso simultáneo de distintos dispositivos de
cómputo**.

---

## 2. Breve historia del cómputo

### Los primeros computadores fueron humanos
Personas contratadas para realizar cálculos numéricos repetitivos **a mano**. Trabajaban **en
grupos, dividiendo problemas complejos en tareas simples** — es decir, ya era cómputo paralelo con
descomposición de dominio. Usados en contextos militares, científicos y de ingeniería (foto de NACA
Dryden, California, ~1949; ver la película *Hidden Figures*, 2016).

### El pronóstico del clima: Richardson (1922)
*Weather Prediction by Numerical Process*, Lewis Fry Richardson:

- **64.000 computadores humanos** en una sala esférica, **cada uno a cargo de una región de la
  atmósfera** (descomposición espacial del dominio).
- Un **director al centro** coordinaba el ritmo (sincronización / scheduler).
- **Meta:** predecir el clima más rápido de lo que evoluciona — el criterio de "tiempo real" que
  sigue definiendo hoy el cómputo científico.
- Su propio intento manual (1916): **6 semanas para predecir 6 horas**, con errores.

Es el ejemplo conceptual central de la clase: el paralelismo masivo con comunicación y sincronización
precede por décadas al hardware que lo hace viable.

### Computadores electrónicos: ENIAC (1946)
*Electronic Numerical Integrator and Computer*:

| Característica | Valor |
|---|---|
| Elementos de cómputo | **17.468 tubos de vacío** |
| Fiabilidad | los tubos fallaban con frecuencia, **varios por día** en promedio |
| Consumo | ~**150 kW** |
| Peso | ~**27 toneladas** |
| Rendimiento | ~**5.000 operaciones por segundo** |

### Computadores personales y uso cotidiano
Apple I kit computer (1976) → el cómputo deja el laboratorio y se vuelve cotidiano.

### Supercomputadores
El **IBM Roadrunner** logró cómputo a nivel de **petaflops en 2008**.

---

## 3. Métricas: FLOP, FLOPS, Byte, Bit

| Término | Definición |
|---|---|
| **FLOP** | *Floating Point Operation* en **precisión doble (8 byte)** |
| **FLOPS** (o FLOP/s) | FLOP **por segundo** |
| **Byte** | tamaño de los datos. Precisión **doble: 8 byte**; **simple: 4 byte** |
| **Bit** | unidad básica. **1 Byte = 8 Bit** |

### Formato de punto flotante de doble precisión (IEEE 754, 64 bit)

```
 bit 63   bit 62 .............. bit 52   bit 51 ......................... bit 0
+------+--------------------------------+---------------------------------------+
| sign |      exponent (11 bit)         |          fraction (52 bit)            |
+------+--------------------------------+---------------------------------------+
```

1 (signo) + 11 (exponente) + 52 (fracción) = **64 bit = 8 byte**.

Las dos preguntas que la clase deja planteadas y que estructuran el curso:

1. ¿Cuántas operaciones matemáticas simples podemos resolver **por segundo**?
2. ¿Con cuántos **decimales de precisión**?

Son la misma tensión precisión ↔ recursos: la respuesta a (1) depende de la respuesta a (2).

### Prefijos útiles para ejercicios

| Prefijo | Factor | Ejemplo |
|---|---|---|
| mega (M) | 10⁶ | MFLOPS |
| giga (G) | 10⁹ | GHz, GB/s |
| tera (T) | 10¹² | teraflops |
| peta (P) | 10¹⁵ | Roadrunner, 2008 |
| exa (E) | 10¹⁸ | Frontier, 2022 |

---

## 4. TOP500 y el estado del arte

La lista **TOP500** (<https://top500.org/>) clasifica los supercomputadores. El rendimiento se mide
con un **benchmark basado en un algoritmo de la librería Linpack** (álgebra lineal densa — es decir,
mide esencialmente un caso cpu-bound favorable, lo que conviene recordar al interpretar el ranking).

**El más rápido del mundo según la clase — LineShine (2026, Shenzhen, China): 2,2 exaflops**

| Característica | Valor |
|---|---|
| Cores CPU | 13.790.000 |
| GPUs | **ninguna (solo CPU)** |
| Procesador | LX2 (Arm), 304 cores |
| Potencia | 42 MW |

Antecesores citados: **El Capitán** (2024, EE.UU., 1,8 exaflops) y **Frontier** (2022), el **primer
sistema en superar 1 exaflop**.

---

## 5. La Ley de Moore

> "El número de transistores en un chip se duplicará cada dos años aproximadamente."
> — Gordon Moore, co-fundador de Intel, **1975**.

Mayor poder para operaciones más complejas. **Limitantes observadas en el tiempo:**

- el **tamaño** de los chips,
- la **temperatura** del chip.

Consecuencia (la bisagra del curso): como no se puede seguir subiendo frecuencia ni densidad sin
límite, el rendimiento adicional viene de **más núcleos**, no de núcleos más rápidos. El paralelismo
deja de ser una especialización y pasa a ser la vía por defecto.

---

## 6. Arquitectura de procesadores

### Un procesador antiguo: un solo núcleo
Los primeros procesadores personales tenían un **único núcleo**:

```
            RAM del Sistema
                   |
            Bus Frontal (FSB)
                   |
   +---------------------------------+
   |        Intel Pentium            |
   |          Caché L2               |
   |   +-------------------------+   |
   |   |     Núcleo único        |   |
   |   |  Unidad de Ejecución    |   |
   |   |     ALU      FPU        |   |
   |   |  Caché L1 instrucciones |   |
   |   |  Caché L1 datos         |   |
   |   +-------------------------+   |
   +---------------------------------+
```

### Dentro del núcleo: ALU y FPU
La **Unidad de Ejecución** dentro de un núcleo tiene dos componentes principales:

- **ALU** (*Arithmetic Logic Unit*): operaciones con **enteros** y operaciones **lógicas**
  (comparaciones, desplazamientos de bits, …).
- **FPU** (*Floating Point Unit*): operaciones aritméticas en **punto flotante**. **Es la unidad de
  cómputo relevante en HPC**, porque el rendimiento se mide en FLOP/s.

Cada núcleo dispone además de cachés **L1** (separadas para instrucciones y datos) y **L2**, que
almacenan datos cercanos al procesador para **reducir la latencia**.

### Un procesador moderno (multicore)
Un computador actual tiene uno o más **procesadores (chips)**; cada procesador contiene **varios
núcleos (cores) independientes**:

```
                    Memoria RAM (compartida)
   +--------------------------------------------------------+
   |                 Procesador (chip)                      |
   |              Caché compartida (L3)                     |
   | +----------+ +----------+ +----------+ +----------+    |
   | | Core 0   | | Core 1   | | Core 2   | | Core 3   |    |
   | | Unid.cómp| | Unid.cómp| | Unid.cómp| | Unid.cómp|    |
   | | L1/L2    | | L1/L2    | | L1/L2    | | L1/L2    |    |
   | +----------+ +----------+ +----------+ +----------+    |
   +--------------------------------------------------------+
```

- Cada núcleo **ejecuta instrucciones de forma independiente**.
- Los núcleos **comparten la RAM** y una caché de último nivel.
- Las tareas de un programa **se pueden repartir** entre los núcleos para ejecutarse en paralelo.
- Cifras típicas: **escritorio actual 4–16 cores**; **nodo de supercomputador 32–128 cores**.

### CPU + GPU: arquitectura con coprocesador

```
   +---------------------------+            +---------------------------+
   |           CPU             |            |    GPU (Coprocesador)     |
   |  Core 0  Core 1           |   PCIe     |   Caché L2 compartida     |
   |  Core 2  Core 3           | <=======>  |                           |
   |       Caché L3            |  copia de  |        VRAM (GPU)         |
   +---------------------------+   datos    +---------------------------+
             |
       RAM del Sistema
```

Punto clave: la GPU tiene **su propia memoria (VRAM)** y los datos deben **copiarse por el bus
PCIe**. Esa copia es un costo explícito que puede dominar el tiempo total si el cómputo en GPU es
pequeño.

### Apple M1/M2: Sistema en un Chip (SoC)

```
   Apple M1/M2 — System on a Chip (SoC)
   +------------------------------------------------------------+
   |      Memoria Unificada (compartida CPU + GPU)              |
   |  CPU: P-cores (rendimiento) P P P P                        |
   |       E-cores (eficiencia)  E E E E                        |
   |  GPU                                   Neural Engine       |
   +------------------------------------------------------------+
```

La **memoria unificada** elimina la copia explícita CPU↔GPU del esquema PCIe. Núcleos
**heterogéneos**: P-cores de rendimiento y E-cores de eficiencia.

---

## 7. Futuras tendencias

**Equipamiento:**
- computación paralela masiva,
- sistemas **heterogéneos**,
- máquinas ***purpose built*** (diseñadas para un propósito).

**Ciencia interdisciplinaria:** matemáticas aplicadas + ciencia de la computación + ciencias
aplicadas (ingeniería, física, economía, sociología, etc).

---

## 8. Observaciones prácticas

**No es tan simple hacer uso de supercomputadores:**
- hay que **pagar por tiempo de cómputo a través de concursos**,
- la seguridad es muy restrictiva.

**El progreso es rápido:**
- la vanguardia de hace pocos años es común hoy,
- **todos los nuevos computadores tienen múltiples núcleos**.

**En este curso no se usan supercomputadores ni la nube.** Todas las tareas se pueden hacer en un
**computador personal o en Google Colab**. Los principios, algoritmos y librerías que se aprenden
**sí son relevantes** para el uso de supercomputadores.

---

## 9. Por qué importa el HPC (las dos razones de la clase)

- **Razón 1 — la arquitectura paralela es el futuro:** hay una tendencia a usar cada vez más
  procesadores en el mismo dispositivo.
- **Razón 2 — la arquitectura paralela ya está disponible:** se trata de usar **todo** el poder
  disponible en los dispositivos que ya tenemos.

---

## 10. Tarea administrativa de la clase

En **Canvas**, pestaña **Evaluaciones**, contestar la **Encuesta 0**.
