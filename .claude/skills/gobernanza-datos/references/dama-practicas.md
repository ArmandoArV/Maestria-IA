# Clase 5 · El marco DAMA y sus prácticas en detalle

## 1. Qué es DAMA

- **DAMA** (`www.dama.org`) es un marco de trabajo que define **11 prácticas** o ámbitos de trabajo
  para la gestión de información.
- Documentado en el **DAMA Body of Knowledge (DMBOK v2)**, disponible en español.
- Existe **capítulo chileno**: `www.damachile.org`.
- Es el marco de gestión de información **más difundido en Chile**.

**Contenido del DMBOK v2:** Introducción a la Gestión de Datos · Manejo Ético de los Datos ·
Prácticas DAMA (11 capítulos) · Big Data y Ciencia de Datos · Evaluación de la Madurez de Gestión de
Datos · Organización de la Gestión de Datos y Roles · Gestión del Cambio.

### Los 7 elementos "ambientales"
- **Objetivos y Principios**
- **Procesos** (cómo lo hago): actividades, prácticas y técnicas
- **Personas** (con quiénes): organización, cultura, roles y responsabilidades
- **Tecnología**: herramientas, entregables

### Ficha de práctica
DAMA propone completar, para **cada** práctica: definición · objetivos · actividades (proceso) ·
entradas y salidas · roles (proveedores, responsables, consumidores e interesados) · métricas. Y
generar una **ficha de la práctica** (diagrama o documento).

### Lo que DAMA NO aborda (o solo parcialmente)
- Temas **legales y normativos** (propios de cada país).
- **Gestión del cambio**.
- **Cómo implementar**.

Estos tres vacíos son el aporte propio del curso.

---

## 2. Práctica 1 · Gobernanza de Datos (GD)

**Definición.** Definición de una **visión, políticas y estrategias**, alineadas a los objetivos
institucionales, orientadas a potenciar los datos como **activos organizacionales**, y las acciones
necesarias para implementarlas.

**Objetivos.**
- Definir, comunicar y guiar a la organización respecto de la visión, políticas y estrategias de
  gestión de la información (GI).
- Asegurar el cumplimiento de las definiciones mediante procesos y equipos de trabajo.
- Asegurar el adecuado funcionamiento de las prácticas de gestión de la información.
- Mejorar de manera continua la GI y sus prácticas.
- Resolver casos o problemas relativos a la GI (generalmente por escalamiento).

**Insumos.** Leyes y normativa (globales o específicas) · Plan Estratégico · Metodología (DAMA u otra),
mejores prácticas y otras experiencias.

**Productos.**
- **Misión y Visión** de la GI.
- **Estrategia**: la guía a seguir para alcanzar los objetivos.
- **Definiciones, orientaciones y estándares** que deben ser entendidos y acatados por todos.
- **Procesos de gobernanza**.
- **Roles y organización** para abordar la GI.

**Política de Gestión de Información.** Política organizacional: conjunto de definiciones y
lineamientos a observar en la toma de decisiones; debe ser **divulgada, entendida y acatada** por
todos los miembros de la organización.

**Ejemplos de misión y visión usados en clase:**
- *Misión:* promover una cultura de trabajo que valore y promueva la toma de decisiones basadas en
  evidencia (*data-driven*).
- *Visión:* ser una organización donde los datos se utilicen intensivamente para generar valor público
  dentro del marco ético, normativo y legal.

**Estrategia — las cinco preguntas.** Debe generarse desde el entendimiento de las necesidades de datos
inherentes a la estrategia organizacional:
1. ¿Qué datos necesita la organización para cumplir los objetivos estratégicos?
2. ¿Cómo se van a **obtener**?
3. ¿Cómo se van a **administrar**?
4. ¿Cómo se va a **generar información** a partir de los datos?
5. ¿De qué manera se **utilizará** esa información?

Es decir: **qué datos y cómo se cubrirá su ciclo de vida**.

**El ciclo que la gobernanza atraviesa:** Captura → Integración → Análisis → Publicación, con
**Administración** transversal, y **Gobernanza de datos** por encima de todo.

**Principios generales de la GD:**
- Los datos e información **internos y externos** serán tratados como **activos estratégicos**. Incluye
  documentos y otros contenidos digitales (imágenes, audio, video).
- Todo activo o conjunto de información será **catalogado y documentado** con variables descriptivas y
  de clasificación (**metadatos**).
- Todo activo tendrá asignado un **responsable (dueño)** que velará por su actualización y
  mantenimiento, procurando su **confiabilidad, precisión, completitud y disponibilidad**.
- Se promoverá la **digitalización**, el **uso analítico** y el **trabajo colaborativo** en torno a los
  datos.
- Se promoverá la **evaluación de la calidad** de los datos, para contar con información confiable o
  con grados de certeza conocidos.

---

## 3. Práctica 2 · Arquitectura de Datos / Información

Tres modelos **complementarios** para dar cuenta de la información global de una organización.

### 3.1 Modelo de capas (niveles de información)
| Capa | Qué es | Ejemplos |
|------|--------|----------|
| **Información de Gestión** | Información consolidada y/o proyectada que se usa para decidir | Gestión presupuestaria, EERR, KPIs |
| **Información Operacional** | Se genera en los procesos operacionales y de apoyo; se relaciona entre sí y con los maestros | Solicitudes, trámites, compras, ventas, atención de cliente |
| **Datos maestros (base)** | Datos básicos que la organización requiere para operar | Clientes, sucursales, productos, canales, plan de cuentas |

Advertencia del curso: **no olvidar la información del entorno ni las planillas**.

### 3.2 Matriz proceso × nivel de información
Se abre por procesos para ver **dónde falta información**:

| Proceso | Datos Maestros | Información Operacional | Información de Gestión |
|---------|----------------|--------------------------|-------------------------|
| Ventas | Clientes, Sucursales, Productos | Transacciones de ventas | Totales mensuales por cliente, sucursal, producto |
| … | … | … | … |

Se puede construir la matriz de **lo existente vs. lo deseado** para identificar **gaps**, midiendo
cobertura por proceso y cobertura por nivel de información.

### 3.3 Modelo de dominios
- La información se describe por los **dominios (temas) y subdominios** que aborda.
- Sirve para **clasificar**: representa una **taxonomía** (ciencia de la clasificación).
- **No** necesariamente es una partición (un dato puede pertenecer a más de un dominio).
- Debe ser **comprensible y orientada al negocio**.
- Debe abordar al menos información de base (maestros), operacional y de gestión, y cubrir también la
  **información externa** de entrada y salida.
- Es **evolutiva**.

*Ejemplo de clase:* Nueva Educación Pública (NEP), Ley 21.040 de nov-2017, implementación a 8 años, 70
Servicios Locales de Educación Pública, coordinada por la Dirección de Educación Pública (DEP).
Dominios de nivel 1: Estudiantes y Párvulos · Directivos, Docentes y Asistentes de la Educación ·
Establecimientos Educacionales · SLEPs y Sostenedores Municipales · DEP.

### 3.4 Modelo de plataforma
Conceptualiza las componentes (**no solo tecnológicas**) de la "plataforma de datos". Sirve para la
implementación y debe cubrir todo el ciclo de vida, de la captura a la publicación:

Captura de datos (internos y externos: ERP, RRHH, CRM, apps cloud, archivos) → **Integración y carga
(ETL)** → Capa Operacional → Capa de Gestión (DW/DM/ODS) → Análisis y Publicación (dashboards,
análisis, reportes, analítica, publicar/compartir).

### 3.5 Tecnologías que almacenan información
- **Bases de datos** — datos estructurados y relacionados entre sí (modelo).
- **Gestor documental** — orientado al manejo de documentos y contenido.
- **Data lake** — repositorio centralizado con datos de varias fuentes en formato **granular y sin
  procesar**; admite estructurados, semiestructurados y no estructurados, lo que permite conservarlos
  en un formato más flexible para usos futuros. Al guardar, asocia **identificadores y etiquetas de
  metadatos** para extraerlos más rápido.

---

## 4. Práctica 3 · Modelamiento y Diseño de Datos

> **Arquitectura: visión global. Modelo de datos: visión detallada.**

El modelo ayuda a entender el detalle de cómo se estructuran los datos; sirve para construir las bases
de datos y los sistemas, y después como **documentación**.

### Técnicas tradicionales
- **Entidad-Relación** — entidades y relaciones. Es el más usado.
- **Dimensional (cubo)** — hechos (*fact*) y dimensiones.
- **Taxonomía** — clasificación jerárquica (documental/contenido).

En general se definen **antes** de almacenar la información.

**Entidad-Relación en detalle.** Las entidades representan objetos de la realidad (datos referenciales,
maestros u operacionales); las relaciones representan vínculos de información. Se representa como un
diagrama más la descripción de entidades y atributos. Sirve para bases operacionales y de gestión.
Las bases relacionales requieren buena definición de tablas y **especialmente de las relaciones** para
asegurar integridad: columnas con **tipo de dato**, obligatorias u opcionales (NULL/NOT NULL), **llave
primaria** (evita duplicados) y **llaves foráneas** (evitan información inconsistente). El beneficio es
que esto se **declara** y la base se encarga de que se cumpla; una planilla puede tener estructura
similar pero es mucho más difícil garantizar la integridad.

**Dimensional (cubo).** Variante del E-R basada en una o más entidades "de hechos" y dimensiones.
Adecuado para **análisis** de información (OLAP).

### Técnicas no relacionales (NoSQL)
Más flexibles; en algunos casos **no requieren** definición completa previa (*schemaless*), pueden
crecer dinámicamente y soportan datos (números, fechas, texto) y binarios (documentos, imágenes, audio,
video).

| Modelo | Idea | Fuerte en | Débil en | Ejemplos |
|--------|------|-----------|----------|----------|
| **Llave-Valor** | Los datos se asocian a una llave única | Consultas/procesos masivos con filtro por clave | — | — |
| **Columnar** | Almacenamiento por columnas, asociadas a una llave | Consultas masivas con filtros por columnas | Consultar **un** registro | Sybase IQ, Amazon Redshift, Google BigQuery |
| **Objetos/Documentos** | Estructura jerárquica flexible de nodos; XML o JSON | Consultas masivas por clave **y** consultar un objeto | — | MongoDB, Amazon DocumentDB |
| **Grafos** | Nodos y relaciones | Datos altamente conectados | — | — |

> *"You Still Need a Model!"* — se sigue requiriendo modelar, pero cambia la **forma** (nuevas
> técnicas) y a veces el **momento** (modelado a posteriori).

**Práctica: Modelamiento y Diseño de Datos.**
- *Definición:* generación de modelos y diseños conceptuales, lógicos y físicos que permiten
  implementar los requerimientos de información del negocio según la arquitectura definida.
- *Objetivos:* entendimiento común entre negocio y tecnología; formalizar los requerimientos del
  negocio y de implementación; documentar la estructura conceptual, lógica y física.
- *Actividades:* definir políticas, estándares, técnicas y herramientas · generar los modelos ·
  actualizarlos ante cambios · auditar calidad y vigencia · implementar medidas correctivas y
  retroalimentar.
- *Herramientas citadas:* Erwin (E-R), TOAD (E-R), Moon Modeler (MongoDB y NoSQL).

---

## 5. Práctica 8 · Datos Maestros y Referenciales

| | **Datos Maestros** | **Datos Referenciales** |
|---|---|---|
| Qué son | Constitutivos o centrales de la organización | Internos o externos, usados **exclusivamente** para caracterizar o relacionar otros datos |
| Forma típica | Entidades del negocio | Códigos + descripción |
| Identificación | **Subjetiva** (se declaran) | **Objetiva** |
| Modificación | Afectados por transacciones | Esporádica |
| Ejemplos | Clientes, funcionarios | Regiones, comunas, códigos de clasificación |

Son centrales para obtener **"visión 360°"**.

**Problemas típicos:**
- Múltiples valores que llevan a **inconsistencias**. Ej.: varias versiones de un código de
  clasificación generan problemas al totalizar.
- Datos de personas (nombre, mail, dirección) en múltiples bases: ¿cuál es la información "correcta" o
  la "actual"?

**Gestión:** centralizada o mediante réplicas que aseguren consistencia. Existen herramientas de
**Master Data Management (MDM)** (Powerdata, TIBCO, etc.).
- Con múltiples valores de datos **maestros** hay que **conciliarlos** (de varias direcciones,
  seleccionar una como la actual: ¿la más reciente?, ¿la que se repite más?).
- Con múltiples valores de datos **referenciales** hay que **estandarizarlos**: que todos los sistemas
  tengan la misma versión de los códigos, o que estén centralizados.
- Definir **procedimientos de cambio** consistentes y asegurar la **difusión** de los cambios.

*Definición de la práctica:* procesos para asegurar la consistencia de datos comunes (internos o
externos) entre distintas aplicaciones o plataformas. *Objetivos:* identificar y gestionar los datos
comunes y su utilización; habilitar y promover su **uso compartido**.

---

## 6. Práctica 10 · Metadatos

- Son **datos que describen otros datos**: datos estructurados y codificados que describen
  características que sirven para **identificar, describir, buscar y administrar** los datos.
- Pueden ser a nivel de grupos de datos o de datos individuales.
- Metadatos básicos de un dato: **nombre, descripción, tipo de dato, valores posibles**.
- Un **modelo de datos** es un metadato que describe un conjunto de datos; un **diccionario de datos**
  también.
- **Estándares** (complejos): ID3, Dublin Core, RDF (Resource Definition Framework), OWL (Web Ontology
  Language).

**Vocabulario controlado** para garantizar uniformidad y compatibilidad:
- **Taxonomía** (gr. *taxis* 'ordenamiento' + *nomos* 'norma'): clasificación ordenada y jerárquica.
- **Ontología** (gr. *ontos* 'ente' + *lógos* 'estudio'): sistema de categorías que además **define las
  relaciones** entre los términos del vocabulario. Una taxonomía es una ontología en forma de jerarquía.
- **Folksonomía**: igual que la ontología pero definida **por los propios usuarios** en vez de por
  expertos. Útil en dominios específicos.

*Objetivos de la práctica:* proveer conocimiento acerca de los datos que se manejan · recolectar e
integrar metadatos de distintas fuentes · proveer un **acceso estándar** (repositorio) · asegurar la
calidad y seguridad de la metadata. Múltiples prácticas generan o manejan metadata.

---

## 7. Práctica 6 · Integración e Interoperabilidad

- **Integración:** consolida información a formatos físicos o lógicos consistentes.
- **Interoperabilidad:** capacidad de múltiples sistemas de **intercambiar** información.
- Cubre convertir, migrar, integrar, compartir y distribuir información. **Incluye el ETL de
  Analítica/BI.**

**Dificultades de la integración:**
- Falta de **estandarización** (datos maestros y referenciales).
- Falta de conocimiento y/o documentación de estructuras y contenidos (catálogos, diccionarios, modelos
  y diseño).
- Distintos **niveles de detalle** en distintas bases.
- **Datos faltantes** para el cruce (*missing link*).

**Mecanismos:** carga de archivos (básico) y procesos **ETL** (extracción, transformación y carga).

**Cuatro ámbitos de la interoperabilidad** (eje de la Ley 21.180 de Transformación Digital):
1. **Legal y normativo:** ¿puedo hacerlo? ¿debo hacerlo?
2. **Organizativo:** ¿responsables? ¿procesos?
3. **Semántico:** ¿cómo se interpretan los datos (entrada/salida)?
4. **Técnico:** ¿qué mecanismos usar?

Referencia: *Gobernanza Digital e Interoperabilidad: una guía para su implementación*, A. Nasser,
CEPAL 2019.

**Construcción de una Política de Interoperabilidad de Datos** (tres piezas):
1. **Política de anonimización** — para no identificar a la persona física en un conjunto de datos.
2. **Protocolo de actuación** — identificación de activos implicados, equipo asignado y segregación de
   funciones, realización de **EIPD**, formación e información al personal, descripción sistemática de
   los tratamientos, gestión de riesgos, análisis de cumplimiento.
3. **Adopción de medidas tecnológicas.**

Complementada con **garantías jurídicas**: acuerdos de confidencialidad y cláusulas contractuales que
garanticen la privacidad incluso ante brechas de reidentificación · compromisos de mantenimiento de la
anonimización suscritos con los destinatarios · **auditorías** del uso de la información anonimizada.

**Descripción semántica:** conocer la tipología de datos a tratar, los soportes, la duración prevista,
las tecnologías involucradas y sus aspectos funcionales, el flujo de datos y los destinatarios. Ese
nivel de detalle permite considerar desde el inicio **métodos menos invasivos**.

---

## 8. Práctica 4 · Almacenamiento y Operación

**Monitoreo y soporte** (en general bien cubierto): administración de la base de datos (DBA),
optimización (*tuning*), monitoreo de uso y crecimiento, respaldo y recuperación, seguridad a nivel de
base de datos, aplicación de parches.

**Respaldos y recuperación:** deben existir procedimientos **probados** para plataformas, aplicaciones
y bases de datos, más un **DRP** (plan de recuperación ante desastres) y un **BCP** (plan de
continuidad de negocio).

*Caso de clase (Chile, feb-2022):* falla en el sistema de Migraciones y falta de respaldo obligaron a
reconstruir datos de miles de extranjeros desde 1993 a 2021; algunos registros se recuperaron "a mano"
y no hay certeza de que se haya restaurado todo (CIPER Chile).

**Preguntas incómodas de la práctica:**
- ¿Existe un **diseño** detrás del almacenamiento de los datos?
- ¿Se **monitorean** las plataformas de datos?
- ¿Se hace planificación de crecimiento (*capacity planning*)?
- ¿Está gestionado adecuadamente el **respaldo** (interno/externo)?
- ¿Existe **DRP** y/o **BCP**?
- ¿Se han hecho **pruebas de recuperación**?

*Objetivos:* diseñar y gestionar los almacenamientos · asegurar **disponibilidad** · implementar la
seguridad en el acceso · asegurar el **desempeño** · asegurar la **integridad** (respaldo y
recuperación). Incluye los almacenamientos de Analítica/BI.

---

## 9. Práctica 5 · Seguridad de la Información

**Definición.** Conjunto de procesos, metodologías, políticas, normativas, estándares, procedimientos,
controles, software, hardware y otros elementos necesarios para mantener la **confidencialidad,
integridad y disponibilidad** de la información. *La ciberseguridad es un componente relevante de la
seguridad*, no su sinónimo.

**SGSI (Sistema de Gestión de Seguridad de la Información):**
- Se basa en la **identificación y gestión de riesgos** de seguridad.
- **No son solo temas de tecnología**, sino de los **procesos y datos** de la organización.
- Existió el PMG Seguridad de la Información (DIPRES 2010-2016), basado en **NCh ISO 27001**
  (homologación de ISO 27001). Ejemplos citados: Minsal, Aduana.

*Definición de la práctica:* definir, planear, desarrollar y ejecutar políticas de seguridad y
procedimientos para proveer **autorización, acceso controlado, autenticación y auditoría** sobre los
datos.

*Objetivos:* definir las políticas de acuerdo a las regulaciones legales de privacidad, protección y
confidencialidad, a los acuerdos contractuales y a los requerimientos del negocio · proteger la
información según esas políticas · asegurar que se **apliquen y auditen** · prevenir y gestionar los
**incidentes**.

### Proyecto de seguridad: capítulos de ISO 27001:2022
Organización · Políticas · Recursos humanos · Gestión de activos · Control de acceso · Criptografía ·
Física y entorno · Operaciones · Comunicaciones · Adquisición, desarrollo y mantenimiento de sistemas
de información · Relación con proveedores · Gestión de incidentes · Continuidad de negocio ·
Cumplimiento.

### Análisis GAP contra ISO/IEC 27002:2022
**Objetivos:** identificar el nivel de seguridad existente · analizar el Modelo de Seguridad
Corporativo · analizar las vulnerabilidades técnicas de la infraestructura crítica · definir y
planificar acciones a corto, medio y largo plazo · evaluar y priorizar las inversiones con criterio
**coste-beneficio**.

**Alcance:** procesos de negocio críticos · todo el personal · oficinas centrales y red de oficinas ·
alcance de revisión técnica.

**Cuatro fases:**
1. **Análisis de la situación actual** — documentación organizativa y del entorno; procesos y
   tecnología más críticos; aspectos regulatorios que afectan a la empresa; determinar objetivos de
   seguridad a largo plazo; definir alcance del GAP; identificar interlocutores.
2. **Diagnóstico de la situación** — elaboración del **SoA (Declaración de Aplicabilidad)** en base a
   niveles de madurez de los controles: nivel actual (**AS-IS**) y nivel objetivo (**TO-BE**).
3. **Revisión técnica (*hacking ético*)** — análisis externo (recopilación de información, análisis de
   arquitectura, análisis y explotación de vulnerabilidades) e interno (arquitectura y elementos
   funcionales, explotación y metástasis, plan de acción sobre riesgos tecnológicos).
4. **Plan de acción** — elaboración del plan, análisis coste-beneficio, planificación y desarrollo de
   fichas de proyectos.

---

## 10. Práctica 7 · Documentos y Contenido

**Gestión documental:** conjunto de normas técnicas y prácticas usadas para administrar los documentos
de todo tipo, recibidos y creados en una organización. Se preocupa de:
- Facilitar el **almacenamiento, clasificación y recuperación** de los documentos.
- Aplicar las definiciones de **seguridad** en el acceso.
- Asegurar la **preservación (custodia)** según el tiempo que deban guardarse, y **eliminar** los que
  ya no sirven.

Coexisten sistemas muy diversos: desde el registro manual de la correspondencia hasta sistemas que
manejan la documentación administrativa (papel o electrónica), controlan los **flujos de trabajo** de
tramitación de expedientes, capturan información desde bases de datos, enlazan con archivos y
bibliotecas y permiten búsquedas sofisticadas: eso es **gestión documental electrónica**.

Una estructura de carpetas compartidas es una forma básica pero carece de la funcionalidad de un gestor
documental. Algunos gestores disponibles en Chile: **Alfresco, SharePoint (MS), FileNet (IBM), ExeDoc,
Ceropapel**; la mayoría con opción cloud y on-premise.

**Implementación (secuencia):** clasificación de información → definición de políticas → definición de
metadatos → definición (o mejoras) de procesos → proyecto de implementación.

*Objetivos:* cumplir las disposiciones legales y requerimientos de manejo de documentos y contenidos ·
asegurar almacenamiento, recuperación y uso · asegurar la **integración entre datos estructurados y los
documentos y contenido**.

---

## 11. Práctica 9 · Analítica, BI y Data Warehouse

**Niveles de gestión de BI/Analítica:**
- **Operativo** — decisiones operativas, información detallada de un proceso, subproceso o actividad.
- **Táctico** — información más agrupada/consolidada a nivel de uno o más procesos.
- **Estratégico** — información global o de macroprocesos.

**Visualización:** facilita la comprensión y asimilación de la información y ayuda al análisis, pero
**no sustituye la habilidad analítica**, y **una mala visualización induce a error**.

**Dashboard / Panel de control:** herramienta que muestra visualmente indicadores (KPI), métricas y
datos. Sirve para seguir el estado de una empresa, departamento o proceso. A diferencia de un reporte,
tiene cierto grado de **interactividad**: filtro, reordenamiento y *drill* a detalle.

Tipos de gráficos citados: barras, líneas, combinados, área, torta, medidor/indicador, tabla, mapas,
burbujas, dispersión, radar, rectángulos, cascada (referencia: `www.datavizproject.com`).

---

## 12. Práctica 11 · Calidad de Datos

**Definición.** Grado de conformidad de los valores de un dato o conjunto de datos respecto de los
**requerimientos y criterios de aceptación** para su correcto y adecuado uso por parte de la
organización o el público destino. Para determinar ese grado hay que **definir previamente** esos
requerimientos y criterios, lo que es variable en el tiempo y dentro de la organización (no todos
requieren la misma calidad).

**Para controlar la calidad de manera sistemática hay que:**
1. **Evaluar** (*assess*) la calidad.
2. **Controlar** los procesos que generan la información (no siempre se puede: datos externos).
3. **Mejorar** esos procesos para asegurar el cumplimiento de la calidad requerida.

La calidad aplica tanto a los datos como a los **metadatos**. El costo de la mala calidad a veces se
mide (impacto de los errores) y muchas veces es **inconmensurable o intangible** (reputación).

**Limpieza de datos (*data cleansing*):** remover, corregir o normalizar/homogenizar datos (dejar
textos en mayúsculas, fechas en un solo formato DD/MM/YYYY). Es importante **preservar los datos
originales** y conocer el **linaje** de los datos, para saber si han sido modificados.

### Atributos de calidad
| Atributo | Significado | Ejemplo |
|----------|-------------|---------|
| **Conformidad** | Los valores son consistentes con la definición del dato | Tipo de dato |
| **Completitud** | Contienen toda la información requerida, a nivel de registro o de dato | No hay fechas faltantes; no hay nulos |
| **Validez** | Se ajustan a las especificaciones | Valores posibles, reglas de negocio |
| **Precisión** | Los valores son correctos | No hay datos fuera de rango |
| **No duplicación** | No hay registros duplicados | — |

### Estándar ISO 8000
- **General** — introducción, principios de calidad de datos, conceptos fundamentales y vocabulario.
- **Gestión de calidad de datos** — modelo de referencia de procesos y modelo de evaluación de la
  **madurez organizacional** de esos procesos.
- **Datos maestros** — intercambio de datos maestros; propone un formato específico de mensajes entre
  organizaciones.
- **Información de ingeniería** — aplicación de la calidad de datos a productos.

*Actividades (ciclo PDCA):* definir una estrategia y **Plan de Calidad** (Planear) · aplicar procesos y
técnicas a los datos en operación (Ejecutar) · medir y monitorear (Controlar) · generar e implementar
planes de mejora (Actuar).

Herramientas citadas: SAS Data Management, Talend Open Studio, OpenRefine.

---

## 13. Implementación de la Gestión de la Información

Supuesto de trabajo del curso: **implementación institucional, *top-down***.

**Etapa 1 — Definiciones:** concientización de equipos directivos · formación de equipo(s) · redacción
de la **Política de GI** · definiciones de gobernanza.

**Etapa 2 — Implementación inicial:** difusión · implementación de la gobernanza (inicial) ·
definiciones e implementación de **prácticas priorizadas** · productos iniciales · proyectos.

**Etapa 3 — Implementación y redefiniciones:** más difusión · implementación de la gobernanza ·
implementación de prácticas · revisar/actualizar políticas · productos en paralelo · proyectos.

Sobre ellas corre un **Plan Base**.

## 14. Cultura y gestión del cambio (el vacío que DAMA no cubre)

> "La cultura de la empresa es lo que hace la gente espontáneamente, cuando nadie les ve."
> — Xavier Marcet

- Muchos planes estratégicos y transformaciones digitales **se estrellan ante culturas corporativas**
  que se amarran a viejas inercias e impiden silenciosamente el cambio.
- El cambio es difícil porque **implica cambiar algo importante en cada persona**. Las personas nos
  sentimos seguras aferradas a nuestras rutinas profesionales y a nuestras fórmulas de éxito.
- Muchos proyectos de cambio cultural se basan solo en **formación**, lo que resulta insuficiente:
  **una cosa es ser formado y otra aprender**. Se aprende cuando se convierten los nuevos conceptos,
  métodos o hábitos en una **práctica personal**.
- El gran problema tiene más que ver con la **incapacidad de desaprender** que con la capacidad de
  aprender. Lo que genera miedo es dejar de hacer cosas que siempre funcionaron (pero que pertenecen a
  contextos que se desvanecieron).
- Las culturas corporativas han tenido más que ver con **explotar** negocios eficientemente que con
  **explorar** negocios innovadores.
