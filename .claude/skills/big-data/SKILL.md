---
name: big-data
description: >
  Expert knowledge base for the INF3862 Big Data course (Magíster en IA, PUC Chile, Prof. Sebastián
  Hagedorn): almacenamiento de datos, pipelines y cómputo distribuido. Covers: fundamentos de bases
  de datos y DBMS (datos estructurados/semiestructurados/no estructurados, CRUD, query engine,
  storage manager, esquema y catálogo de metadatos, transacciones, COMMIT/ROLLBACK, ACID,
  autenticación y autorización, respaldos); OLTP vs. OLAP (cargas, latencia vs. rendimiento
  analítico, separación de cargas, organización física por filas vs. por columnas, poda de columnas,
  compresión columnar, ClickHouse/Snowflake); modelos de datos (relacional, NoSQL clave-valor,
  documental, grafos, series temporales, vectorial con embeddings y RAG, objetos, jerárquico,
  multimodelo) y qué modelo elegir según la consulta; rendimiento y escalabilidad (índices, caché,
  optimización de planes, particionamiento, paralelismo, scale up vs. scale out, sharding,
  replicación); Data Warehouse (arquitectura de tres capas, ETL, servidor OLAP, modelado dimensional
  con hechos y dimensiones, metadatos, gobernanza, separación almacenamiento/cómputo en la nube);
  Data Lake (object storage, objeto/clave/metadatos, S3, Parquet/Avro/ORC, Athena/Presto,
  schema-on-write vs. schema-on-read, y sus problemas: correcciones a medias, versiones, calidad);
  Data Lakehouse y Delta Lake (delta log, commit, validación de esquema, versiones y time travel,
  Apache Iceberg con snapshots y manifiestos, Hudi, compactación, retención); ETL y orquestación
  (estrategias de extracción full/incremental/update notification, webhooks, watermark y
  updated_at, técnicas de transformación: limpiar, deduplicar, estandarizar, derivar, join, split,
  resumir/cambiar el grano, cifrar), estrategias de carga full/incremental, UPSERT/MERGE, batch vs.
  streaming, idempotencia, ETL vs. ELT); Apache Airflow (DAG, task, operator, TaskFlow, schedule,
  DAG Run, dependencias con >>, Jinja, datasets/assets, ObjectStoragePath, airflow standalone) y
  Dagster (asset, materialization, definitions, run, dg dev, create-dagster); el ecosistema (dbt,
  Airbyte, AWS Glue, Lakeflow Jobs); y Apache Hadoop (escalamiento horizontal, GFS, HDFS con bloques
  réplicas NameNode y DataNode, localidad de datos, YARN con ResourceManager/ApplicationMaster/
  NodeManager/containers, MapReduce paso a paso: input splits, map, particionador, shuffle, sort,
  reduce, part-r-00000), skew, reintentos, K-means distribuido con MapReduce, Cloudera, Amazon
  EMR). Includes the OLTP vs. OLAP benchmark built for Actividad 1 (SQLite vs. DuckDB over 1M sales,
  EXPLAIN QUERY PLAN, SCAN vs. SEARCH, índice cubriente, columna materializada, tabla de resumen).
  Use for any INF3862 question (clases, actividades prácticas, formulario de evaluación,
  entregables), or to reason about choosing a storage engine, designing a pipeline, or deciding
  whether a problem needs a distributed system. Also trigger on big data, INF3862, almacenamiento de
  datos, base de datos, DBMS, OLTP, OLAP, transacción, ACID, atomicidad, aislamiento, durabilidad,
  commit, rollback, motor columnar, almacenamiento por columnas, orientado a filas, poda de columnas,
  compresión, DuckDB, SQLite, ClickHouse, Snowflake, modelo de datos, NoSQL, clave-valor, documental,
  MongoDB, Redis, DynamoDB, grafos, Neo4j, Neptune, series temporales, InfluxDB, TimescaleDB, base de
  datos vectorial, pgvector, Milvus, Weaviate, Qdrant, embedding, RAG, índice, caché,
  particionamiento, sharding, replicación, escalamiento vertical u horizontal, scale up, scale out,
  data warehouse, bodega de datos, modelado dimensional, tabla de hechos, dimensión, ETL, ELT,
  extract, transform, load, staging, deduplicar, estandarizar, idempotencia, UPSERT, MERGE, batch,
  streaming, data lake, lago de datos, object storage, bucket, S3, Parquet, Avro, ORC, Athena,
  Presto, Databricks, schema-on-read, schema-on-write, lakehouse, Delta Lake, delta log, Apache
  Iceberg, Hudi, time travel, Airflow, DAG, operator, TaskFlow, Jinja, Dagster, asset,
  materialización, dbt, Airbyte, AWS Glue, Hadoop, HDFS, NameNode, DataNode, bloque, réplica, YARN,
  ResourceManager, container, MapReduce, mapper, reducer, shuffle, sort, particionador, input split,
  localidad de datos, skew, word count, K-means distribuido, Cloudera, Amazon EMR, GFS, Doug Cutting,
  or the course code INF3862.
  Respond in Spanish when the user writes in Spanish.
---

# Big Data (INF3862)

Knowledge base for **INF3862**, Pontificia Universidad Católica de Chile, Magíster en Inteligencia
Artificial. Profesor **Sebastián Hagedorn**. Material del repo: `~/Maestria-IA/BigData/`.

El curso recorre la pila de datos **de abajo hacia arriba**: primero **dónde** viven los datos
(bases de datos, warehouse, lake, lakehouse), luego **cómo se mueven** (ETL y orquestación), y
después **cómo se procesan cuando no caben en una máquina** (Hadoop, MapReduce).

> **El hilo conductor:** *"¿Una misma solución sirve para todas estas necesidades?"* La respuesta del
> curso es **no**, y cada clase da un criterio para elegir. Toda recomendación debe salir del
> **patrón de acceso** (qué consulta, cuántos registros, qué latencia, lectura o escritura), no de
> qué tecnología está de moda.

## Cómo usar esta skill

1. **Lee el archivo de `references/` correspondiente** antes de responder más allá del resumen de
   abajo. SKILL.md es el mapa; las referencias tienen las tablas, los ejemplos y las cifras.
2. **Responde en español.** El curso es en español.
3. **Empieza por la consulta, no por la tecnología.** Es el método explícito de la Clase 01
   (*"elegir un modelo empieza por la consulta"*). Pregunta: ¿cuántos registros toca?, ¿lee o
   escribe?, ¿qué latencia necesita?, ¿se puede dividir el cálculo? De ahí sale el motor, el modelo
   y la arquitectura: en ese orden.
4. **Nombra el costo, no solo el beneficio.** El profesor cierra casi cada lámina con un matiz:
   *"cada mecanismo tiene costos"*, *"la tolerancia a fallos tiene un costo"*, *"el Lakehouse agrega
   capacidades; también requiere configuración y mantenimiento"*. Una respuesta que solo lista
   ventajas no está respondiendo como el curso.
5. **Distingue las tres capas que se confunden constantemente.** Es la trampa conceptual favorita
   del curso:
   - **formato de archivo** (Parquet) ≠ **formato/gestión de tabla** (Delta Lake, Iceberg, Hudi) ≠
     **motor de consultas** (Athena, DuckDB, Spark) ≠ **arquitectura** (Lakehouse);
   - **Object Storage** (tecnología) ≠ **Data Lake** (arquitectura);
   - **orquestador** (Airflow, Dagster) ≠ **motor de procesamiento** (el que realmente mueve los
     datos). *"Airflow coordina el trabajo; cada tarea procesa datos o invoca otro sistema."*
6. **OLTP y OLAP son orientaciones de uso, no categorías de producto.** Pueden coexistir en una
   plataforma. No digas "SQLite es OLTP" como si fuera una propiedad esencial: di que **su
   organización por filas + índices favorece el acceso puntual**.
7. **Las garantías dependen del sistema.** ACID no es un interruptor binario: *"las garantías
   concretas dependen del sistema y del nivel de aislamiento"*. Lo mismo con los formatos abiertos:
   *"la compatibilidad depende del motor y las funciones utilizadas"*.
8. **No toda carga grande es distribuida.** La Clase 03 lo dice explícitamente: *"podemos trabajar
   por bloques: que los datos superen la RAM no obliga por sí solo a distribuir"*. Antes de proponer
   Hadoop, descarta una sola máquina con un motor columnar.
9. **Al comparar rendimiento, mide y explica.** La rúbrica de la Actividad 1 es clara: *"se evalúa la
   explicación; los tiempos no deben coincidir con un valor prefijado"*. Reporta órdenes de magnitud
   y el **mecanismo** (plan de ejecución, bytes leídos), no decimales.
10. **Las actividades son entregables con rúbrica.** Antes de resolver una, revisa en la referencia
    qué se entrega **exactamente** (formulario, `.py` + captura de una run exitosa, PDF de tres
    láminas): el formato es parte de la nota.

## Mapa del curso

| Clase | Tema | Reference |
|-------|------|-----------|
| 01 | Almacenamiento de datos: DBMS, OLTP/OLAP, modelos, Warehouse, Lake, Lakehouse | `references/clase01-almacenamiento-de-datos.md` |
| 02 | ETL y orquestación: técnicas de transformación, Airflow, Dagster | `references/clase02-etl-y-orquestacion.md` |
| 03 | Apache Hadoop: HDFS, YARN, MapReduce, K-means distribuido | `references/clase03-hadoop-mapreduce.md` |
| - | **Actividad 1 resuelta:** benchmark OLTP vs. OLAP (SQLite vs. DuckDB, 1M ventas) | `references/actividad01-oltp-vs-olap.md` |

> Material disponible hasta la fecha: `Presentaciones/Clase01.pdf` (80 láminas), `Clase02.pdf` (55),
> `Clase03.pdf` (53). Si alguien pide una clase posterior, **dilo**: no está en el repositorio.

## Evaluaciones conocidas

| Actividad | Modalidad | Entregable | Puntaje |
|-----------|-----------|------------|---------|
| **Actividad práctica 1**: OLTP vs. OLAP | 60 min, individual o en parejas; notebook preparado; 1–5 M de ventas en SQLite y DuckDB | **solo el formulario**: 7 preguntas objetivas (70 %, 10 % c/u) + 2 respuestas breves de interpretación (30 %, 15 % c/u). **No se entrega código ni notebook.** Cierre: jueves 29 de octubre, 23:59 | rúbrica por respuesta breve: 0 incorrecta · 1 parcial · 2 correcta y justificada |
| **Actividad práctica 2**: construir un ETL local | individual o en parejas; elegir **Airflow o Dagster** y crear su propio dataset | **práctica (0,5 pt):** archivos `.py` (DAG o assets + lógica de transformación) **+ imagen de una run exitosa**. **Teoría (0,5 pt):** elección de herramienta, caso de uso y escalamiento, **con fuentes** | **1 punto** |
| **Actividad 3**: elegir y diseñar arquitectura | individual o en parejas; dos casos dados (logs de 60 TB vs. stock con < 100 ms) | **PDF de tres láminas:** decisión justificada · diagrama HDFS (bloques, réplicas, nodos, un fallo) · diagrama MapReduce (4 registros, pares intermedios, agrupación, resultado). **No se requiere código** | - |

> **Advertencias que el profesor repite:** el ETL de la Actividad 2 **debe transformar de verdad**
> ("no basta con tareas que solo impriman mensajes") y la captura **debe permitir identificar el
> pipeline entregado**.

## Resumen de conceptos

### DBMS: qué hace el software además de guardar
**Base de datos** = la colección almacenada; **DBMS** = el software que la administra y que
**abstrae el almacenamiento físico**. El problema que lo justifica: *queda una unidad y llegan dos
compradores: **1 unidad ≠ 2 ventas***. Cuatro necesidades → cuatro capacidades: **encontrar y
organizar** (consultas, esquemas, metadatos), **compartir sin romper reglas** (integridad,
transacciones, concurrencia), **responder a tiempo** (índices, caché, optimización) y **proteger y
recuperar** (permisos, respaldos). Componentes internos: **interfaces** → **query engine**
(interpretar, elegir un plan, ejecutar) → **storage manager** (organizar, reducir trabajo,
recuperar), con **esquema/catálogo** (incluye las **estadísticas** que usa el optimizador) y
**transaction manager** atravesándolo todo. **ACID** sobre el ejemplo de la transferencia:
**atomicidad** (ambos cambios o ninguno), **consistencia** (restricciones), **aislamiento**
(concurrencia coordinada), **durabilidad** (lo confirmado persiste).

### OLTP vs. OLAP y la organización física
| | **OLTP** | **OLAP** |
|-|----------|----------|
| Objetivo | operar | analizar |
| Por consulta | pocos registros | muchos registros |
| Actividad | leer y escribir | leer y agregar |
| Prioridad | latencia y concurrencia | rendimiento analítico |

**Por qué separarlos:** compiten por CPU, memoria y almacenamiento: *"una consulta extensa puede
afectar la respuesta de la aplicación"*. **Filas** = acceder a un registro completo; **columnas** =
leer pocos atributos de muchas filas (**poda de columnas**) y **comprimir mejor** valores similares
(`Ropa·Ropa·Ropa` → `Ropa × 3`) → **menos espacio y menos bytes leídos**, al costo de codificar,
descomprimir y **actualizar**. Columnar favorece **muchas** consultas analíticas, **no todas** las
operaciones.

### Modelos de datos → cuándo
| Necesidad | Modelo | Ejemplos |
|-----------|--------|----------|
| Pedidos y reglas de integridad | **relacional** | PostgreSQL, MySQL, SQL Server, Aurora |
| Sesión por identificador | **clave-valor** | Redis, DynamoDB |
| Catálogo con atributos variables | **documental** | MongoDB, DocumentDB |
| Eventos por dispositivo | **series temporales** | Timestream, InfluxDB, TimescaleDB |
| Caminos entre personas | **grafos** | Neptune, Neo4j |
| Búsqueda por similitud | **vectorial** (embeddings, RAG) | pgvector, Milvus, Weaviate, Qdrant |

**NoSQL no significa «sin estructura» ni garantías uniformes**, y **las categorías no son
excluyentes** (PostgreSQL es objeto-relacional; JSON representa jerarquías).

### Rendimiento y escala
**Evitar trabajo o repartirlo:** índices (menos registros examinados), caché (menos lecturas),
optimización (menos trabajo por plan), particionamiento (menos datos **si el filtro permite podar**),
paralelismo (menos tiempo). **Scale up** = una máquina más capaz; **scale out** = más máquinas.
**Sharding** (repartir: `A–M ∣ N–Z`) y **replicación** (copiar: `A–Z ∣ A–Z`) **resuelven problemas
diferentes**.

### Warehouse → Lake → Lakehouse
- **Warehouse:** datos **integrados** (moneda común, IDs unificados) en **tres capas**
  (almacenamiento / servidor OLAP / herramientas de acceso) alimentadas por **ETL**. **Modelado
  dimensional**: los **hechos** dicen *cuánto* (medidas + claves), las **dimensiones** permiten
  preguntar *por qué grupo*. Consecuencia del ETL periódico: *el dashboard puede reflejar un estado
  anterior al de la aplicación*. En la nube: **separar almacenamiento y cómputo**.
- **Data Lake:** conservar los archivos originales (CSV, JSON, JPG, PDF) en **object storage**
  (objeto = contenido + **clave** + metadatos). **Un bucket no basta:** también hace falta
  **catálogo, permisos, calidad y procesamiento**. **Schema-on-read** vs. **schema-on-write**:
  asociación tradicional con Lake y Warehouse, **no una regla absoluta**. Sus dos problemas
  concretos: una **corrección puede quedar a medias** (90+30 = 120 en vez de 130) y **no se sabe qué
  versión lee el reporte**.
- **Lakehouse:** **gestionar tablas sobre archivos**, object storage + capa de gestión (metadatos,
  esquemas, transacciones, versiones) + motores. **Delta Lake** = Parquet + **delta log**: el
  **commit** hace visible el cambio completo (la corrección aparece entera en la **versión 11**),
  valida el esquema y conserva versiones. **Iceberg** hace lo mismo con **snapshots y manifiestos**.
  Nomenclatura del curso: **Data Lake = repositorio · Delta Lake = tecnología · Lakehouse =
  arquitectura**, y **Parquet es formato de archivo, no de tabla**.

### ETL: las tres etapas y sus decisiones
- **Extract:** **update notification** (webhook; *¿y si llega dos veces o no llega?* → deduplicar y
  poder recuperar), **incremental** (`WHERE updated_at > :ultima_lectura`; guardar el punto de
  control **tras persistir**; *un `updated_at` no detecta borrados*), **full** (comparar o reemplazar
  snapshots; adecuado para carga inicial o fuentes pequeñas).
- **Transform:** limpiar y **deduplicar** (*un valor vacío no significa cero; dos filas parecidas no
  siempre son duplicados*), **estandarizar** (`03/04/2026` es ambiguo: hay que conocer la
  convención del origen), **derivar** (`importe = cantidad × precio`, *pero la fórmula necesita una
  regla de negocio*), **joinear** (*¿y si el catálogo tiene dos filas para el producto 10? el join
  puede duplicar la venta* → definir cardinalidad y qué hacer sin coincidencia), **separar**
  (`SCL-2026-00101`; conservar el original), **resumir** (**cambia el grano**: se gana el total, se
  pierde el detalle) y **cifrar** (*ocultar, hashear y cifrar son técnicas diferentes*).
- **Load:** **full** vs. **incremental** (que **también actualiza y borra** → **UPSERT/MERGE**),
  **batch** vs. **streaming** (eventos **repetidos o fuera de orden**; microlotes). Y la regla de
  oro: **idempotencia**, *repetir la misma carga produce el mismo estado final*.
- **ETL vs. ELT:** transformar **antes** de cargar (estructuras validadas, entorno previo) vs.
  **después** (aprovechar el cómputo del destino, que **debe poder procesar y gobernar** los datos).

### Orquestación: Airflow y Dagster
| Aspecto | **Airflow** | **Dagster** |
|---------|-------------|-------------|
| Concepto inicial | **DAG y tareas** | **Assets y dependencias** |
| Pregunta de diseño | *¿qué tareas ejecutamos?* | *¿qué datos producimos?* |
| Ejecución | ejecutar un DAG | **materializar** activos |
| Observación | DAG Runs, tareas, logs | Assets, Runs, materializaciones |

**Airflow:** workflows **como código Python** (dinámico con Jinja, extensible, versionable en Git).
**DAG** = grafo dirigido sin ciclos (schedule, tasks, dependencias, callbacks, reintentos y
timeouts). `extract() >> transform() >> load()`: **`>>` expresa dependencia; no transfiere datos**:
los datos van por almacenamiento compartido (`ObjectStoragePath`) y entre tareas se pasa la
**referencia**. **Datasets/assets** permiten disparar un DAG consumidor **cuando el productor
declara la actualización**, en vez de confiar en el horario. Local: `uv venv --python 3.12` +
`apache-airflow==3.3.2` con constraints + `airflow standalone` → `localhost:8080`.
**Dagster:** centrado en **assets**; `@dg.asset` puede **encapsular todo el ETL** (*tres etapas no
implican tres assets*); `dg dev` → `localhost:3000` → **Materialize**. **Ecosistema:** dbt
(transformaciones y pruebas), Airbyte (ingesta), AWS Glue (integración administrada), Lakeflow Jobs
(orquestación en Databricks): *ingerir, transformar, procesar y orquestar son funciones distintas*.

### Hadoop: HDFS, YARN, MapReduce
**El problema:** 10 TB de datos en un servidor de 2 TB / 64 GB / 16 núcleos: hay que **almacenar**
*y* **terminar el cálculo dentro del tiempo disponible**. Historia: **GFS (2003)** → **MapReduce
(2004)** → **Hadoop (2006**, de Nutch, por Doug Cutting y Mike Cafarella con impulso de Yahoo!;
top-level Apache en **2008**).
- **HDFS:** archivo → **bloques** con **réplicas** en nodos distintos. **NameNode** = metadatos
  (*dónde* están los bloques); **DataNode** = los bytes (*el contenido no pasa por el NameNode*). Si
  un nodo cae, se lee otra réplica y el sistema **recupera el nivel configurado**: **3 copias de
  1 TB cuestan ~3 TB**. **Localidad:** ejecutar donde ya hay una réplica **reduce tráfico, no lo
  elimina**.
- **YARN:** **ResourceManager** (clúster) + **ApplicationMaster** (una aplicación) +
  **NodeManager** (un nodo) + **containers** (recursos por tarea). Reparto de roles: *YARN administra
  recursos, MapReduce organiza el cálculo, HDFS conserva los archivos*, y **Airflow podría
  coordinar cuándo enviar el trabajo**.
- **MapReduce:** el **programador** define qué emite Map, cómo se agrupa y qué calcula Reduce; el
  **framework** distribuye, planifica, transfiere y **recupera intentos fallidos**. Contrato:
  `Map(k1,v1) → (k2,v2)`; el framework agrupa por `k2`; `Reduce(k2,[v2]) → resultados`. **La clave
  expresa qué información debe reunirse.** Seis pasos: **input splits** (lógicos, **no** = bloques) →
  **map** → **particionar** (hash de la clave; *todos los pares con la misma clave a la misma
  partición*) → **shuffle** → **sort/agrupar** (orden **por partición**, no global) → **reduce**
  (`part-r-00000`, `part-r-00001`). Costos reales: el shuffle paga **I/O, red y coordinación**.
  **Skew:** si una clave concentra el 90 % de los registros, **agregar reducers no la divide**.
- **K-means con MapReduce:** **Map** asigna cada punto a su centro más cercano (independiente por
  punto) emitiendo `(grupo, punto)`; **shuffle** reúne por grupo; **Reduce** promedia → nuevos
  centros. **Una iteración = un trabajo MapReduce**, y **un controlador decide si inicia otra**.
  *Repetir lecturas y trabajos tiene un costo*.
- **Plataformas:** **Cloudera** (administración, seguridad, catálogo, gobierno, on-prem y nube) y
  **Amazon EMR** (aprovisiona y configura; **el equipo sigue definiendo el trabajo, los datos, los
  permisos y los recursos**).

## Árbol de decisión: ¿dónde guardo y proceso estos datos?

1. **¿Qué pregunta tengo que responder?** Identificar · relacionar · comparar · agregar. *Elegir un
   modelo empieza por la consulta.*
2. **¿Pocos registros con baja latencia y escrituras con reglas?** → **OLTP**: motor **de filas**
   con **índices** sobre las claves de acceso (relacional si hay integridad; clave-valor si es
   acceso por identificador).
3. **¿Muchos registros y agregaciones?** → **OLAP**: motor **columnar**. **Y separa la carga** de la
   base operacional.
4. **¿Cabe en una máquina?** Un motor columnar sobre una sola máquina (DuckDB) cubre muchísimo más de
   lo que la gente supone: 1M filas se agregan en **1,5 ms**. **No distribuyas todavía.**
5. **¿Necesito integrar varias fuentes para analizar?** → **ETL/ELT** hacia un **Warehouse** (si el
   esquema analítico está claro y los datos son estructurados) o un **Lake/Lakehouse** (si hay
   variedad, exploración o cargas de DS/ML).
6. **¿Guardo archivos crudos y varios procesos los leen y escriben?** → necesitas **gestión de
   tablas** (**Delta Lake** o **Iceberg**): commits atómicos, validación de esquema y versiones. Un
   bucket con Parquet suelto te dará **correcciones a medias** y lecturas de versiones mezcladas.
7. **¿Hay que coordinar, reintentar, programar y auditar los pasos?** → **orquestador** (Airflow si
   piensas en tareas; Dagster si piensas en activos). **El orquestador no es el motor de
   procesamiento.**
8. **¿Decenas de TB de archivos inmutables, batch, con ventana de tiempo?** → **recién aquí**
   escalamiento horizontal: **HDFS + YARN + MapReduce** (o un framework equivalente). Verifica
   primero que el cálculo **se pueda dividir y combinar**.
9. **¿Latencia de milisegundos con concurrencia y control de stock?** → **nunca** MapReduce: es el
   Caso B de la Clase 03, y necesita **transacciones**.
10. **Antes de cerrar la recomendación, nombra el costo:** réplicas (×3 en disco), compactación y
    retención en el Lakehouse, mantenimiento de una tabla de resumen, overhead del orquestador,
    carga sobre el origen al extraer.

## Advertencias que el curso repite (úsalas al responder)

- *"Son orientaciones de uso; pueden coexistir en una plataforma."* (OLTP/OLAP)
- *"Las garantías concretas dependen del sistema y del nivel de aislamiento."* (ACID)
- *"NoSQL no significa «sin estructura» ni garantías uniformes."*
- *"Cada mecanismo tiene costos; su utilidad depende de la carga."* (índices, caché, particiones)
- *"Guardar un archivo no garantiza poder encontrarlo, entenderlo y analizarlo."* (Lake)
- *"Un formato de tabla no es por sí solo un DBMS ni un motor de consultas."*
- *"Preparar archivos no es publicar la versión: el commit hace visible el cambio."* (Delta)
- *"Un valor vacío no siempre significa cero. Dos filas parecidas no siempre son duplicados."* (ETL)
- *"Incremental no significa solo agregar filas: también puede actualizar o borrar."*
- *"Una `>>` expresa una dependencia; no transfiere automáticamente los datos."* (Airflow)
- *"Que los datos superen la RAM no obliga por sí solo a distribuir."* (Hadoop)
- *"La localidad reduce tráfico; no elimina la comunicación entre etapas."* (shuffle)
- *"Agregar reducers no divide automáticamente el trabajo de una misma clave."* (skew)
- *"Un servicio administrado reduce parte del trabajo de infraestructura; el diseño del procesamiento
  sigue siendo necesario."* (EMR)

## Herramientas y versiones usadas en el curso

| Herramienta | Uso | Versión/nota |
|-------------|-----|--------------|
| **SQLite** | motor de filas del benchmark | 3.53.4 (vía `sqlite3` de la stdlib) |
| **DuckDB** | motor columnar del benchmark | 2.0.0 |
| **Apache Airflow** | orquestación por tareas | **3.3.2** con `uv` y Python **3.12**; `airflow standalone`, `localhost:8080` |
| **Dagster** | orquestación por assets | `uvx create-dagster@latest`, Python **3.10+**; `dg dev`, `localhost:3000` |
| **pandas / Polars** | transformación en la Actividad 2 | recomendadas por el profesor |
| **Parquet** | formato columnar de archivo | el formato por defecto del Lake/Lakehouse |

## Referencias externas citadas en clase

- **Google File System** (2003) y **MapReduce** (2004): las publicaciones que originaron Hadoop.
- **Apache Hadoop** (HDFS, YARN, MapReduce, Hadoop Common): proyecto Apache desde 2008.
- **Delta Lake** y **Apache Iceberg**: formatos de tabla abiertos; **Apache Hudi** mencionado.
- **Apache Airflow**: <https://airflow.apache.org>; constraints en
  `raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.12.txt`.
- **Dagster**: <https://dagster.io>.
- **Cloudera** y **Amazon EMR**: plataformas de gestión y procesamiento administrado.
- Servicios nombrados: S3, Azure Blob Storage / ADLS Gen2, Google Cloud Storage, Athena, Presto /
  Starburst, Databricks SQL, Snowflake, ClickHouse, Redis, DynamoDB, MongoDB, DocumentDB, Neptune,
  Neo4j, Timestream, InfluxDB, TimescaleDB, pgvector, Milvus, Weaviate, Qdrant, dbt, Airbyte,
  AWS Glue, Lakeflow Jobs.
