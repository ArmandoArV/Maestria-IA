# Evaluación, materiales y lecturas del curso

## 1. Normas del curso y evaluación

**Sistema de evaluación:**
- **1 trabajo grupal** (grupos de **2 o más** integrantes).
- **1 control de lectura.**

**Mecánica de entrega:**
- Las pruebas **se enviarán por email** y **se pueden entregar por la plataforma CANVAS**.
- El plazo de entrega **vence a las 24:00 horas del día indicado**.
- Se descuentan **0,5 décimas por cada día de atraso** en el envío con las respuestas.

**Fechas de recepción:**
| Evaluación | Fecha |
|------------|-------|
| **Control de Lectura** | jueves **3 de septiembre de 2026** |
| **Entrega del trabajo** | jueves **24 de septiembre de 2026** |

**Contacto del profesor:** `apumarin@uc.cl`

## 2. Material del curso

Ruta: `GobernanzaDeDatos/Presentaciones/`

### Presentaciones de clase
| Archivo | Clase | Formato |
|---------|-------|---------|
| `(2026) Clase 1 Introduccion_vf.pdf` (y `_vf-1.pdf`, duplicado) | 1 | PDF, 144 láminas |
| `(2026) Clase 2.pptx.pdf` | 2 | PDF, 96 láminas |
| `(2026) Clase 3.pdf` | 3 | PDF, 110 láminas |
| `(2026) Clase 4 .pdf` | 4 | PDF, 61 láminas |
| `(2026) Clase 5.pdf` | 5 | PDF, 194 láminas |
| `(2026) Clase 6 (1).pptx` | 6 | **PPTX**, 67 diapositivas (no PDF) |
| `(2026) Clase 7.pdf` | 7 | PDF, 103 láminas |

**Advertencias sobre el material:**
- Las clases **se solapan mucho**: la clase 2 repite buena parte de la 1, y la 4 es una versión
  reducida de la 3. Cuando dos versiones difieran en una cifra, **usa la de la clase más reciente**.
- Varias láminas arrastran **fechas y cifras de la edición 2025** del curso (los sellos "07-08-25",
  "14-08-25", "21-08-25" al pie de los enlaces de interés, y las cifras antiguas de UNCTAD e IAPP).
- Muchas láminas son **solo imágenes sin texto**: gráficos, portadas de prensa, esquemas. Si una
  respuesta depende de una figura, conviene abrir el PDF directamente.
- `Offshoring.pdf` y `Offshoring-1.pdf` son **escaneos sin capa de texto** (0 caracteres extraíbles):
  requieren OCR o lectura visual.

### Herramienta propia del profesor
**`Checklist_Auditoria_IA_Ley21719_Pumarino.docx`** — *Checklist de auditoría de seguridad y
cumplimiento de sistemas de Inteligencia Artificial*, elaborado por Pumarino (Legal & Cybersecurity),
agosto de 2026.

Integra: el *AI Security Checklist* de Cyber Defentech (traducido y adaptado), el marco de control
interno **COSO/IIA** (*Auditoría Interna de la Inteligencia Artificial aplicada a procesos de negocio*,
Fábrica de Pensamiento del Instituto de Auditores Internos de España, 2023), la guía *Auditing
Artificial Intelligence* de **ISACA** (2018, mapeo a **COBIT 2019**) y los requisitos de la **Ley N°
21.719**.

**Cómo está organizado:**
- Controles con **códigos trazables** (G-01, D-03, M-01, L-05…) para referenciarlos en papeles de
  trabajo, matrices de riesgo-control o tickets de remediación.
- **Escala de cumplimiento:** **C** (cumple totalmente) · **PC** (cumple parcialmente, requiere plan de
  acción) · **NC** (no cumple) · **N-A** (no aplica al sistema evaluado).
- Cada control debe quedar respaldado por **evidencia verificable** (política, log, captura de
  pantalla, ticket, contrato, RAT), **no por una simple declaración**.
- *Nota metodológica del propio documento:* la sección de la Ley 21.719 se elaboró a partir de fuentes
  secundarias públicas, por lo que **recomienda validar cada control frente al texto legal vigente y su
  reglamento** antes de usarlo como evidencia formal de cumplimiento.

**Zona 1 — Gobernanza y cultura de la IA (G-01 a G-12).** Owner único con nombre y rendición de cuentas
documentada · casos de uso aprobados, restringidos y prohibidos · inventario de modelos, proveedores,
integraciones y dependencias críticas · cuándo la revisión humana es obligatoria · ciclo periódico de
revisión de seguridad y privacidad · Código Ético de IA · Comité de IA · capacitación del Consejo y la
Alta Dirección · análisis de ROI documentado · matriz de segregación de funciones · alineación con la
Ley 21.719 y la regulación sectorial · plan de auditoría interna basado en riesgos específico para IA.

**Zona 2 — Datos, calidad de datos y protección de datos personales (D-01 a D-15).** Clasificación de
datos de entrenamiento, prompts, archivos y salidas por sensibilidad, incluidos datos personales y
sensibles (salud, biométricos, origen étnico, situación socioeconómica, orientación sexual, datos de
NNA) · minimización del envío a servicios de IA externos · base de licitud documentada para
entrenamiento, *fine-tuning* y *prompting* · principio de finalidad · cifrado en tránsito y en reposo ·
mínimo privilegio · reglas de retención y eliminación · **linaje** de los datos · el **RAT incluye los
tratamientos hechos con IA** · evaluación de si procede una **EIPD/DPIA** (datos sensibles a gran
escala, perfilamiento automatizado, videovigilancia masiva o combinación de fuentes que amplíe el
riesgo) · mecanismos para derechos **ARSO+** (acceso, rectificación, supresión, oposición y
portabilidad) · procedimiento de **notificación de brechas** a la Agencia y a los titulares · mecanismo
habilitante de **transferencia internacional** cuando el modelo o proveedor procesa fuera de Chile ·
cláusulas de protección de datos en contratos con proveedores que actúan como encargados ·
**información al titular e intervención humana** cuando hay decisiones automatizadas o perfilamiento
con efectos jurídicos o significativos.

**Zona 3 — Modelo, identidad y accesos (M-…).** Los modelos, los prompts de sistema, las llaves de API
y las acciones privilegiadas se tratan como **activos de seguridad de producción**: fuentes de modelos
aprobadas y registro de modelos y versiones · control de quién puede actualizar modelos, prompts de
sistema, *guardrails* y permisos de herramientas.
> "Un modelo potente con control de acceso débil se convierte en una superficie de ataque igualmente
> potente."

*(El documento continúa con zonas adicionales y la sección 8 dedicada a la Ley N° 21.719.)*

## 3. Catálogo de lecturas de apoyo

### Gobierno del dato y auditoría
- **`Auditoria de gobierno de datos.pdf`** — *Auditoría Interna del Gobierno del Dato*, Instituto de
  Auditores Internos de España (44 pp.). Cómo auditar un programa de gobierno del dato.
- **`ESP-Clasificacion-de-Datos.pdf`** (y sus duplicados `-1`, `-2`) — *White Paper Series, Edición 6,
  2019: Clasificación de Datos*, **OEA** (24 pp.). **Fuente directa** del bloque de clasificación de
  datos de las clases 1 y 2.
- **`52-63 Borja Martin Doble velocidad datosC_ (2).pdf`** — *La doble velocidad de los datos: cómo
  incorporar una estrategia 'data-driven' en la organización*, Harvard Deusto Business Review.
- **`06-13 Gawer PlataformasC_HBR El negocio de las plataformas.pdf`** — Annabelle Gawer, *El negocio
  de las plataformas*, Harvard Deusto. Modelos de negocio de plataforma digital.
- **`drucker Gestionarse a sí mismo (2).pdf`** (y `-1`, duplicado) — Peter F. Drucker, *Gestionarse a
  sí mismo*, HBR, enero 2005 (reimpresión r0501k-e). Lectura de desarrollo profesional.
- **`Offshoring.pdf`** / **`Offshoring-1.pdf`** — escaneo sin capa de texto.

### Protección de datos y privacidad
- **`Libro big-data.pdf`** — Elena Gil, *Big data, privacidad y protección de datos*, Accésit 2015 del
  Premio de Investigación de la **AEPD** (145 pp.). **Fuente de la definición de big data** usada en la
  clase 7.
- **`Guía de Protección de datos por defecto (1).pdf`** — *Guía de Protección de Datos por Defecto*,
  octubre de 2020 (39 pp.). Aplicación práctica del **art. 25 del RGPD** (privacidad por defecto).
- **`enisa-ingenieria-de-la-proteccion-de-datos 2022.pdf`** — **ENISA**, *Ingeniería de la protección
  de datos: de la teoría a la práctica*, enero de 2022 (51 pp.).
- **`guia-codigo-de-buenas-practicas-proyectos-de-big-data (1) (1).pdf`** — *Código de buenas prácticas
  en protección de datos para proyectos Big Data* (40 pp.).
- **`Proy protección de datos y privacidad EEUU.pdf`** — texto legislativo de EE.UU.: *American Data
  Privacy and Protection Act* (H.R. 8152, enmienda sustitutiva, 132 pp.).
- **`IA EEUU.pdf`** — proyecto de ley del 118° Congreso de EE.UU. que exige a las agencias federales
  usar el **AI Risk Management Framework** del NIST (10 pp.).

### Gobernanza y riesgo de IA
- **`ISO 42001 integración con ISO 27001.pdf`** — *ISO 42001 and ISO 27001 Integration: Running One
  System, Not Two*, guía de Synergy Compliance Consulting (SCC-PG-025, 15 pp.). **Fuente directa** del
  bloque central de la clase 6: la columna vertebral compartida, el mapeo del Anexo A, las dos SoA.
- **`ISO 42001 check list.pdf`** — *The ISO 42001 compliance checklist* (7 pp.): definir el alcance del
  AIMS, familiarizarse con los principios de IA, etc.
- **`Guia gestión de riesgos IA 2025.pdf`** — guía desarrollada en el marco del **piloto español de
  sandbox regulatorio de IA** (63 pp.).
- **`Gobierno de LA IA herramientras 2025.pdf`** — *Gobierno de la IA: recursos prácticos
  descargables* (20 pp.). Incluye un ejemplo de **Model Card** para un sistema ficticio de evaluación
  de solvencia crediticia.
- **`NIST.AI.600-1.pdf`** — **NIST AI 600-1**, *AI Risk Management Framework: Generative AI Profile*
  (64 pp.).
- **`google_secure_ai_framework_summary_ASLv3.pdf`** — resumen del **Secure AI Framework (SAIF)** de
  Google (1 p.).
- **`Gobernanza etica de los sistemas de IA.pdf`** — Daniel Castaño, *La gobernanza ética de los
  sistemas de Inteligencia Artificial* (44 pp.), artículo académico.
- **`La_Gestión_Ética_de_los_Datos.pdf`** — César Buenadicha, Gemma Galdon Clavell, María Paz
  Hermosilla, Daniel Loewe y Cristina Pombo, *La gestión ética de los datos: por qué importa y cómo
  hacer un uso justo de los datos en un mundo digital*, **BID**, 2019 (56 pp.). **Fuente directa** del
  bloque de uso ético, discriminación algorítmica y tipos de opacidad de la clase 7.
- **`AB-EB-the-resilient-enterprise-using-ai-to-connect-governance-risk-and-compliance.pdf`** — *The
  Resilient Enterprise: Using AI to Connect Governance, Risk, and Compliance*, HBR Analytic Services
  briefing paper (12 pp.).
- **`artic-mes-siete-retos-inteligencia.pdf`** — monográfico *Límites y retos de la inteligencia
  artificial en el entorno empresarial*, Harvard Deusto Business Review N° 316 (18 pp.).

### Lecturas de tendencia sugeridas por el profesor (clase 6)
- Cómo enfrentaremos la **economía gig**.
- Prepararse a trabajar más allá de lo que creemos.
- Aprender a **gestionarnos ante los cambios** (enlaza con la lectura de Drucker).
- Cómo abordaremos la **IA en el mercado laboral**.

## 4. Enlaces y referencias citados en clase

**Institucionales y normativos:**
- Biblioteca del Congreso Nacional: `https://www.bcn.cl/leychile/`
- Política Nacional de IA (Ministerio de Ciencia):
  `https://minciencia.gob.cl/areas/inteligencia-artificial/politica-nacional-de-inteligencia-artificial/`
- Portal de datos abiertos de Chile: `datos.gob.cl`
- Consulta ciudadana sobre estrategia de gestión de datos del Estado:
  `https://participacion.digital.gob.cl/`
- CMF, NCG 461: `https://www.cmfchile.cl/normativa/ncg_461_2021.pdf`
- Normas técnicas de la Ley 21.180 (Diario Oficial, 17-08-2023):
  `https://www.diariooficial.interior.gob.cl/publicaciones/2023/08/17/43629/01/...`
- European AI Alliance: `https://digital-strategy.ec.europa.eu/en/policies/european-ai-alliance`

**Marcos y organizaciones:**
- DAMA Internacional: `www.dama.org` · DAMA Chile: `www.damachile.org`
- DMBOK v2: `https://technicspub.com/dmbok/`
- Cloud Security Alliance: `www.cloudsecurityalliance.org`
- IAPP, *US State Privacy Legislation Tracker*:
  `https://iapp.org/resources/article/us-state-privacy-legislation-tracker/`
- UNCTAD, ciberlegislación: `https://unctad.org/page/cybercrime-legislation-worldwide`
- CEPAL, gobernanza digital: `https://biblioguias.cepal.org/gobierno-digital/concepto-gobernanza`
- Nasser, *Gobernanza Digital e Interoperabilidad* (CEPAL 2019):
  `https://repositorio.cepal.org/bitstream/handle/11362/47018/1/S2100258_es.pdf`
- Centro de Estudios en Derecho Informático, U. de Chile:
  `http://derecho.uchile.cl/centro-de-estudios-en-derecho-informatico`
- Alfa-Redi: `www.alfa-redi.com` · Instituto Chileno de Derecho y Tecnología: `www.icdt.cl`

**Calidad de datos y herramientas:**
- *7 Steps to Ensure and Sustain Data Quality* (Towards Data Science)
- International Association for Data Quality, Governance and Analytics: `www.iadqga.com`
- IBM Data Quality Methodology · Framework for the Code of Practice for Statistics (UK)
- SAS Data Management · Talend Open Studio · OpenRefine
- Erwin · TOAD Data Modeler · Moon Modeler · Powerdata (MDM)
- Catálogo de tipos de gráfico: `www.datavizproject.com`

**Divulgación:**
- Documental *The Great Hack* ("Nada es privado"): `https://www.thegreathack.com/`
- `thispersondoesnotexist.com` (datos sintéticos)
- Datos sintéticos, Gobierno de España: `https://datos.gob.es/es/documentacion`
- CIPER Chile sobre la falla del sistema de Migraciones (feb-2022)
