---
name: gobernanza-datos
description: >
  Expert knowledge base for the Gobernanza de Datos course (Magíster en IA, PUC Chile, Prof. Andrés
  Pumarino, 2026). Covers data governance end to end: datos e información como activo, gobierno de
  datos y gobierno de información, activos de información, arquitectura de información (modelos de
  capas, dominios y plataforma), el marco DAMA/DMBOK v2 y sus 11 prácticas, clasificación de datos
  (white paper OEA), calidad de datos, metadatos, datos maestros y referenciales, integración e
  interoperabilidad, almacenamiento, SGSI e ISO 27001, gestión documental, analítica/BI; regulación
  chilena del dato (Ley 21.719 de protección de datos, Ley 21.663 marco de ciberseguridad, Ley 21.459
  delitos informáticos, Ley 21.180 transformación digital y sus normas técnicas, Ley 19.799 firma
  electrónica, Ley 21.595 delitos económicos, Ley Fintec, NCG 461) y GDPR; programa de protección de
  datos, Registro de Actividades de Tratamiento (RAT), Evaluación de Impacto en Protección de Datos
  (EIPD/DPIA), consentimiento, derechos ARCOP, transferencias internacionales; gobernanza de IA con
  ISO/IEC 42001 y su integración con ISO 27001, Proyecto de Ley de IA de Chile, Política Nacional de
  IA, Modelo de Prevención de Infracciones (MPI) y el Delegado de Protección de Datos, responsabilidad
  civil, big data, anonimización y seudonimización, discriminación algorítmica, opacidad y uso ético
  de los datos. Use for any question about this course: clases, control de lectura, trabajo grupal,
  lecturas, slides. Also trigger on gobernanza de datos, gobierno de datos, data governance, DAMA,
  DMBOK, CDO, CAIO, DPO, DPD, CISO, activo de información, arquitectura de información, datos
  maestros, datos referenciales, MDM, metadatos, taxonomía, ontología, calidad de datos, ISO 8000,
  linaje de datos, data lake, interoperabilidad, ETL, SGSI, ISO 27001, ISO 27701, ISO 42001, SoA,
  declaración de aplicabilidad, protección de datos personales, datos sensibles, Ley 21.719, Agencia
  de Protección de Datos Personales, RAT, EIPD, DPIA, consentimiento informado, derechos ARCO/ARCOP,
  transferencia internacional de datos, cláusulas contractuales tipo, BCR, anonimización,
  seudonimización, reidentificación, big data, RGPD, GDPR, privacidad por diseño y por defecto,
  Modelo de Prevención de Infracciones, MPI, Proyecto de Ley de IA Chile, riesgo inaceptable, alto
  riesgo, discriminación algorítmica, transparencia algorítmica, explicabilidad, opacidad, clasificación
  de datos, ciclo de vida del dato, DRP, BCP, or the professor's name (Pumarino).
  Respond in Spanish when the user writes in Spanish.
---

# Gobernanza de Datos (Magíster en IA, PUC Chile)

Knowledge base for the course **Gobernanza de Datos 2026**, Prof. **Andrés Pumarino**
(`apumarin@uc.cl`), abogado (UAI), Magíster en Gestión de Negocios (UAI), postítulos en Derecho
Informático (U. de Chile) y Gestión de Negocios (UAI); miembro de Alfa-Redi y consejero del Instituto
Chileno de Derecho y Tecnología (ICDT).

El curso es **jurídico-organizacional, no técnico**: la pregunta de fondo no es *cómo* procesar los
datos sino **quién decide sobre ellos, con qué política, bajo qué ley y con qué evidencia auditable**.

## Cómo usar esta skill

1. **Lee el archivo de `references/` que corresponda** antes de responder algo que vaya más allá del
   resumen de abajo. SKILL.md es el mapa; los archivos de referencia tienen el detalle, las listas
   completas de controles, las fases y los artículos de ley.
2. **Responde en español.** El curso es en español.
3. **Distingue siempre tres planos** y nómbralos explícitamente, porque el curso evalúa esa distinción:
   **legal** (qué exige la ley y el regulador), **organizativo** (roles, políticas, capacitación) y
   **técnico** (controles, cifrado, arquitectura). Una respuesta que solo cubre lo técnico está
   incompleta en este curso.
4. **Cita la norma con su número** (Ley N° 21.719, Ley N° 21.663, artículo 5 del Proyecto de Ley de
   IA, artículo 32 RGPD…). El profesor es abogado y el curso trabaja con normativa nombrada.
5. **Cuidado con las fechas.** Varias láminas arrastran datos de la edición 2025 del curso y de
   versiones antiguas de los trackers (IAPP, UNCTAD). Las cifras que aparecen en más de una clase
   están actualizadas en la versión más reciente: úsala. Si una fecha no aparece explícita en el
   material, dilo en vez de inventarla.
6. **Integridad académica:** la evaluación es un trabajo grupal y un control de lectura. Usa esta
   skill para explicar conceptos, estructurar entregables y revisar razonamiento, no para redactar la
   entrega completa en lugar del grupo.

## Mapa del curso

| Clase | Tema principal | Reference |
|-------|----------------|-----------|
| 1 | Introducción: datos, información y negocio · activos de información · arquitectura de información · primera mirada a la regulación · DAMA · clasificación de datos | `references/clase1-fundamentos-gobierno-datos.md` |
| 2 | Repaso y profundización: marcos de gestión (DAMA/CoBIT/ITIL) · gestión integral del ciclo de vida del dato · clasificación de datos · protección de datos y GDPR | `references/clase1-fundamentos-gobierno-datos.md`, `references/regulacion-chile-y-datos-personales.md` |
| 3 | Regulación del dato · fases para instalar un programa de protección de datos · RAT · EIPD · formularios modelo | `references/rat-eipd-y-ciclo-de-vida.md` |
| 4 | Continuación de la EIPD (mismo bloque que la clase 3, versión reducida) | `references/rat-eipd-y-ciclo-de-vida.md` |
| 5 | Prácticas DAMA en detalle: modelamiento y diseño · datos maestros y referenciales · metadatos · integración e interoperabilidad · almacenamiento y operación · seguridad de la información (SGSI/ISO 27001) · documentos y contenido · analítica/BI · calidad de datos · cloud computing legal | `references/dama-practicas.md`, `references/regulacion-chile-y-datos-personales.md` (§cloud) |
| 6 | Gobernanza de IA: riesgos de la IA · ISO/IEC 42001 e integración con ISO 27001 · roles (CAIO/CDO/DPO/CISO) · Política Nacional de IA · Proyecto de Ley de IA de Chile · responsabilidad civil | `references/gobernanza-de-ia.md` |
| 7 | Big data y protección de datos · anonimización y seudonimización · uso ético de los datos · discriminación algorítmica y opacidad · Ley 21.719 y la Comisión de Implementación · Modelo de Prevención de Infracciones (MPI) | `references/gobernanza-de-ia.md`, `references/regulacion-chile-y-datos-personales.md` |

Evaluación, lecturas del repo y el checklist de auditoría del profesor:
`references/evaluacion-y-lecturas.md`.

Material: `GobernanzaDeDatos/Presentaciones/` (7 clases + ~28 lecturas de apoyo).

## Objetivos declarados del curso

1. Identificar definiciones claves en gobierno de datos (conceptos).
2. Relación con la protección de datos y la evaluación de impacto en protección de datos (EIPD).
3. Discutir sobre el valor de la información y el ciclo de vida de los datos en las organizaciones.
4. Conocer el marco de trabajo de gestión de información **DAMA** y sus prácticas.
5. Revisar el ciclo de vida de la información y su vinculación con las prácticas DAMA.
6. Discutir cómo implementar la gestión de información.

## Conceptos núcleo (referencia rápida)

### Gobierno de datos: la definición del curso
> "Es un **proceso político** que abarca a las **personas**, los **procesos** y las **tecnologías** de
> la información necesarias para crear un manejo coherente y adecuado."

Tres implicancias que el curso repite: (a) la gobernanza **no es un objetivo en sí misma**, se alinea a
la estrategia organizacional y a la normativa vigente; (b) **guía a todas las demás prácticas** de
gestión de datos; (c) no se puede **comprar** un programa de gobierno de datos, se construye a medida.

**Componentes esenciales:** Estrategia · Personas · Cumplimiento · Métricas · Tecnología · Comunicación.

**Fases:** armar un equipo → establecer objetivos → empezar pequeño → fomentar la transparencia →
integrar a todos los departamentos → definir riesgos → evaluar el proyecto → refinar continuamente.

### Gobernanza digital (CEPAL, Nasser 2021)
> "Articulación y concreción de políticas de interés público con los diversos actores involucrados
> (Estado, Sociedad Civil y Sector Privado), con la finalidad de alcanzar competencias y cooperación
> para crear valor público y la optimización de los recursos de los involucrados, mediante el uso de
> tecnologías digitales."

La **gobernanza de datos** es una pieza dentro de la gobernanza digital.

### Las 11 prácticas DAMA (DMBOK v2)
1. **Gobernanza de Datos** — visión, políticas y estrategias; guía a las otras diez.
2. **Arquitectura de Datos** — dominios, inventarios, modelos y diseño de plataformas.
3. **Modelado y Diseño de Datos** — modelos conceptual, lógico y físico.
4. **Almacenamiento y Operación** — implementación y operación de las plataformas.
5. **Seguridad de Datos** — privacidad, confidencialidad y acceso apropiado.
6. **Integración e Interoperabilidad** — mover y consolidar datos dentro y fuera.
7. **Documentos y Contenidos** — reglas para los datos no estructurados.
8. **Datos Maestros y de Referencia** — estandarización y centralización de lo transversal.
9. **Data Warehousing & BI** — inteligencia de negocio y analítica.
10. **Metadatos** — catálogos y diccionarios: datos sobre los datos.
11. **Calidad de Datos** — definir, controlar y mejorar la calidad.

**DAMA no aborda (o solo parcialmente):** temas legales y normativos de cada país, gestión del cambio,
y **cómo implementar**. Esos tres huecos son precisamente lo que el curso llena.

### Arquitectura de información: tres modelos complementarios
- **Modelo de capas** — datos maestros (base) → información operacional → información de gestión.
- **Modelo de dominios** — taxonomía por contenido/tema; orientada al negocio, evolutiva.
- **Modelo de plataforma** — componentes de la plataforma de datos, de la captura a la publicación.

Cruzar capas × procesos en una **matriz** revela dónde falta información (análisis de brechas).

### Ciclo de vida del dato (seis etapas, con checklist por etapa)
Recolección → Uso → Almacenamiento → Compartir → Archivo → Eliminación.
Cada etapa tiene su lista de preguntas de control en `references/rat-eipd-y-ciclo-de-vida.md`.

### Las dos herramientas operativas de protección de datos
- **RAT (Registro de Actividades de Tratamiento):** documento obligatorio que describe cada
  tratamiento (responsable/encargado, finalidad, categorías de datos y de interesados, destinatarios,
  transferencias internacionales, plazos de conservación, medidas de seguridad). Materializa el
  principio de **responsabilidad proactiva**.
- **EIPD (Evaluación de Impacto en Protección de Datos, DPIA):** proceso para identificar y tratar los
  riesgos de un tratamiento sobre los derechos de las personas. Cinco fases: participantes → normativa
  aplicable → análisis preliminar → plan de implementación → informe final y ejecución. **No es solo
  para grandes organizaciones**, también aplica a PYMES.

### Marco normativo chileno del dato (lo mínimo que hay que saber de memoria)
| Norma | Materia | Regulador |
|-------|---------|-----------|
| **Ley N° 21.719** | Protección de datos personales (reemplaza el estándar de la 19.628) | Agencia de Protección de Datos Personales |
| **Ley N° 21.663** | Ley Marco de Ciberseguridad | Agencia Nacional de Ciberseguridad (ANCI) |
| **Ley N° 21.459** | Delitos informáticos | Tribunales penales |
| **Ley N° 21.180** | Transformación digital del Estado (+ 6 normas técnicas) | Contraloría General de la República |
| **Ley N° 19.799** | Firma electrónica | SII / Ministerio de Economía |
| **Ley N° 21.595** | Delitos económicos | Ministerio Público, CMF, SII |
| **Ley Fintec** | Servicios financieros tecnológicos | CMF |
| **NCG 461 (CMF)** | Reporte de políticas y metas ASG | CMF |

### Gobernanza de IA: el mensaje central de la clase 6
**No se construye un segundo sistema de gestión.** Se **amplía el alcance** del SGSI que ya opera.
ISO 27001 (seguridad) e ISO/IEC 42001 (IA) comparten la estructura armonizada de cláusulas 4 a 10, por
lo que se reúsa el contexto, el liderazgo, el soporte, la auditoría y la mejora. Para cada control
existente la pregunta es: **¿la IA cambia lo que este control debe lograr?** → reusar / extender /
añadir. Se mantiene **un solo set documental**, pero **dos Declaraciones de Aplicabilidad (SoA)**
separadas: 93 controles en ISO 27001 frente a 38 en ISO 42001; fusionarlas destruye la trazabilidad
para el auditor.

**La gran diferencia sin equivalente en un SGSI** es la **Evaluación de Impacto de IA** (SGAI 6.1.4
frente a riesgo SGSI 6.1.2): el objeto protegido ya no son los activos de información sino
**individuos, grupos y la sociedad**, y el daño típico ya no es la brecha de datos sino el **sesgo, la
pérdida de transparencia y la reducción de la agencia humana**.

### Cuatro roles que el curso distingue
- **CAIO** (Chief AI Officer) — define la estrategia de IA y gestiona su implementación.
- **CDO** (Chief Data Officer) — tratamiento de datos y su gobernanza.
- **DPO / DPD** (Delegado de Protección de Datos) — normativa de protección de datos; obligatorio para
  certificar un Modelo de Prevención de Infracciones.
- **CISO** — seguridad de la información.

### Big data y el límite de la anonimización
- **Anonimización:** imposibilidad de vincular el dato con la persona. Posibilidad **cero** de
  reidentificación; muy difícil de lograr en bases completas. La variante realista es la
  **anonimización funcional** (riesgo mínimo de reidentificación).
- **Seudonimización:** el dato no se atribuye a un individuo **sin información adicional**; se
  reemplaza el identificador por un código (encriptación, tokenización).
- Big data **rompió** el modelo clásico de anonimización en dos fases: el volumen y la diversidad
  permiten reidentificar incluso después de anonimizar.

### Tres tipos de opacidad algorítmica
- **Intencional** — por propiedad intelectual o porque revelar el algoritmo lo volvería inútil
  (detección de evasión tributaria). Justificable a veces por interés público, no siempre.
- **Analfabeta** — falta de competencias técnicas de los afectados: el algoritmo es explicable pero
  solo para expertos. Exige un esfuerzo pedagógico, no solo transparencia formal.
- **Intrínseca** — redes neuronales complejas que ni sus creadores pueden explicar. Difícilmente
  justificable cuando decide sobre prestaciones sociales básicas.

Frente a ellas, el curso propone **transparencia significativa**: comunicar la **política**, el
**rendimiento**, la **equidad** y los **efectos** del algoritmo.

## Evaluación

- **1 trabajo grupal** (2 o más integrantes) + **1 control de lectura**.
- Las pruebas se envían por email y se entregan por **CANVAS**.
- El plazo vence a las **24:00 del día indicado**; se descuentan **0,5 décimas por cada día de atraso**.
- **Control de lectura:** jueves 3 de septiembre de 2026.
- **Entrega del trabajo:** jueves 24 de septiembre de 2026.

Detalle y catálogo de lecturas: `references/evaluacion-y-lecturas.md`.
