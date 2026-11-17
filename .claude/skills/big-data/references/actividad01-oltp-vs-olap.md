# Actividad práctica 1: OLTP vs. OLAP (SQLite vs. DuckDB)

**INF3862**, Clase 01. Trabajo realizado en el repo: `~/Maestria-IA/BigData/`.
Artefactos: `bench.py`, `bench_opt.py`, `graficos.py`, `resultados.json`, `resultados_opt.json`,
`graficos/*.png`. **Entrega: solo el formulario** (7 preguntas objetivas + 2 de interpretación);
**no se entrega código ni notebook**.

**Pregunta de la actividad:** *¿cómo influye el diseño de una base de datos en el rendimiento?*
**Objetivo:** relacionar **consultas, índices y organización por filas o columnas** con los **tiempos
medidos**.

---

## 1. Diseño del experimento

- **Dataset:** `ventas.csv` con **1.000.000** de registros (3 años: 2023-01 → 2025-12), 10 columnas:
  `venta_id, fecha, cliente_id, producto_id, categoria, cantidad, precio_unitario, monto_total,
  region, canal`. Categorías: Vestuario, Alimentos, Tecnología, Deportes, Hogar.
- **Los mismos datos en dos motores:**
  - **SQLite 3.53.4**: motor **de filas**, OLTP embebido.
  - **DuckDB 2.0.0**: motor **columnar**, OLAP embebido.
- **Decisión de diseño importante:** el DDL declara `venta_id` **sin `PRIMARY KEY`** para que **no
  exista un índice implícito** y poder medir el efecto del índice de forma limpia.
- **Metodología de medición** (`cronometrar()`): **2 iteraciones de *warmup*** descartadas + N
  repeticiones cronometradas con `time.perf_counter()`, reportando **media, mediana, min y max**.
  Semilla fija `random.seed(7)` y **500 parámetros pregenerados** para que ambos motores reciban
  exactamente los mismos valores.
  - `IDS` = 500 `venta_id` aleatorios (columna **única y ordenada** por inserción).
  - `CLIENTES` = 500 `cliente_id` aleatorios (columna **no ordenada**, ~10 filas por cliente).
- **Verificación de corrección:** `resultados_iguales = True`, los agregados por categoría coinciden
  entre motores (tolerancia < 1 en la suma). *Primero correcto, después rápido.*

### Las consultas
| # | Rol | SQL |
|---|-----|-----|
| **Q1** | OLTP sin índice | `SELECT venta_id, fecha, categoria, monto_total FROM ventas WHERE venta_id = ?` |
| **Q1b** | OLTP sin índice, columna **no ordenada** (extra) | igual pero `WHERE cliente_id = ?` |
| **Q2** | OLTP **con índice** | Q1 tras `CREATE INDEX idx_ventas_id ON ventas(venta_id)` |
| **Q3** | OLAP agregación | `SELECT categoria, COUNT(*), SUM(monto_total), AVG(monto_total) FROM ventas GROUP BY categoria ORDER BY total DESC` |
| **Q4** | OLAP agregación + función por fila | `SELECT strftime('%Y-%m', fecha) AS mes, COUNT(*), SUM(monto_total) FROM ventas GROUP BY mes ORDER BY mes` |

---

## 2. Resultados principales (media, ms · 1M registros)

| Consulta | SQLite | DuckDB | Gana |
|----------|-------:|-------:|------|
| **Q1** ID sin índice | **20,352** | **0,254** | DuckDB **80×** |
| **Q1b** `cliente_id` sin índice | **27,795** | **0,417** | DuckDB **67×** |
| **Q2** ID **con** índice | **0,0116** | **0,200** | **SQLite 17×** |
| **Q3** ventas por categoría | **222,556** | **1,556** | DuckDB **143×** |
| **Q4** ventas por mes | **350,744** | **4,979** | DuckDB **70×** |

| Métrica | SQLite | DuckDB |
|---------|-------:|-------:|
| Carga de 1M filas | **1,24 s** | **0,27 s** (**4,6×** más rápido) |
| `CREATE INDEX` | **0,10 s** | **0,03 s** |
| Tamaño en disco | **77,2 MB** | **22,0 MB** |

CSV original: **73,7 MB** → DuckDB ocupa **3,3× menos** que el CSV; SQLite ocupa **más** que el CSV.

### El efecto del índice (SQLite, Q1 → Q2)
**20,352 ms → 0,0116 ms = ≈ 1.750× más rápido.** Los planes lo explican:

| Sin índice | Con índice |
|------------|------------|
| `SCAN ventas` | `SEARCH ventas USING INDEX idx_ventas_id (venta_id=?)` |

- **`SCAN`** = *full table scan*: examina el millón de filas para encontrar una.
- **`SEARCH ... USING INDEX`** = descenso por el **B-tree**: unas pocas páginas.
- Plan de Q3 en SQLite: `SCAN ventas` + `USE TEMP B-TREE FOR GROUP BY` + `USE TEMP B-TREE FOR ORDER
  BY`: **un índice sobre `venta_id` no ayuda nada a una agregación por `categoria`**.
- Plan de DuckDB para la búsqueda por ID: **`Seq Scan`** con `Filters: venta_id = 500000` →
  **DuckDB también escanea**, pero su escaneo columnar + vectorizado es ~80× más rápido que el de
  SQLite. En Q2 **DuckDB no mejora** (0,200 ms): su índice **no es el camino de acceso preferido** y
  el *overhead* por consulta domina.

---

## 3. Las siete lecturas que la actividad busca

1. **Sin índice, ambos motores escanean**, pero el escaneo columnar de DuckDB es **~80× más
   rápido** que el de filas, porque solo lee las **4 columnas proyectadas** de las 10 y las procesa
   en **vectores**.
2. **El índice es la herramienta del OLTP, no del OLAP.** Convierte `SCAN` en `SEARCH` y da
   **1.750×** en la búsqueda puntual; **no sirve** para la agregación de Q3 si no cubre sus columnas.
3. **Para una búsqueda puntual, SQLite con índice gana a DuckDB (17×).** El motor de filas trae el
   registro completo de una página; es exactamente la carga **OLTP** de la Clase 01.
4. **Para agregaciones, el columnar gana por uno a dos órdenes de magnitud** (143× en Q3): **poda de
   columnas** (leer 2 de 10) + **compresión** + ejecución vectorizada.
5. **La columna no ordenada es peor** (Q1b 27,8 ms vs. Q1 20,4 ms en SQLite): `cliente_id` no tiene
   correlación con el orden físico de inserción y devuelve **~10 filas** en vez de 1.
6. **El almacenamiento también es un resultado:** 22 MB vs. 77 MB. **Menos bytes en disco = menos
   bytes leídos**: la ventaja analítica empieza en el almacenamiento, no en la CPU.
7. **Carga:** DuckDB ingiere el CSV **4,6×** más rápido porque lee el archivo de forma nativa y
   vectorizada (`read_csv`), mientras SQLite hace `executemany` fila por fila.

---

## 4. Experimento complementario: cuatro optimizaciones (`bench_opt.py`)

| Optimización | Antes | Después | Ganancia |
|--------------|------:|--------:|---------:|
| **1. Sentencia preparada** (`?`) vs. literal interpolado: SQLite Q2 | 0,0493 ms | 0,0059 ms | **8,3×** |
| **2. Índice cubriente** `(categoria, monto_total)`: SQLite Q3 | 232,66 ms | 44,24 ms | **5,3×** |
| **3. Columna `mes` materializada** (evita `strftime` por fila): SQLite Q4 | 350,94 ms | 245,94 ms | **1,4×** |
| **3b.** idem en **DuckDB** Q4 | 4,93 ms | 1,38 ms | **3,6×** |
| **4. Tabla de resumen pre-agregada** (36 filas): SQLite Q4 | 350,94 ms | 0,0127 ms | **≈ 27.700×** |

**Interpretación de cada una:**
1. **Sentencia preparada:** el literal interpolado fuerza a **re-parsear y re-planificar** la
   consulta en cada ejecución. Con parámetros `?` el plan se reutiliza. También es la defensa contra
   **inyección SQL**.
2. **Índice cubriente:** un índice sobre `(categoria, monto_total)` contiene **todas** las columnas
   que la consulta necesita → SQLite agrega **recorriendo el índice**, sin tocar la tabla. Es la
   forma de que un motor **de filas** imite la **poda de columnas** del columnar. Sigue siendo
   **5× más lento** que DuckDB sin ningún índice (44 ms vs. 1,6 ms).
3. **Columna materializada:** `strftime` se evalúa **una vez por fila** (1M veces). Precalcular `mes`
   lo elimina del camino caliente. La ganancia es **mayor en DuckDB (3,6×) que en SQLite (1,4×)**
   porque en SQLite el **escaneo** sigue dominando el costo, mientras en DuckDB el escaneo ya era
   barato y la función **era** el cuello de botella.
4. **Tabla de resumen:** el salto de **cuatro órdenes de magnitud** no viene de un motor más rápido
   sino de **no hacer el trabajo**: leer 36 filas pre-agregadas en vez de agregar 1.000.000. Es,
   en pequeño, **exactamente la idea del Data Warehouse** (§6 de la Clase 01) y de una vista
   materializada. El costo que no aparece en el cronómetro: hay que **mantenerla actualizada**.

---

## 5. Respuestas de interpretación (30 % de la nota)

### "Organización física" (filas vs. columnas)
La organización física decide **qué bytes hay que leer para responder**. En una tabla de 10 columnas,
`SUM(monto_total) GROUP BY categoria` necesita **2 columnas**: un motor **columnar** lee solo esas
dos y, al tener valores homogéneos contiguos, los **comprime** (22 MB vs. 77 MB) y los procesa
**vectorizado** → 143× en Q3. Un motor **de filas** debe traer la fila completa, incluidas las 8
columnas que no se usan. La simetría es exacta en la dirección contraria: para `WHERE venta_id = ?`
el motor de filas con índice trae el registro completo de **una** página (0,0116 ms) y gana 17× al
columnar, que **no tiene un camino de acceso puntual eficiente**. **Ningún diseño gana siempre: el
ganador lo define el patrón de acceso**, que es precisamente la distinción OLTP/OLAP.

### "Elección de plataforma"
- **Operar** (confirmar compras, descontar stock, baja latencia y concurrencia, escrituras con
  reglas de integridad) → motor **de filas, OLTP, con índices** sobre las claves de acceso: SQLite en
  este experimento, PostgreSQL/MySQL/Aurora en producción.
- **Analizar** (tendencias por mes y categoría, años de historia, agregaciones sobre muchas filas) →
  motor **columnar, OLAP**: DuckDB para una sola máquina; ClickHouse/Snowflake/BigQuery a escala.
- **Y por eso se separan las cargas:** correr Q3/Q4 (222 ms y 351 ms, escaneando 1M filas) contra la
  base operacional **compite por CPU, memoria y almacenamiento** con las consultas de 0,0116 ms de
  la aplicación: el riesgo que la Clase 01 plantea en la lámina *"¿qué pasa si compiten por los
  mismos recursos?"*. La arquitectura resultante es la de la §9 de la Clase 01: OLTP en el
  operacional, **ETL** hacia un warehouse/lakehouse, y el análisis sobre el motor analítico.

---

## 6. Advertencias metodológicas

- > **La actividad evalúa la explicación; los tiempos no deben coincidir con un valor prefijado.**
  Los números de aquí son de **una** máquina (macOS, SQLite 3.53.4, DuckDB 2.0.0) con **1M** filas:
  los **órdenes de magnitud y la dirección** de cada comparación son el resultado, no los decimales.
- **Descartar el *warmup*** es imprescindible: la primera ejecución paga caché frío de SO y
  planificación.
- **Reportar la mediana además de la media**: en Q1 el `max` (33,4 ms) es 1,8× la mediana
  (19,2 ms): hay ruido del sistema.
- **Medir el mismo trabajo:** `Q_MES` usa `strftime('%Y-%m', fecha)` en SQLite y
  `strftime(fecha, '%Y-%m')` en DuckDB (**el orden de los argumentos difiere**); si se equivoca la
  sintaxis, no se está midiendo la misma consulta.
- **No comparar con índice contra sin índice entre motores**: Q1 (ninguno tiene índice) y Q2 (ambos
  lo tienen) son las comparaciones justas.

---

## 7. Gráficos generados (`graficos/`)

| Archivo | Contenido |
|---------|-----------|
| `01_tiempos_por_consulta.png` | Q1–Q4, SQLite vs. DuckDB (escala log) |
| `02_efecto_del_indice.png` | Q1 → Q2 en SQLite: el salto de ~1.750× |
| `03_que_motor_gana.png` | qué motor gana cada consulta y por cuánto |
| `04_almacenamiento_y_carga.png` | MB en disco y segundos de carga |
| `05_poda_de_columnas.png` | columnas leídas vs. columnas de la tabla |
| `06_optimizaciones.png` | las cuatro optimizaciones de `bench_opt.py` |
| `07_ventas_por_categoria.png` | resultado de negocio de Q3 |
| `08_ventas_por_mes.png` | resultado de negocio de Q4 (36 meses) |

### Resultados de negocio (Q3)
| Categoría | Ventas | Total | Ticket promedio |
|-----------|-------:|------:|----------------:|
| Vestuario | 211.725 | $90.209.905.966 | $426.071 |
| Alimentos | 200.049 | $87.953.099.974 | $439.658 |
| Tecnología | 209.837 | $86.117.841.132 | $410.404 |
| Deportes | 196.439 | $77.153.847.934 | $392.762 |
| Hogar | 181.950 | $76.117.115.183 | $418.340 |

Q4 devuelve **36 meses** (2023-01 → 2025-12) con ~27.000–28.600 ventas y ≈ $11,5 mil millones
mensuales: distribución **uniforme por construcción** del dataset sintético (febrero más bajo por
tener menos días).
