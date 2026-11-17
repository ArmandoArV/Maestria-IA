# Clase 03. Apache Hadoop: datos y cálculo distribuido

**INF3862**, Prof. Sebastián Hagedorn. Fuente: `Presentaciones/Clase03.pdf` (53 láminas).

**Recorrido de la clase:** Por qué nació Hadoop · Almacenar y coordinar (HDFS, YARN) · MapReduce
paso a paso · Ejemplo: K-means con MapReduce · Plataformas y separación de recursos · Actividad:
elegir y diseñar.

---

## 1. Por qué nació Hadoop

**Una máquina tiene una capacidad finita.**
- **Situación:** analizar **10 TB** de documentos y registros.
- **El servidor:** **2 TB** de disco, **64 GB** de RAM y **16 núcleos**.
- > Ampliar el disco permite **guardar** más datos. **Leerlos y procesarlos sigue tomando tiempo.**
- **El problema es doble:** *almacenar los datos* **y** *terminar el cálculo dentro del tiempo
  disponible*.

### ¿Dónde está el límite?
```
Disco y red (leer datos) → CPU y RAM (procesar) → Disco y red (guardar salida)
```
- **Una CPU rápida puede quedar esperando I/O.** **Más RAM no aumenta por sí sola el ancho de banda
  del disco.**
- > **Matiz importante de la clase:** podemos trabajar **por bloques**, **que los datos superen la
  > RAM no obliga por sí solo a distribuir**. (No todo problema grande es un problema distribuido.)

### Vertical vs. horizontal
| **Vertical (*scale up*)** | **Horizontal (*scale out*)** |
|---------------------------|------------------------------|
| un servidor con más CPU, RAM y disco | agregar máquinas (servidor 1, 2, 3…) |

> **Agregar máquinas exige repartir datos, coordinar tareas y responder a fallos.**

### Las dos preguntas de ingeniería
| **Almacenar** | **Procesar** |
|---------------|--------------|
| *¿cómo repartir archivos entre servidores y seguir leyendo si uno falla?* | *¿cómo ejecutar partes del cálculo en paralelo y reunir sus resultados?* |

> **A mayor cantidad de servidores, más importante es poder continuar ante fallos de componentes.
> Recuperar fallos debe formar parte del diseño del sistema.**

### Historia: de Google y Nutch a Hadoop
| Año | Hito |
|-----|------|
| **2003** | **GFS** (Google File System): *almacenar* |
| **2004** | **MapReduce**: *procesar* |
| **2006** | **Hadoop**: proyecto abierto |

**Doug Cutting** y **Mike Cafarella** desarrollaron en **Nutch** componentes inspirados en las
publicaciones de Google. **Yahoo!** impulsó su desarrollo. Hadoop **se separó de Nutch en 2006** y
pasó a ser **proyecto de primer nivel de Apache en 2008**.

### Hadoop integra las piezas
| Componente | Rol |
|------------|-----|
| **HDFS** | distribuir archivos y mantener **réplicas** |
| **YARN** | administrar **CPU y memoria** del clúster |
| **MapReduce** | **expresar y ejecutar** cálculos distribuidos |
| **Hadoop Common** | bibliotecas y utilidades compartidas |

---

## 2. HDFS: almacenar y coordinar

### De un archivo a bloques distribuidos
```
Archivo = A + B + C

DataNode 1 : A  C
DataNode 2 : A  B
DataNode 3 : B  C
```
Cada bloque del ejemplo tiene **dos réplicas en nodos distintos**.
> Distribución **didáctica**; el **tamaño de bloque, la replicación y la colocación son
> configurables**.

### NameNode vs. DataNode
```
Cliente --1. ubicación--> NameNode (metadatos)
Cliente --2. lectura directa--> DataNode (bloque A)
```
> **El NameNode conoce dónde están los bloques; el contenido no pasa normalmente por él.**

### Tolerancia a fallos
Si DataNode 1 no está disponible: **leer A desde el nodo 2 y C desde el nodo 3**. El sistema
**detecta réplicas faltantes y busca recuperar el nivel configurado**.
> **El costo:** tres copias de 1 TB consumen **aproximadamente 3 TB**. **La tolerancia a fallos
> tiene un costo.**

### Localidad: ejecutar cerca de los datos
```
Nodo 1 (bloque A) → tarea Map sobre A
Nodo 2 (bloque B) → tarea Map sobre B
Nodo 3 (bloque C) → tarea Map sobre C
```
> **Si hay recursos disponibles**, ejecutar donde ya existe una réplica **evita transferir todo el
> bloque**. **La localidad reduce tráfico; no elimina la comunicación entre etapas** (el *shuffle*
> sigue moviendo datos).

### YARN
| Componente | Rol |
|------------|-----|
| **ResourceManager** | recursos del clúster |
| **ApplicationMaster** | coordina el trabajo de **una** aplicación |
| **NodeManager** | gestiona la ejecución en **un** nodo; levanta *containers* |
| **Container** | asigna recursos a una tarea |

### Las tres piezas juntas
```
HDFS (datos de entrada) → YARN + MapReduce (ejecutar tareas) → HDFS (archivos de salida)
```
> **YARN administra recursos. MapReduce organiza el cálculo. HDFS conserva los archivos.**
> Y, como en la clase anterior, **Airflow podría coordinar cuándo enviar y supervisar este trabajo**.
> El orquestador es **otra** capa.

---

## 3. MapReduce paso a paso

**MapReduce es un modelo de programación.** Reparto de responsabilidades:

| **El programador define** | **El framework hace** |
|---------------------------|------------------------|
| qué emite **Map**, cómo se **agrupa** y qué calcula **Reduce** | distribuye registros, **planifica tareas**, **transfiere datos** y **recupera intentos fallidos** |

> **El mismo modelo permite contar palabras, construir índices o calcular estadísticas.**

### Un cálculo, muchas tareas
```
Datos de entrada → Map 1, Map 2, Map 3 → [shuffle y sort] → Reduce 1, Reduce 2 → Salida 1, Salida 2
```
> **Map trabaja sobre registros; Reduce trabaja sobre los valores de cada clave.** Las tareas pueden
> ejecutarse en distintas máquinas; **una máquina puede ejecutar varias tareas**.

### El contrato
```
Map(k1, v1) → emite (k2, v2)
Framework   → agrupa por k2
Reduce(k2, [v2]) → emite resultados
```
> **Map puede emitir cero, uno o muchos pares por registro. Reduce puede emitir cero, uno o muchos
> resultados por clave.**
> **Idea central: la clave expresa qué información debe reunirse para calcular algo.**

### El ejemplo canónico: contar nueve palabras
Archivo: `DOG CAT RAT / CAR CAR RAT / DOG CAR CAT`

**1. Input: dividir el trabajo de lectura**
| Split 1 | Split 2 | Split 3 |
|---------|---------|---------|
| DOG CAT RAT | CAR CAR RAT | DOG CAR CAT |

Cada mapper procesa los registros de un **input split**.
> Una línea por split **solo para el ejemplo**. **Un split es lógico; no es una réplica ni equivale
> siempre a un bloque HDFS.**

**2. Map: emitir un par por aparición**
| Map 1 | Map 2 | Map 3 |
|-------|-------|-------|
| (DOG,1) (CAT,1) (RAT,1) | (CAR,1) (CAR,1) (RAT,1) | (DOG,1) (CAR,1) (CAT,1) |

> Map emite `(palabra, 1)`. **Los totales todavía están repartidos entre tareas.**

**3. Particionar: elegir el reducer de cada clave**
Salida de Map 3 `(DOG,1) (CAR,1) (CAT,1)` → **partición 0**: `(CAR,1) (CAT,1)` · **partición 1**:
`(DOG,1)`.
- Regla del ejemplo: **CAR/CAT → 0; DOG/RAT → 1**.
- > **Todos los pares con la misma clave deben ir a la misma partición.**
- > La regla explícita es **didáctica**: **el particionador habitual se basa en el *hash* de la clave
  > y el número de reducers.**

**4. Shuffle: transferir las particiones**
Cada reducer obtiene **su** partición de las salidas de **todos** los mappers:
- Reducer 0 → `CAR: [1,1,1]`, `CAT: [1,1]`
- Reducer 1 → `DOG: [1,1]`, `RAT: [1,1]`
> Una sola conexión puede transportar muchos pares.

**5. Sort y agrupación: preparar cada llamada a Reduce**
Lo recibido en el reducer 0 llega desordenado (`(CAT,1), (CAR,1), (CAR,1), (CAT,1), (CAR,1)`) y se
ordena por clave → `CAR: [1,1,1]`, `CAT: [1,1]`.
> **Reduce se invoca por clave:** primero un grupo, luego otro. **Las claves se ordenan dentro de
> cada partición; no hay una ordenación global garantizada entre archivos.**

**6. Reduce: sumar y escribir**
| `part-r-00000` | `part-r-00001` |
|----------------|----------------|
| CAR 3 · CAT 2 | DOG 2 · RAT 2 |

> Comprobación: **3 + 2 + 2 + 2 = 9** apariciones. **No necesitamos reunir todo en un único archivo.**

### ¿Dónde consume tiempo el shuffle?
```
Mapper (buffer y disco local) → Shuffle (transferir particiones) → Reducer (mezclar y agrupar)
```
- Los pares intermedios **se ordenan y pueden escribirse en disco**; los reducers **recuperan esas
  salidas y las combinan**.
- > **Además del cálculo, pagamos I/O, red y coordinación.**
- > **El shuffle puede comenzar antes de terminar todos los mappers; pero Reduce necesita el grupo
  > completo de su clave** (de ahí la barrera efectiva).

### Skew: si una clave concentra los datos, concentra trabajo
El **90 % de los registros** tiene la clave `NORTE` → el reducer 0 hace **mucho** trabajo y el
reducer 1 **poco**.
> **Agregar reducers no divide automáticamente el trabajo de una misma clave.** Es el problema de
> **skew**. **La estrategia para repartir una clave depende de si su cálculo admite agregaciones
> parciales** (p. ej. una suma sí; una mediana exacta no, directamente).

### Recuperación de fallos
`Map 2 falla` (sin salida válida) → **nuevo intento** (releer su split) → `Map 2 termina` (salida
disponible).
> Si se pierde la salida intermedia de un mapper, **el framework puede volver a calcularla**; HDFS
> permite **releer réplicas** disponibles.
> **Dos mecanismos distintos: la replicación protege los datos de entrada; el reintento recupera el
> cálculo.**

---

## 4. Ejemplo: K-means con MapReduce

### Qué es K-means
**Algoritmo de clustering: agrupa observaciones según su cercanía.**
- **Pregunta:** *¿podemos encontrar grupos de clientes con comportamientos de compra parecidos?*
- **Información disponible:** variables **numéricas**, frecuencia de compra, gasto o cantidad de
  productos.
- > Es **aprendizaje no supervisado**: **no recibe etiquetas** con el grupo correcto de cada
  > observación.

Entrada: puntos sin grupo. Salida: **grupos y centroides**. *Buscamos que los puntos de cada grupo
queden cerca de su centro.*

### Tres conceptos
| **K** | **Grupo / cluster** | **Centroide** |
|-------|---------------------|---------------|
| cantidad de grupos que elegimos buscar (`K = 2` pide dos grupos) | observaciones asignadas al mismo centroide **por cercanía** | **promedio de las coordenadas** de los puntos del grupo |

> En una dimensión el centroide es **un número**; en dos dimensiones tiene **una coordenada por
> eje**. **K-means recibe los datos y K; produce una asignación de grupo y los centroides finales.**
> **La cercanía depende de las variables y su escala.** Las etiquetas de grupo **no son categorías
> conocidas de antemano**.

### El algoritmo a mano (una dimensión)
Datos: **10, 20, 30, 80, 100**, con **K = 2**. Centros iniciales: **20** y **80**.
> *Para seguir el ejemplo a mano elegimos estos centros.* **La inicialización influye en el
> resultado.**

**Paso 1: asignar cada punto al centro más cercano.** Para el punto 30: distancia a 20 = **10**;
distancia a 80 = **50** → grupo 1.
- Grupo 1: **10, 20, 30** · Grupo 2: **80, 100**.
- *Todos los puntos comparan sus distancias usando **los mismos** centros.*

**Paso 2: mover cada centro al promedio de su grupo.**
- Centro 1 = (10 + 20 + 30)/3 = **20** (se mantiene).
- Centro 2 = (80 + 100)/2 = **90** (pasa de 80 a 90).

**Repetir hasta estabilizar.** Con centros 20 y 90 los grupos siguen siendo `[10,20,30]` y
`[80,100]`, y al recalcular los centros vuelven a dar 20 y 90 → **terminamos**.
> **En general se usa una tolerancia de cambio y un máximo de iteraciones.**

### ¿Qué parte se puede repartir?
| **Asignar puntos** | **Actualizar centros** |
|--------------------|------------------------|
| cada punto puede buscar su centro más cercano **sin consultar a los otros puntos** | necesitamos **reunir** los valores asignados al mismo grupo para calcular su promedio |
| → **Map** | → **Shuffle + Reduce** |

> **Una iteración de K-means se puede expresar como un trabajo MapReduce.**

### Map
Clave = **grupo más cercano**. Valor = **el punto asignado**.
| Map 1 (puntos 10, 80) | Map 2 (puntos 20, 30, 100) |
|-----------------------|-----------------------------|
| (G1, 10) · (G2, 80) | (G1, 20) · (G1, 30) · (G2, 100) |

> Primera iteración: **todos los mappers reciben los centros 20 y 80**. Cada mapper procesa una
> partición de los puntos.

### Shuffle y Reduce
`G1: [10,20,30]` → Reduce G1 = (10+20+30)/3 → **Centro 1 = 20**
`G2: [80,100]` → Reduce G2 = (80+100)/2 → **Centro 2 = 90**
> **Shuffle reúne los puntos del mismo grupo; Reduce calcula su promedio.** *Un reducer físico puede
> procesar más de un grupo.*

### El controlador inicia la siguiente iteración
```
Trabajo 1 (centros 20 y 80) → guardar centros 20 y 90 → Trabajo 2 (usar centros nuevos)
```
- **Los puntos originales se vuelven a procesar**; los centros actualizados **se entregan a todos los
  mappers**.
- > **MapReduce distribuye cada iteración. Un controlador decide si debe iniciar otra.**
- > Honestidad del curso: *con cinco puntos lo hacemos a mano*. Con muchos puntos puede interesar
  > repartir el cálculo, pero **repetir lecturas y trabajos tiene un costo** (ésta es exactamente la
  > limitación de MapReduce que motivó frameworks que mantienen datos en memoria entre iteraciones).

---

## 5. Plataformas y separación de recursos

### Cloudera
**Plataforma que integra herramientas para almacenar, procesar y administrar datos.**
- administración y monitoreo de servicios;
- **seguridad, catálogo y gobierno de datos**;
- despliegue en infraestructura propia **y en la nube**.
- > **Además del motor de cálculo, una organización necesita operar y gobernar su plataforma.**

### Amazon EMR
**Facilita ejecutar frameworks de datos, como Hadoop, sobre infraestructura de AWS.**
| El servicio facilita | El equipo define |
|----------------------|------------------|
| aprovisionar recursos y configurar el entorno de procesamiento | **el trabajo, los datos, los permisos y los recursos** que necesita |

> **Un servicio administrado reduce parte del trabajo de infraestructura; el diseño del
> procesamiento sigue siendo necesario.**

---

## 6. Actividad: elegir una arquitectura y explicar su diseño

**Individual o en parejas.** Se reciben **dos casos** con sus datos y objetivo.
1. Elegir cuál resolverían **con Hadoop y MapReduce**.
2. Justificar **por qué el otro caso necesita otra arquitectura**.
3. **Dibujar** cómo se almacenan y procesan los datos del caso elegido (proceso MapReduce).

### Caso A: analizar registros de una plataforma web
- **Datos:** **60 TB** de logs de los últimos 30 días; llegan **2 TB diarios**. **Los archivos
  históricos no se modifican.**
- **Campos:** `timestamp`, `sitio`, código HTTP, bytes enviados.
- **Objetivo:** publicar **cada mañana antes de las 08:00** las solicitudes y el **porcentaje de
  errores por sitio y día**.
- Supuestos: **error = HTTP 500–599**; registros válidos, sin duplicados, fechas en **UTC**.

### Caso B: confirmar compras con stock disponible
- **Datos:** **50.000 productos**, **≈ 20 MB**. Campos: `producto_id`, `stock`, `precio`.
- **Objetivo:** **consultar y descontar stock** al confirmar una compra, **en menos de 100 ms**.
- **Condición:** si queda **una** unidad y llegan **dos** compras simultáneas, **solo una puede
  confirmarse**.

> *(El caso A es el batch analítico masivo sobre archivos inmutables → Hadoop/MapReduce. El caso B
> es OLTP transaccional de baja latencia con control de concurrencia → un DBMS relacional/clave-valor
> con transacciones, como en la Clase 01. La actividad pide justificarlo con los cuatro criterios de
> abajo.)*

### Parte 1: comparar y justificar
Comparar ambos casos con **cuatro criterios**:
1. **volumen de datos**;
2. **tiempo de respuesta requerido**;
3. **lectura de archivos frente a actualizaciones de registros**;
4. **posibilidad de dividir y combinar el cálculo**.

Cerrar con **la elección y la justificación de por qué no es adecuado para el otro caso**.

### Parte 2: representar el almacenamiento en HDFS
Dibujar, para el caso elegido:
- un archivo **dividido en bloques**;
- **tres DataNodes** y **dos réplicas** de cada bloque;
- el **NameNode** y la ubicación de los bloques que administra;
- **marcar un DataNode como caído** e indicar **desde dónde se leerían sus bloques**.

> **Las réplicas son copias para disponibilidad; no son registros adicionales que debamos contar.**

### Parte 3: representar el procesamiento MapReduce
Usar **al menos cuatro registros inventados** del caso elegido y mostrar:
1. **Entrada:** qué registros recibe cada mapper.
2. **Map:** qué **clave** y qué **valor** emite.
3. **Shuffle:** qué valores se reúnen por clave.
4. **Reduce:** qué calcula y qué resultado produce.

Indicar **desde dónde se leen los datos** y **dónde se guardan los archivos de salida**.

### Entregable
**Un PDF con tres láminas:**
1. **Decisión**: comparación de los dos casos, elección justificada y alternativa para el otro caso.
2. **HDFS**: diagrama de bloques, réplicas y nodos; explicación de un fallo.
3. **MapReduce**: diagrama con los cuatro registros, pares intermedios, agrupación y resultado.

> **No se requiere código.**
