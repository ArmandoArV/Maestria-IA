# Clase 02. ETL y Orquestación: de los datos al pipeline

**INF3862**, Prof. Sebastián Hagedorn. Fuente: `Presentaciones/Clase02.pdf` (55 láminas).

**Recorrido de la clase:** Fundamentos de ETL · Apache Airflow · Dagster · Comparación y ecosistema ·
Actividad práctica.

**Motivación:** las organizaciones tienen data **estructurada y no estructurada**, de muchos tipos y
formatos. Ejemplo guía:

| Tienda física | Tienda web | Negocio |
|---------------|------------|---------|
| ventas en CSV | pedidos en una API | **una** cifra de ventas |
| fechas día/mes/año | fechas ISO y estados | **mismas reglas para todos** |

> **Datasets sin procesar requieren un proceso de ETL para ser consumidos por el negocio.**

---

## 1. ETL: extraer, transformar y cargar

```
Extract (obtener datos) → Transform (preparar y validar) → Load (guardar salida)
```
- **Entrada:** fuentes operacionales, archivos y servicios.
- **Salida:** datos preparados para consultas, reportes y modelos.
- > **ETL convierte datos de distintas fuentes en información utilizable.**

---

## 2. Extract: ¿cómo sabemos qué traer?

*Ayer copiamos los pedidos. Hoy el origen cambió.* Tres estrategias:

| Estrategia | Mecánica |
|------------|----------|
| **Update notification** | el origen avisa: "cambió el pedido 101" |
| **Incremental** | consultamos: "¿qué cambió desde mi última lectura?" |
| **Full** | copiamos **todos** los pedidos incluidos en el alcance |

> **La estrategia depende de qué cambios puede informar o identificar el origen.**

### Cómo llegan los datos y cómo los leemos
| Acceso | Ejemplo de llegada y lectura | Qué debemos acordar |
|--------|------------------------------|---------------------|
| **API por HTTPS** | consultar pedidos; interpretar JSON | token, páginas y límite de solicitudes |
| **SFTP** | el proveedor deja un CSV cada noche | horario, nombre y archivo completo |
| **Base de datos** | consultar tablas mediante SQL | permisos y **carga sobre el origen** |
| **Bucket o carpeta** | detectar y leer CSV/JSON/Parquet | ruta, formato y **archivos ya leídos** |
| **Eventos o cola** | consumir mensajes de cambios | **posición de lectura** y duplicados |

### Update notification
```
Pedido 101 cambia a pagado → Notificación "cambió el 101" → Extractor consulta el 101
```
- Ejemplo: **webhook**, la tienda web envía un aviso a nuestro endpoint cuando cambia un pedido.
- **¿Qué contiene el aviso?** Puede incluir **solo el ID** o también los datos del cambio → *hay que
  revisar el contrato*.
- > **¿Y si el aviso llega dos veces o no llega?** Necesitamos **deduplicar** y poder **recuperar**
  > cambios.

### Incremental
Última lectura confirmada: **10:00**.

| Pedido | Última modificación | ¿Lo extraemos? |
|--------|---------------------|----------------|
| 101 · pagado | 10:05 | **sí**: cambió su estado |
| 102 · nuevo | 10:08 | **sí**: fue creado |
| 103 · sin cambios | 09:40 | **no**: ya lo teníamos |

```sql
WHERE updated_at > :ultima_lectura
```
- **Leemos cambios, no solo filas nuevas.** Pregunta abierta de la clase: *¿cómo detectaríamos un
  pedido **borrado** del origen?* (un `updated_at` no lo revela).
- Reglas de operación: **guardar el punto de control tras persistir la extracción**; **resolver
  empates de timestamp** y **cambios tardíos**.

### Full
| Copia de ayer | Copia de hoy | Diferencia |
|---------------|--------------|------------|
| 101 · pendiente | 101 · pagado | **actualizado** |
| - | 102 · nuevo | **nuevo** |
| 103 · pagado | - | **ausente** |

- Comparar copias detecta diferencias **si ambas cubren el mismo alcance y están completas**.
- Adecuado para una **carga inicial** o **fuentes pequeñas**. Releer todo **aumenta transferencia y
  carga del origen**.
- **No siempre es necesario comparar:** también podemos simplemente **reemplazar el snapshot**.

---

## 3. Transform: preparar los datos para su destino

```
Datos extraídos → copia en staging → reglas (limpiar e integrar) → datos preparados
```
- **Transformaciones básicas:** limpiar errores y duplicados; unificar formatos y unidades.
- **Transformaciones avanzadas:** calcular, cruzar, separar y resumir datos **según el negocio**.
- > Pregunta guía: *¿qué significa cada campo y qué necesita el análisis que vamos a construir?*

### 3.1 Limpiar y deduplicar: ¿error o dato válido?
| Dato recibido | Decisión | Resultado |
|---------------|----------|-----------|
| Estado: `" PAGADO "` | quitar espacios y normalizar | `"pagado"` |
| Cantidad: vacía | **marcar para revisión** | **no asumir cantidad = 0** |
| Línea 101/1 recibida dos veces | misma clave y contenido: conservar una copia | una línea 101/1 |
| Dos líneas con el mismo precio | **distintas claves**: conservar ambas | **dos ventas válidas** |

> **Un valor vacío no siempre significa cero. Dos filas parecidas no siempre son duplicados.**

### 3.2 Estandarizar
| Origen A | Origen B | Formato común |
|----------|----------|---------------|
| `05/11/2026` | `2026-11-05` | fecha: `2026-11-05` |
| `1 kg` | `1.000 g` | masa en kg: `1` |
| `"25.000"` | `"25000"` | entero: `25000` CLP |
| `"PAGADO"` | `"paid"` | estado: `"pagado"` |

> *¿`03/04/2026` es 3 de abril o 4 de marzo?* **Necesitamos conocer la convención del origen.**
> También se acuerdan **codificación de caracteres, separadores decimales y zonas horarias**.

### 3.3 Derivar (calcular nuevas columnas)
Una fila = una línea de pedido; importes en CLP.

| Línea | Cantidad | Precio unitario | Importe |
|-------|----------|-----------------|---------|
| 101/1 | 2 | 12.000 | 24.000 |
| 101/2 | 1 | 25.000 | 25.000 |

**Importe = cantidad × precio unitario.**
> *¿El precio incluye impuestos? ¿Aplicamos descuentos?* **La fórmula necesita una regla de negocio.**

### 3.4 Joining (cruzar)
Línea de venta (producto 10, importe 24.000 CLP) **JOIN por `producto_id`** con el catálogo
(producto 10 → categoría *Accesorios*) → venta enriquecida.
> **¿Qué pasa si el catálogo tiene dos filas para el producto 10? El join puede duplicar la venta.**
> Hay que **definir la cardinalidad esperada** y qué hacer **cuando no existe coincidencia**.
> *Cruzar datos y sumar importes son operaciones distintas.*

### 3.5 Splitting (separar un campo)
El origen define un código `sucursal-año-pedido`: `SCL-2026-00101` → sucursal `SCL`, año `2026`,
pedido `00101`.
> **Separar funciona si conocemos la estructura.** *¿Qué haríamos si falta una parte del código?*
> Un **nombre completo** no siempre se separa correctamente por espacios. **Conservar el original
> ayuda a revisar errores.**

### 3.6 Resumir (cambiar el grano)
| Antes: una fila por línea | Después: cliente y día |
|---------------------------|------------------------|
| Ana · 05/11 · 24.000 | **Ana · 05/11 · 49.000** |
| Ana · 05/11 · 25.000 | |
| Luis · 05/11 · 12.000 | **Luis · 05/11 · 12.000** |

Agrupar por cliente y fecha; sumar importes.
> **Cambiamos el grano:** el total permite analizar ventas, pero **ya no muestra cada producto
> comprado**. Supuesto: solo ventas válidas y misma moneda. *El gasto acumulado de un período no
> equivale por sí solo al CLV.*

### 3.7 Cifrar campos sensibles antes de cargar
Dato sensible (correo del cliente) → **cifrado con una clave** → destino (texto cifrado).
- **Uso autorizado:** recuperar el correo **requiere acceso a la clave** de descifrado.
- **Decisión del pipeline:** *¿el análisis necesita el correo original o basta con un identificador
  de cliente?*
- > **Cifrar protege el contenido; también debemos controlar quién accede a los datos y a las
  > claves.** *Ocultar caracteres, aplicar un hash y cifrar son técnicas diferentes*: elegir según
  > el uso que tendrá el dato.

---

## 4. Load: publicar los datos preparados

```
Datos preparados → carga (escribir y validar) → destino (listo para consultar)
```
Dos ejes de decisión:
- **¿Cuánto cargamos?** **Full** (el conjunto completo) o **incremental** (los cambios).
- **¿Cuándo cargamos?** **Batch** (en lotes periódicos) o **streaming** (de forma continua).
- > Elegimos **qué escribir, con qué frecuencia y cuándo estará disponible** para consultar.

### Full load
Destino vacío → preparar **todo el alcance** → cargar y validar **una nueva versión** → publicar
datos completos.
> **Si repetimos una carga full, ¿reemplazamos la versión anterior o duplicamos el historial?**
> Habitual en la carga inicial; también permite **reconstruir** conjuntos. Hay que **definir cómo
> reemplazar sin exponer resultados parciales**.

### Incremental load
El destino ya tiene 101 y 103; llega un lote.

| Cambio recibido | Acción en destino | Resultado |
|-----------------|-------------------|-----------|
| 101 pasa a pagado | **actualizar** por clave | 101 queda pagado |
| 102 es nuevo | **insertar** si no existe | se agrega 102 |
| 103 tiene marca de borrado | aplicar la **política de borrado** | marcar inactivo o eliminar |

> **Incremental no significa solo agregar filas: también puede actualizar o borrar.**
> **UPSERT / MERGE** permite insertar o actualizar según la clave. *Una fecha de creación no detecta
> todos los cambios.*

### Batch incremental
`10:00–10:15` reunir cambios → `10:15` procesar el lote → tras confirmar, publicar cambios.
- Ejemplo: dashboard de ventas que **actualiza cada 15 minutos**; mientras espera, **muestra la
  última carga publicada**.
- **Decisiones del lote:** *¿qué ventana procesamos? ¿cómo recuperamos un fallo? ¿y los cambios
  tardíos?*
- > **Batch no exige detener el negocio:** necesitamos una **lectura consistente** y una
  > **publicación controlada**. La frecuencia se elige según **frescura requerida, costo y capacidad**.

### Streaming incremental
Evento (pedido 101 pagado) → pipeline continuo → destino actualiza el 101.
- Caso: **seguimiento de pedidos**, reflejar cambios con poca demora, sin esperar el lote.
- **Desafíos:** eventos **repetidos o fuera de orden**, reinicios y recuperación, **capacidad del
  destino**.
- > *Si llega "pagado" y luego un evento antiguo "pendiente", ¿con qué estado nos quedamos?*
- Puede implementarse con **microlotes**. Se elige por **latencia y capacidad**; **no está limitado a
  volúmenes pequeños**.

### Cargar bien: repetir sin duplicar
| Situación | Decisión de carga |
|-----------|-------------------|
| el lote se confirma pero perdemos la respuesta | **reintentar con claves y escrituras idempotentes** |
| fallamos tras escribir parte del lote | **recuperar o revertir antes de publicar** |
| el dashboard consulta durante la carga | usar una **transacción** o publicar una **versión validada** |
| la carga termina sin errores técnicos | **revisar claves, conteos e importes esperados** |

> **Idempotencia:** repetir la misma carga produce el **mismo estado final**.
> **Confirmar el avance después de persistir** los cambios de forma durable. *La recuperación depende
> de las garantías del sistema.*

---

## 5. Qué ganamos con ETL, y ETL vs. ELT

**Beneficios:**
- **Calidad e integración:** reglas compartidas; fuentes comparables; errores identificables.
- **Automatización y confianza:** menos preparación manual; procesos repetibles; origen y cambios
  documentados.
- > **El beneficio depende de definir y verificar las reglas del negocio.**

| ETL | ELT |
|-----|-----|
| Extraer → **Transformar** → Cargar | Extraer → Cargar → **Transformar** |
| preparar **antes** de cargar al destino analítico | conservar datos extraídos y transformar **en el destino** |
| útil para entregar **estructuras ya validadas** | útil para **aprovechar el cómputo del destino** |
| la transformación usa un **entorno previo** | el destino **debe poder procesar y gobernar** los datos |

> **La elección depende del destino, el volumen, la privacidad y la necesidad de reprocesar.**

---

## 6. Apache Airflow

**Plataforma open source para desarrollar, programar y monitorear workflows definidos en Python.**
- **Desarrollar:** definir tareas y dependencias **como código**.
- **Programar:** iniciar ejecuciones por **horario, eventos o de forma manual**.
- **Monitorear:** ver **estados, historial y logs** desde una interfaz web.
- > Podemos coordinar un ETL, **entrenar un modelo** o ejecutar un proceso con un **LLM**. Desde un
  > entorno local hasta una ejecución distribuida, según la configuración.

### Orquestación = coordinar la ejecución
```
Extraer ventas → Transformar ventas → Cargar ventas
```
- **Dependencias:** transformar **cuando termine** la extracción; cargar **si las validaciones pasan**.
- **Operación:** programar ejecuciones; **reintentar, registrar y alertar**.
- > **Airflow coordina el trabajo; cada tarea procesa datos o invoca otro sistema.** (Distinción
  > clave: el orquestador **no es** el motor de procesamiento.)

### Workflows como código
| Propiedad | Ejemplo concreto |
|-----------|------------------|
| **Dinámico** | generar tareas para **cada sucursal** a partir de una configuración |
| **Extensible** | usar **operadores** existentes o escribir una operación propia |
| **Flexible** | parametrizar una consulta con la fecha del intervalo mediante **plantillas Jinja** |
| **Versionable y comprobable** | revisar cambios en **Git** y **probar la lógica** antes de ejecutar |

> Si cambiamos la regla de un pipeline, **podemos revisar quién la cambió, cuándo y por qué**.

### El DAG
**DAG = grafo dirigido sin ciclos.** Partes en nuestro ETL:

| Elemento | En nuestro ETL |
|----------|----------------|
| **Schedule** | ejecutar todos los días |
| **Tasks** | extraer, transformar y cargar ventas |
| **Dependencias** | transformar depende de extraer **correctamente** |
| **Callbacks** | invocar una acción al terminar con éxito o fallar |
| **Parámetros operativos** | definir **reintentos** y **tiempos máximos** |

> *¿Qué ocurriría si **cargar** dependiera de sí misma?*, no sería un DAG (habría un ciclo).

### Por qué Airflow en ETL y ELT
| Capacidad | En nuestro pipeline de ventas |
|-----------|-------------------------------|
| **Agnóstico a herramientas** | coordinar una API, archivos, Python y un warehouse |
| **Extensible** | usar integraciones existentes o crear operaciones propias |
| **Dinámico** | adaptar las tareas a los archivos que llegan en cada ejecución (Jinja) |
| **Escalable** | repartir tareas entre **workers**, con límites de concurrencia |

> En **ETL** coordina transformar antes de cargar; en **ELT**, cargar antes de transformar en el
> destino. **Escalar exige recursos y configuración:** también limitan **la base de metadatos** y los
> **sistemas externos**.

### Datasets / assets: ejecutar cuando los datos están listos
```
DAG de ingesta (publica ventas) → [ventas_preparadas] → DAG de análisis (actualiza reporte)
```
- **Solo por horario:** ejecutar el reporte a las 03:00 → *¿qué pasa si la ingesta se demora?*
- **Basado en datos:** programar el DAG consumidor **a partir de la actualización declarada por el
  productor**.
- > **La tarea productora debe declarar el asset y terminar correctamente** para registrar su
  > actualización.

### Object Storage
`ObjectStoragePath` ofrece una API **similar a `Path`** para trabajar con **S3, GCS o Azure Blob**.
```
Extraer (escribe ventas.parquet) → bucket compartido → Transformar (lee por su ruta)
```
> **Los datos quedan en el almacenamiento compartido; entre tareas pasamos su referencia**: la
> siguiente tarea abre esa ruta **aunque se ejecute en otro worker**.

### Conceptos principales de Airflow
| Concepto | Qué representa |
|----------|----------------|
| **DAG** | grafo dirigido sin ciclos: tareas y dependencias |
| **Task** | unidad de trabajo dentro del workflow |
| **Operator** | tipo de operación; **TaskFlow** permite definir tareas con **decoradores** |
| **Dependency** | relación que condiciona el orden de ejecución |
| **Schedule** | programación de las ejecuciones |
| **DAG Run** | una ejecución concreta del DAG |

### Organizar un ETL con Airflow
`extract_sales` (leer ventas) → `transform_sales` (preparar importes) → `load_sales` (publicar tabla).
- **Una responsabilidad por tarea** → identificar **qué falló y qué debemos repetir**.
- **Datos entre tareas:** usar almacenamiento compartido y **pasar referencias** cuando el volumen es
  grande.
- > **Una `>>` expresa una dependencia; no transfiere automáticamente los datos.**

### Primer DAG
```python
from datetime import datetime, timezone
from airflow.sdk import DAG, task

with DAG("etl_ventas", schedule="@daily",
         start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
         catchup=False):

    @task
    def extract():
        print("Extrayendo ventas")

    @task
    def transform():
        print("Transformando ventas")

    @task
    def load():
        print("Cargando ventas")

    extract() >> transform() >> load()
```
> Ejemplo de **coordinación**: imprime mensajes; **todavía no mueve ni transforma datos**.

### Instalación local (entorno docente, no de producción)
Requisitos: **Python 3.12 y `uv`** · Linux o macOS · en Windows **WSL2**.
```bash
# 1. crear y activar el entorno
uv venv --python 3.12
source .venv/bin/activate

# 2. instalar e iniciar
BASE=https://raw.githubusercontent.com/apache/airflow
uv pip install "apache-airflow==3.3.2" \
  --constraint "$BASE/constraints-3.3.2/constraints-3.12.txt"
airflow standalone
```
`standalone` inicializa los componentes locales: **dejar esa terminal abierta**.

En una segunda terminal:
```bash
# credenciales generadas
cat ~/airflow/simple_auth_manager_passwords.json.generated
# crear la carpeta de DAGs y el archivo
mkdir -p ~/airflow/dags
cursor ~/airflow/dags/etl_ventas.py     # alternativa: nano
```
Abrir **`localhost:8080`**, localizar `etl_ventas`, **habilitarlo y ejecutar**; revisar **estados y
logs**.
> **Cuidar la indentación de Python:** conservar los niveles del ejemplo y **no mezclar tabs y
> espacios**. (En `nano`: Ctrl+O, Enter, Ctrl+X.)

---

## 7. Dagster

**Plataforma de orquestación con un enfoque centrado en activos de datos: *assets*.**
- **Definir:** qué datos queremos producir.
- **Relacionar:** de qué otros activos dependen.
- **Observar:** cuándo se generaron y cómo resultó la ejecución.
- > **Un asset puede ser una tabla, un archivo o un dataset que queremos actualizar.**

### Conceptos principales de Dagster
| Concepto | Qué representa |
|----------|----------------|
| **Asset** | activo de datos producido o actualizado |
| **Materialization** | evento que registra la generación o actualización de un asset |
| **Definitions** | conjunto de definiciones que carga Dagster |
| **Run** | ejecución cuyo estado y logs podemos revisar |
| **Dependencia** | relación entre un activo y los datos que necesita |

> **Materializar un asset ejecuta la lógica necesaria para producirlo.**

### Un asset puede encapsular todo el ETL
```
sample_data.csv → processed_data (leer · clasificar · guardar) → processed_data.csv
```
- **Entrada:** personas con una columna `age`.
- **Transformación:** agregar `age_group` según intervalos de edad.
- > **Tres etapas ETL no implican tres assets:** aquí el activo representa el **resultado completo**.

### Crear el proyecto local
Requisitos: **Python 3.10+ y `uv`**.
```bash
uvx create-dagster@latest project dagster-quickstart
cd dagster-quickstart
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv add pandas
dg scaffold defs dagster.asset assets.py
```
- Al crear el proyecto, **aceptar `uv sync`** para instalar el entorno.
- Archivo de assets: `src/dagster_quickstart/defs/assets.py`. **Ejecutar desde la raíz del proyecto.**

### Definir el asset
```python
from pathlib import Path
import pandas as pd
import dagster as dg

DATA = Path(__file__).parent / "data"

@dg.asset
def processed_data():
    df = pd.read_csv(DATA / "sample_data.csv")
    df["age_group"] = pd.cut(
        df["age"], bins=[0, 30, 40, 100],
        labels=["Young", "Middle", "Senior"]
    )
    df.to_csv(DATA / "processed_data.csv", index=False)
```
Crear `defs/data/sample_data.csv` con columnas `id,name,age,city`.
> Los intervalos son **(0, 30]**, **(30, 40]** y **(40, 100]**; **fuera de ellos se obtiene un valor
> faltante** (`NaN`): de ahí la pregunta de la clase: *¿qué ocurre con una edad vacía o igual a 0?*
> (edad 0 queda fuera del primer intervalo porque es **abierto** en 0).

### Materializar y verificar
```bash
dg list defs
dg check defs
dg dev
```
1. Abrir **`localhost:3000`**.
2. En **Assets**, seleccionar `processed_data` y usar **Materialize**.
3. En **Runs**, revisar estado y logs.
4. Abrir el CSV de salida y comprobar `age_group`: `28 → Young`, `35 → Middle`, `42 → Senior`.

### Ventajas y consideraciones
| Ventaja | Decisión que debemos tomar |
|---------|----------------------------|
| representación de activos | definir **qué resultado representa cada asset** |
| relaciones entre datos | **declarar correctamente** sus dependencias |
| registro de materializaciones | agregar **metadatos y comprobaciones** útiles |
| código Python e interfaz web | estructurar el proyecto y elegir **bibliotecas de procesamiento** |

> **La visibilidad de los activos complementa la revisión de las ejecuciones.**

---

## 8. Airflow vs. Dagster, y el ecosistema

| Aspecto | **Airflow** | **Dagster** |
|---------|-------------|-------------|
| Concepto inicial | **DAG y tareas** | **Assets y dependencias** |
| Pregunta de diseño | *¿qué tareas ejecutamos?* | *¿qué datos producimos?* |
| Ejecución | ejecutar un DAG | **materializar** activos |
| Observación | DAG Runs, tareas y logs | Assets, Runs y materializaciones |
| Ejemplo | Extraer → Transformar → Cargar | CSV → asset procesado |

> **Son ejemplos introductorios:** Dagster admite múltiples assets **y tareas**; Airflow **también
> dispone de capacidades orientadas a assets**. No es una oposición rígida.

### Otras herramientas del ecosistema ETL/ELT
| Herramienta | Función principal |
|-------------|-------------------|
| **dbt** | transformaciones, modelos y **pruebas** sobre datos |
| **Airbyte** | **ingesta** y replicación entre fuentes y destinos |
| **AWS Glue** | integración y procesamiento de datos **administrados** |
| **Lakeflow Jobs** | **orquestación** de workflows en Databricks |

> **Ingerir, transformar, procesar y orquestar son funciones distintas que pueden combinarse.**

---

## 9. Actividad práctica: construir un ETL local

**Elegir Airflow o Dagster y crear su propio dataset.** Individual o en parejas.

```
Extract (leer datos locales) → Transform (aplicar técnicas) → Load (guardar en local)
```
- **Herramienta:** Airflow → definir un **DAG**; Dagster → definir **uno o más assets**.
- **Foco del trabajo:** preparar datos con las **técnicas de transformación vistas en clases**. Se
  recomienda **pandas o Polars**.
- > **Lo central es la transformación:** convertir el dataset inicial en un **resultado útil**.

### Parte práctica
1. Crear un **dataset con un contexto**: ventas, inventario, clientes u otro caso de su elección.
2. Leerlo desde un **archivo local** y aplicar **una o más técnicas de transformación** vistas en
   clases.
3. Guardar el resultado en un **archivo o base de datos local**.
4. **Ejecutar el ETL desde Airflow o Dagster** y verificar el resultado.

> Ejemplo sugerido: crear ventas **con duplicados**, depurarlas y calcular el **total por producto**.

### Parte teórica (tres preguntas)
1. **Elección de herramienta:** *¿por qué eligieron Airflow o Dagster para este ETL?* Justificar
   **según el trabajo que realizaron**.
2. **Aplicación:** describir un **caso de uso visto en la práctica** donde podrían aplicar Airflow o
   Dagster. *¿Qué proceso coordinaría?*
3. **Escalamiento:** investigar **cómo** Airflow o Dagster permiten trabajar con cantidades masivas
   de datos. **Distinguir el rol del orquestador del procesamiento** y explicar **qué recursos o
   motores se necesitan**.

> **Fundamentar las respuestas e indicar las fuentes consultadas.**

### Entrega y puntaje: **1 punto en total**
| Práctica · 0,5 pt | Teoría · 0,5 pt |
|-------------------|-----------------|
| subir el/los archivos **`.py`**: DAG o assets + lógica de transformación | respuestas a las **tres** preguntas |
| adjuntar una **imagen de una run exitosa** del mismo pipeline | justificación, caso de uso y explicación del escalamiento |
| | **fuentes** de la investigación |

> **La imagen debe permitir identificar el pipeline entregado y comprobar que su ejecución fue
> exitosa.** **El proceso debe realizar un ETL real con transformación; no basta con tareas que solo
> impriman mensajes.**
