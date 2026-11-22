---
name: dla-material
description: >
  Local companion skill for the `DeepLearningAvanzado/` directory (INF3813 · Advanced Topics in AI ·
  MIA 2026-2, PUC Chile). Mapa del material del curso en este repo y recetas para abrirlo: qué archivo
  corresponde a cada clase, cómo leer las presentaciones HTML autocontenidas de la Clase 1 (cuyo
  contenido lo genera JavaScript y no se extrae con un strip de tags), cómo leer el PDF de la Clase 4
  que no tiene capa de texto (hay que rasterizar las páginas), cómo extraer texto de los PDFs de las
  Clases 2 y 3 con pymupdf, cómo volcar el código de los notebooks sin los outputs embebidos, las
  trampas de nombres del repo (el PDF de interpretabilidad se llama `clase-2.pdf`; la portada de la
  Clase 3 dice «Clase 2»), y el flujo del Laboratorio 1 (Colab con GPU T4, celdas `#@param`,
  entrega del .ipynb ejecutado en UC Canvas). Use when working inside
  `~/Maestria-IA/DeepLearningAvanzado`: para localizar material de una clase, abrir o convertir las
  slides y notebooks, preparar o revisar el Laboratorio 1 o el proyecto final, o cuando el usuario
  pregunte «dónde está la clase N», «ábreme las slides», «extrae el texto de esa presentación»,
  «qué dice el PDF de la clase 4», «cómo entrego el laboratorio». Para el contenido conceptual del
  curso (Transformers, transferencia, autosupervisión, interpretabilidad) usa la skill
  `deep-learning-avanzado`. Also trigger on Presentaciones, Laboratorios, clase 1, clase 2, clase 3,
  clase 4, Laboratorio1.ipynb, binding-colab, práctico, slides, diapositivas, Colab, Canvas, INF3813.
  Respond in Spanish when the user writes in Spanish.
---

# Material local · Deep Learning Avanzado (INF3813)

Skill de **este directorio** (`~/Maestria-IA/DeepLearningAvanzado`). Dice **dónde está cada cosa y cómo
abrirla**. Para la **materia** del curso, carga `deep-learning-avanzado` (skill del repo, cubre las
cuatro clases con sus ecuaciones y cifras).

## Mapa del directorio

```
DeepLearningAvanzado/
├── Presentaciones/
│   ├── Clase 1 - Intro + Transformers/
│   │   ├── clase-1-parte-1.html          Advanced models overview      (HTML, ~1.1 MB)
│   │   └── clase-1-parte-2.html          Introducción a Transformers   (HTML, ~650 KB)
│   ├── Clase 2 - Transferencia de Conocimiento y Generalización/
│   │   ├── Clase 2 - ….pdf               62 pp · CON capa de texto
│   │   └── Practico - Transferencia de Conocimiento.ipynb
│   ├── Clase 3 - Modelos Autosupervisados/
│   │   ├── Clase 3 - Modelos Autosupervisados.pdf   61 pp · CON capa de texto
│   │   └── Práctico_Aprendizaje_Autosupervisado.ipynb
│   └── Clase 4 - Interpretabilidad en Transformers/
│       ├── clase-2.pdf                   49 pp · SIN capa de texto (imágenes)
│       └── binding-colab.ipynb
└── Laboratorios/
    └── Laboratorio1.ipynb                Evaluado · entrega 24/11/2026
```

| Clase | Fecha | Docente | Tema | Archivo |
|---|---|---|---|---|
| 1 | 20/10/2026 | Felipe Urrutia | Panorama + Introducción a Transformers | 2 HTML |
| 2 | 27/10/2026 | Felipe del Río | Transferencia de conocimiento | PDF + notebook |
| 3 | 03/11/2026 | Felipe del Río | Modelos autosupervisados (GPT, MAE, CLIP) | PDF + notebook |
| 4 | 10/11/2026 | Felipe Urrutia | Interpretabilidad en Transformers | PDF + notebook |
| Lab 1 | 17/11/2026 | Felipe Urrutia | La tarea del puntero | `Laboratorios/Laboratorio1.ipynb` |

**Aún no hay material** de las clases de GNNs (24/11), integración (01/12), RL (08/12) ni del proyecto
final. Si falta algo, dilo en vez de inventarlo.

## Trampas de este repo (léelas antes de buscar nada)

1. **El PDF de la Clase 4 se llama `clase-2.pdf`.** Es un nombre heredado: el contenido es
   *Interpretabilidad en Transformers*, 10/11/2026, 49 diapositivas. No lo confundas con la Clase 2.
2. **La portada del PDF de la Clase 3 dice «Clase 2: Modelos Autosupervisados».** La agenda y el
   contenido son los de la Clase 3. Es un error de la diapositiva de título.
3. **El PDF de la Clase 4 no tiene capa de texto.** `page.get_text()` devuelve ~0 caracteres en las 49
   páginas. Hay que **rasterizar y leer las imágenes** (receta abajo).
4. **Las presentaciones de la Clase 1 son HTML, no slides estáticas.** Todo el contenido se **genera con
   JavaScript** al cargar la página: si les quitas las etiquetas con una regex, te quedan ~130
   caracteres. El contenido real está **dentro de los `<script>`** (receta abajo).
5. **Los notebooks tienen imágenes base64 embebidas** en las celdas markdown (`binding-colab.ipynb` y
   `Laboratorio1.ipynb` superan los 390 KB de puro `source`). Filtra los `data:image/...` antes de leer.

## Recetas

Todas asumen `cwd = ~/Maestria-IA/DeepLearningAvanzado` y `pymupdf` instalado (lo trae la skill global
`pdf-reader`). **Escribe los archivos intermedios en el scratchpad de la sesión, no en el repo.**

### PDFs con texto (Clases 2 y 3)
```python
import pymupdf
d = pymupdf.open('Presentaciones/Clase 2 - .../Clase 2 - ….pdf')
for i, pg in enumerate(d):
    print(f'\n===== PAG {i+1} =====\n' + pg.get_text())
```
> Usa `import pymupdf`, no `import fitz` (deprecado, emite warning).

### PDF sin texto (Clase 4): rasterizar en hojas 2×2
Leer 49 páginas sueltas con la herramienta de lectura de imágenes es caro. Compón **4 diapositivas por
hoja** → 13 imágenes, perfectamente legibles a 96 dpi:
```python
import pymupdf, os
OUT = '<scratchpad>/c4g'; os.makedirs(OUT, exist_ok=True)
src = pymupdf.open('Presentaciones/Clase 4 - Interpretabilidad en Transformers/clase-2.pdf')
W, H = src[0].rect.width, src[0].rect.height      # 1152 × 648
for k, g in enumerate(range(0, src.page_count, 4), start=1):
    doc = pymupdf.open()
    pg = doc.new_page(width=W*2+10, height=H*2+10)
    for idx, pn in enumerate(range(g, min(g+4, src.page_count))):
        x, y = (idx % 2)*(W+10), (idx // 2)*(H+10)
        pg.show_pdf_page(pymupdf.Rect(x, y, x+W, y+H), src, pn)
    pg.get_pixmap(dpi=96).save(f'{OUT}/g{k:02d}.png')
```
Luego lee cada `gNN.png` con la herramienta de lectura de imágenes.

### Presentaciones HTML de la Clase 1
El contenido vive en los `<script>`. Vuelca los scripts quitando los blobs base64:
```python
import re
s = open('Presentaciones/Clase 1 - Intro + Transformers/clase-1-parte-1.html',
         encoding='utf-8', errors='replace').read()
for i, sc in enumerate(re.findall(r'<script[^>]*>([\s\S]*?)</script>', s, flags=re.I)):
    sc = re.sub(r'data:[^"\')]{200,}', '[DATA]', sc)      # imágenes inline
    print(f'\n===== SCRIPT {i} ({len(sc)}) =====\n{sc}')
```
**Dónde está qué:**
- **Parte 1** — el **último script** (índice 9) tiene todo el contenido: `weeks` (calendario), `topics`
  (los 8 módulos), `examples` (los 5 casos de estudio), `people` (equipo docente), `ceniaLines`,
  `ceniaInitiatives`, `ceniaPapers` y las llamadas `add(...)` que construyen cada diapositiva. Los
  scripts 2–8 son las **demos interactivas** (portada, nextToken, LoRA, SSL, interpretabilidad, GNN, RL)
  y sus comentarios de cabecera explican qué modelo entrenan.
- **Parte 2** — `buildSlides()` y `references` están en el **script 8**; el motor de diapositivas en el
  **9**; el recorrido numérico del Transformer (todas las vistas: `tokens`, `embed`, `qkv`, `rope`,
  `scores`, `mask`, `weights`, `mix`, `multi`, `residual`, `mlp`, `stack`, `logits`, `probs`,
  `generate`, `train`) en el **script 4**; el preámbulo de ética (`ETH`) en el **5**.

Para **ver** las presentaciones basta abrirlas en el navegador (`open <archivo>.html`): son
autocontenidas, tienen modo presentación y navegación con flechas.

### Notebooks sin outputs
```python
import json
nb = json.load(open(path, encoding='utf-8'))
for i, c in enumerate(nb['cells']):
    src = ''.join(c.get('source', []))
    print(f'\n--- [{i}] {c["cell_type"]} ---\n' + re.sub(r'data:image/[^"\')]+', '[IMG]', src))
```
Para un **índice rápido**, imprime solo las celdas markdown y las primeras líneas de cada celda de
código.

## Flujo del Laboratorio 1

- **Sesión:** martes **17/11/2026**, 18:50–20:00 (ahí se hacen las dudas).
- **Entrega:** martes **24/11/2026, 23:59**, en **UC Canvas**.
- **Individual.** Se entrega el **`.ipynb` con todas las celdas ejecutadas**.
- **21 actividades, 100 puntos**, en 2 partes y 7 pasos.
- Se corre en **Colab con GPU T4**. La primera celda (`🎨 Estilo CENIA`) **debe ejecutarse antes que
  cualquier otra**: descarga la tipografía Quicksand y la paleta, y define funciones de mensajes.
- Las respuestas van en variables `#@param` (`R1`, `R2`, …, `E1`, `E2`, …), no en celdas de texto
  libre. **El output de una celda de código no cuenta como respuesta.**
- Hay celdas `# TODO: Complete el código a continuación` (actividades 5, 9, 14 y el patching).
- Antes de entregar: completar el **nombre** en las Instrucciones Generales y verificar que **todas** las
  celdas corrieron en orden.

> **Integridad académica:** el laboratorio es individual. Úsame para explicar conceptos, depurar errores
> de ejecución y revisar razonamiento — no para escribir las respuestas de las actividades.

## Dónde más mirar

- **`deep-learning-avanzado`** (repo) — la materia del curso, clase por clase, con las ecuaciones y las
  cifras medidas en las diapositivas.
- **`deep-learning`** (repo) — INF3812, el curso base (MLP, CNN, entrenamiento, RNN, Transformers
  introductorios). Útil cuando algo de INF3813 lo da por sabido.
- **`pdf-reader`** (repo) — extracción de texto de PDFs.
- **`maestria-ia`** (repo) — índice de todos los cursos del magíster.
- Repo del magíster: `~/Maestria-IA`. Utilidad `md_to_pdf.py` en la raíz para generar PDFs desde
  Markdown.
