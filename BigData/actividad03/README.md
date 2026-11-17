# Actividad 03 — INF3862 Big Data

Entregable: **`Actividad03_BigData_ArredondoValle.pdf`**, formato 16:9: una **portada** con la
identidad UC (`Logo.png`, azul `#004B87` y oro `#C6A650`, los mismos de la plantilla LaTeX del
magíster) y las **tres láminas** que pide la rúbrica.

1. **Decisión** — comparación de los casos A y B con los cuatro criterios de la clase, elección
   justificada y alternativa para el caso descartado.
2. **HDFS** — bloques, réplicas, DataNodes, NameNode y la caída de DN1.
3. **MapReduce** — cuatro registros, pares intermedios, agrupación por clave y resultado.

## Cómo se construye

Los dos diagramas son **Mermaid** (`diagramas/*.mmd`, la fuente). `build.py` los renderiza a SVG en
una página por diagrama con Chrome headless, los empotra en `deck.template.html` y emite el PDF:

```sh
curl -sSL -o vendor/mermaid.min.js https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js
python3 build.py
```

Salidas: `diagramas/*.svg`, `actividad03.html` (el deck, que usa `Logo.png`) y el PDF.

> Los diagramas usan `htmlLabels:false`: con etiquetas HTML (`foreignObject`) Mermaid mide el texto
> antes de que cargue IBM Plex y recorta los rótulos.
