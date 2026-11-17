# Actividad 2: Parte Teórica (50%)

**INF3862 Big Data | Armando Arredondo Valle**
Herramienta elegida: **Dagster** (proyecto `etl-ventas`, 6 assets + 7 asset checks).

---

## 1. Elección de herramienta: ¿por qué Dagster para este ETL?

Elegí Dagster **por la naturaleza del trabajo que terminé haciendo**, no por preferencia previa.
Cuando describí mi propio pipeline, no me salió una lista de acciones sino una lista de
**resultados**: una tabla de ventas limpias, un archivo de filas en cuarentena, un resumen por
categoría y mes, y una base DuckDB publicada. Esa es exactamente la pregunta de diseño que
distingue a las dos herramientas: Airflow pregunta *¿qué tareas ejecutamos?* y Dagster pregunta
*¿qué datos producimos?*. Mi ETL se describía mejor con la segunda.

Tres cosas concretas del trabajo lo confirmaron:

**(a) El punto 4 de la actividad es "verificar el resultado", y en Dagster esa verificación es
parte del pipeline.** Escribí **7 `asset_check`** adheridos a los activos: claves únicas, importe
coherente (`importe = cantidad × precio`), estados normalizados, fechas válidas, cuadre
detalle-vs-resumen, cuadre del warehouse contra el Parquet, y un cuadre contra el manifiesto de
suciedad plantada. Cada uno es un objeto de primera clase con su propio historial y su propia
metadata en la UI (captura `04_asset_checks.png`). En Airflow habría escrito esas validaciones
como tareas más del DAG, y su resultado habría quedado en los logs: visible si uno va a buscarlo,
pero no adherido al dato ni comparable en el tiempo.

**(b) La metadata de materialización prueba que la transformación ocurrió, no solo que la tarea
no falló.** Esta es la diferencia que más me importó. Un DAG verde demuestra que ningún paso
levantó una excepción. La materialización de `ventas_limpias` publica
`filas_entrada: 2043 → filas_salida: 1978`, `T7_duplicados_por_clave_eliminados: 40`,
`T2_estados_normalizados: 1508` (de 10 formas distintas de escribir el estado a 3),
`T4_precios_con_separador_miles: 840`, `T10_ventas_sin_match_en_catalogo: 18`. Eso es evidencia
de que el dato cambió como yo quería. El profesor advirtió explícitamente que *"no basta con
tareas que solo impriman mensajes"*; la metadata de assets es el mecanismo que convierte esa
advertencia en algo comprobable desde la interfaz.

**(c) Un `@multi_asset` modela honestamente que una sola computación produce dos productos.**
Limpiar las ventas y aislar las filas no interpretables es **un solo recorrido** de los datos,
pero son **dos activos** con destinatarios distintos: `ventas_limpias` alimenta el análisis y
`ventas_cuarentena` va a revisión humana. Dagster me dejó expresarlo tal cual. En un DAG de tareas
la cuarentena habría sido un efecto secundario de la tarea de transformación: algo que existe en
el disco pero que el orquestador no sabe que existe.

A esto se suma una razón práctica menor: la instalación local es más liviana
(`uvx create-dagster` + `dg dev` en un puerto), frente a `airflow standalone` que levanta
api-server, scheduler, triggerer y dag processor.

**Dónde habría elegido Airflow.** No creo que Dagster gane siempre, y la propia clase advierte
que *"son ejemplos introductorios"*: Airflow también tiene capacidades orientadas a assets
(datasets) y Dagster también admite tareas. Habría elegido Airflow si el problema fuera
principalmente **coordinar en el tiempo sistemas heterogéneos que no producen un activo de datos**
(disparar un job en un sistema externo, esperar un archivo por SFTP, llamar a una API y gatillar
un proceso de negocio), o si el equipo **ya operara Airflow**, porque el costo de introducir un
segundo orquestador en una organización casi nunca lo paga la elegancia del modelo. Para este ETL,
cuyo producto es un conjunto de tablas, el modelo de activos describía mejor lo que estaba
construyendo.

---

## 2. Aplicación: un caso de uso donde aplicaría esta herramienta

**El caso: el benchmark OLTP vs. OLAP de la Actividad 1 de este mismo curso.**

Lo elijo porque es un proceso que ya ejecuté a mano y cuyas costuras conozco. Hoy son tres scripts
sueltos que se corren en orden y en los que el orden es puramente mental:

1. generar `ventas.csv` (1.000.000 de filas),
2. `bench.py`: cargar los mismos datos en SQLite y DuckDB, crear el índice, cronometrar Q1–Q4 y
   escribir `resultados.json`,
3. `bench_opt.py`: medir cuatro optimizaciones adicionales sobre **las bases que dejó `bench.py`**,
   escribiendo `resultados_opt.json`,
4. `graficos.py`: leer ambos JSON y producir los 8 PNG del informe.

**Qué proceso coordinaría Dagster aquí.** La dependencia real es de **datos**, no de horario:
`bench_opt.py` no puede correr antes de que existan `ventas_sqlite.db` y `ventas_duck.db`, y
`graficos.py` no puede correr sin los dos JSON. Hoy ese orden vive en mi cabeza y en el orden en
que tipeo los comandos; si corro `bench_opt.py` sobre una base vieja obtengo números que parecen
válidos y no lo son. Modelado como activos (`dataset_ventas` → (`bench_sqlite`, `bench_duckdb`) →
`resultados_benchmark` → `resultados_optimizaciones` → `graficos`), el grafo deja de depender de mi
memoria, y la materialización de cada activo registra **con qué versión de los datos y en qué
máquina** se produjo cada medición.

El valor concreto para ese caso sería:

- **Reproducibilidad de un resultado publicado.** La Actividad 1 pide explicar tiempos medidos. Si
  dos semanas después alguien pregunta por qué Q3 dio 222 ms, hoy tendría que reconstruir a mano
  qué corrí y en qué orden. Una materialización con metadata (versión de SQLite/DuckDB, nº de
  filas, fecha) responde eso sin arqueología.
- **Checks como parte del experimento.** Varias validaciones que hice a ojo son `asset_check`
  naturales: que los dos motores devuelvan **resultados idénticos** antes de comparar tiempos
  (`resultados_iguales`), que el `warmup` se haya descartado, que el plan de SQLite diga `SEARCH`
  y no `SCAN` después de crear el índice. Si una falla, el gráfico no debería publicarse.
- **Rematerialización selectiva.** Al cambiar solo `graficos.py` no hay por qué volver a cargar un
  millón de filas: se rematerializa el activo de gráficos y Dagster sabe que los upstream siguen
  vigentes.

> **Nota para quien entregue esto:** si tienes un caso de tu trabajo (un reporte que alguien arma
> a mano cada mes, una carga que se corre "cuando alguien se acuerda", un reentrenamiento de
> modelo), úsalo en vez de este: un caso propio siempre es más fuerte que uno de clase. La
> estructura de la respuesta sirve igual: **(i)** cuál es el proceso, **(ii)** cuál es la
> dependencia real entre pasos, **(iii)** qué se gana al hacerla explícita.

---

## 3. Escalamiento: ¿cómo se trabaja con cantidades masivas de datos?

### 3.1 La distinción de fondo: el orquestador no procesa los datos

La documentación de Airflow lo dice de forma explícita:

> *"Airflow is not a data streaming solution. Tasks do not move data from one to the other (though
> tasks can exchange metadata!). Airflow is not in the Spark Streaming or Storm space, it is more
> comparable to Oozie or Azkaban."*
> Fuente: [Airflow 2.0.0, *Beyond the Horizon*](https://airflow.apache.org/docs/apache-airflow/2.0.0/index.html)

Esa frase es la respuesta corta a toda la pregunta. Un orquestador **decide cuándo corre algo, en
qué orden, qué hacer si falla y deja registro de lo ocurrido**. El trabajo pesado (leer 10 TB,
hacer un join, entrenar un modelo) lo hace **otro sistema**. Es la misma separación de roles de la
Clase 03: *"YARN administra recursos, MapReduce organiza el cálculo, HDFS conserva los archivos"*,
con el orquestador una capa más arriba decidiendo **cuándo enviar** ese trabajo. La versión actual
de la documentación lo formula en positivo: *"Airflow is a platform for orchestrating batch
workflows"*, y *"Airflow itself is agnostic to what you're running - it will happily orchestrate
and run anything"*
([Overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)).

**Mi propio ETL ilustra las dos caras de esto, y conviene ser honesto con la segunda.**

Lo que sí hice bien: **los datos nunca viajaron a través del orquestador**. Cada asset escribe su
resultado en disco (`staging/`, `processed/`, `warehouse/`) y el siguiente lo lee desde ahí; entre
activos solo pasa la dependencia (`deps=[...]`), no el DataFrame. Es la lección que la Clase 02
enseña con `ObjectStoragePath`: *"los datos quedan en el almacenamiento compartido; entre tareas
pasamos su referencia"*. Airflow castiga explícitamente lo contrario: los XComs

> *"are only designed for small amounts of data; do not use them to pass around large values, like
> dataframes."*
> Fuente: [XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)

Lo que **no** escala en mi ETL: el procesamiento ocurre **dentro del proceso del orquestador**. El
cuerpo de `transformar_ventas` hace `pd.read_parquet` y opera en memoria con pandas. Con 2.043
filas es instantáneo; con 2.043 millones el worker se queda sin RAM, y **ninguna configuración del
orquestador lo arregla**, porque el problema no está en la orquestación sino en dónde se ejecuta
el cómputo. La propia documentación de Dagster marca ese límite al describir cuándo *no* usar sus
I/O managers:

> *"I/O managers may not be the best fit if: […] Your assets won't fit in memory, such as a
> database table with billions of rows."*
> Fuente: [I/O managers](https://docs.dagster.io/guides/build/io-managers)

Escalar, entonces, no es "poner Dagster más grande": es **sacar el cómputo del orquestador**.

### 3.2 Tres ejes de escalamiento, que se confunden a menudo

**Eje A: escalar la orquestación (cuántas tareas en paralelo).** En Airflow lo determina el
*executor*: el `LocalExecutor` corre las tareas *"locally within the scheduler process"* y por eso
*"shares resources with the Airflow scheduler"*, mientras que los ejecutores remotos
(`CeleryExecutor`, `KubernetesExecutor`, `EcsExecutor`) las ejecutan en workers separados,
*"decoupling workers from the scheduler process"*
([Executor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html)).
Dagster separa el mismo problema en **dos niveles**, lo que resulta más claro:

> *"The run launcher is the interface to the computational resources that will be used to actually
> execute Dagster runs."* […] *"Once execution starts within the run worker, it is the executor -
> an in-memory abstraction in the run worker process - that takes over management of computational
> resources."*
> Fuente: [Run launchers](https://docs.dagster.io/deployment/execution/run-launchers)

Es decir: el **run launcher** asigna una unidad de cómputo por *run* (`K8sRunLauncher` lanza un job
de Kubernetes, `EcsRunLauncher` una tarea de ECS) y el **executor** reparte los *steps* dentro de
ese run (`multiprocess_executor`, `k8s_job_executor` que ejecuta *"each step within an ephemeral
Kubernetes pod"*) ([Run executors](https://docs.dagster.io/guides/operate/run-executors)).

**Pero este eje aumenta el paralelismo, no la capacidad de cada tarea.** Cien workers no permiten
que una tarea procese un dataset que no cabe en la memoria de uno solo. Y tiene su propio techo:
la **base de metadatos**, que la clase ya mencionaba (*"también limitan la base de metadatos y los
sistemas externos"*) y que Airflow documenta sin eufemismos:

> *"Airflow is known for being 'database-connection hungry' - the more Dags you have and the more
> you want to process in parallel, the more database connections will be opened. […] It is a
> general consensus that if you have even medium size Postgres-based Airflow installation, the best
> solution is to use PGBouncer as a proxy to your database."*
> Fuente: [Fine-tuning your Scheduler performance](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html)

Un recurso relacionado son los **deferrable operators**: cuando una tarea solo está esperando a un
sistema externo, puede suspenderse y *"free up the worker for other processes by deferring"*, de
modo que *"the task no longer occupies a worker slot"*
([Deferrable operators](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html)).
Es la forma correcta de esperar un job de Spark de dos horas sin bloquear un worker.

**Eje B: empujar el cómputo hacia afuera (el eje que realmente resuelve el volumen).** La
herramienta canónica en Dagster es **Dagster Pipes**, cuyo propósito declarado es exactamente ése:

> *"Dagster pipes is our toolkit for orchestrating remote compute from Dagster. It allows you to
> run code outside of the Dagster process, and stream logs and events back to Dagster. This is the
> recommended approach for running Spark jobs."* […] *"the code inside the asset or op definition
> submits a Spark job to an external system like Databricks or AWS EMR"*
> Fuente: [Spark con Dagster](https://docs.dagster.io/integrations/libraries/spark)

El proceso externo *"is not required to know anything about Dagster. It can even be a process
running a different language on a remote machine"*, y devuelve *"log and metadata back to
Dagster"* por el protocolo de Pipes
([Dagster Pipes](https://docs.dagster.io/integrations/external-pipelines)). Se conserva la
observabilidad **sin** que el cómputo ocurra dentro del orquestador. En Airflow el patrón es el
mismo con otro nombre: operadores que **envían** un job a un sistema externo y esperan su
resultado.

La otra variante del mismo eje es **ELT**: en vez de transformar en Python, cargar primero y
transformar **en el destino** con SQL (dbt sobre Snowflake, BigQuery, ClickHouse o DuckDB). El
orquestador pasa a emitir SQL y vigilar el resultado; quien mueve los bytes es el motor columnar.
Es la decisión ETL/ELT de la Clase 02 leída desde el escalamiento: *"útil para aprovechar el
cómputo del destino"*.

**Eje C: partir el problema.** Dagster lo modela con **particiones y backfills**: una tabla
particionada se materializa **por rebanada** (un día, un mes) en vez de monolíticamente, lo que
permite reprocesar un período sin tocar los demás y reintentar solo lo que falló
([Partitioning assets](https://docs.dagster.io/guides/build/partitions-and-backfills/partitioning-assets)).
Airflow logra lo equivalente con el intervalo de ejecución y plantillas Jinja parametrizadas por
fecha. Conceptualmente es lo mismo que un *input split* de MapReduce: dividir el trabajo de lectura
para poder repartirlo.

Y aquí la documentación de Dagster entrega, a mi juicio, **la mejor frase de las dos herramientas
sobre esta pregunta**: dice explícitamente que cuando hay un motor de procesamiento de verdad, el
orquestador debe hacerse a un lado:

> *"if you're using a parallel-processing engine like Spark and Snowflake, you often don't need
> Dagster to help with parallelism, so splitting up the backfill into multiple runs just adds extra
> overhead. Dagster supports backfills that execute as a single run that covers a range of
> partitions, such as executing a backfill as a single Snowflake query."*
> Fuente: [Backfilling data](https://docs.dagster.io/guides/build/partitions-and-backfills/backfilling-data)

### 3.3 Qué recursos y motores se necesitan, concretamente

| Capa | Qué se necesita | Por qué |
|---|---|---|
| **Almacenamiento** | Object storage (S3/GCS/ADLS) + formato columnar (Parquet) + formato de tabla (Delta/Iceberg) | Separar almacenamiento de cómputo; el formato de tabla aporta commits atómicos, esquema y versiones (Clase 01) |
| **Cómputo** | Spark/EMR/Databricks, o un warehouse columnar (Snowflake, BigQuery, ClickHouse), o DuckDB si cabe en un nodo | Es **aquí** donde se procesan los datos, no en el orquestador |
| **Orquestación** | Workers en Kubernetes o Celery (run launcher + executor) y base de metadatos Postgres, con PGBouncer si crece | Lanzar, reintentar, registrar; su huella es pequeña **si** el cómputo está afuera |
| **Observabilidad** | Metadata de materialización, checks de calidad, linaje | Verificar el resultado, no solo que la tarea no falló |

> **Advertencia que vale la pena mantener a la vista:** no todo problema grande es un problema
> distribuido. La Clase 03 lo dice textual: *"podemos trabajar por bloques: que los datos superen
> la RAM no obliga por sí solo a distribuir"*. Antes de montar Spark y Kubernetes conviene
> comprobar si un motor columnar en una sola máquina alcanza: en la Actividad 1 de este mismo
> curso, DuckDB agregó **un millón de filas en 1,6 ms**.

### 3.4 Cómo reescribiría mi ETL para 100 millones de filas

Para cerrar con algo concreto: a escala, **el grafo de activos no cambia**, solo cambia quién hace
el trabajo.

1. **Particionar por mes.** `ventas_limpias` pasa a ser un asset particionado; cada run procesa un
   mes y un backfill reconstruye el histórico.
2. **Sacar pandas del cuerpo del asset.** La transformación se expresa en **SQL sobre DuckDB o el
   warehouse**, o se delega a **Spark vía Dagster Pipes**. El asset deja de *procesar* y pasa a
   *coordinar*.
3. **Los checks pasan a ser consultas.** `claves_unicas` deja de ser `df.duplicated()` y se vuelve
   un `SELECT ... GROUP BY ... HAVING COUNT(*) > 1` que ejecuta el motor.
4. **La carga deja de ser `CREATE OR REPLACE`.** A ese volumen se vuelve un **MERGE/UPSERT** por
   partición sobre una tabla Delta o Iceberg, para mantener la atomicidad sin reescribir todo el
   histórico en cada corrida.

---

## Fuentes consultadas

**Apache Airflow**
- *Beyond the Horizon*: "Airflow is not a data streaming solution. Tasks do not move data from one
  to the other": <https://airflow.apache.org/docs/apache-airflow/2.0.0/index.html>
  (la redacción actual, más breve, está en
  <https://airflow.apache.org/docs/apache-airflow/2.11.0/index.html>)
- *Overview / core concepts*: Airflow como orquestador agnóstico:
  <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html>
- *XComs*: "only designed for small amounts of data… do not use them to pass around large values,
  like dataframes": <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html>
- *Executor*: ejecutores locales vs. remotos:
  <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html>
- *Deferrable operators & triggers*: liberar el worker mientras se espera:
  <https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html>
- *Fine-tuning your Scheduler performance*: la base de metadatos como límite y PGBouncer:
  <https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html>

**Dagster**
- *Dagster Pipes*: invocar cómputo externo conservando scheduling y observabilidad:
  <https://docs.dagster.io/integrations/external-pipelines>
- *Spark*: "orchestrating remote compute… the recommended approach for running Spark jobs":
  <https://docs.dagster.io/integrations/libraries/spark>
- *Run launchers*: launcher (recursos por run) vs. executor (steps dentro del run):
  <https://docs.dagster.io/deployment/execution/run-launchers>
- *Run executors*: `in_process`, `multiprocess`, `k8s_job_executor`, Celery:
  <https://docs.dagster.io/guides/operate/run-executors>
- *Partitioning assets*: procesamiento incremental por rebanadas:
  <https://docs.dagster.io/guides/build/partitions-and-backfills/partitioning-assets>
- *Backfilling data*: cuándo dejar el paralelismo al motor y no al orquestador:
  <https://docs.dagster.io/guides/build/partitions-and-backfills/backfilling-data>
- *I/O managers*: cuándo NO usarlos ("assets won't fit in memory… billions of rows"):
  <https://docs.dagster.io/guides/build/io-managers>

**Material del curso**
- INF3862, Prof. Sebastián Hagedorn: Clase 01 (OLTP/OLAP, warehouse, lake, lakehouse), Clase 02
  (ETL, técnicas de transformación, Airflow y Dagster), Clase 03 (HDFS, YARN, MapReduce).
