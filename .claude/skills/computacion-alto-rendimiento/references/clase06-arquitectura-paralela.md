# Clase 06 — Arquitectura paralela: memoria, caché, localidad y coherencia

**IMT3870**, Prof. Ignacio Labarca. Fuente: `Presentaciones/clase06.pdf` (37 láminas), lunes 2 de
noviembre.

**Agenda:** ¿cómo acceden los distintos núcleos a la memoria?

**Repaso:** arquitectura de Von Neumann (instrucciones como datos; fetch → execute → store). El
**acceso a la memoria suele ser lento**, muchas veces **más lento que ejecutar la instrucción**; de ahí
la jerarquía de memoria con niveles de caché para **acelerar el fetch**.

```
RAM        ~160 ciclos   ~16–128 GB    ↑ mayor tamaño
L3          ~28 ciclos    ~8–32 MB
L2           ~8 ciclos     ~256 KB
L1           ~4 ciclos      ~32 KB
Registros    ~1 ciclo        ~1 KB     ↓ menor latencia
```

---

## 1. Datos: procesos vs. hilos

Una **diferencia clave** entre procesos e hilos:
- **Distintos procesos nunca comparten los mismos datos.**
- **Distintos hilos pueden acceder a los datos del mismo proceso.**

Por este motivo, las librerías basadas en el modelo **multiprocessing no tienen variables
compartidas**: los **workers en joblib pueden tener una copia local** de una variable, pero **nunca
comparten una variable**.

---

## 2. Tipos de memoria

- **La memoria es algo físico** en el hardware — se pueden instalar distintos **módulos de memoria**.
- Un **espacio de datos (*dataspace*)** es algo de **software**, una **configuración**: una parte de
  la memoria **reservada para un proceso**; distintas **particiones** de la memoria.

**La principal distinción** entre tipos de memoria es **memoria compartida** vs. **memoria
distribuida**. Para esta distinción, "memoria" se refiere al **espacio de datos virtual**, **no
necesariamente a la memoria física**. La memoria refiere al **conjunto de memoria que una unidad de
cómputo puede acceder directamente** (normalmente el **núcleo**, pero podría ser **procesador** o
**nodo**).

### 2.1 Memoria compartida — los procesadores **multi-core**
- Memoria **lógicamente compartida**: el **mismo dataspace** (podría ser **físicamente separada**).
- Los procesos e hilos **pueden acceder a toda la memoria compartida**.
  - Los procesos **no comparten exactamente la misma memoria al mismo tiempo**.
  - Se **reserva una parte de memoria para cada proceso o hilo**.
- **Los compiladores se hacen cargo de buscar los datos.**

### 2.2 Memoria distribuida — los **clústers**
- Memoria **lógicamente distribuida**: suele estar **físicamente separada**, aunque también pueden ser
  **distintas particiones en la misma memoria física**.
- Los procesadores **solo pueden acceder a los datos en otra ubicación pasando información de forma
  explícita** → **MPI (*Message Passing Interface*)**.
- **La mejor arquitectura para escalar redes.**
- **Es más difícil de programar.**

---

## 3. Asignación de memoria

En la memoria, cada unidad de datos tiene una **dirección asignada (*memory address*)**:
- Esta dirección **es un número**.
- Se puede **modelar la memoria como una secuencia unidimensional** de datos.
  > El orden unidimensional de la memoria es un **modelo adecuado, no la realidad física**.
- Se puede acceder a esta dirección en **lenguajes de bajo nivel** → se llaman **punteros (*pointers*)**
  en C++.

**Los compiladores ubican los elementos de un array consecutivamente en la memoria.**
- **Python: solo para NumPy arrays, no es así para listas.** *(Razón de fondo por la que NumPy es
  rápido.)*

Las **matrices multidimensionales** requieren una **numeración unidimensional**:
- **row-major ordering** → **C, Python**.
- **column-major ordering** → **Fortran, MATLAB**.

---

## 4. El caché

Un **cache hit** (acierto) ocurre cuando los datos solicitados **se encuentran en el caché**.

Un **cache miss** (fallo) ocurre cuando la unidad de procesamiento necesita datos que **no están en el
caché**. Tres tipos:
- **Compulsory** — **primera vez** de referencia.
- **Capacity** — el registro **se borró** del caché debido al **tamaño limitado** del caché.
- **Conflict** — **uso múltiple de la misma ubicación** del caché.

### 4.1 El problema del mapeo
¿Cómo hacer uso eficiente del caché? Específicamente, **¿cómo almacenar los datos que vienen de la
RAM en el caché?** La **RAM es de alrededor de 16 GB**, mientras que **L3 es de ~4 MB**.

### 4.2 Mapeo directo
**Mapeo directo del caché:** la ubicación se determina por la **ubicación en el nivel superior, módulo
el tamaño de la memoria**.
- Es **rápido de calcular**: un número **módulo 2ⁿ** es **usar los últimos n bits**.
- Hay **riesgo de muchos cache misses de tipo *conflict***.

```
RAM:   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
             ↓ (mod 4)
Caché: 0  1  2  3
```

### 4.3 Mapeo asociativo y n-asociativo
**Mapeo asociativo:** los datos **se pueden transferir a cada ubicación**. Requiere **tablas de
búsqueda** y por lo tanto **overhead**.

**Mapeo n-asociativo:** **combina** mapeo directo y asociativo.
- Los datos se pueden transferir a **n ubicaciones**.
- **Tiene flexibilidad y velocidad.**

Los mapeos asociativos requieren una **política de reemplazo**:
- **FIFO** (*first in – first out*): primero en entrar, primero en salir.
- **LRU** (*least recently used*): menos utilizado recientemente.

**Típicamente asociatividad de hasta 8.** Esta asociatividad es **pequeña en comparación con el tamaño
de caché** → **la localidad de datos sigue siendo importante**.

---

## 5. Línea de caché

El flujo de datos entre niveles de caché **es siempre con una línea de caché (*cache line*)**:
- Una línea de caché tiene normalmente **64 o 128 bytes** (**8 o 16 floats** en Python).
- **Cada llamado a una dirección de memoria incluye a los elementos contiguos** a través de una línea
  de caché.

*(Consecuencia práctica: leer un elemento trae gratis a sus vecinos → recorrer con paso 1 es casi
gratis; recorrer con paso grande desperdicia la línea completa.)*

---

## 6. Localidad y reutilización de datos

El **mapeo del caché conserva la localidad** de los datos:
- Los elementos de un arreglo **se almacenan juntos en la RAM**.
- Al pasar al caché, **siguen juntos**.
- **"Juntos" significa en direcciones de memoria consecutivas.**

El caché **permite reutilizar los datos**:
- Un dato **permanece en el caché hasta que otro ocupa su lugar**.
- Los datos **usados recientemente se leen rápido** desde el caché.

> **Más localidad implica más reutilización y mejor rendimiento.** Hay **dos tipos de localidad**.

### 6.1 Localidad **temporal**
Es probable que los datos **utilizados recientemente** aún se puedan encontrar en la caché.
- Los cachés normalmente usan la **política de reemplazo LRU** (*least recently used*).
- Aquí, **"reciente" significa el tiempo antes de que se vacíe el slot** del caché — **depende del
  tamaño de caché y la asociatividad**.
- **Estrategia del programador: localizar el uso de datos dentro de unas pocas líneas de código.**

### 6.2 Localidad **espacial**
La **dirección de memoria tiene un orden** — es una **cadena de bits** que se puede interpretar como
un número. La dirección determina:
- la **ubicación de los datos en una línea de caché**;
- la **ubicación de la línea de caché en un conjunto de caché**.

El **mapeo directo de caché preserva las secuencias de datos**.
- **Estrategia del programador: dejar que las instrucciones funcionen en elementos de datos vecinos.**

### 6.3 La localidad está bajo control del programador
Mantener **todo local** para mejorar el rendimiento, en los cuatro niveles:
- **Formulación del modelo.**
- **Código de software.**
- **Asignación de memoria.**
- **Mapeo de caché.**

---

## 7. ¿Qué se puede controlar del caché?

- **El flujo entre niveles de caché NO se controla explícitamente.**
- **Sí** se puede escribir código que **reutilice mejor los datos** en el caché:
  - **Reutilizar los datos mientras siguen en el caché.**
  - **Dividir el problema en bloques que quepan en el caché.** *(blocking / tiling)*

**Recomendaciones en Python:**
- **Usar arreglos de NumPy en lugar de listas.**
- **Recorrer los arreglos con paso 1**, o al menos con un **paso pequeño**.

---

## 8. Vectorizar

**Estrategia de vectorización de un código:**
- **Usar NumPy arrays en lugar de listas.**
- **Usar funciones de NumPy en lugar de for-loops.**

La librería **NumPy corre código compilado** y por eso aprovecha **las cuatro cosas a la vez**:
- **Pipelining.**
- **Reutilización del caché.**
- **Localidad de datos.**
- **Múltiples hilos.**

---

## 9. Coherencia del caché

El caché **guarda copias de datos que viven en la memoria principal**.

**Coherencia:** **garantía de que las copias en caché son consistentes con la memoria principal.**

**¿Cuándo puede romperse la coherencia?**
- El procesador **modifica un dato en caché**, pero **aún no lo escribe en memoria**.
- **Otro núcleo lee de memoria un valor obsoleto.**

### 9.1 Coherencia en procesadores multi-core

```
Un núcleo:                      Dos núcleos:
Núcleo                          Núcleo        Núcleo
Registros                       Registros     Registros
Caché L1                        Caché L1      Caché L1
Caché L2                        Caché L2 (compartida)
Memoria (RAM)                   Memoria (RAM)
```

- **Cada núcleo tiene su propio caché** con **copias privadas** de los datos.
- Si un núcleo **modifica un dato, las otras copias quedan obsoletas**.
- Un **protocolo de coherencia coordina las copias** entre núcleos.

### 9.2 El protocolo MESI

Protocolo de coherencia **muy usado**. Cada **línea de caché** está en **uno de cuatro estados**:

| Estado | Nombre | Significado |
|--------|--------|-------------|
| **M** | **Modificada** | **cambiada en este caché, única copia** |
| **E** | **Exclusiva** | **igual a la memoria, única copia** |
| **S** | **Compartida** | **igual a la memoria, en varios cachés** |
| **I** | **Inválida** | **la copia ya no sirve** |

Transiciones (este núcleo / otro núcleo):
- **I → E**: **lee** (sin copias).
- **I → S**: **lee** (con copias).
- **E → M**, **S → M**: **escribe**.
- **M → S**, **E → S**: **otro lee**.
- **M → I**, **S → I**, **E → I**: **otro escribe**.

---

## Resumen de la clase
- **Acceso paralelo de memoria** (compartida vs. distribuida).
- **Mapeo de caché** (directo, asociativo, n-asociativo).
- **Localidad de datos** (temporal y espacial).
- **Coherencia del caché** (MESI).

**Próxima clase:** ¿cómo programar múltiples hilos?
