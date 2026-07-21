---
name: redaccion-informes
description: >
  Cómo redactar informes académicos para los cursos del Magíster en IA (PUC Chile) de @ArmandoArV,
  siguiendo la rúbrica del curso y el estilo visual LaTeX de la casa (formato del Informe Sociotécnico
  de Ética). Usa esta skill cuando el usuario pida escribir, redactar, estructurar, armar o dar formato
  a un informe, reporte, entrega o proyecto de un curso (p.ej. el proyecto de Aprendizaje No Supervisado
  EPG4002), o cuando quiera convertir un notebook/análisis en un documento entregable. Cubre la
  estructura obligatoria (Portada con integrantes, Introducción, Objetivos, Resultados con EDA + al
  menos dos técnicas + selección de modelo + técnica del marco teórico, Conclusión, Anexos con
  co-evaluación) y la plantilla LaTeX con portada tikz azul/dorado UC, titlesec, fancyhdr y natbib.
  Responde en español.
---

# Redacción de informes (Magíster en IA, PUC Chile)

Guía para producir informes de curso entregables: **estructura según rúbrica** + **estilo LaTeX de la
casa**. La plantilla LaTeX completa está en `references/plantilla-latex.tex` — léela y cópiala como
punto de partida.

## Cómo usar esta skill

1. **Confirma el entregable y el idioma.** Los cursos son en español → el informe va en español.
2. **Sigue la estructura obligatoria** (abajo). No omitas secciones de la rúbrica.
3. **Destila, no copies código.** Si el análisis vive en un notebook, extrae resultados, tablas y
   figuras; **no incluyas código Python** en el cuerpo del informe.
4. **Usa el estilo LaTeX de la casa** (`references/plantilla-latex.tex`): portada tikz azul/dorado con
   `Logo.png`, secciones en color `accent`, encabezado `fancyhdr`, bibliografía `natbib`.
5. **Compila y verifica**: `pdflatex → bibtex → pdflatex → pdflatex`. Revisa que no queden
   referencias/citas sin resolver y que las figuras se rendericen (usa `\graphicspath`).

## Estructura obligatoria (rúbrica)

1. **Portada.** Título, subtítulo, **nombres de todos los integrantes del grupo**, curso, profesor,
   universidad y fecha. (En la plantilla: bloque `titlepage`.)
2. **Introducción.** Descripción breve del contenido y del contexto del problema; cierra con un
   párrafo que anuncia cómo se organiza el documento.
3. **Objetivos.** Objetivo general + específicos, **ligados al contexto de los datos**.
4. **Resultados** (el núcleo). Presenta los principales resultados **en el contexto de la base de
   datos**, sin código. Debe incluir:
   - **Análisis exploratorio de datos** con indicadores, **tablas y gráficas** apropiadas.
   - **Al menos dos técnicas** de aprendizaje no supervisado vistas en clases (p.ej. K-Means, GMM,
     PCA, jerárquico) **con sus formas de seleccionar el mejor modelo** (Silhouette, codo,
     Calinski-Harabasz, Gap statistic, BIC/AIC, dendrograma, ARI…).
   - **La técnica descrita en el marco teórico** (la técnica moderna/de investigación del proyecto;
     p.ej. ECOD, Isolation Forest). Conviene una subsección "Marco teórico" antes de Resultados que
     la describa, y luego aplicarla dentro del análisis.
5. **Conclusión.** Relacionada explícitamente con los **resultados y los objetivos** planteados.
6. **Anexos.** Información adicional relevante (reproducibilidad, tablas extensas) **e incluir un
   Anexo de co-evaluación con una fila/valoración por cada integrante** del grupo.

## Reglas de contenido

- **Sin código**: los resultados se comunican con prosa, tablas (`booktabs`) y figuras. Referencia
  cada figura/tabla desde el texto (`Fig.~\ref{...}`, `Tabla~\ref{...}`).
- **Sin rayas largas (em-dash)**: no uses `---` (—) en el texto; el guion largo resta profesionalismo
  y "delata" texto generado. Usa comas, paréntesis o dos puntos según el caso. Los en-dash `--` en
  rangos y compuestos (`2019--2020`, `Calinski--Harabasz`) sí son correctos.
- **Cifras en español**: miles con punto (`1.296.675`), decimales con coma (`0,873`), porcentajes
  con espacio fino antes de `%` cuando aplique.
- **Cada técnica con su criterio de selección**: no basta aplicarla, hay que justificar por qué ese
  hiperparámetro/modelo (curva, métrica interna).
- **Trazabilidad**: los números provienen de la ejecución (notebook / `execution_log.json`); no
  inventes valores.
- **Figuras desde el notebook**: extrae las imágenes embebidas en los outputs (`image/png` en base64)
  a `figures/*.png` y decláralas con `\graphicspath{{figures/}{./}}`.

## Estilo LaTeX de la casa (resumen)

- `\documentclass[12pt, a4paper]{article}`, `babel` español, `geometry` margen 2.5cm, `onehalfspacing`.
- Colores: `accent` RGB(0,90,130), `ucblue` RGB(0,75,135), `ucgold` RGB(198,166,80).
- Secciones con `titlesec` en `accent` + regla horizontal; `fancyhdr` con título del informe a la
  izquierda y nombre del curso a la derecha.
- Portada `tikz`: barra superior `ucblue` (4cm) + línea `ucgold`, barra inferior simétrica, `Logo.png`
  centrado, título en `ucblue`.
- Bibliografía `natbib` (`\bibliographystyle{plainnat}`) con archivo `referencias.bib`.
- `Logo.png` está en el repo Maestria-IA (raíz y en `Etica/InformeSocioTecnicoAvance/`).

## Toolchain

Instalación mínima de TeX Live: **evita `siunitx`** (no instalado); formatea números a mano.
Disponibles: `booktabs`, `subcaption`, `caption`, `float`, `titlesec`, `natbib`, `tikz`, `fancyhdr`,
`enumitem`, `amsmath/amssymb`. Compila con `pdflatex`/`bibtex` (no hay `latexmk`).
