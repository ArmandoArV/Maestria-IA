# Clases 6-7 · Gobernanza de Inteligencia Artificial

## 1. La IA como nueva fuente de riesgo

**Tres familias de riesgo:**
- **Riesgos de uso malintencionado** — ciberataques, creación de material de abuso sexual infantil
  generado por IA, desarrollo de armas biológicas.
- **Fallas del sistema** — sesgos, problemas de confiabilidad y posible **pérdida de control** sobre
  sistemas avanzados de IA.
- **Riesgos sistémicos** — derivados de la adopción generalizada: interrupciones en la fuerza laboral,
  preocupaciones sobre privacidad e impactos ambientales.

**Riesgos específicos de datos que introduce la IA:**
- **El consentimiento es clave.** Muchas soluciones de IA utilizan datos sin que el usuario sepa cómo,
  dónde ni para qué serán procesados.
- Los **empleados pueden usar IA generativa sin control** de la empresa, exponiendo datos internos
  (*shadow AI*).
- **Reidentificación** de datos supuestamente anonimizados.

### Ciberseguridad frente a protección de datos personales en Chile
| Aspecto | Ciberseguridad | Protección de Datos Personales |
|---------|----------------|--------------------------------|
| **Enfoque principal** | Protección de sistemas y redes contra accesos no autorizados y ataques | Garantizar los derechos de las personas sobre su información personal |
| **Riesgos comunes** | Denegación de servicio, malware, phishing | Tratamiento indebido de datos, falta de consentimiento, brechas de privacidad |
| **Normativa aplicable** | **Ley N° 21.663** (Ley Marco de Ciberseguridad) | **Ley N° 21.719** (Protección de Datos Personales) |
| **Autoridad competente** | Agencia Nacional de Ciberseguridad | Agencia de Protección de Datos Personales |

### Las tres medidas que siempre hay que nombrar
- **Técnicas:** la adecuación de las soluciones debe pensarse **en relación a las exigencias legales**.
- **Legales:** identificar las exigencias que pide la ley y el regulador.
- **Organizativas:** capacitación y concientización en las diversas áreas de la organización.

## 2. ISO/IEC 42001 — Sistema de Gestión de IA (SGAI)

### Contexto de normas
| Norma | Año | Qué es |
|-------|-----|--------|
| **ISO 27001** | 2022 | ISMS Standard — Sistema de Gestión de Seguridad de la Información |
| **ISO 42001** | 2023 | Sistema de Gestión de Inteligencia Artificial (*AI management systems*) |
| **ISO 27701** | 2025 | PIMS Standard — gestión de privacidad |

### Documentación exigida por ISO/IEC 42001
**Documentación estratégica.** Manual del Sistema de Gestión de IA · Política de IA · Declaración de
compromiso de la alta dirección.

**Gobernanza y organización.** Identificación de roles y responsabilidades · organigrama y líderes
clave · matriz de competencias y registros de formación.

**Gestión de riesgos e impactos.** Procedimiento de evaluación de riesgos de IA · plan para tratar
riesgos y oportunidades · **Evaluación de impactos del sistema de IA** (*AI System Impact Assessment*).

**Control documental y operacional.** Procedimientos de control de documentos y registros · listado de
procesos y su interacción · procedimientos de auditoría interna y revisión por la dirección.

**Comunicación y partes interesadas.** Lista de partes interesadas y sus necesidades · evidencia de
comunicación de la política · matriz de comunicación.

**Requisitos específicos del ciclo de vida de IA.** Documentación del desarrollo, verificación,
validación y operación del sistema de IA · gestión de datos, recursos y herramientas de IA.

### El principio central: no se construye un segundo sistema

> **El instinto equivocado:** al adoptar IA, las organizaciones suelen crear un SGAI **separado** de
> sus propias políticas, auditorías y revisiones. Esto es **costoso, burocrático y estratégicamente
> incorrecto**.

**El principio correcto:** no se está construyendo un segundo sistema, se está **ampliando el alcance**
del que ya opera. El trabajo estructural de la organización está hecho: el objetivo es **especializar,
no reinventar**.

**Una columna vertebral compartida** — ISO 27001 (seguridad) e ISO 42001 (IA) comparten la estructura
armonizada de las **cláusulas 4 a 10**:
- Contexto (cláusula 4)
- Liderazgo y políticas (cláusula 5)
- Soporte y recursos (cláusula 7)
- Auditoría y mejora (cláusulas 9 y 10)

Una adopción exitosa requiere: **análisis de contexto · estructura de liderazgo · programa de auditoría
· dos certificados**.

### Qué se comparte y qué se debe añadir
**La pregunta clave para cada elemento del SGSI actual: ¿la IA cambia lo que este control debe
lograr?**

1. **Reusar sin cambios** — mecanismos que funcionan idéntico: control de documentos, programas de
   auditoría interna, acciones correctivas.
2. **Extender** (ampliar el alcance) — mecanismos existentes cuyo alcance debe incluir a la IA.
3. **Añadir (genuinamente nuevo)** — mecanismos sin equivalencia en 27001: **evaluación de impacto de
   IA, controles de transparencia, protocolos de supervisión humana**.

### Mapeo de controles (Anexo A): de 27001 a 42001
> ISO 27001 da la base; ISO 42001 la especializa.

| Base (ISO 27001) | Extensión (ISO 42001) |
|------------------|------------------------|
| Relaciones con proveedores (A.5.19) | Responsabilidades de proveedores de IA (A.10.2) |
| Privacidad y PII (A.5.34) | Calidad y adquisición de datos para IA (A.7.2, A.7.4) |
| Ciclo de vida seguro (A.8.25) | Diseño, verificación y despliegue responsable (A.6.2.2) |
| *Sin equivalente en el SGSI* | **Añadir:** transparencia para usuarios (A.8.2), supervisión e interacción humana (A.6.2.3) |

### La gran diferencia: la Evaluación de Impacto
El elemento de ISO 42001 **sin equivalente en un SGSI**. No es un análisis de riesgo técnico, sino un
**análisis de consecuencias humanas**.

| | **SGSI — Riesgo (6.1.2)** | **SGAI — Impacto IA (6.1.4)** |
|---|---|---|
| **Objeto a proteger** | Activos de información | **Individuos, grupos y sociedad general** |
| **Gatillo** | Amenazas a confidencialidad, integridad, disponibilidad | **Despliegue o cambio material de un sistema algorítmico** |
| **Daño típico** | Brechas de datos, interrupción de servicio | **Sesgo, pérdida de transparencia, reducción de agencia humana** |

### Un solo set documental, dos SoA
**Duplicar documentos es la forma más rápida de fracasar.** La organización opera con **un solo manual
de sistema, una matriz de competencias unificada y un solo registro de riesgos** (con dos vistas
etiquetadas).

**Pero se mantienen dos Declaraciones de Aplicabilidad (SoA) separadas:** ISO 27001 exige evaluar **93
controles**; ISO 42001 evalúa **38**. **Fusionarlas destruye la trazabilidad para el auditor.** Ambas
SoA se mantienen bajo el **mismo ciclo de revisión**.

### Operaciones combinadas
**Auditoría interna combinada.** El trabajo de campo ocurre **una vez**; los auditores evalúan las
cláusulas compartidas en una sola entrevista.
*Importante:* la **independencia del auditor se mantiene en ambos alcances** — quien diseña el impacto
de la IA **no puede auditarlo**.

**Revisión por la dirección.** Una sola reunión de liderazgo · una agenda con **dos bloques
integrados** · decisiones de recursos e inversiones consolidadas en **una sola acta**.

## 3. Elementos para la gobernanza de un sistema de IA

**Aspectos básicos.** Las organizaciones deben dotarse de modelos y estructuras de gobierno que
contemplen al menos: los **principios** en base a los que se desarrollará o usará la IA · el
**cumplimiento normativo** · la **gestión de los riesgos** derivados de la IA con seguimiento activo ·
la **atención a las partes afectadas y autoridades competentes**. Deben establecerse estructuras,
normas, procedimientos, protocolos internos, herramientas técnicas y programas de formación.

**Siete elementos** (destaca la importancia de la **participación de la alta dirección**, que debe
aportar recursos, experiencia y autoridad para dirigir la estrategia de IA y supervisar su
implementación):

1. **Adaptación de las estructuras internas de gobierno.** Texto unificado que defina los roles e
   integre los principios rectores; crear una estrategia de IA a nivel organizativo y un **Comité de
   gobierno**.
2. **Establecimiento de un Comité o Foro de IA.** Competencias: supervisión de sistemas de IA de alto
   riesgo, aceptación de nuevos miembros propuestos y **comunicación de incidentes a la alta
   dirección**.
3. **Roles y responsabilidades a integrar** (además de profesionales legales y de cumplimiento, equipos
   de negocio, atención al cliente, comunicación, RR.HH. y analistas de sistemas):
   - **CAIO** (*Chief Artificial Intelligence Officer*) — define la estrategia de IA y gestiona su
     implementación.
   - **CDO** (*Chief Data Officer*) — tratamiento de datos y su gobernanza.
   - **DPO** (*Data Protection Officer*) — normativa de protección de datos.
   - **CISO** (*Chief Information Security Officer*) — seguridad de la información.
4. **Elaboración de políticas y procedimientos internos** con enfoque responsable y **centrado en el
   ser humano**, que promueva el respeto a los derechos humanos, la protección del medioambiente y la
   inclusión.
5. **Formación y concientización** sobre los aspectos legales y éticos del diseño y uso de sistemas de
   IA, incluida la necesidad de cumplir evaluaciones legales como la **evaluación de conformidad**.
6. **Determinación de los objetivos de negocio** relacionados con la estrategia de IA: incorporación de
   talento, definición de la estructura operativa, investigación y desarrollo de plataformas, posible
   adquisición de soluciones del mercado.
7. **Apoyo de la gerencia.** Se sugiere asignar un miembro del Comité de Dirección para **liderar el
   equipo multidisciplinar y presidir el comité o foro de IA**.

### Principios rectores (dos grandes grupos)
Los principios listados (limitación de la finalidad · lealtad y transparencia · limitación del plazo de
conservación · integridad y confidencialidad · responsabilidad proactiva · minimización de datos ·
exactitud) pueden resumirse en dos:
1. Establecimiento de un **proceso de toma de decisiones explicable, transparente y justo**.
2. La tecnología debe centrarse en el **bienestar y la seguridad de las personas**.

## 4. Transparencia significativa

**El nivel de opacidad determinará el nivel de transparencia de un algoritmo.** Pero que un sistema sea
opaco no significa que no se deba entregar información pública sobre él. La **transparencia
significativa** refiere a la necesidad de comunicar los aspectos básicos de un algoritmo.

**Cuatro componentes:**
- **Política del algoritmo** — cómo y bajo qué parámetros se toman las decisiones en la etapa de
  entrenamiento.
- **Rendimiento del algoritmo** — medidas de bondad de ajuste: qué tan bien representa o predice la
  realidad.
- **Equidad del algoritmo** — en qué medida está replicando sesgos. Buena práctica: presentar
  resultados **por subgrupos de la población** (por ejemplo hombres/mujeres), buscando que los
  resultados no difieran entre ellos.
- **Efectos del algoritmo en la capacidad del gobierno** — cómo lo utilizan los funcionarios públicos.

## 5. Gestión de riesgo de IA y ciclo de vida

**Proceso para el análisis de riesgo** (enfoque **preventivo o de mitigación** mediante controles
adecuados y monitoreo continuo), cinco pasos:
1. Un **inventario de IA** en la organización.
2. **Identificación y evaluación** de riesgos.
3. **Gestión** de los riesgos detectados.
4. Análisis de los **riesgos regulatorios**.
5. Elaboración de un **informe**, implantación de las recomendaciones y **mejora continua**.

**Ciclo de vida de una solución de IA (cinco fases):**
1. **Diseño** — acciones que garanticen resolver problemas y minimizar riesgos: definición de la
   estrategia, priorizar una hoja de ruta de soluciones, concientizar sobre los riesgos, contratar
   personal adecuado, confeccionar un equipo multidisciplinar.
2. **Desarrollo** — garantizar calidad y fiabilidad del modelo: recopilar y tratar datos, identificar
   la **cadena de suministro de datos**, adoptar prácticas de cumplimiento legal y gestión de riesgos,
   desarrollar un **modelo de gobierno de datos**, elaborar planes de prueba y prototipos.
3. **Despliegue** — planificación cuidadosa, coordinación entre equipos y consideración de posibles
   incompatibilidades tecnológicas.
4. **Seguimiento y control** — supervisión continua, ajuste y **reentrenamiento**, auditorías
   periódicas, gestión del riesgo, para que el modelo siga siendo eficaz y ético.
5. **Retirada** — por razones técnicas, éticas o empresariales; seguir un proceso que garantice la
   transición fluida y la gestión adecuada de los datos y modelos involucrados.

## 6. Política Nacional de IA (Chile)

- Documento con los **lineamientos estratégicos** en los que debe enfocarse el país en materia de IA
  durante los próximos **10 años** (proyección a 2031). Proceso iniciado en septiembre de 2019, con
  participación ciudadana sobre las consecuencias legales, éticas, sociales y económicas.
- El acelerado avance de la **IA generativa** motivó la actualización del **Eje 3 de Gobernanza y
  Ética**. La versión oficial fue promulgada por Decreto Supremo del Ministerio de Ciencia tras
  concluir la consulta pública de 2024.
- En paralelo se tramita el **Proyecto de Ley de IA** (Boletín 16821-19), que clasifica los sistemas
  por nivel de riesgo e impone exigencias de transparencia, supervisión humana y ciberseguridad.

**Objetivo:** fomentar el desarrollo y uso ético y responsable de la IA en Chile, para que la
tecnología juegue un rol promotor en el nuevo modelo de desarrollo y crecimiento del país.

**Tres principios transversales:**
1. **Uso ético y responsable de la IA, centrada en las personas** — contribuir al bienestar general,
   mejorando la calidad de vida; abordar los riesgos e impactos negativos respetando derechos y
   dignidad.
2. **La IA al servicio de un desarrollo sostenible** — motor para diversificar la economía, aumentar la
   productividad e impulsar investigación, tecnología, innovación y emprendimiento, dentro de un marco
   de desarrollo sostenible.
3. **IA en articulación internacional y multiactor** — cooperación internacional, reconociendo que gran
   parte de los debates trascienden las fronteras nacionales.

**Tres ejes:**
- **Eje 1 — Factores habilitantes:** elementos basales que posibilitan la existencia y el despliegue de
  sistemas de IA.
- **Eje 2 — Desarrollo y adopción:** espacio donde se investiga, desarrolla y despliega la IA; incluye
  academia, Estado, sector privado y sociedad civil.
- **Eje 3 — Gobernanza y ética:** aborda las discusiones y desafíos surgidos de la interacción
  humano-máquina y el **sistema sociotécnico** que configura esta tecnología.

**Actualizaciones nuevas al Eje 3:**
- Promover y articular la discusión sobre gobernanza de la IA y la cooperación internacional en América
  Latina y el Caribe.
- Colaborar e incidir activamente en la discusión de gobernanza y estándares a nivel internacional.
- Fomentar el uso de IA para combatir la **crisis climática**.
- Fomentar el uso de **energías renovables no convencionales** en el desarrollo de la IA.
- Desarrollar e implementar la **Estrategia Nacional de Prospección Laboral**.
- Diseñar mecanismos que permitan planificar rutas de **reconversión y capacitación**, fomentando el
  empleo formal en áreas de menor riesgo de automatización.
- Revisar y actualizar la **legislación laboral** para proteger a trabajadoras y trabajadores ante los
  cambios tecnológicos.
- Fomentar el uso responsable de IA con la perspectiva de **niños, niñas y adolescentes**.
- Desarrollar capacidades en IA que permitan preservar y poner en valor el **patrimonio cultural** de
  Chile.
- Focalizar fondos de investigación en **desinformación, violencia digital y salud mental**.

## 7. Proyecto de Ley de IA de Chile

Anunciado el **7 de mayo de 2024** como proyecto de ley oficialista para regular el uso y desarrollo de
IA en Chile.

### Título I — Disposiciones generales

**Objeto (art. 1).** Promover la creación, desarrollo, innovación e implementación de sistemas de IA
**al servicio del ser humano**, respetuosos de los principios democráticos, el Estado de Derecho y los
derechos fundamentales de las personas frente a los efectos nocivos que determinados usos pudieran
irrogar.

**Ámbito de aplicación (art. 2).** Se aplica a:
1. Los **proveedores** que introduzcan en el mercado o pongan en servicio sistemas de IA en el
   territorio nacional.
2. Los **implementadores** domiciliados en el territorio nacional.
3. Los proveedores e implementadores **domiciliados en el extranjero**, cuando la información de salida
   generada por el sistema **se utilice en Chile**.
4. Los **importadores y distribuidores**, y los **representantes autorizados** de los proveedores,
   cuando estén domiciliados en Chile.

**Definiciones clave (art. 3):**
- **Sistema de IA** — sistema basado en máquinas que, por objetivos explícitos o implícitos, **infiere**
  a partir de la entrada que recibe cómo generar salidas tales como predicciones, contenidos,
  recomendaciones o decisiones, que pueden influir en entornos físicos o virtuales.
- **Proveedor** — quien **desarrolle** un sistema de IA con miras a introducirlo en el mercado o
  ponerlo en servicio, a título gratuito u oneroso.
- **Implementador** — quien **utilice** un sistema de IA, salvo uso privado en los términos de la ley
  N° 17.336 sobre propiedad intelectual.
- **Proveedor de tecnología** — proveedor involucrado con el implementador en la comercialización y
  suministro de software, herramientas, componentes, modelos y datos previamente entrenados.
- **Importador** — domiciliado en Chile que introduzca en el mercado o ponga en servicio un sistema.
- **Distribuidor** — parte de la cadena de suministro, distinto del proveedor o importador, que
  comercializa un sistema **sin influir sobre sus propiedades**.
- **Representante de autoridad** — domiciliado en Chile que haya recibido y aceptado el mandato por
  escrito de un proveedor.
- **Operador** — término paraguas: el proveedor, el implementador, el representante autorizado, el
  importador y el distribuidor.
- **Persona afectada** — persona natural o grupo expuesto a un sistema de IA que sufra un perjuicio
  como consecuencia de esa exposición.
- **Riesgo** — combinación de la **probabilidad** de que se produzca un daño a las personas naturales,
  su salud, seguridad o derechos fundamentales, y la **gravedad** de dicho daño.
- **Riesgo significativo** — resulta de la combinación de gravedad, intensidad, probabilidad de
  ocurrencia y duración de sus efectos, y su capacidad de afectar a una o varias personas naturales.
- **Puesta en servicio** — suministro de un sistema para su primer uso directamente por el
  implementador o para uso propio en el mercado nacional.
- **Finalidad prevista** — el uso para el que el proveedor concibe el sistema, incluido el contexto y
  las condiciones de uso concretas, según las instrucciones de uso, los materiales de promoción y venta
  y la documentación técnica.
- **Uso indebido razonablemente previsible** — utilización que no corresponde a la finalidad prevista
  pero que puede derivarse de un comportamiento humano o de la interacción con otros sistemas
  razonablemente previsible.
- **Componente de seguridad de un producto o sistema** — componente que cumple una función de seguridad
  y cuya falla pone en peligro la salud y seguridad de las personas.
- **Identificación biométrica** — reconocimiento automatizado de características físicas, fisiológicas
  o conductuales para determinar la identidad, comparando datos biométricos con una base de datos.
- **Verificación biométrica** — verificación automatizada de la identidad comparando datos biométricos
  con los proporcionados con anterioridad; incluye la autenticación.
- **Categorización biométrica** — clasificación de personas según categorías concretas, o inferencia de
  características y atributos, en función de sus datos biométricos.
- **Sistema de identificación biométrica remota** — identifica personas **a distancia** comparando con
  una base de datos de referencia.
- **Sistema de reconocimiento de emociones** — detecta o deduce emociones, pensamientos, estados de
  ánimo o intenciones a partir de datos biométricos y de base biométrica.
- **Elaboración de perfiles** — tratamiento automatizado de datos personales sensibles para evaluar
  determinados aspectos personales.
- **Espacio de acceso público** — cualquier lugar físico de propiedad pública o privada accesible al
  público, con independencia de condiciones de acceso o restricciones de aforo.
- **Espacio controlado de pruebas (*sandbox*)** — entorno controlado creado por un órgano de la
  Administración que facilita el desarrollo, prueba y validación de sistemas innovadores durante un
  período limitado antes de su introducción en el mercado.
- **Incidente grave** — todo incidente o defecto de funcionamiento que, directa o indirectamente, tenga
  o pueda tener alguna de estas consecuencias:
  a) fallecimiento de una persona o daños graves para su salud;
  b) alteración grave de la gestión y funcionamiento de **infraestructura crítica** (art. 32 N° 21 inc.
  2° de la Constitución);
  c) vulneración de **derechos fundamentales** protegidos por la Constitución y las leyes;
  d) daño en la persona o propiedad de otro, o **daño ambiental** (art. 2 letra e de la ley N° 19.300).

### Principios rectores (ocho)
1. **Solidez y seguridad técnica** — minimizar los daños previsibles.
2. **Diversidad, no discriminación y equidad** — durante todo el ciclo de vida.
3. **Intervención y supervisión humana** — la IA como **herramienta al servicio del ser humano**.
4. **Privacidad y gobernanza de datos** — conformidad con las normas vigentes.
5. **Transparencia y explicabilidad** — facilitando trazabilidad y explicabilidad adecuadas.
6. **Bienestar social y medioambiental** — uso sostenible y respetuoso.
7. **Rendición de cuentas y responsabilidad** — correcto funcionamiento a lo largo del ciclo de vida.
8. **Protección de los derechos de los consumidores.**

### Clasificación de los sistemas de IA por riesgo (art. 5)
Sigue el enfoque de la **Ley de IA de la Unión Europea**.

| Nivel | Título del proyecto | Definición |
|-------|---------------------|------------|
| **Riesgo inaceptable** | Título II | Sistemas incompatibles con el respeto y garantía de los derechos fundamentales; su introducción en el mercado o puesta en servicio está **prohibida** |
| **Alto riesgo** | Título III | Sistemas autónomos o componentes de seguridad de productos que **pueden afectar negativamente** la salud y seguridad de las personas, sus derechos fundamentales o el medio ambiente, así como los derechos de los consumidores, especialmente si fallan o se usan de forma impropia |
| **Riesgo limitado** | Título IV | Sistemas que presentan riesgos **no significativos** de manipulación, engaño o error, producto de su interacción con personas naturales |
| **Sin riesgo evidente** | — | Todos los demás |

### Títulos V a VIII
- **Título V — Incidentes graves.** Cualquier persona que detecte un incidente grave (art. 3 N° 18)
  puede informarlo a la **Agencia de Protección de Datos Personales**; la Agencia notificará al
  operador para que alerte a las personas afectadas y tome medidas. La notificación debe realizarse
  **tan pronto se tenga conocimiento** y se establezca un vínculo causal entre el sistema de IA y el
  incidente, o una **posibilidad razonable** de dicho vínculo.
- **Título VI — Gobernanza.** Se crea el **Consejo Asesor Técnico de Inteligencia Artificial**,
  instancia **consultiva y permanente** que asesora al Ministro de Ciencia, Tecnología, Conocimiento e
  Innovación. Presidido por ese Ministro, e integrado por representantes de varios ministerios y
  agencias, académicos expertos y representantes de la industria tecnológica y de organizaciones de la
  sociedad civil.
- **Título VII — Medidas de apoyo a la innovación.** Los órganos de la Administración pueden crear
  **espacios controlados de pruebas** con un plan acordado entre proveedores potenciales y autoridades.
  Ofrecen orientación y supervisión para identificar y mitigar riesgos significativos para derechos
  fundamentales, salud, seguridad, democracia y medio ambiente. Si se detectan riesgos significativos,
  el operador debe mitigarlos **inmediatamente**, y las autoridades pueden **suspender las pruebas**.
  Los proveedores en estos espacios son **responsables de cualquier daño a terceros** causado por las
  pruebas.
- **Título VIII — Confidencialidad, infracciones y sanciones.**
  - **Confidencialidad (art. 23).** Toda persona u órgano involucrado debe respetar la confidencialidad
    de: derechos de propiedad intelectual e industrial e información empresarial confidencial o
    secretos comerciales, **incluido el código fuente** · los datos personales y su tratamiento · el
    interés público y la seguridad nacional · la integridad de las causas penales o procedimientos
    administrativos.
  - **Infracciones (art. 24).** **Gravísima:** puesta en servicio o utilización de un sistema de
    **riesgo inaceptable** (art. 6). **Grave:** incumplimiento de las reglas del art. 8 para sistemas
    de **alto riesgo**. **Leve:** incumplimiento de las obligaciones de **transparencia** respecto de
    sistemas de riesgo limitado (art. 11).
  - **Sanciones (art. 25).** Leves: multa de hasta **5.000 UTM** · Graves: hasta **10.000 UTM** ·
    Gravísimas: hasta **20.000 UTM**.

### Conclusiones del curso sobre proyectos de IA o ciencia de datos
Al formular un proyecto, no se debe olvidar:
1. **Revisar las leyes vigentes** en cuanto a la capacidad de actuar de la institución y la protección
   de datos.
2. Evaluar si se cumple el **principio de finalidad** de los datos.
3. Definir **subgrupos de la población que deben ser protegidos**.
4. **Documentar todas las decisiones** del proceso de formulación y ejecución, para favorecer la
   transparencia algorítmica.
5. La **opacidad será necesaria** para el algoritmo; aun así se debe entregar información a la
   ciudadanía.
6. Analizar la potencial **licencia social**, o falta de ella, que puede tener el proyecto.
7. Implementar un **programa piloto** y un sistema de corrección de errores.
8. Realizar un **análisis comparado** de otros sistemas similares implementados en el mundo.

## 8. Responsabilidad civil

**Fundamentos.** La responsabilidad civil es el **deber jurídico de reparar el daño causado a otra
persona**. Busca restituir el equilibrio alterado y proteger derechos e intereses legítimos. Puede
implicar **indemnización económica o restitución**.

**Elementos:**
1. **Daño** — lesión o menoscabo a un interés protegido.
2. **Culpa** — dolo o negligencia imputable al autor.
3. **Relación de causalidad** — nexo entre conducta y daño.

**Objetiva frente a subjetiva:**
- **Subjetiva** — requiere **probar culpa o dolo**.
- **Objetiva** — basta **daño + causalidad**, sin culpa. Aplica en actividades riesgosas (vehículos,
  medioambiente, trabajo).

**Responsabilidad por productos defectuosos.** Bien defectuoso que causa daño al consumidor;
responsabilidad **objetiva**: basta el daño y el nexo causal. Ejemplos: medicamentos mal rotulados,
alimentos contaminados.

**Responsabilidad en entornos tecnológicos.** Plataformas digitales (contenidos dañinos o ilícitos) ·
ciberseguridad (daños por vulneración de datos) · **inteligencia artificial** (decisiones
automatizadas) · IoT (fallas en dispositivos conectados).

## 9. Big data, anonimización y seudonimización (clase 7)

**Contexto:** el aumento acelerado de la implementación de IA se explica por tres factores: **poder de
cómputo** (la nube como motor de IA), **explosión de datos** (163 zettabytes proyectados para 2025,
IDC) y **progreso en algoritmos** (deep learning, reinforcement learning).

**Big data (Elena Gil, 2016).** "Conjunto de tecnologías que permite tratar cantidades masivas de datos
provenientes de fuentes dispares, con el objetivo de poder otorgarles una utilidad que proporcione
valor." Permite descubrir patrones de comportamiento de los clientes para crear publicidad dirigida,
predecir tendencias económicas o descubrir relaciones antes desconocidas entre variables.
**Riesgo:** análisis masivo de datos **frente a** privacidad de las personas.

**Anonimización.** Tratamiento de datos personales de manera tal que sea **imposible vincularlos** con
la persona a quien se hubiese podido identificar a través de aquellos.

**Seudonimización.** Tratamiento de manera tal que los datos **no se puedan atribuir a un individuo
determinado sin utilizar información adicional**. Se reemplaza el dato identificador (nombre,
identificador único) por un **código**.

**El modelo clásico de anonimización tenía 2 fases:**
1. Despojar los conjuntos de datos de todos los rasgos identificadores personales (PII): fecha de
   nacimiento, número de cédula de identidad.
2. Modificar o eliminar otras categorías de datos que pudieran actuar como identificadores en ese
   contexto concreto (p. ej. el banco elimina los números de tarjetas de crédito).

**Pero con big data** se incrementa la cantidad y diversidad de información, lo que **permite la
reidentificación** de individuos incluso después de haber sido anonimizados.

**Dos tipos de anonimización:**
- **Anonimización (plena)** — posibilidad **cero** de reidentificar directa o indirectamente a ninguno
  de los sujetos. **Difícil de conseguir** en bases de datos muy completas.
- **Anonimización funcional** — riesgo **mínimo** de reidentificación. Es la meta realista.

En el contexto de big data, el análisis de grandes volúmenes puede llegar a identificar personas a
partir de datos que **nadie habría considerado de identificación personal** o que antes eran anónimos,
así como gustos y comportamientos aunque no se conozca la identidad.

**Métodos de seudonimización:**
- **Encriptación** — clave secreta que permite al dueño de la clave reidentificar a los sujetos
  desencriptando (volver a asociar cada número de cédula con el nombre).
- **Tokenización** — aplicada principalmente en el sector financiero para el procesamiento de tarjetas
  de crédito. Sustituye los identificadores por valores de escasa utilidad que garantizan la misma
  operatividad, mediante un sistema de encriptado **unidireccional** que genera un número aleatorio.

### Cinco desafíos de las normas de protección de datos frente al big data
1. **No adaptación al entorno tecnológico** (big data, cloud computing).
2. **No implementación efectiva del principio de minimización de datos** — en la práctica se recopila
   más de lo mínimo necesario para el fin.
3. **Excesiva confianza en el consentimiento informado** — las personas no leen los términos y
   condiciones.
4. **La anonimización ha demostrado tener limitaciones** — cada vez es más fácil identificar personas.
5. **Riesgo de toma de decisiones de forma automática** — por ejemplo, el *scoring* crediticio.

## 10. El uso ético en la gestión de los datos

**Ética.** Ciencia filosófica que se encarga de reflexionar sobre los comportamientos morales del ser
humano con el objetivo de realizar valoraciones genéricas que pueden ser universales (Muñoz, J. M.,
2021).

**Inteligencia.** De *inter* ('entre') y *legere* ('leer, escoger'): la habilidad humana de analizar
todas las posibilidades y **escoger** la que se cree más adecuada según las circunstancias. El curso
plantea que ese proceso puede ser **auxiliado** por la IA.

**Autonomía y responsabilidad:**
- La **autonomía es un rasgo exclusivo de los seres humanos**: desde un punto de vista ético, solo el
  ser humano es capaz de escoger con libertad y guiar sus acciones.
- **El primer principio y norma ética esencial debería ser el control y la supervisión humana durante
  todo el ciclo de vida de un sistema de IA.**
- Los sistemas inteligentes actúan de forma **automática**: operan conforme a su programación, dentro
  de instrucciones y parámetros predefinidos, bajo una capacidad de decisión **aparentemente autónoma**
  que responde a un cálculo de probabilidades e impacto.
- Por ello, la responsabilidad ética debería situarse necesariamente sobre **las partes involucradas en
  su diseño y desarrollo**.

### Casos y ejemplos
- **2002** — EE.UU. e IBM inician un esfuerzo colaborativo para gestionar el alto volumen de datos del
  gobierno; de ahí nacen *IBM InfoSphere Stream* e *IBM Big Data*.
- **2012** — La National Science Foundation y el NIH lanzan el *Core Techniques and Technologies for
  Advancing Big Data Science & Engineering Program*.
- **Nueva York** destinó mayores recursos a la lucha contra el fraude fiscal: aumentaron los ingresos
  públicos en **USD 100 millones** y las transferencias fraudulentas disminuyeron en más de **USD 1.000
  millones** en el primer año (Thayer, 2014). También cruza datos de distintas agencias para abordar
  proactivamente el déficit de vivienda.
- **Países Bajos** — el sistema para combatir el fraude en servicios sociales se diseñó **para no ser
  de aplicación automática**, sino un elemento más de evaluación de riesgos que considera el personal,
  que es quien finalmente decide abrir una investigación o suspender una prestación. Lección: *la mejor
  forma de aprovechar las oportunidades de los datos pasa por combinar su potencial intrínseco con la
  **intervención humana***.
- **InBloom (EE.UU., 2014)** — startup que ofrecía a los centros educativos un espacio en la nube para
  almacenar los datos de la relación alumno-escuela; quebró tras ser acusada de vulnerar la privacidad
  de alumnos y escuelas, cuando los padres empezaron a preguntar: ¿podían terminar los historiales
  académicos en manos de terceros y determinar el futuro de sus hijos? ¿Cómo se protegían datos
  delicados como dificultades de aprendizaje? ¿InBloom almacenaría esta información de manera
  permanente? El caso evidenció el **interés comercial** por esta cantidad ilimitada de datos
  personales y la necesidad de ser cautelosos al incorporar sistemas de proveedores externos en
  entornos educativos.
- En 2015 la administración Obama promulgó una **Ley de Privacidad Digital para los Estudiantes**.
- **Uber y Airbnb** han sufrido crisis cíclicas de confianza por cómo gestionan los datos personales de
  sus clientes.

### Desafíos identificados
- **No existen aún estrategias nacionales o regionales** que definan los usos de estos datos en el
  sector público, su potencial y riesgos, los estándares de interoperabilidad necesarios, ni cómo
  articular la relación de confianza con la ciudadanía.
- La **discriminación algorítmica, la privacidad, la transparencia y los derechos digitales** no se han
  abordado de forma consistente como parte de una visión estratégica.
- Riesgo de que el aprendizaje automatizado, la predicción algorítmica y la IA **no sean aprovechados
  plenamente en beneficio de la ciudadanía**.
- Evitar que los gobiernos desarrollen sistemas que usen datos de los ciudadanos **sin incorporar
  paralelamente un enfoque ético y responsable desde el diseño**.

> Lo que está en juego es **sentar las bases de un nuevo contrato social** que permita una utilización
> masiva y responsable de los datos por parte de las entidades gubernamentales para proporcionar
> mejores servicios sociales, manteniendo la confianza de los ciudadanos.

### Discriminación algorítmica
- **Discriminación:** trato diferente y perjudicial que se da a una persona debido a categorizaciones
  **arbitrarias o irrelevantes**.
- Es **"algorítmica"** porque lo que permite que la discriminación se instale y prolifere en los
  sistemas informáticos es el uso del aprendizaje automatizado y la IA.
- Refiere a los procesos por los cuales los tipos de discriminación del mundo real **se reproducen en
  entornos de datos**, o a los que surgen exclusivamente en ellos, como cuando los sistemas de
  reconocimiento facial producen **más errores al procesar rostros no caucásicos**.
- También hay problemas de **insuficiencia, errores, y exceso o déficit de representación** de ciertos
  grupos, lo que puede redundar en una decisión algorítmica equivocada.
- La **falta de actualización oportuna** de los datos puede perjudicar al sujeto o a terceros: si no se
  actualizan los datos de una persona que estaba en un registro de deudores, puede resultar perjudicada
  al postular a un empleo o solicitar un crédito.
- **La capacidad teóricamente predictiva de estos sistemas no es más que la extrapolación al futuro de
  dinámicas identificadas en el pasado.** Un algoritmo entrenado con sentencias judiciales y
  reincidencia en EE.UU. aprenderá que la población afroamericana ha sufrido tasas de encarcelación
  superiores a las de la población blanca.
- Los **sesgos existen también en el proceso humano** de toma de decisiones. **El reto es incorporar
  los algoritmos, el aprendizaje automatizado y la IA para evitar los sesgos humanos, no para
  reproducirlos.**
- De ahí el surgimiento del **derecho a la explicabilidad**. El **RGPD** requiere a los organismos que
  manejan algoritmos un procesamiento **justo y transparente** y que expliquen cómo los sistemas
  automatizados toman decisiones, especialmente las que afectan significativamente las vidas
  individuales (acceso a prestaciones sociales, a un trabajo o a un crédito). Quien haya sufrido un
  daño (material o no) por vulneración de su privacidad tiene **derecho a compensación**.

### Opacidad: los tres tipos
Frente a los errores y riesgos de los sistemas, una de las exigencias más generalizadas es la
**transparencia**, íntimamente ligada a la evaluación y la **rendición de cuentas**: para que los
ciudadanos se formen un juicio, la información pertinente debe estar disponible.

La falta de transparencia en los sistemas de datos (qué información recogen, cómo la gestionan, cómo la
analizan, con quién la comparten, qué decisiones se toman a partir de ella y en base a qué factores)
supone **un problema de gran calado para la calidad de la democracia**.

El riesgo se acentúa porque los sistemas informáticos son percibidos por la mayoría de la población
como **"cajas negras"**: mecanismos incomprensibles que a menudo bordean lo mágico. No es posible
exigir al ciudadano un dominio pleno de los sistemas que afectan su vida cotidiana.

1. **Opacidad intencional.** Ocurre cuando un algoritmo no es transparente por motivos de **propiedad
   intelectual** (el motor de búsqueda de Google) o porque revelar su funcionamiento **llevaría a su
   irrelevancia** (detección de evasión de impuestos). En el segundo caso la opacidad respondería al
   interés público; pero usar un algoritmo opaco por razones de propiedad intelectual para **asignar
   una prestación social** podría impedir la transparencia y la rendición de cuentas del departamento
   responsable.
2. **Opacidad analfabeta.** Ocurre por la **falta de competencias técnicas** de las personas
   potencialmente afectadas para entender el funcionamiento de los algoritmos y modelos. Aunque un
   algoritmo sea explicable, si solo lo comprende la población con altas capacidades técnicas, la
   confianza entre los actores sufre. **La transparencia formal no sería aconsejable sin un esfuerzo
   pedagógico y de transparencia significativo.**
3. **Opacidad intrínseca.** Surge de la dificultad de explicar procesos algorítmicos en los que
   participan **redes neuronales complejas**: el sistema puede realizar tal cantidad de cálculos que ni
   sus creadores logran explicar cómo llegó a una solución. **Difícilmente justificable** cuando lo que
   está en juego forma parte de la canasta básica de servicios sociales o cuando esas redes deciden
   sobre la asignación de oportunidades vitales clave.

## 11. Modelo de Prevención de Infracciones (MPI)

### Contexto normativo
- **Ley N° 21.719** regula la protección y tratamiento de datos personales y crea la **Agencia de
  Protección de Datos Personales**.
- Modifica la **Ley N° 19.628**, elevando el estándar de protección.
- Incorpora los **artículos 49 a 53**, que establecen el **Modelo de Prevención de Infracciones (MPI)**.
- **Reglamento de Modelos de Prevención de Infracciones** — Ministerio de Hacienda, 2025. **Decreto
  N° 662, 9 de septiembre de 2026.**

**Objeto del reglamento.** Establecer requisitos, modalidades y procedimientos para la
**implementación, certificación, registro y supervisión** de los MPI. **Adopción voluntaria** por
cualquier responsable de datos, público o privado.

### Elementos del programa de cumplimiento
- **Designación de Delegado de Protección de Datos.**
- **Caracterización de datos y operaciones de tratamiento** (RAT).
- **Matriz de riesgos y protocolos de prevención.**
- **Mecanismos de reporte interno y externo.**
- **Sanciones internas y canales de denuncia confidencial.**

> Visto desde el curso, un MPI cruza tres planos: **compliance**, **seguridad de la información** y
> **gobierno de datos**.

### Delegado de Protección de Datos (DPD)
- **Designación obligatoria para la certificación** del MPI.
- Puede ser **dependiente o contratado externo**.
- Debe contar con **autonomía, conocimientos especializados y actualización permanente**.
- **Funciones:** asesorar, supervisar, capacitar y actuar como **punto de contacto con la Agencia**.

### Certificación y registro
- Certificación otorgada por la **Agencia de Protección de Datos**.
- **Vigencia: 3 años**, renovable.
- Registro en el **Registro Nacional de Sanciones y Cumplimiento**, de **acceso público**.
- **Causales de caducidad:** revocación, disolución, cese de actividad, resolución judicial.

### Supervisión y revocación
- La Agencia **supervisa** el cumplimiento del modelo certificado.
- Puede **requerir información, aplicar sanciones y revocar** la certificación por incumplimiento.
- El responsable puede **repostular**, acreditando medidas correctivas.

### Conclusiones
- El MPI es un mecanismo de **cumplimiento voluntario**, pero actúa como **atenuante de sanciones**.
- Requiere una **cultura organizacional** de protección de datos y **compromiso directivo**.
- Conviene preparar **desde ahora** la designación de delegados, la matriz de riesgos y los protocolos
  internos.

### Checklist de implementación del MPI (10 pasos)
1. **Planificación y gobernanza inicial** — nombrar un patrocinador interno (alta dirección) ·
   conformar equipo de trabajo (jurídico, TI, compliance, RR.HH.) · definir cronograma y presupuesto ·
   revisar normativa aplicable (Ley 19.628, Ley 21.719, Reglamento MPI).
2. **Diagnóstico de cumplimiento** — inventariar tratamientos y evaluar licitud · identificar brechas
   respecto a la Ley 21.719 y su reglamento · analizar riesgos y sanciones potenciales (arts. 34 bis,
   ter, quáter) · preparar informe de brechas y plan de acción.
3. **Delegado de Protección de Datos** — designarlo (obligatorio para certificación) · asegurar
   autonomía, competencias y recursos · publicar datos de contacto y notificar a la Agencia · definir
   **líneas de reporte directo a la máxima autoridad**.
4. **Registro y caracterización de datos** — crear o actualizar el **RAT**: tipos de datos,
   finalidades, bases de licitud, transferencias · categorías de titulares y terceros receptores ·
   plazos de conservación y **decisiones automatizadas**.
5. **Matriz de riesgos y controles** — identificar procesos críticos con mayor riesgo de infracción ·
   elaborar matriz de riesgos (gravedad y probabilidad) · definir controles preventivos y correctivos.
6. **Programa de cumplimiento** — redactar el documento con los elementos mínimos (protocolos, reglas y
   procedimientos · mecanismos de reporte interno y externo · sanciones internas y medidas
   disciplinarias) · incorporar obligaciones en **contratos y reglamento interno**.
7. **Capacitación y difusión** — plan de capacitación continua para todo el personal · sesiones de
   sensibilización en cultura de protección de datos · difundir el programa a trabajadores y
   prestadores.
8. **Implementación y operación** — poner en marcha **canales de denuncia confidenciales** · activar
   mecanismos de reporte a la Agencia y a los titulares · ejecutar planes de contingencia y respuesta
   ante incidentes.
9. **Certificación y registro** — solicitar la certificación ante la Agencia · preparar antecedentes y
   documentación exigida · verificar la incorporación al Registro Nacional de Sanciones y Cumplimiento.
10. **Supervisión continua** — definir indicadores de desempeño y mecanismos de monitoreo · realizar
    **auditorías internas periódicas** · actualizar el programa ante cambios normativos o nuevos
    tratamientos · **renovar la certificación cada 3 años**.
