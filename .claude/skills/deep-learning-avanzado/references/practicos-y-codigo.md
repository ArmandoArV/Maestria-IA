# Prácticos, laboratorios y código (PyTorch + Colab)

Todo el curso trabaja en **PyTorch sobre Google Colab** (GPU T4 recomendada). Tres prácticos de clase y
un laboratorio evaluado.

---

## Práctico clase 2 · Transferencia: Feature Extraction y Fine-tuning

`Practico - Transferencia de Conocimiento.ipynb` — Prof. Felipe del Río · Ayudante Andreina Cota.

**Objetivo:** aprovechar un modelo preentrenado en ImageNet para clasificar **especies de flores** con
pocos datos etiquetados. Tres modelos con la **misma arquitectura (ResNet18)**:
1. **Preparación** — dataset *flowers*, exploración, hiperparámetros, `DataLoader`s, transformaciones.
2. **Modelo base** — ResNet18 **desde cero** (punto de comparación).
3. **Feature Extraction** — ResNet18 preentrenada como extractor **fijo**: pesos congelados, solo se
   entrena la última capa.
4. **Fine-tuning** — mismos pesos preentrenados, **ajustando toda la red**.
5. **Resultados** — comparación de accuracy y loss en train/val/test.
6. **¿Por qué funcionan las características?** — espacio de embeddings (aleatoria vs. preentrenada) y
   **búsqueda semántica**.

### Setup
```python
root_dir = 'data/flowers'            # ImageFolder con all/ train/ val/ test/
batch_size    = 128
learning_rate = 5e-4                 # ≈ 1/10 de la lr desde cero para ResNet
n_epochs      = 5
criterion = nn.CrossEntropyLoss()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# seed fija para reproducibilidad
random.seed(1666); np.random.seed(1666)
torch.manual_seed(1666); torch.cuda.manual_seed(1666)

# Pixel medio y std de ImageNet
mean_pixel = [0.485, 0.456, 0.406]
std_pixel  = [0.229, 0.224, 0.225]
transforms.Compose([transforms.Resize([224, 224]),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=mean_pixel, std=std_pixel)])
```
`shuffle=True` **solo** en el loader de train.

### La función que decide todo
```python
def get_model(n_classes, pretrained=None, frozen=False):
    model = models.resnet18(pretrained=pretrained)
    if frozen:
        for param in model.parameters():
            param.requires_grad = False
    model.fc = nn.Linear(in_features=512, out_features=n_classes, bias=True)
    model.to(device)
    return model
```
- **Base:** `get_model(n_classes)`
- **Feature extraction:** `get_model(n_classes, pretrained=True, frozen=True)`
- **Fine-tuning:** `get_model(n_classes, pretrained=True, frozen=False)`

Optimizador `Adam(model.parameters(), lr=learning_rate)` en los tres casos. Funciones de apoyo del
notebook: `run_epoch(phase, …)` (limpia gradientes, hace `backward()` y `step()` **solo en train**),
`run_training`, `run_testing`, `graph_training_metrics`, `print_report`, `show_prediction`.

### Por qué funcionan las características
El **embedding** de ResNet18 es la salida del *average pooling*, justo antes de `fc`: **512
dimensiones**. Para extraerlo se reemplaza el cabezal por la identidad:
```python
extractor = get_model(n_classes=n_classes, pretrained=pretrained)
extractor.fc = nn.Identity()
extractor.eval()
```
Se comparan **dos redes que nunca vieron flores**: ResNet18 con **pesos aleatorios** vs. ResNet18
**preentrenada en ImageNet**.
- **t-SNE** (`n_components=2, perplexity=30, init='pca'`) sobre 10 especies al azar, solo para colorear.
- **k-NN** `KNeighborsClassifier(n_neighbors=5, metric='cosine')` ajustado en train y evaluado en test:
  **sin parámetros que entrenar, el resultado depende solo de la calidad de los embeddings.**

> **Insight del práctico:** con pesos aleatorios las especies aparecen mezcladas; con la red
> preentrenada forman **grupos bien definidos**, aunque la red nunca vio estas clases. El
> preentrenamiento masivo y diverso le enseñó **características generales** (colores, texturas, formas,
> partes). Eso explica el buen rendimiento de Feature Extraction.

### Búsqueda semántica
```python
def semantic_search(query_emb, database_emb, k=5):
    # al normalizar, el producto punto equivale a la similitud coseno
    query    = F.normalize(query_emb.unsqueeze(0), dim=1)
    database = F.normalize(database_emb, dim=1)
    similarities = (query @ database.T).squeeze(0)
    return torch.topk(similarities, k=k)
```
Es lo que hacen a gran escala las **bases de datos vectoriales**, que además usan **ANN** para escalar a
millones de vectores.

> Con pesos aleatorios los valores de similitud **son altos y muy parecidos entre sí**: esos vectores
> no distinguen bien entre imágenes. Para buscar **con texto** hace falta un modelo que ponga texto e
> imágenes en el mismo espacio: **CLIP** (siguiente práctico).

---

## Práctico clase 3 · Entrenamiento autosupervisado: CLIP

`Práctico_Aprendizaje_Autosupervisado.ipynb` — basado en el notebook oficial de OpenAI.

### Setup
```bash
pip install ftfy regex tqdm
pip install git+https://github.com/openai/CLIP.git
```
```python
import clip
clip.available_models()
model, preprocess = clip.load("ViT-B/32")
model.to(device).eval()
model.visual.input_resolution, model.context_length, model.vocab_size
```
**Lectura de los nombres de modelo:** `RN` = backbone ResNet para el encoder visual (`RN50` = ResNet50);
el sufijo `xN` (p. ej. `x4`) significa escalado para **N veces más cómputo**. `ViT` = Vision
Transformer; `-B`/`-L` = Base/Large; `/32` = **parches de 32×32**. El práctico usa **`ViT-B/32`**, basado
íntegramente en Transformers.

### Clasificación zero-shot
```python
query_template = 'A photo of {}, a type of food.'       # Food101
queries = [query_template.format(l.replace('_', ' ')) for l in food_dataset.classes]
tokenized_queries = clip.tokenize(queries).to(device)

with torch.no_grad():
    image_features = model.encode_image(image_input).float()
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features  = model.encode_text(tokenized_queries).float()
    text_features  /= text_features.norm(dim=-1, keepdim=True)

text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)
top_probs, top_labels = text_probs.cpu().topk(5, dim=-1)
```

**Datasets evaluados:** **Food101** (101 comidas, 101.000 imágenes; template *«A photo of {}, a type of
food.»*) y **Stanford Cars** (template *«A photo of {}»*). Se reportan **top-1** y **top-5** accuracy con
`evaluate_model(...)`. **El modelo no fue entrenado en ninguno de los dos: es zero-shot.**

**Actividades abiertas del práctico:**
- Probar **templates propios** y medir cómo cambia la exactitud (sensibilidad al prompt).
- Subir **imágenes propias** con sus queries y graficar la **matriz de similitud coseno** texto×imagen.
- **Visualización de embeddings:** concatenar `image_features` y `text_features`, aplicar `PCA(3)` y
  graficar en 3D con plotly, coloreando por modalidad.

---

## Material práctico clase 4 · Entity binding en un LLM abierto

`binding-colab.ipynb` — Felipe Urrutia. **Los mismos siete pasos de la clase, pero en un LLM real.**

**Modelo:** `Qwen/Qwen2.5-1.5B-Instruct` (también `-0.5B` y `-3B`). **Atención `eager`** obligatoria:
con otras implementaciones aparecen activaciones inf/NaN y el modelo queda al azar. En GPU el notebook
tarda ~12 minutos; en CPU, más de una hora (usar `RAPIDO = 0.2`).

**La tarea:** cada contexto tiene **NP = 8 pares objeto–color** al azar y una pregunta por uno de ellos
(«The desk is»). Se usan solo objetos y colores que son **un solo token** (con espacio inicial) en el
tokenizador, para que **todos los prompts tengan el mismo largo y las posiciones se alineen** — requisito
del *patching*.

**Resultados medidos en el notebook** (están en bloques `<details>` para abrir después de predecir):

| Paso | Hallazgo |
|---|---|
| **Comportamiento** | **95,0 %** entre los 8 colores del contexto; **79,6 %** top-1 sobre todo el vocabulario. Por posición: 100 % en los pares 1–2, ≈97 % en 3–5, ≈88 % en 6–8 |
| **1 · Observar (logit lens)** | El color correcto **no aparece hasta la capa ≈25**. El logit lens muestra cuándo es **legible** por el unembedding, **no cuándo se calcula** |
| **1 · Observar (atención)** | Objeto de la pregunta: muchas cabezas en todas las profundidades (L1.H4 = 0.90). Mismo objeto en el contexto: **débil y difuso** (máx ≈0.15). Color correcto: **pocas cabezas muy nítidas** — L19.H1 (0.59), L14.H3 (0.49), L22.H7 (0.49): **cabezas de recuperación** |
| **2 · Proponer** | La hipótesis «primero buscar el objeto, después copiar el color» **no se sostiene**: ambas ocurren en la misma franja de capas |
| **2 · Etiquetado** | Cabezas que desde el color miran a **su** objeto: L13.H7 (0.61), L13.H2 (0.51), L3.H10, L7.H10, L18.H0, L6.H0. A **otros** objetos ≤0.07. Están **antes** de las de recuperación — mismo orden que en la inducción |
| **5 · Ablación** | Sin intervención 93,3 %; top-8 cabezas de recuperación → **63,3 %**; 8 al azar → 94,2 %. Importan causalmente, pero **el mecanismo está repartido en más cabezas** |
| **5 · Patching** | Capas 0–17: domina «receptor». Capas **18–21: «léxico» ≈40 %** vs. «posicional» ≈15% → lo que viaja es la **entidad**, no el índice. Desde la capa ≈20 crece «donante» (≈100 % en la última): ahí viaja el **color** |
| **5 · Resultado negativo** | Apagar las 4 cabezas de etiquetado baja solo 3 puntos (90,0 %), **menos que 4 al azar** (86,1 %). **Que miren a su objeto no las hace necesarias: atención ≠ causa.** El etiquetado está repartido o pasa por las MLP |
| **6 · PCA** | **Índice:** gradiente del par 0 al 7 en las capas 14 y 21. **Color:** no organiza las dos primeras componentes en ninguna capa, aunque el probe lo lea con 97 %. **Legible ≠ dominante en varianza** |
| **7 · Probes** | **Entidad: 100 % desde la capa 1** — es una trampa (la última posición lee el objeto, dos tokens antes). **Índice:** 60–77 % entre las capas 8 y 21. **Color:** cerca del azar hasta la 19 y **salta a 83 % en la capa 20** (≈97 % al final), coincidiendo con el patching |

**La analogía inducción ↔ binding:**

| | Inducción (modelo de juguete) | Binding (Qwen) |
|---|---|---|
| paso previo | capa 1: cada posición copia su **token previo** | ¿alguna cabeza copia en «gold» **su objeto** «ring»? |
| búsqueda | la query compara con «previo = C» | la pregunta «ring» compara con «mi objeto = ring» |
| copia | el value es el propio token → «D» | el value es el propio color → «gold» |

**Referencias del notebook:** Feng & Steinhardt (2023), *How do language models bind entities in
context?* · Dai et al. (2024), *Representational analysis of binding in language models* · Wu et al.
(2024), *Retrieval head mechanistically explains long-context factuality*.

---

## Laboratorio 1 · Interpretabilidad en Transformers: la tarea del puntero

`Laboratorios/Laboratorio1.ipynb` — Felipe Urrutia. **Sesión: martes 17/11/2026, 18:50–20:00.
Entrega: martes 24/11/2026, 23:59, en UC Canvas.**

### Reglas de entrega
- **Individual.**
- Formato: el **`.ipynb` con todas las celdas ejecutadas**, subido a **UC Canvas**.
- Todas las preguntas se responden **en las celdas de respuesta indicadas** (`R1`, `R2`, … como
  `#@param`). **No se acepta el output de una celda de código como respuesta.**
- Completar el **nombre** en las Instrucciones Generales.
- **2 partes, 7 pasos, 21 actividades, 100 puntos.** GPU T4 recomendada.
- Las dudas se hacen **durante la sesión del 17 de noviembre**.

### Objetivos de aprendizaje
1. *Explicar* qué es la interpretabilidad, para qué sirve y qué ingredientes necesita un análisis.
2. *Explicar* la tarea del puntero y contrastarla con la **inducción** vista en clases.
3. *Aplicar* el protocolo de **siete pasos** para descubrir el mecanismo de un Transformer de solo
   atención.
4. *Distinguir* tipos de evidencia (observación, plausibilidad, consistencia, causal, correlacional) y
   *justificar* qué herramienta responde cada pregunta **y qué no puede responder**.
5. *Diseñar* intervenciones **con controles** y *criticar* conclusiones: **qué resultado refutaría una
   hipótesis**.

**Conceptos de la clase que se ponen en práctica:** inducción, circuitos de atención, RoPE, residual
stream, activation patching, probes lineales.

### La tarea del puntero
- **Tokens:** letras simples `a`…`h` (8) y **marcadores** `a1`…`h9` (72), cada marcador **un solo token**.
- **Secuencias:** 12 tokens de contexto con **4 marcadores** (de letras distintas) en posiciones al azar,
  y al final una letra simple: **la consulta**.
- **Regla:** (1) buscar el marcador con la letra de la consulta (`c` → `c3`); (2) desde ese marcador,
  **retroceder tantos tokens como dice su dígito** (3); (3) responder la letra que está ahí.
- **Reglas de referencia:** el azar acierta 1 de 8; la **inducción** de la clase respondería lo que
  siguió a la última aparición simple de la letra consultada.

### El modelo del laboratorio
El mismo Transformer de la clase: **solo atención, una cabeza por capa, sin MLP ni LayerNorm, con
RoPE**. La pérdida se mide **solo en la última posición**. `modelo.run(x)` devuelve logits y un **caché**:

| clave | qué es | forma |
|---|---|---|
| `resid0` | embedding | `[n, T, 64]` |
| `atn1`, `atn2` | patrón de atención de capa 1 y 2 (fila = desde, columna = hacia) | `[n, T, T]` |
| `sal1`, `sal2` | lo que escribe cada capa en el residual | `[n, T, 64]` |
| `resid1`, `resid2` | residual tras capa 1 y 2 | `[n, T, 64]` |

Con `ganchos={clave: f}` se reemplaza esa activación por `f(activación)`: así se **interviene** (paso 5).

Se entrenan **dos modelos: 2 capas y 1 capa**. (Pregunta: ¿alcanza 1 capa?)

### Estructura por actividades
| Parte | Paso | Actividades |
|---|---|---|
| Introducción | ¿qué es la interpretabilidad? | 1 (selección múltiple, 3 pts), 2 (pregunta, 5 pts) |
| **I** | La tarea | 3 (4 pts) |
| **I** | El modelo y su entrenamiento | 4 (5 pts) |
| **I** | **1 · Observar** — patrones de atención | 5 (`TODO`: atención media, 6 pts), 6 (3 pts), 7 (5 pts) |
| **II** | **2 · Proponer** | 8 (pregunta) |
| **II** | **3 · Demostrar a mano** | 9 (`TODO`: construcción a mano con RoPE), 10 (5 pts), 11 (3 pts, barrido de θ) |
| **II** | **4 · Caracterizar** — atención por dígito y por posición; **planos de RoPE** | 12 (4 pts), 13 (5 pts) |
| **II** | **5 · Intervenir** — activation patching | 14 (`TODO`, 6 pts), 15 (6 pts), 16 (5 pts) |
| **II** | **6 · Descomponer** — PCA sin etiquetas | 17 (4 pts) |
| **II** | **7 · Confirmar** — probes lineales | 18 (4 pts) |
| **Desafío** | marcadores en posiciones **fijas** (8–11) vs. al azar | 19 (4 pts) |
| Cierre | — | 20, 21 |

**Claves conceptuales que el laboratorio refuerza:**
- La puntuación de la capa 1 depende de `k = i − j − d_i` (cuántos pasos se aleja la key j del destino
  correcto) y vale `β₁cos(kθ)`, **máxima en k = 0**. Falla si θ es muy chico (`cos θ` casi no se
  distingue de `cos 0`) o si `cos(kθ) = 1` con algún `k ≠ 0`.
- **Planos de RoPE:** 16 planos con `θ_p` de 57° a <1° por posición. En un plano **rápido** el coseno
  cambia mucho entre distancias → sirve para **elegir una distancia**; en uno **lento** depende casi solo
  del **contenido**. (Mismo análisis de las diapositivas «Frecuencias» y «Distribución».)
- **El desafío:** con marcadores en posiciones fijas, ¿alcanza la misma exactitud? ¿**usa el mismo
  mecanismo**? Es el caso de «dos modelos con la misma exactitud resuelven la tarea de formas distintas,
  y una puede romperse fuera de la distribución».

**Para seguir (sugerencias del propio laboratorio):** entrenar SAEs TopK sobre `sal1` en los marcadores ·
qué pasa si dos marcadores comparten letra · encadenar dos punteros (¿cuántas capas hacen falta?).

**Referencias del laboratorio:** Elhage et al. (2021) · Olsson et al. (2022), arXiv:2209.11895 ·
Su et al. (2021), arXiv:2104.09864 · Heimersheim & Nanda (2024), arXiv:2404.15255 · Alain & Bengio
(2016), arXiv:1610.01644.

---

## Convenciones de código del curso

- **PyTorch**, no Keras ni TensorFlow. **Colab** como entorno; `device = cuda if available else cpu`.
- **Semillas fijas** en los prácticos (`1666` en el de transferencia) para reproducibilidad.
- `torchvision.models` para visión; `transformers` de Hugging Face para LLMs; `clip` de OpenAI para
  multimodal.
- `scikit-learn` para t-SNE, PCA, k-NN y `LogisticRegression` (los probes).
- Los notebooks de Colab usan `#@param` para los controles de formulario y celdas `#@title … {
  display-mode: "form" }` para plegar el código de apoyo.
- El estilo visual de los gráficos es el de **CENIA** (colores y tipografía Quicksand); el Laboratorio 1
  lo aplica en una celda que **debe ejecutarse primero**.
