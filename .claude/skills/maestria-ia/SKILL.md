---
name: maestria-ia
description: >
  Umbrella index/router for @ArmandoArV's Magíster en Inteligencia Artificial (PUC Chile,
  Maestria-IA repo), spanning ALL courses: Aprendizaje Supervisado (EPG4001), Aprendizaje No
  Supervisado (EPG4002), Fundamentos Matemáticos de IA (IMT3850), Bases de Datos, Introducción a
  Data Science (IMT3860), Ética en IA, Recuperación de Información (INF3841), Gobernanza de Datos, Deep Learning
  (INF3812), Deep Learning Avanzado / Advanced Topics in AI (INF3813), Computación de Alto Rendimiento
  (IMT3870), and Big Data (INF3862). Use for broad or
  cross-course questions about the maestría, when unsure which course a topic belongs to, for a
  program overview, or when working in the Maestria-IA repo without naming a course. Routes to the
  per-course skills for depth and directly covers courses lacking one (Bases de Datos, Data Science,
  Ética). Also trigger on maestría, magíster IA, MIA, EPG4001, EPG4002,
  IMT3850, IMT3860, INF3841, álgebra relacional, SQL, ciencia de datos, inferencia estadística, EDA,
  ética de la IA, sesgo algorítmico, XAI, SHAP, LIME, recuperación de información, information
  retrieval, descriptores de imágenes, procesamiento de imágenes, convolución, detección de bordes,
  Sobel, Canny, histograma, HOG, EHD, búsqueda por similitud, OpenCV, gobernanza de datos, gobierno de
  datos, DAMA, DMBOK, protección de datos personales, Ley 21.719, RAT, EIPD, ISO 42001, ISO 27001,
  INF3812, deep learning, aprendizaje profundo, red neuronal, MLP, backpropagation, CNN, RNN, LSTM,
  Transformer, atención, PyTorch, dropout, Adam, transfer learning, IMT3870, computación de alto
  rendimiento, HPC, programación paralela, paralelismo, FLOPS, intensidad aritmética, jerarquía de
  memoria, caché, GIL, multiprocessing, multithreading, pipelining, superescalar, peak performance,
  speedup, eficiencia paralela, Ley de Amdahl, Ley de Gustafson, escalabilidad fuerte, escalabilidad
  débil, joblib, memoria compartida, memoria distribuida, MPI, OpenMP, línea de caché, localidad de
  datos, coherencia de caché, MESI, granularidad, embarrassingly parallel, condición de carrera,
  thread safe, Numba, njit, prange, JIT, vectorización, INF3862, big data, almacenamiento de datos,
  DBMS, OLTP, OLAP, ACID, transacción, motor columnar, poda de columnas, DuckDB, SQLite, NoSQL,
  clave-valor, documental, grafos, series temporales, base de datos vectorial, embedding, RAG,
  sharding, replicación, data warehouse, modelado dimensional, tabla de hechos, ETL, ELT, data lake,
  object storage, Parquet, schema-on-read, lakehouse, Delta Lake, Apache Iceberg, Airflow, DAG,
  Dagster, asset, materialización, dbt, Airbyte, Hadoop, HDFS, NameNode, DataNode, réplica, YARN,
  MapReduce, mapper, reducer, shuffle, input split, skew, Cloudera, Amazon EMR, INF3813, deep learning
  avanzado, advanced topics in AI, CENIA, atención, self-attention, RoPE, máscara causal, RMSNorm,
  SwiGLU, caché KV, GQA, MLA, FlashAttention, MoE, BERT, T5, GPT, transfer learning, feature
  extraction, fine-tuning, PEFT, LoRA, catastrophic forgetting, modelos fundacionales, aprendizaje
  autosupervisado, self-supervised, MAE, ViT, CLIP, zero-shot, prompting, scaling laws,
  interpretabilidad mecanicista, cabeza de inducción, logit lens, activation patching, probe lineal,
  SAE, entity binding, GNN, reinforcement learning.
  Respond in Spanish when the user writes in Spanish.
---

# Magíster en Inteligencia Artificial (PUC Chile): Master Index

Umbrella knowledge base for the whole maestría. Use it to answer cross-course questions, figure out
which course a topic belongs to, and route to the dedicated per-course skill for deep work. For a
single-course question, the specific skill below usually triggers on its own: this skill is the map.

## How to use this skill

1. **Identify the course** from the routing table, then load the matching dedicated skill for depth.
2. **For courses without a dedicated skill** (Bases de Datos, Data Science, Ética), answer directly
   from the sections in this file.
3. **Respond in the student's language** (Spanish course → Spanish answer). Keep notation standard.
4. **Match the conventions each course uses** (libraries, notation) rather than introducing new ones.

## Course routing table

| Curso | Código | Profesor | Skill dedicada | Estado |
|-------|--------|----------|----------------|--------|
| Aprendizaje Supervisado | EPG4001 | J. L. Bazán | `aprendizaje-supervisado` (global) | ✅ completa (Clases 1–7) |
| Aprendizaje No Supervisado | EPG4002 | J. Acosta | `aprendizaje-no-supervisado` (global) | ✅ completa |
| Fundamentos Matemáticos de IA | IMT3850 | M. A. Sánchez | `fundamentos-matematicos-ia` (global) | ✅ completa |
| Bases de Datos | - | A. L. Reyes | - | 📄 cubierta aquí (§1) |
| Introducción a Data Science | IMT3860 | A. Cataldo | - | 📄 cubierta aquí (§2) |
| Ética en IA | - | - | - | 📄 cubierta aquí (§3) |
| Recuperación de Información | INF3841 | J. M. Barrios | `recuperacion-informacion` (global) | ✅ completa (Sesiones 01–03) |
| Gobernanza de Datos | - | A. Pumarino | `gobernanza-datos` (repo) | ✅ completa (Clases 1–7) |
| Deep Learning | INF3812 | H. Löbel | `deep-learning` (repo) | ✅ completa (Sesiones 1–9) |
| Deep Learning Avanzado | INF3813 | Equipo CENIA | `deep-learning-avanzado` (repo) | ✅ Clases 1–4 · faltan GNNs, integración y RL |
| Computación de Alto Rendimiento | IMT3870 | I. Labarca | `computacion-alto-rendimiento` (repo) | ✅ completa (Clases 01–08) |
| Big Data | INF3862 | S. Hagedorn | `big-data` (repo) | ✅ completa (Clases 01–03) |

> Repo: `~/Maestria-IA`. **Todas** las skills dedicadas viven hoy bajo `.claude/skills/` del repo y
> cargan al trabajar dentro de él. Las marcas "(global)"/"(repo)" reflejan su origen histórico, no su
> ubicación actual.

## Topic → course cheat sheet

- Regresión lineal/logística, LDA/QDA, Naive Bayes, árboles, Random Forest, SVM, KNN, ROC, F1,
  validación cruzada, bootstrap, Ridge/Lasso → **EPG4001** (`aprendizaje-supervisado`).
- Clustering (K-means, PAM, jerárquico, Ward), distancia de Gower, PCA, número de clusters
  (codo, silhouette, gap) → **EPG4002** (`aprendizaje-no-supervisado`).
- Álgebra lineal, SVD, mínimos cuadrados, probabilidad, desigualdades de concentración, LLN/CLT,
  optimización, convexidad, gradiente/Newton → **IMT3850** (`fundamentos-matematicos-ia`).
- Álgebra relacional, SQL, modelo entidad-relación, llaves → **Bases de Datos** (§1).
- Qué es la ciencia de datos, Big Data, muestreo/poblaciones, inferencia estadística, distribuciones,
  EDA → **IMT3860 / Data Science** (§2).
- Sesgo algorítmico, justicia, responsabilidad, sistemas sociotécnicos, explicabilidad (SHAP/LIME)
  → **Ética en IA** (§3).
- Recuperación de información (IR/RIM), descriptores de contenido, procesamiento de imágenes,
  convolución/kernels, detección de bordes (Sobel, Canny, LoG/DoG), histogramas/OMD, HOG/EHD,
  búsqueda por similitud k-NN, OpenCV → **INF3841** (`recuperacion-informacion`, resumen en §4).
- Gobierno/gobernanza de datos, DAMA/DMBOK, activos de información, arquitectura de información, datos
  maestros, metadatos, calidad de datos, protección de datos personales, Ley 21.719, RAT, EIPD, ISO
  27001/42001, Modelo de Prevención de Infracciones, anonimización → **Gobernanza de Datos**
  (`gobernanza-datos`).
- Redes neuronales, MLP, backpropagation, descenso de gradiente estocástico, Adam, dropout, batch
  normalization, CNN/convolución, RNN/LSTM/GRU, embeddings, word2vec, seq2seq, atención, Transformer,
  transfer learning, PyTorch → **INF3812 / Deep Learning** (`deep-learning`).
- Transformers en detalle (Q/K/V, RoPE, máscara causal, RMSNorm, SwiGLU, caché KV, GQA/MQA/MLA,
  FlashAttention, atención dispersa y lineal, MoE), familias GPT/BERT/T5, transferencia de conocimiento
  (feature extraction, fine-tuning, PEFT/LoRA, catastrophic forgetting), aprendizaje autosupervisado
  (GPT, MAE, CLIP, SimCLR/DINO), interpretabilidad mecanicista (cabezas de inducción, logit lens,
  activation patching, probes lineales, SAEs), GNNs y RL → **INF3813 / Deep Learning Avanzado**
  (`deep-learning-avanzado`, resumen en §6).
- Computación de alto rendimiento, paralelismo, FLOP/FLOPS, Ley de Moore, TOP500, arquitectura de Von
  Neumann, latencia y ancho de banda, T(n) = α + βn, cpu-bound vs. memory-bound, intensidad
  aritmética, GEMM/DAXPY, jerarquía de memoria y cachés, procesos e hilos, multiprocessing vs.
  multithreading vs. hyperthreading, GIL de Python, pipelining y procesadores superescalares (R_peak
  vs. R_max), joblib (`Parallel`/`delayed`, fork vs. spawn, pickle), speedup y eficiencia, Ley de
  Amdahl y Ley de Gustafson, escalabilidad fuerte y débil, memoria compartida vs. distribuida, MPI y
  OpenMP, mapeo y línea de caché, localidad temporal/espacial, coherencia y MESI, granularidad,
  problemas perfectamente paralelos, condiciones de carrera y locks, vectorización, Numba (`@njit`,
  `prange`, JIT/LLVM) → **IMT3870** (`computacion-alto-rendimiento`).
- Almacenamiento de datos, DBMS, OLTP vs. OLAP, motores de filas vs. columnares (SQLite/DuckDB,
  poda de columnas), modelos de datos (relacional, clave-valor, documental, grafos, series
  temporales, vectorial/RAG), índices y planes de consulta, sharding y replicación, Data Warehouse y
  modelado dimensional, Data Lake y object storage (S3, Parquet, schema-on-read), Lakehouse, Delta
  Lake e Iceberg, ETL/ELT y sus técnicas de transformación, idempotencia, UPSERT/MERGE, batch vs.
  streaming, orquestación con Airflow (DAG) y Dagster (assets), dbt/Airbyte/Glue, Hadoop (HDFS,
  NameNode/DataNode, réplicas, YARN) y MapReduce (splits, shuffle, skew, K-means distribuido),
  Cloudera, Amazon EMR → **INF3862 / Big Data** (`big-data`, resumen en §5).

---

## 1. Bases de Datos (Prof. A. L. Reyes)

Curso de modelado y consulta de datos relacionales. Trabajo práctico en **SQLite** (`guia2.db`,
`ev1.db`) y evaluación de **álgebra relacional**.

### 1.1 Álgebra relacional
Operadores fundamentales (notación del curso):

| Operador | Símbolo | Significado |
|----------|---------|-------------|
| Selección | σ_condición(R) | filas que cumplen la condición |
| Proyección | π_atributos(R) | columnas seleccionadas (elimina duplicados) |
| Producto/Join | R ⋈_cond S | combina tuplas que cumplen la condición de join |
| Renombre | ρ_a→b(R) | renombra atributos/relación (para self-joins) |
| Unión / Diferencia | R ∪ S, R − S | conjuntos de tuplas compatibles |

**Patrones clave:**
- "Los que NO…" → **diferencia**: π(todos) − π(los que sí).
- "Solo en categorías X o Y" → π(todos) − π(los que actuaron en alguna categoría distinta de X,Y).
- "Más de un director/valor distinto" → **self-join** con ρ y σ_(dir ≠ dir2).

**Ejemplo (esquema películas):** actores(<u>id</u>, anombre); peliculas(<u>id</u>, pnombre, año,
categoria, calificacion, pdirector); actuo_en(id_actor, id_pelicula).
Actores en películas de 'C. Nolan':
```
π_anombre( actores ⋈_{id=id_actor} actuo_en ⋈_{id_pelicula=id}
           σ_{pdirector='C. Nolan'}(peliculas) )
```

### 1.2 SQL (SQLite)
Traducción directa del álgebra: σ→`WHERE`, π→`SELECT`, ⋈→`JOIN ... ON`, ρ→alias, −→`EXCEPT`,
∪→`UNION`. Agregación con `GROUP BY`/`HAVING`, `COUNT/SUM/AVG`, subconsultas y `DISTINCT`.
"Más de un director": `GROUP BY actor HAVING COUNT(DISTINCT director) > 1`.

---

## 2. Introducción a Data Science (IMT3860, Prof. A. Cataldo)

### 2.1 ¿Qué es la ciencia de datos?
Ciencia de extraer información significativa de los datos: formular una pregunta cuantitativa,
**recolectar y limpiar**, **analizar** y **comunicar** la respuesta a la audiencia relevante.
A diferencia de la ciencia clásica (foco en causalidad), integra un enfoque interdisciplinario.

**Big Data (las V):** Volumen, Velocidad, Variedad (estructurada/no estructurada), Veracidad, Valor.
Definición relativa: "es Big Data cuando no cabe en una sola unidad de cómputo". Advertencia: tener
muchos datos no implica N = todo ni que baste con correlaciones: se necesitan modelos y contexto.

### 2.2 Inferencia estadística
Objetivo: concluir sobre una **población** (N) a partir de una **muestra** (n) ruidosa. Dos fuentes
de aleatoriedad: la del proceso y la de la recolección. Cuidar **representatividad** y **sesgo**
(datos faltantes, diseño del estudio, variables no observadas).

**Modelo estadístico:** representación matemática (con parámetros desconocidos) del proceso
subyacente; se construye vía EDA y estadística descriptiva.

### 2.3 Probabilidad y distribuciones
- Variable aleatoria X; **pdf** f_X(x); **cdf** F_X(x) = P(X ≤ x); supervivencia P(X > x).
- El área bajo la pdf entre a y b es P(a ≤ X ≤ b).
- Distribuciones paramétricas usuales: uniforme, normal, lognormal, Poisson, Weibull, Gamma,
  exponencial.

### 2.4 EDA (Análisis Exploratorio de Datos)
Estadística descriptiva cuantitativa y gráfica antes de modelar. Trabajo en Python (pandas,
matplotlib, geopandas para datos censales/geoespaciales; HDF5 para datasets grandes: nsfg, gss,
brfss). Talleres: análisis descriptivo (elecciones USA 2020), datos del Censo RM.

---

## 3. Ética en Inteligencia Artificial

Curso sobre las implicancias éticas y sociales de la IA. Lecturas base: Coeckelbergh, *Ética de la
Inteligencia Artificial*; Kudina & van de Poel, *A sociotechnical perspective on AI*; lecturas sobre
sesgos del algoritmo.

### 3.1 Sesgo algorítmico
El sesgo **no comienza en el algoritmo**: la IA **amplifica, escala y despersonaliza** sesgos
humanos y patrones sociales previos. Rompe la ilusión de "objetividad automatizada": el algoritmo no
elimina la subjetividad del proceso (p. ej. de contratación), la automatiza. Caso de estudio:
*Survival of the Best Fit* (contratación automatizada discriminatoria).

### 3.2 Perspectiva sociotécnica
La IA no es un artefacto aislado sino un **sistema sociotécnico**: tecnología + personas +
instituciones + normas. La responsabilidad es **difusa** (¿quién responde cuando el modelo
discrimina: el usuario, el equipo que lo diseñó, la empresa que lo implementó sin auditoría?) y la
**opacidad** dificulta la rendición de cuentas.

### 3.3 Justicia, responsabilidad y explicabilidad (XAI)
Principios: fairness, accountability, transparency. La **explicabilidad** hace auditables las
decisiones de modelos opacos. Herramientas usadas en laboratorio (Python):
- **SHAP**: atribución de contribución de cada variable a la predicción (valores de Shapley);
  gráficos summary, bar, dependence, force.
- **LIME**: explicación local aproximando el modelo alrededor de una instancia.
- Diagnóstico de desempeño y sesgo con matriz de confusión (p. ej. Random Forest).

---

## 4. Recuperación de Información (INF3841, Prof. Juan Manuel Barrios)

> **Skill dedicada:** `recuperacion-informacion`. Cárgala para cualquier pregunta de INF3841:
> tiene los apuntes por clase, las recetas de OpenCV y el formato de las evaluaciones.

Curso de **Recuperación de Información (multimedia)**: cómo representar, indexar y buscar contenido
(imágenes, audio, texto) por *similitud*, no por metadatos. 9 sesiones (03-ago a 05-oct 2026) en 3
partes: **(1) Descriptores de contenido** (imágenes, audio, texto, 5 sesiones), **(2) Búsquedas por
similitud** (índices multidimensionales, evaluación de efectividad, alta dimensionalidad, 2 sesiones),
**(3) Descriptores avanzados** (deep features de imágenes y texto, 2 sesiones). Trabajo en **Python +
OpenCV** (`cv2`, imágenes como matrices NumPy; también C++ con `cv::Mat`).

- **Evaluación:** individual, sin copia ni IA generativa. NF = (C1 + C2 + T1 + T2)/4, aprueba con
  NF ≥ 4.0. **Tareas** (T1, T2) en Python: solo `.py`, hay evaluador automático con hasta +10 décimas
  bonus. **Controles** (C1, C2) en papel/Excel/PDF (no se programa). Entregas parciales cada domingo
  con feedback; no se aceptan atrasos.
- **Temas cubiertos:** fundamentos de IR (relevancia, ranking, IR vs. BD, RIM), procesamiento de
  imágenes (operadores punto a punto, histograma, ecualización, Otsu, convolución, blur gaussiano,
  mediana, morfología), detección de bordes (Prewitt, Sobel, Scharr, Laplaciano, LoG, DoG, Canny),
  descriptores globales de gris (vector de intensidades, OMD, histogramas por zona, spatial pyramid,
  HOG, EHD, descriptor basado en Canny), color (sistema visual humano, cubo RGB, histogramas 3×1D vs
  3D, división regular de bins, CIE LAB, EMD) y búsqueda por similitud k-NN.
- **Bibliografía:** Gonzalez & Woods, *Digital Image Processing* (2008); Baeza-Yates & Ribeiro-Neto,
  *Modern Information Retrieval* (2011); Knees et al., *Music Similarity and Retrieval* (2016);
  Chollet, *Deep Learning with Python* 2ª ed. (2021).

---

## 5. Big Data (INF3862, Prof. Sebastián Hagedorn)

> **Skill dedicada:** `big-data`. Cárgala para cualquier pregunta de INF3862: tiene los apuntes por
> clase, las rúbricas de las actividades y el benchmark OLTP vs. OLAP ya medido.

Curso sobre **la pila de datos de abajo hacia arriba**: dónde viven los datos, cómo se mueven y cómo
se procesan cuando no caben en una máquina. Material en `~/Maestria-IA/BigData/` (3 clases
disponibles).

- **Clase 01: Almacenamiento de datos:** bases de datos y DBMS (query engine, storage manager,
  esquema y metadatos, transacciones y **ACID**), **OLTP vs. OLAP**, organización física **por filas
  vs. por columnas** (poda de columnas y compresión), **modelos de datos** (relacional, clave-valor,
  documental, grafos, series temporales, **vectorial**/RAG), rendimiento (índices, caché, planes,
  particionamiento) y escala (scale up/out, **sharding** vs. **replicación**), **Data Warehouse**
  (tres capas, ETL, modelado dimensional), **Data Lake** (object storage, schema-on-read y sus
  problemas) y **Lakehouse / Delta Lake** (delta log, commit, versiones; **Iceberg**).
- **Clase 02: ETL y orquestación:** estrategias de **extracción** (full, incremental, update
  notification), **técnicas de transformación** (limpiar, deduplicar, estandarizar, derivar, join,
  split, resumir, cifrar), estrategias de **carga** (full/incremental, UPSERT/MERGE, batch vs.
  streaming, **idempotencia**), **ETL vs. ELT**, **Apache Airflow** (DAG, tasks, operators, Jinja,
  datasets) y **Dagster** (assets, materializaciones); ecosistema dbt / Airbyte / AWS Glue /
  Lakeflow.
- **Clase 03: Apache Hadoop:** límites de una máquina y escalamiento horizontal, **HDFS** (bloques,
  réplicas, NameNode/DataNode, localidad), **YARN** (ResourceManager, ApplicationMaster, containers)
  y **MapReduce** paso a paso (input splits, map, particionador, shuffle, sort, reduce, **skew**,
  reintentos), con **K-means distribuido** como caso; **Cloudera** y **Amazon EMR**.
- **Evaluación:** actividades prácticas con entregables específicos: Actividad 1 (**solo
  formulario**: 7 objetivas 70 % + 2 de interpretación 30 %), Actividad 2 (**1 punto**: `.py` +
  captura de una run exitosa, más tres preguntas teóricas con fuentes) y Actividad 3 (**PDF de tres
  láminas**: decisión, diagrama HDFS, diagrama MapReduce).
- **Criterio transversal del curso:** *una misma solución no sirve para todas las necesidades*. Toda
  recomendación sale del **patrón de acceso** y debe **nombrar su costo**. Distinguir siempre
  **formato de archivo** (Parquet) ≠ **formato de tabla** (Delta/Iceberg) ≠ **motor de consultas** ≠
  **arquitectura** (Lakehouse), y **orquestador** ≠ **motor de procesamiento**.

> **Ojo con el solapamiento:** *Bases de Datos* (§1, Prof. A. L. Reyes) cubre álgebra relacional y
> SQL; *Data Science* (§2) usa "Big Data" en el sentido de las **V**. Las preguntas de
> **almacenamiento, pipelines y cómputo distribuido** son de **INF3862**.

---

## 6. Deep Learning Avanzado · Advanced Topics in AI (INF3813, equipo CENIA)

> **Skill dedicada:** `deep-learning-avanzado`. Cárgala para cualquier pregunta de INF3813: tiene las
> cuatro clases con sus ecuaciones y las cifras medidas en las diapositivas, más los prácticos y el
> Laboratorio 1. Para ubicar y abrir el material en disco, `dla-material` (skill local de
> `DeepLearningAvanzado/`).

Continuación de **INF3812**, dictada por el **CENIA** en **MIA 2026-2**: Felipe Urrutia (introducción e
interpretabilidad), Felipe del Río (fundamentos y RL), Nicolás Alvarado (GNNs y técnicas avanzadas),
Rex Liu (RL y proyecto), Andreina Cota (ayudante). Material en `~/Maestria-IA/DeepLearningAvanzado/`
(clases 1–4 disponibles).

- **Clase 1 · Panorama + Transformers:** los 8 módulos del curso y 5 casos de estudio (DeepSeek-R1,
  Gemini Robotics, AlphaFold 3, circuit tracing en Claude, AlphaEvolve); un **decoder-only moderno tipo
  Llama paso a paso** (tokens → embeddings → Q/K/V → RoPE → scores → máscara causal → softmax → mezcla
  de values → multi-head → residual + MLP SwiGLU → unembedding → probabilidades → generación con caché
  KV); las tres familias **GPT / BERT / T5**; historia de la atención y de los embeddings posicionales
  (sinusoidal, Shaw, T5, ALiBi, **RoPE**); y arquitecturas y eficiencia (sliding window, DSA, atención
  lineal, Strassen, **FlashAttention**, **MHA/GQA/MQA/MLA**, caché KV, **MoE**).
- **Clase 2 · Transferencia de conocimiento:** tipos de transferencia; **feature extraction** vs.
  **fine-tuning**; embeddings, búsqueda semántica y bases de datos vectoriales; **catastrophic
  forgetting** y sus mitigaciones; **PEFT/LoRA** (ΔW = BA de rango bajo); foundation models.
- **Clase 3 · Modelos autosupervisados:** tareas de pretexto y las tres familias de objetivos
  (generativo, contrastivo, adversarial); **GPT** y modelamiento de lenguaje, scaling laws, prompting
  zero-/few-shot y chain-of-thought; **ViT + MAE** (75 % de parches ocultos); SimCLR/MoCo/BYOL/DINO;
  **CLIP** (WIT de 400 M pares, objetivo contrastivo, zero-shot con «A photo of a {class}»).
- **Clase 4 · Interpretabilidad en Transformers:** protocolo de **siete pasos** (observar → proponer →
  demostrar a mano → caracterizar → intervenir → descomponer → confirmar) sobre **cabezas de
  inducción** en un Transformer de juguete: patrones de atención, logit lens, construcción a mano con
  RoPE, puntajes **pos/sym**, **activation patching** y ablación, **PCA** y **SAE TopK**, **probes
  lineales**.
- **Evaluación:** Laboratorio 1 (interpretabilidad, individual, entrega 24/11/2026 en Canvas),
  Laboratorio 2 (GNNs) y proyecto final. **El programa no especifica ponderaciones.**
- **Criterio transversal del curso:** separar siempre las dimensiones de diseño (conectividad ≠ memoria
  y ejecución ≠ forma de interacción ≠ posición ≠ capacidad) y **el tipo de evidencia** (observación ≠
  plausibilidad ≠ consistencia ≠ causal ≠ correlacional). *Los pesos de atención no son por sí solos
  una explicación causal.*

> **Ojo con el solapamiento:** **INF3812** (`deep-learning`, Prof. Löbel) cubre los fundamentos — MLP,
> CNN, entrenamiento, RNN/LSTM y una introducción a atención y Transformers. **INF3813** parte de ahí:
> si la pregunta es sobre RoPE, GQA, caché KV, LoRA, CLIP, MAE o interpretabilidad mecanicista, es
> **INF3813**.

---

## Notas del programa

- **Institución:** Pontificia Universidad Católica de Chile, Magíster en Inteligencia Artificial.
- **Idioma:** cursos en español; responder en español salvo que el usuario escriba en inglés.
- **Utilidad:** `pdf-reader` (global) extrae texto de PDFs y `md_to_pdf.py` (repo) genera PDFs desde Markdown.
- **Para profundizar** en EPG4001/EPG4002/IMT3850/INF3841/INF3812/INF3862/IMT3870 o en Gobernanza de
  Datos, deja que su skill dedicada tome el control; este índice solo enruta y cubre los cursos sin
  skill propia (Bases de Datos, Data Science, Ética).
