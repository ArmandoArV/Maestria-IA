# Clases 1-2 · Fundamentos: datos, información y gobierno de datos

Base conceptual del curso. Todo lo posterior (DAMA, protección de datos, gobernanza de IA) se apoya en
estas definiciones.

## 1. Contexto: por qué el dato importa ahora

**Estrategia de datos en las organizaciones — cuatro razones:**
1. **Toman mejores decisiones.** Decisiones basadas en hechos reales y no en suposiciones.
2. **Aumentan la eficiencia y reducen costos.** Detectar errores, optimizar procesos, reducir
   desperdicios.
3. **Impulsan el crecimiento y la innovación.** Entender clientes, mejorar productos, detectar
   oportunidades antes que la competencia.
4. **Tienen impacto en la privacidad y la ética.** ¿Quién los recoge? ¿Para qué se usan? ¿Cómo se
   protegen?

**Tres etapas de madurez del dato en las empresas:**
1. **Recolección y almacenamiento** — tienen mucha data, hacen reportes, quieren "hacer algo"
   significativo pero no saben por dónde empezar.
2. **Exploración, transformación y valor agregado** — organizan los datos y los explotan con
   dashboards, pero deciden de forma atemporal, en comités mensuales o trimestrales.
3. **Aprendizaje y optimización** — madurez: automatización, gobierno de datos y dashboards que
   permiten decidir en días u horas.

La meta es interconectar **hindsight** (retrospectiva), **insight** (conocimiento) y **foresight**
(previsión). Para eso es clave desarrollar **cultura de datos**, capacitar a las personas y alinear el
análisis con los objetivos estratégicos.

Problema diagnosticado en Latam y Chile: **falta de gobernanza, datos centralizados y brechas de
gestión**.

### Datos sintéticos
Información fabricada artificialmente que imita las características y distribuciones de datos reales
**sin contener información personal o sensible**; se generan con algoritmos que preservan la estructura
y las propiedades estadísticas del original.

- **Usos:** investigación científica, pruebas de software y sistemas, entrenamiento de modelos de IA.
  Permiten explorar enfoques sin acceder a datos sensibles y probar aplicaciones sin exponer datos
  reales.
- **Métodos:** remuestreo, modelado probabilístico y generativo, perturbación y enmascaramiento.
- Referencia usada en clase: `datos.gob.es`. Ejemplo ilustrativo: `thispersondoesnotexist.com`.

## 2. Gobierno de datos

### Definición del curso
> "Es un **proceso político** que abarca a las **personas**, los **procesos** y las **tecnologías** de
> la información necesarias para crear un manejo coherente y adecuado."

### Fases del gobierno de datos
1. **Armar un equipo** — personas de distintos departamentos: líderes, TI, propietarios de datos y
   usuarios finales. Permite adaptar el proyecto a las necesidades y objetivos específicos.
2. **Establecer objetivos** — definirlos y comunicarlos claramente para alinear a todos.
3. **Empezar pequeño** — un proyecto a escala reducida y manejable (p. ej. analizar los datos de un
   solo equipo: estado, recopilación, almacenamiento y uso). Evaluar el éxito y recién ahí definir
   cuánto presupuesto asignar.
4. **Fomentar la transparencia** — informar a las partes interesadas externas cómo se recopilan,
   almacenan y utilizan los datos, para mantener la confianza.
5. **Integrar a todos los departamentos** — que todos entiendan sus roles y responsabilidades y
   cooperen entre áreas.
6. **Definir riesgos** — identificar hitos de gestión de riesgos para mitigar violaciones de datos o
   vulnerabilidades de seguridad.
7. **Evaluar el proyecto** — al completarlo, medir su eficacia y determinar mejoras.
8. **Refinar continuamente** — mejora continua al ritmo de los avances tecnológicos, los cambios en
   las prácticas de gestión y la evolución de los requisitos reglamentarios.

> "Desarrollar un gobierno de datos no es fácil ni rápido, pero aporta valor al negocio."

### Componentes esenciales
No se puede **comprar** un programa de gobierno de datos listo: cada organización debe desarrollarlo
según sus necesidades, capacidades y presupuesto.

- **Estrategia** — visión para gestionar eficazmente los datos, alineada con los objetivos del negocio.
- **Personas** — el corazón del gobierno; equipo interdisciplinario con funciones y responsabilidades
  claras.
- **Cumplimiento** — políticas, procesos y normas uniformes para toda la organización.
- **Métricas** — KPI cuantificables y relevantes para las metas del negocio.
- **Tecnología** — herramientas adaptadas al tamaño y necesidades específicas de la empresa.
- **Comunicación** — informar el impacto en cada persona y fomentar la colaboración entre equipos.

## 3. Gobierno de información

Actividad organizacional orientada a:
1. **Adquisición** de información de una o más fuentes.
2. **Almacenamiento y administración** de la misma.
3. **Distribución** de esa información a quienes la necesitan.
4. **Disposición final** mediante archivado o borrado.
5. Se realiza generalmente a través del levantamiento, modelado y operación de la información en
   sistemas informáticos.
6. Cubre información **interna** de la organización y **externa** disponible.

> "El desafío es convertir datos en conocimiento, y usar la información como un **activo** para el
> negocio."

### Principios y definiciones básicas
- Casi cualquier cosa es información.
- La información es un **modelo (imperfecto) de la realidad**. Por lo tanto hay que **entender la
  realidad primero**: qué objetos se manejan y cómo se manejan.
- La información debe estar **al servicio del negocio**; influirá en su concepción, habilitación y
  eficiencia. Para eso hay que comprender el **Modelo del Negocio**.
- Vale la pena **anticipar necesidades futuras**. Contra incertidumbre, **flexibilidad**.
- Un sistema computacional es una representación de los objetos (información) que se manejan mediante
  reglas de negocio (programas) sobre dichos objetos.

### La información es imperfecta en estructura y contenido
1. **No representa la realidad** (se manejan clientes pero no las relaciones entre ellos).
2. **Tiene errores** (un apellido mal digitado, una fecha mal ingresada).
3. **No se ajusta a la realidad** (declaro 3 hijos e identifico a 2).
4. **Se vuelve caduca** (cambié el celular, la dirección). Regla práctica: **nunca almacenar la edad,
   casi nunca almacenar un cálculo**.
5. **No existe** (ingrese su número de fax).
6. **No da cuenta de la historia o es incoherente en el tiempo** (no hay series, o cambió la forma de
   medir: cómo medir un índice de precios).

### Qué le hace la información a un negocio
Lo **apoya** · lo **fortalece** · le establece **ventajas competitivas** · genera **barreras de
entrada** · lo **asegura** · lo hace **dependiente** · lo **crea** · … lo **destruye**.

### El uso de la información depende de cada negocio
1. En línea (Spotify).
2. En tiempo real (tráfico de autopistas).
3. Que conectan oferta y demanda (Uber, PedidosYa).
4. Donde la **calidad** es esencial (Censo).
5. Donde la **agregación** es esencial (mapas).
6. Donde la información **no es propia** (Bloomberg, X/Twitter).
7. Donde **el tiempo crea valor** (Conservador de Bienes Raíces, Justicia).
8. Donde el **modelo predictivo** es esencial (clima).
9. Donde el valor **no lo determina la operación** (en minería lo determina la exploración).

### Información de terceros
- No toda la información es propia: esa es una de las características centrales de **big data**.
- Operamos con grandes volúmenes cuyos **modelos y calidad no definimos ni manejamos**. El desafío es
  **cuánto creo en la información que uso**.
- Existen **restricciones de uso**: puedo usarla pero quizá no entregarla a un tercero. ¿Y los
  resultados de procesarla, puedo compartirlos?
- Desafío de la **anonimización y la seudoanonimización**.
- Una organización puede estar sometida a la regulación de **más de un país**: hay jurisdicciones y
  negocios que no permiten que la información salga del territorio o se comparta entre empresas.

### Características de la información
- Es un **continuo en el tiempo**: las series agregan valor; dibujar la curva es una contribución.
- **Se corrompe**, y se empieza a operar sobre información incierta.
- **Duración variable**: el registro de nacimiento dura infinito; el número de la ruleta dura hasta que
  se pagan las fichas.
- **Granularidad**: distintos usuarios necesitan distinto nivel de detalle, pero puede interesar la
  capacidad de **drill-down** hasta el dato elemental.
- **Oportunidad**: distinta en sistemas de tiempo real que para curvas históricas.

## 4. Activos de información

**Definición:** componentes de información estructurada (organizada) con **alta cohesión y bajo
acoplamiento**, junto a sus mecanismos de acceso y la relación entre componentes.

- Cada activo agrega valor por su sola existencia (es valioso para componentes del negocio) o porque
  **apoya a otro activo**.
- El valor será mayor si: **posibilita un negocio por sí mismo**, apoya a **más componentes o áreas**,
  **dura más** en el tiempo, apoya **más negocios**, permite **más formas de estructuración**.
- Un activo tiene **propiedades** (duración, origen, sensibilidad, etc.).
- Debe existir un **catálogo de activos de información** → **ISO/IEC 27001**.

**Cohesión y acoplamiento:** un conjunto de componentes tiene alta cohesión y bajo acoplamiento si los
elementos dentro de cada componente están muy relacionados entre sí (tiene sentido que estén agrupados)
y si dos componentes comparten pocos elementos (son independientes). Las **formas normales** de las
bases de datos ayudan a cumplirlo, aunque a veces se desnormaliza por eficiencia.

### Metodología de identificación de activos de información
**Paso A — identificar modelos/representaciones de información en:**
1. Objetivos estratégicos, productos y servicios, procesos de negocio, funciones operacionales y de
   soporte.
2. Sistemas computacionales.
3. Manuales de operación, auditoría y control.
4. Marcos o modelos de industria.
5. Negocios y sistemas de soporte similares.
6. Prácticas y artefactos requeridos en gobierno (directorio), alta administración, regulador,
   reportería.
7. Potenciales modelos de negocio futuros.

**Paso B — identificar entidades y relaciones en:**
1. Procesos.
2. Formularios físicos y templates de pantallas.
3. Reclamos (mail, redes sociales).
4. Diálogos de call center internos y externos.
5. Relaciones con terceros en la cadena de valor: clientes, proveedores, reguladores.
6. Catálogo de transacciones (interactivas o masivas) y planes de producción tecnológicos.
7. Máquinas o dispositivos físicos (sensores, sistemas de control).

**Paso C — construir el modelo:** identificar, caracterizar y relacionar componentes de información;
relacionarlos con procesos, sistemas, productos, roles, reportes, matrices productivas y stakeholders;
identificar **propietarios, contribuyentes y beneficiarios** de cada activo, con sus privilegios de
uso; **clasificar y valorizar** los activos.

### Control de la información: las preguntas incómodas
- ¿Quién es el **dueño** de la información? ¿Quién es responsable de mantenerla? ¿Qué puede hacer cada
  stakeholder con ella?
- Caso de la **información de salud**: ¿le pertenece al paciente? ¿Él debe administrarla? ¿Qué
  atribuciones tiene cada actor? (ejemplo de clase: la información de la pandemia COVID-19).
- ¿Quién es el dueño del **modelo** de información, es decir, de la estructura?
- De muchas cosas es responsable TI, el Data Modeler o el **Chief Data Officer**, pero **en algunos
  casos nadie**, por ejemplo cuando es información de terceros. Ahí se puede regular el mecanismo de
  adquisición, la conexión, la validación o el modelo interno de representación, pero no mucho más.

## 5. Arquitectura de información (visión global)

Conjunto de modelos de datos a nivel corporativo que da cuenta de los requerimientos de información del
negocio y de su manejo.

- Debe representar **todos los niveles implementativos**, del conceptual a la representación física:
  bases de datos, servidores, mecanismos de conexión, herramientas de replicación, respaldo, etc.
- Incluye **responsabilidades** (personas y funciones), **procesos** (y flujos), **políticas**,
  **procedimientos** y **tecnologías** de implementación.
- ¿La **seguridad** es parte de la arquitectura de información? Más bien deben **alinearse**.
- ¿La **provisión de servicios** es parte? Quizás en casos específicos.

El detalle de los tres modelos (capas, dominios, plataforma) está en `dama-practicas.md` §2.

## 6. Marcos y modelos de gestión de información

Los tres que el curso nombra: **DAMA DMBOK**, **CoBIT** e **ITIL**. El curso profundiza en DAMA (ver
`dama-practicas.md`) porque es el más difundido en Chile para gestión de información.

## 7. Clasificación de datos (White Paper OEA, edición 6, 2019)

### Principios
- **Apertura, transparencia y valores sociales.** La clasificación debe usarse con precaución y de
  acuerdo con la sensibilidad, el valor y la criticidad de los datos. Las restricciones de acceso solo
  deben elegirse cuando la divulgación sea perjudicial para intereses legítimos y obligaciones legales.
  **El desafío será no clasificar en exceso** por conveniencia o practicidad, lo que iría en detrimento
  de la transparencia y la confianza pública.
- **Enfoque basado en el contenido y tecnológicamente neutral.** La información se clasifica en función
  de su **contenido** y de los riesgos asociados a su compromiso, con independencia de su formato,
  medio u origen: analógica o digital, en un sistema, en medios de almacenamiento, en dispositivos
  móviles o en la nube. Confiar en fuentes públicas no determina automáticamente que la información
  **agregada** deba revelarse públicamente.
- **Enfoque de gestión de riesgos.** Protección graduada según el nivel de sensibilidad, valor y
  criticidad. Se consideran tanto el **daño potencial** del compromiso (divulgación no autorizada,
  modificación o pérdida) como el **valor potencial** de los datos.
- **Proporcionalidad.** La información se clasificará a un nivel **lo más bajo posible, pero tan alto
  como sea necesario**.
- **Papeles y responsabilidades claras**, confirmadas por el compromiso y la conciencia de seguridad de
  la gerencia.
- **Enfoque del ciclo de vida.** El sistema de clasificación debe considerar la información durante
  todo su ciclo: creación o recepción, almacenamiento, recuperación, modificaciones, transferencia,
  copia, transmisión y destrucción. La política **no debe estar escrita en piedra**: se evalúa
  regularmente.

### Implementación, paso a paso
1. **Inventario de activos de datos ("auditoría de datos").** Comprensión amplia de los tipos de datos
   procesados, su valor, sensibilidad y criticidad. Incluye identificar los **requisitos legales**
   aplicables y auditar las políticas y procedimientos existentes, roles y responsabilidades.
2. **Evaluación de riesgos.** Identificar y cuantificar riesgos de **gravedad y probabilidad**, y
   priorizarlos según los criterios de aceptación de riesgo de la organización.
3. **Definición de los niveles de protección y su aplicación**, agrupados por categorías de
   clasificación, para cada tipo de activo.
4. **Determinación de los papeles de gestión de datos.** Definir roles, responsabilidades y las
   obligaciones de gestión de riesgos de cada rol; traducirlos en **rutinas organizacionales** mediante
   políticas y procedimientos. Buena fase para revisar y actualizar las regulaciones internas.
5. **Clasificación.** Según la evaluación de riesgos se asigna el nivel considerando **individualmente
   cada objetivo de seguridad: confidencialidad, integridad y disponibilidad**. La clasificación
   general se asigna según el **valor más alto** entre los tres. Algunos sistemas reconocen un nivel
   combinado (alta confidencialidad, integridad moderada, baja disponibilidad).
6. **Consideraciones para tecnologías emergentes** (nube, móvil, IoT): enfoque basado en riesgo,
   independiente de si son equipos tradicionales on-premise, dispositivos móviles, nube o IoT.
7. **Monitoreo: supervisión y garantía de calidad.** Asignar una entidad responsable de supervisión,
   asesoramiento y revisión de las decisiones de clasificación: **CIO, CDO o CISO**.
8. **Revisión y ajuste periódico.** Revisiones sistemáticas que permitan ajustar el acceso y revisar
   los datos clasificados. Una metodología de **reclasificación** asegura medidas adecuadas al entorno
   de amenaza/riesgo actual y al valor y sensibilidad cambiantes.
