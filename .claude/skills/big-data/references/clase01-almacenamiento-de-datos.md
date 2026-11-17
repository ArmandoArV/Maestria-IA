# Clase 01. Almacenamiento de Datos: fundamentos y aplicación

**INF3862**, Prof. Sebastián Hagedorn. Fuente: `Presentaciones/Clase01.pdf` (80 láminas).

**Recorrido de la clase:** Fundamentos · Dentro del DBMS · OLTP y OLAP · Modelos de datos ·
Rendimiento y escala · Data Warehouse · Data Lake · Data Lakehouse · Plataformas e integración ·
Break (20 min) · Actividad práctica 1.

**Pregunta motivadora:** *¿dónde guardamos los datos de una tienda?*: "Comprar ahora. Analizar
después." Hay tres familias de necesidades: **operación** (clientes, productos, compras),
**contenido** (fotos, documentos, navegación) y **análisis** (ventas históricas, dashboards,
predicciones). La pregunta del curso es si **una misma solución sirve para todas**. La respuesta que
desarrolla la clase es que no: cada necesidad tiene un patrón de acceso distinto y conviene
separarla.

---

## 1. Qué es una base de datos

**Una colección organizada de datos almacenados electrónicamente.** Tres grados de estructura:

| Tipo | Ejemplo de la clase | Característica |
|------|---------------------|----------------|
| **Estructurados** | tabla de clientes (ID · Nombre · Ciudad) | esquema fijo, filas y columnas |
| **Semiestructurados** | eventos JSON | claves y valores, estructura variable |
| **No estructurados** | fotos y audio | contenido multimedia sin esquema |

Operaciones básicas: **Leer · Crear · Actualizar · Eliminar** (CRUD).

Ejemplo guía de toda la clase: `clientes` (1·Ana, 2·Pedro), `productos` (101·Notebook, 102·Mouse) y
`compras` (1001·Ana·Notebook, 1002·Pedro·Mouse). Consulta: *¿qué compró Ana?* Actualización:
*descontar una unidad del stock*. **Podemos comenzar con archivos**: la pregunta es qué pasa
cuando compran miles de personas a la vez.

### Base de datos vs. DBMS
```
Aplicaciones y usuarios  →  DBMS (consultas y reglas)  →  Base de datos (información)
```
- **Base de datos:** la colección almacenada.
- **DBMS:** el software que la administra.
- **Clave:** el DBMS **abstrae los detalles del almacenamiento físico**.

### El problema que justifica un DBMS
> Queda **una** unidad. Llegan **dos** compradores. Ana lee stock = 1 e intenta comprar; Pedro lee
> stock = 1 e intenta comprar. **1 unidad ≠ 2 ventas.**

Hay que **coordinar las operaciones y preservar las reglas**. Administrar implica mucho más que
guardar:

| Necesidad | Capacidad del DBMS |
|-----------|--------------------|
| Encontrar y organizar | consultas · esquemas · metadatos |
| Compartir sin romper reglas | integridad · transacciones · concurrencia |
| Responder a tiempo | índices · caché · optimización |
| Proteger y recuperar | permisos · respaldos · recuperación |

---

## 2. Dentro del DBMS

Mapa conceptual de componentes que **colaboran** para acceder a los datos almacenados:

```
Interfaces (SQL / API)
        ↓
Query Engine  ── interpretar y ejecutar
        ↓
Storage Manager ── leer y escribir
        ↓
     Datos

Transversales:
  Esquema y catálogo    : estructuras, reglas y estadísticas
  Transaction Manager   : coordina cambios y concurrencia
```

### Esquema y metadatos
- **Esquema:** estructura de los datos (`cliente_id: INTEGER`, `nombre: VARCHAR`, `fecha: DATE`) más
  **claves y restricciones**.
- **Catálogo de metadatos:** definiciones de tablas, **índices disponibles** y **estadísticas de los
  datos**.
- Frase de la clase: *el esquema describe la estructura; los metadatos describen más que eso*. Las
  estadísticas son lo que permite al optimizador elegir un plan.

### Storage Manager
Del registro solicitado al dispositivo, pasando por **caché e índices** y luego **archivos y
almacenamiento**. Tres funciones:
- **Organizar**: ubicar registros y páginas.
- **Reducir trabajo**: reutilizar memoria y comprimir.
- **Recuperar**: apoyar la restauración ante fallas.

### Query Engine: una consulta, varios caminos
```sql
SELECT nombre, ciudad FROM clientes WHERE edad > 25;
```
Tres pasos: **interpretar → elegir un plan → ejecutar y devolver**. Idea central:
**el mismo resultado puede requerir distinto tiempo y recursos** según el plan elegido.

### Transacciones y ACID
Una transferencia bancaria es **una unidad de trabajo**: cuenta A −$20.000 y cuenta B +$20.000.
**COMMIT** confirma; **ROLLBACK** revierte. Pregunta de la clase: *¿qué debe ocurrir si fallamos
después de descontar?*

| Propiedad | En la transferencia |
|-----------|---------------------|
| **Atomicidad** | se aplican ambos cambios o ninguno |
| **Consistencia** | se preservan las restricciones definidas |
| **Aislamiento** | se coordina la ejecución concurrente |
| **Durabilidad** | lo confirmado persiste ante fallas contempladas |

> **Advertencia de la clase:** las garantías concretas **dependen del sistema y del nivel de
> aislamiento**. ACID no es un interruptor binario.

### Seguridad y recuperación
- **Acceso:** autenticación (*¿quién eres?*) y autorización (*¿qué puedes hacer?*).
- **Protección:** cifrado y auditoría; respaldos y recuperación.
- Ejemplo: *un analista puede consultar ventas sin tener permiso para modificarlas*.

---

## 3. OLTP y OLAP

La misma tienda, dos preguntas: **durante la compra** (*¿queda stock de este producto?*) y **al
analizar el negocio** (*¿cómo evolucionaron cinco años de ventas?*). Misma empresa, **diferente
cantidad de datos y trabajo**.

Comparación del trabajo **antes de nombrarlo**:

| Registrar una compra | Analizar el historial |
|----------------------|------------------------|
| consultar disponibilidad | leer años de ventas |
| crear la compra | agrupar por mes y categoría |
| actualizar inventario | calcular totales |
| **pocos registros · lectura y escritura** | **muchos registros · agregaciones** |

**Por qué separar:** si compiten por los mismos recursos (CPU · memoria · almacenamiento), **una
consulta extensa puede afectar la respuesta de la aplicación**. Separar cargas permite optimizar
cada necesidad.

### OLTP: *Online Transaction Processing*
Mantener funcionando la aplicación.
- **Operaciones:** pequeñas y frecuentes.
- **Prioridad:** baja latencia y concurrencia.
- **Ejemplos:** compras, transferencias y reservas.
```sql
SELECT stock FROM productos WHERE producto_id = 101;
```

### OLAP: *Online Analytical Processing*
Comprender el negocio.
- **Operaciones:** lecturas amplias y agregaciones.
- **Prioridad:** procesar el análisis eficientemente.
- **Ejemplos:** tendencias, indicadores y BI.
```sql
SELECT categoria, SUM(monto) FROM ventas GROUP BY categoria;
```

| Dimensión | OLTP | OLAP |
|-----------|------|------|
| Objetivo | operar | analizar |
| Por consulta | pocos registros | muchos registros |
| Actividad típica | leer y escribir | leer y agregar |
| Prioridad | latencia y concurrencia | rendimiento analítico |

> **Son orientaciones de uso; pueden coexistir en una plataforma.** No son categorías de producto.

### Organización física: filas vs. columnas
```
Por filas                      Por columnas
101 | Notebook | 650000        101, 102
102 | Mouse    |  15000        Notebook, Mouse
                               650000, 15000
Acceder a un registro completo  Leer pocos atributos de muchas filas
```
Pregunta diagnóstica de la clase: *para sumar precios, ¿qué valores necesitamos leer?* Un motor
**columnar** puede leer **solo los atributos necesarios** (ejemplo: sumar `monto` por `categoria` en
una tabla de cinco columnas, o de cincuenta: el principio es el mismo). Esto es **poda de columnas**.

**Compresión:** los valores similares se comprimen mejor. `Ropa · Ropa · Ropa` → codificar
repeticiones → `Ropa × 3`.
- **Ventaja:** menos espacio y **menos bytes leídos**.
- **Compromiso:** codificar, descomprimir y **actualizar** también cuesta.
- > Columnar favorece **muchas** consultas analíticas; **no todas** las operaciones.
- Ejemplos de motores columnares citados: **ClickHouse · Snowflake**.

---

## 4. Modelos de datos

**Elegir un modelo empieza por la consulta.** Tres patrones de pregunta:
- **Identificar**: *¿cuál es la sesión de este usuario?*
- **Relacionar**: *¿qué personas están conectadas?*
- **Comparar**: *¿qué documentos se parecen a esta pregunta?*

> La representación debe **acompañar los patrones de acceso**.

### Relacional
Tablas conectadas por **claves**. `clientes(ID, Nombre)` ⟷ `compras(ID, Cliente, Monto)`.
Capacidades: **claves · restricciones · SQL · transacciones**.
Ejemplos: **PostgreSQL · MySQL · SQL Server · Amazon Aurora**.

### NoSQL: una familia, no un modelo
| Familia | Cómo accedemos |
|---------|----------------|
| Clave-valor | recuperar por identificador |
| Documental | consultar campos de documentos |
| Grafos | recorrer relaciones |

> **NoSQL no significa «sin estructura» ni garantías uniformes.**

- **Clave-valor:** una clave identifica un valor (`sesion:1005` → `{usuario: 25, activa: sí}`). Uso
  típico: **sesiones y accesos repetitivos**. → **Redis · Amazon DynamoDB**.
- **Documental:** documentos con campos y estructuras **anidadas**, y atributos que **varían** entre
  documentos (`{tipo: "notebook", ram: 16, disco: 512}` vs. `{tipo: "polera", talla: "M", color:
  "azul"}`). → **MongoDB · Amazon DocumentDB**.
- **Grafos:** **nodos** = entidades, **aristas** = relaciones; las relaciones son parte del modelo
  (Ana conoce→ Luis conoce→ Sofía). Consulta típica: *¿quién está a dos conexiones de Ana?* →
  **Amazon Neptune · Neo4j**.

### Series temporales
El **tiempo** organiza la consulta (`10:00:00 · A1 · 21,5`). Consulta típica: *¿cuál fue el promedio
durante la última hora?* → **Amazon Timestream · InfluxDB · TimescaleDB**.

### Vectorial
Un **modelo** produce una representación numérica (**embedding**) de un texto o imagen
(`[0.12, -0.35, 0.81]`); la consulta busca **vecinos** según una medida de similitud.
> En **RAG**, lo recuperado aporta contexto al modelo de lenguaje.

→ **PostgreSQL + pgvector · Milvus · Weaviate · Qdrant**.

### Otros modelos y fronteras que se cruzan
**Objetos** (atributos y referencias entre objetos), **jerárquico** (padre–hijo en un árbol) y
**multimodelo** (varias representaciones en un sistema). **Las categorías no son excluyentes:**
PostgreSQL es **objeto-relacional** y combina capacidades, y **JSON puede representar jerarquías**
mediante documentos anidados.

### Tabla de decisión del curso
| Necesidad | Modelo a explorar |
|-----------|-------------------|
| Pedidos y reglas de integridad | **relacional** |
| Sesión por identificador | **clave-valor** |
| Catálogo con atributos variables | **documental** |
| Eventos por dispositivo | **series temporales** |
| Caminos entre personas | **grafos** |
| Búsqueda por similitud | **vectorial** |

---

## 5. Rendimiento y escalabilidad

**Rendimiento = evitar trabajo o repartirlo.**

| Mecanismo | Qué busca reducir |
|-----------|-------------------|
| **Índices** | registros examinados para localizar datos |
| **Caché** | lecturas repetidas del almacenamiento |
| **Optimización** | trabajo de un plan de consulta |
| **Particionamiento** | datos a examinar, **si el filtro permite podar** |
| **Paralelismo** | tiempo, al repartir trabajo |

> **Cada mecanismo tiene costos; su utilidad depende de la carga.**

### Escalar
- **Vertical (*scale up*):** una máquina más capaz, más CPU, RAM o almacenamiento.
- **Horizontal (*scale out*):** más máquinas, distribuir datos o procesamiento.

Dos técnicas que **resuelven problemas diferentes**:
- **Sharding**: repartir datos: `A–M ∣ N–Z`.
- **Replicación**: mantener copias: `A–Z ∣ A–Z`.

---

## 6. Data Warehouse

**El análisis cruza sistemas operacionales.** Para responder *¿cómo evolucionaron las ventas por
región en cinco años?* hay que combinar **ventas** (compras y montos), **clientes** (personas y
regiones) y **facturación** (documentos y ajustes). Hay que **integrar datos y evitar competir con
la operación**.

Un Warehouse entrega **ventas listas para una pregunta**: datos integrados con **moneda común**
(CLP), de modo que *¿cuánto vendimos por región?* se responde directo (Norte $100.000 · Sur
$30.000).

### Arquitectura de tres capas
| Capa | Contenido |
|------|-----------|
| **Superior:** herramientas de acceso | dashboards · reporting · business intelligence |
| **Intermedia:** servidor OLAP | consultas · agregaciones · procesamiento |
| **Inferior:** almacenamiento | datos integrados · históricos · organizados |

**Alimentación:** fuentes → **ETL** → almacenamiento.

### Integración
- **Antes:** cada reporte recompone las fuentes.
- **Después:** los reportes **reutilizan** datos integrados.
- > La integración **requiere acordar qué significa cada dato**.

### ETL (visto en profundidad en la Clase 02)
**Extract** (extraer) → **Transform** (limpiar e integrar) → **Load** (cargar). Ejemplo: ventas del
día → formatos comunes → warehouse.
**Consecuencia:** la actualización puede ser **periódica** → *el dashboard puede reflejar un estado
anterior al de la aplicación*.

### Servidor OLAP
De la pregunta al resultado: **filtrar cinco años → agrupar por región → sumar ventas**. Entrada:
muchos registros del Warehouse. Salida: un total por región.
> **Un resultado pequeño puede exigir mucho procesamiento.**

### Modelado dimensional
- **Hechos de ventas:** una fila por línea de compra. **Medidas**: cantidad, monto. Más **claves a
  las dimensiones**.
- **Dimensiones:** producto (nombre, categoría), cliente (ciudad, región), fecha (día, mes, año).
- > Las **medidas** dicen *cuánto*; las **dimensiones** permiten preguntar *por qué grupo*.

### Capacidades que lo sostienen
| Componente | Función |
|------------|---------|
| Metadatos | describir tablas, atributos y significado |
| Optimización | reducir el trabajo de las consultas |
| Seguridad | controlar qué puede consultar cada usuario |
| Gobernanza | definir responsables, reglas y calidad |

### Cloud: separar almacenamiento y cómputo
Cómputo para BI + cómputo para otras cargas **sobre un almacenamiento compartido** → ajustar
procesamiento **sin duplicar necesariamente todos los datos**.

### El siguiente desafío
- **Nuevos datos:** JSON, logs, imágenes, audio.
- **Nuevas preguntas:** explorar **sin conocer aún el esquema analítico**.
- **Nuevas cargas:** Data Science, Machine Learning.
- > **Preparar toda la información antes de guardarla puede limitar la exploración.**
- Matiz importante de la clase: es una **motivación histórica**; los Warehouses modernos **también
  han ampliado sus capacidades**.

---

## 7. Data Lake

**¿Qué guardaría nuestra tienda?** CSV (ventas originales), JSON (eventos de navegación), JPG (fotos
de productos), PDF (documentos). Dos usos: **conservar** (reprocesar ventas y eventos originales) y
**explorar** (preparar datos para búsqueda o modelos).
> **Los archivos existen; todavía debemos interpretarlos y controlar su calidad.**

### Object Storage
Un **objeto** = contenido + **clave** + **metadatos** (`fotos/101.jpg`; tipo `image/jpeg`, tamaño
240 KB, producto 101). **La API recupera el objeto a partir de su clave.**
Servicios: **S3 · Azure Blob Storage · Google Cloud Storage**.

### Un bucket no basta para tener un Data Lake
| Object Storage | Data Lake |
|----------------|-----------|
| **tecnología** para persistir objetos | **arquitectura** para organizar y utilizar datos |

También necesitamos: **catálogo · permisos · calidad · procesamiento**.
> **Guardar un archivo no garantiza poder encontrarlo, entenderlo y analizarlo.**

### Almacenamiento y procesamiento son funciones distintas
- **Dónde persisten los datos:** Amazon S3 · Azure Data Lake Storage Gen2 · Google Cloud Storage.
- **Quién los procesa:** Amazon Athena · Presto / Starburst · Databricks SQL.
- **Formatos:** CSV/TSV · JSON/BSON · Avro · ORC · **Parquet**.

### Schema-on-write vs. schema-on-read
```
Schema-on-write                    Schema-on-read
definir y adaptar la estructura    guardar datos originales
          ↓                                  ↓
cargar datos preparados            interpretar al leer o procesar
```
Asociación tradicional: **Warehouse ↔ on-write**, **Lake ↔ on-read**. **No es una regla absoluta.**

Ejemplo de las tres tiendas con tres nombres para el mismo dato:

| Tienda A | Tienda B | Tienda C |
|----------|----------|----------|
| producto | product_id | item |
| precio | amount | value |
| fecha | date | timestamp |

**Al escribir:** unificar antes de cargar. **Al leer:** conservar originales y **mapear al
consultar**.

### Los problemas del Lake "a pelo"
1. **Una corrección puede quedar a medias.** Reasignar una venta entre regiones toca dos archivos:
   `A.parquet` Norte 100 → 90 y `B.parquet` Sur 30 → 40. Si falla **antes de escribir el segundo**:
   esperado 90 + 40 = **130**, mezcla 90 + 30 = **120**. *Reasignar una venta entre regiones no
   debería cambiar el total.*
2. **¿Qué versión está leyendo el reporte?** El proceso de carga agrega ventas y reemplaza archivos
   mientras el proceso de análisis lee. Tres preguntas sin respuesta: **versión** (*¿qué archivos
   pertenecen juntos?*), **esquema** (*¿monto sigue siendo numérico?*) y **calidad** (*¿se
   duplicaron ventas al reintentar?*).

> **Conservar archivos exige además coordinar cambios y lecturas.** Esto motiva el Lakehouse.

---

## 8. Data Lakehouse y Delta Lake

**Lakehouse = gestionar tablas sobre archivos.** Tres capas:
```
Motores y herramientas      SQL · Data Science · Machine Learning
Gestión de tablas           Metadatos · Esquemas · Transacciones · Versiones
Object Storage / Data Lake  Archivos de datos, por ejemplo Parquet
```
> **Archivos flexibles con tablas analíticas administradas.**

### Delta Lake
**Tecnología open source para gestionar tablas confiables sobre un Data Lake.**

Una tabla Delta combina:
- **archivos de datos**, normalmente **Parquet**;
- un **registro de transacciones**: el **delta log**.

Qué aporta: **cambios confirmados como una unidad**, **validación del esquema** y **versiones de la
tabla**.

> **Distinción que el curso subraya:** Data Lake = **repositorio** · Delta Lake = **tecnología** ·
> Lakehouse = **arquitectura**.

Vista como archivos:
```
ventas/
  parte-A.parquet   (registros)
  parte-B.parquet   (registros)
  _delta_log/       versión confirmada · archivos vigentes · esquema de la tabla
```
> Los datos guardan filas; **el log permite reconstruir el estado confirmado**.

### La corrección aparece completa en una nueva versión
| Versión 10 | Versión 11 |
|------------|------------|
| Norte 100 · Sur 30 · **Total 130** | Norte 90 · Sur 40 · **Total 130** |
| lo que ve un reporte ya iniciado | tras confirmar el cambio |

> **Preparar archivos no es publicar la versión: el *commit* hace visible el cambio.** Esto resuelve
> el problema de la corrección a medias de §7.

### Esquemas y versiones
- **Administrar el esquema:** validar tipos; autorizar cambios de columnas (ejemplo: agregar
  `descuento` **sin reinterpretar otras columnas**).
- **Conservar versiones:** identificar qué estado se consultó; volver a consultar un estado retenido.
- > **Reproducir un resultado requiere conservar metadatos y archivos de esa versión.**

### Delta Lake vs. Apache Iceberg
| Delta Lake | Apache Iceberg |
|------------|----------------|
| archivos de datos + **registro de transacciones** | archivos de datos + **snapshots y manifiestos** |
| el **log** describe cambios y versiones | los **metadatos** describen los archivos de cada estado |

Ambos son **formatos abiertos**; **los motores interpretan ese protocolo** para leer y modificar
tablas. **La compatibilidad depende del motor y las funciones utilizadas.**

### Parquet ≠ Iceberg: funciones distintas
- **Formato de archivo: Parquet:** representa datos **en columnas**.
- **Gestión de tablas: Iceberg · Delta Lake · Hudi:** organizan **archivos y cambios** (esquemas ·
  metadatos · transacciones · versiones).
- > **Un formato de tabla no es por sí solo un DBMS ni un motor de consultas.**

### Operación del Lakehouse
- **Rendimiento:** compactar archivos pequeños y organizar lecturas.
- **Retención:** decidir cuánto historial conservar.
- **Gobernanza:** gestionar accesos, calidad y responsables.
- > **El Lakehouse agrega capacidades; también requiere configuración y mantenimiento.**

---

## 9. Plataformas e integración

**Integrar herramientas también es un problema:** pipelines (mover y transformar datos), análisis
(SQL, reportes, notebooks) y operación (permisos, dependencias, modelos).
- **Riesgo:** copias divergentes y reglas de acceso separadas.
- **Necesidad:** coordinar **datos, cómputo y administración**.
- Una **plataforma integrada** reúne capacidades que deben funcionar juntas.

### Arquitectura posible para la tienda (esquema didáctico)
```
Bases operacionales          Eventos y archivos
(clientes · pedidos)        (JSON · logs · imágenes)
          ↓                          ↓
            Ingesta y transformación
          ↓                          ↓
    Warehouse                 Lake / Lakehouse
(datos integrados)      (objetos y tablas analíticas)
          ↓                          ↓
            Consumo analítico
   Dashboards · Reportes · Data Science · ML
```
> **No toda empresa necesita todas estas piezas.**

---

## 10. Actividad práctica 1: OLTP vs. OLAP

> Detalle completo del trabajo realizado y sus mediciones en
> `references/actividad01-oltp-vs-olap.md`.

**Pregunta:** *¿cómo influye el diseño de una base de datos en el rendimiento?*

- **Objetivo:** relacionar **consultas, índices y organización por filas o columnas** con los
  **tiempos medidos**.
- **Modalidad:** 60 minutos; individual o en parejas; notebook de Python preparado; **1–5 millones
  de ventas**; **los mismos datos** de ventas en **SQLite** y **DuckDB** → *observar, medir y
  explicar*.
- **Evaluación:**
  - **70 %** resultados y conceptos: **7 preguntas objetivas**, 10 % cada una.
  - **30 %** interpretación y aplicación: **2 respuestas breves** (organización física y elección
    de plataforma), 15 % cada una. Rúbrica por respuesta: **0** incorrecta o sin sustento · **1**
    parcial · **2** correcta y justificada.
  - > **Se evalúa la explicación; los tiempos no deben coincidir con un valor prefijado.**
- **Entrega:** **únicamente el formulario** (7 objetivas + 2 de interpretación). **No se entrega
  código, notebook ni archivos de resultados.** Formulario abierto hasta el **jueves 29 de octubre,
  23:59**.
