---
name: maestria-ia
description: >
  Master expert index for @ArmandoArV's Magíster en Inteligencia Artificial at the Pontificia
  Universidad Católica de Chile (Maestria-IA repo). Acts as the umbrella tutor spanning ALL courses:
  Aprendizaje Supervisado (EPG4001), Aprendizaje No Supervisado (EPG4002), Fundamentos Matemáticos
  de IA (IMT3850), Bases de Datos, Introducción a Data Science (IMT3860), and Ética en IA.
  Use this skill whenever the user asks a broad or cross-course question about their maestría/master's,
  is unsure which course a topic belongs to, wants a program overview, or works anywhere in the
  Maestria-IA repository without naming a specific course. It routes to the dedicated per-course
  skills for depth and directly covers the courses that lack a dedicated skill (Bases de Datos,
  Data Science, Ética). Also trigger on terms like maestría, magíster IA, MIA, EPG4001, EPG4002,
  IMT3850, IMT3860, álgebra relacional, SQL, ciencia de datos, inferencia estadística, EDA,
  ética de la IA, sesgo algorítmico, XAI, SHAP, LIME, or any request that mixes topics from
  several courses. Respond in Spanish when the user writes in Spanish.
---

# Magíster en Inteligencia Artificial (PUC Chile) — Master Index

Umbrella knowledge base for the whole maestría. Use it to answer cross-course questions, figure out
which course a topic belongs to, and route to the dedicated per-course skill for deep work. For a
single-course question, the specific skill below usually triggers on its own — this skill is the map.

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
| Bases de Datos | — | A. L. Reyes | — | 📄 cubierta aquí (§1) |
| Introducción a Data Science | IMT3860 | A. Cataldo | — | 📄 cubierta aquí (§2) |
| Ética en IA | — | — | — | 📄 cubierta aquí (§3) |

> Repo: `D:\Maestria-IA`. Dedicated skills marked "(repo)" live under `.copilot/skills/` and load
> when working inside the repository; "(global)" skills load anywhere.

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
muchos datos no implica N = todo ni que baste con correlaciones — se necesitan modelos y contexto.

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
- **SHAP** — atribución de contribución de cada variable a la predicción (valores de Shapley);
  gráficos summary, bar, dependence, force.
- **LIME** — explicación local aproximando el modelo alrededor de una instancia.
- Diagnóstico de desempeño y sesgo con matriz de confusión (p. ej. Random Forest).

---

## Notas del programa

- **Institución:** Pontificia Universidad Católica de Chile, Magíster en Inteligencia Artificial.
- **Idioma:** cursos en español; responder en español salvo que el usuario escriba en inglés.
- **Utilidad:** `pdf-reader` (global) extrae texto de PDFs y `md_to_pdf.py` (repo) genera PDFs desde Markdown.
- **Para profundizar** en EPG4001/EPG4002/IMT3850, deja que su skill dedicada (global) tome el control;
  este índice solo enruta y cubre los cursos sin skill propia.
