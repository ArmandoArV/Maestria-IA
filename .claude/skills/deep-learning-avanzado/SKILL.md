---
name: deep-learning-avanzado
description: >
  Expert knowledge base for the INF3813 Deep Learning Avanzado course ("Advanced Topics in AI",
  Magíster en IA, PUC Chile, MIA 2026-2), dictado por el equipo de CENIA: Felipe Urrutia, Felipe del
  Río, Nicolás Alvarado y Rex Liu. Cubre el curso completo: panorama de modelos avanzados y casos de
  estudio (DeepSeek-R1, Gemini Robotics, AlphaFold 3, circuit tracing en Claude, AlphaEvolve);
  introducción a Transformers paso a paso en un decoder-only moderno tipo Llama (tokens, tabla de
  embeddings, proyecciones Q/K/V, RoPE, scores escalados, máscara causal, softmax por fila, mezcla de
  values, multi-head y W_O, conexiones residuales, RMSNorm, MLP con compuerta SwiGLU, apilar bloques,
  unembedding, logits, temperatura, generación autorregresiva y caché KV, entrenamiento con
  next-token prediction); las tres familias de Transformers (decoder-only/GPT, encoder-only/BERT,
  encoder-decoder/T5 con cross-attention); historia de la atención (Hopfield 1982, fast weights,
  seq2seq 2014, Bahdanau, Luong, atención descomponible, self-attention estructurada, Vaswani 2017) y
  de los embeddings posicionales (absolutos aprendidos, sinusoidales, relativos de Shaw y
  Transformer-XL, sesgos de T5 y ALiBi, RoPE y fase relativa); arquitecturas y eficiencia (coste
  cuadrático, sliding window, local+global/Longformer, DeepSeek Sparse Attention, atención lineal,
  gated DeltaNet, Strassen attention, FlashAttention, MHA/GQA/MQA, MLA, caché KV, Mixture of
  Experts); transferencia de conocimiento (tarea y dataset de origen/destino, adaptación de tarea,
  dominio, clases y modalidad, pre-entrenamiento, feature extraction, vectores de características,
  búsqueda semántica, bases de datos vectoriales, fine-tuning, catastrophic forgetting, PEFT y LoRA,
  foundation models); aprendizaje autosupervisado (tareas de pretexto, objetivos generativos,
  contrastivos y adversariales; GPT y modelamiento de lenguaje autorregresivo, scaling laws,
  few-shot, prompting zero-shot/few-shot/chain-of-thought; ViT, autoencoders y Masked Autoencoders
  (MAE); SimCLR, MoCo, BYOL, DINO/DINOv2; CLIP, dataset WIT, objetivo contrastivo y clasificación
  zero-shot; BLIP y Flamingo); e interpretabilidad mecanicista en Transformers (protocolo de siete
  pasos observar → proponer → demostrar a mano → caracterizar → intervenir → descomponer → confirmar,
  cabezas de inducción, circuitos y composición de cabezas, flujo residual, logit lens, patrones de
  atención, puntajes pos/sym, frecuencias de RoPE, activation patching y ablación, PCA, autoencoders
  dispersos TopK y códigos, probes lineales, entity binding en LLMs abiertos). Incluye los prácticos
  en PyTorch y Colab (ResNet18 sobre flowers, CLIP ViT-B/32 sobre Food101 y Stanford Cars, binding en
  Qwen2.5) y el Laboratorio 1 de interpretabilidad. Use for any INF3813 question — clases,
  laboratorios, proyecto final, slides, calendario. Also trigger on deep learning avanzado, advanced
  topics in AI, MIA 2026-2, CENIA, Transformer, atención, self-attention, query key value, multi-head,
  máscara causal, RoPE, rotary, embedding posicional, ALiBi, RMSNorm, SwiGLU, caché KV, GQA, MQA, MLA,
  FlashAttention, sliding window, atención dispersa, atención lineal, MoE, decoder-only, encoder-only,
  BERT, T5, GPT, transfer learning, transferencia de conocimiento, feature extraction, fine-tuning,
  PEFT, LoRA, catastrophic forgetting, olvido catastrófico, foundation models, modelos fundacionales,
  búsqueda semántica, base de datos vectorial, embeddings, aprendizaje autosupervisado,
  self-supervised, tarea de pretexto, MAE, masked autoencoder, ViT, vision transformer, autoencoder,
  SimCLR, MoCo, BYOL, DINO, CLIP, multimodal, zero-shot, prompting, chain-of-thought, scaling laws,
  interpretabilidad, interpretability, interpretabilidad mecanicista, cabeza de inducción, induction
  head, circuito, flujo residual, residual stream, logit lens, activation patching, ablación, probe
  lineal, PCA, SAE, autoencoder disperso, superposición, monosemántica, entity binding, Qwen,
  laboratorio 1, proyecto final, GNN, reinforcement learning, or the course code (INF3813).
  Respond in Spanish when the user writes in Spanish.
---

# Deep Learning Avanzado · Advanced Topics in AI (INF3813)

Knowledge base para **INF3813 – Deep Learning Avanzado**, Magíster en Inteligencia Artificial, PUC
Chile, **MIA 2026-2**. El curso lo dicta un equipo del **CENIA** (Centro Nacional de Inteligencia
Artificial) y es la continuación del curso base de Deep Learning (INF3812, skill `deep-learning`).

> El curso recorre **arquitecturas, métodos de aprendizaje y herramientas de análisis**, y los conecta
> entre sí: *"una arquitectura, un objetivo de aprendizaje, un método de adaptación y una pregunta de
> interpretabilidad pueden formar parte del mismo sistema."*

## Cómo usar esta skill

1. **Lee el archivo de `references/` que corresponda** antes de responder más allá del resumen de abajo.
   SKILL.md es el mapa; las referencias tienen las ecuaciones, las cifras medidas en clase y el detalle
   por diapositiva.
2. **Responde en español.** El curso se dicta en español (aunque el título del módulo esté en inglés).
3. **Distingue siempre el tipo de evidencia.** Es el hilo conductor del módulo de interpretabilidad y
   una buena costumbre para todo el curso: *observación* ≠ *plausibilidad* ≠ *consistencia* ≠
   *evidencia causal* ≠ *evidencia correlacional*. Los pesos de atención **no son** por sí solos una
   explicación causal.
4. **Separa las dimensiones de diseño.** Al comparar modelos, nunca mezcles: conectividad (qué pares se
   calculan) ≠ memoria y ejecución (caché KV, GQA/MLA, FlashAttention) ≠ forma de interacción (atención
   lineal, Strassen) ≠ posición (tabla, sinusoidal, sesgo, RoPE) ≠ capacidad (MoE). Y **exactitud y
   eficiencia se miden por separado**.
5. **Usa PyTorch y Colab**, con `torchvision.models` y Hugging Face `transformers`. Es lo que usan los
   prácticos. Ver `references/practicos-y-codigo.md`.
6. **Precaución sobre la referencia "moderna":** el recorrido paso a paso de la clase 1 usa un
   **decoder-only tipo Llama** (pre-norm, RMSNorm, RoPE, GQA, SwiGLU) y un **modelo de juguete**
   entrenado de verdad (d = 8, 2 capas, 2 cabezas, |V| = 34, MHA en vez de GQA). No es un diseño
   universal: las variantes se comparan en el momento 04.
7. **Integridad académica:** el **Laboratorio 1 es individual**. Usa esta skill para explicar, resolver
   ejemplos análogos y revisar razonamiento, no para entregar las respuestas del laboratorio.

## Equipo docente (CENIA)

| Persona | Rol en el curso | Cargo |
|---|---|---|
| **Felipe Urrutia** | Introducción e interpretabilidad | Ingeniero de Investigación, CENIA · Doctorado en Matemáticas UC |
| **Felipe del Río** | Fundamentos (transferencia, autosupervisado) y RL | Investigador, CENIA |
| **Nicolás Alvarado** | GNNs y técnicas avanzadas | Investigador postdoctoral, CENIA |
| **Rex Liu** | RL y proyecto | Investigador, CENIA |
| **Andreina Cota** | Ayudante corrector | Doctorado en IA UC, CENIA |

Horario del curso: **18:50–20:00 / 20:15–21:20** (dos bloques con descanso).

## Calendario 2026 y mapa de referencias

| Semana | Módulo | Docente | Contenido | Reference |
|---|---|---|---|---|
| **20/10** | 1 · Introduction | F. Urrutia | Panorama de modelos avanzados · Introducción a Transformers | `references/clase1-panorama-y-transformers.md` |
| **27/10** | 2 · Fundamentals | F. del Río | Transferencia de conocimiento · Feature extraction, fine-tuning, PEFT (LoRA) | `references/clase2-transferencia.md` |
| **03/11** | 2 · Fundamentals | F. del Río | Self-supervised learning · GPT, MAE, CLIP | `references/clase3-autosupervisado.md` |
| **10/11** | 3 · Interpretability | F. Urrutia | Interpretabilidad en Transformers · inducción, patching, probes, SAEs | `references/clase4-interpretabilidad.md` |
| **17/11** | 3 y 4 | F. Urrutia / N. Alvarado | **Laboratorio 1** · Introducción a GNNs | `references/practicos-y-codigo.md` |
| **24/11** | 4 · Graph Neural Networks | N. Alvarado | GNNs (continuación) · **Laboratorio 2** | — |
| **01/12** | 5 y 7 | N. Alvarado / Rex y Felipe | *Everything all together all at once* · Trabajo de proyecto | — |
| **08/12** | 6 y 7 | Rex Liu y Felipe | Reinforcement Learning · Trabajo de proyecto | — |
| **15/12** | 7 · Final Project | Rex y Nico | Project Q&A | — |

> **Material disponible en el repo:** clases 1–4 (ver `dla-material`, la skill local del directorio
> `DeepLearningAvanzado/`). Las clases de **GNNs, integración y RL** aún no tienen material; esta skill
> solo registra lo que el programa anuncia de ellas.

## Los ocho módulos y su pregunta guía

De la diapositiva de contenidos de la clase 1. Cada módulo se presenta como **una pregunta**:

| # | Módulo | Pregunta |
|---|---|---|
| 01 | **Transformers** | ¿Cómo describimos un Transformer, en particular un GPT? |
| 02 | **Transfer learning** | ¿Qué parte del modelo conviene adaptar? |
| 03 | **Self-supervision** | ¿De dónde viene la señal de aprendizaje? |
| 04 | **Interpretabilidad** | ¿Qué información está representada y qué componentes importan causalmente? |
| 05 | **GNNs** | ¿Cómo representar un problema con nodos y relaciones? |
| 06 | **Integración** | ¿Cómo combinar las herramientas de los módulos anteriores en un sistema? |
| 07 | **RL** | ¿Cómo elegir acciones para maximizar el retorno esperado? |
| 08 | **Proyecto final** | Integrar lo aprendido. |

## Evaluación

- **Laboratorio 1** — semana del **17 de noviembre**, Felipe Urrutia. *Interpretabilidad en
  Transformers: la tarea del puntero.* **Individual**; se entrega el `.ipynb` **con todas las celdas
  ejecutadas** en **UC Canvas**, hasta el **martes 24 de noviembre de 2026, 23:59**. 2 partes, 7 pasos,
  **21 actividades, 100 puntos**. El énfasis está en **entender y justificar**: la mayoría son
  preguntas; unas pocas piden completar código (`TODO`). No se acepta el *output* de una celda como
  respuesta. GPU T4 recomendada.
- **Laboratorio 2** — semana del **24 de noviembre**, Nicolás Alvarado (GNNs).
- **Proyecto final** — trabajo las semanas del **1 y 8 de diciembre** (Rex Liu y Felipe); **Q&A** la
  semana del **15 de diciembre** (Rex y Nicolás).

> **El programa no especifica ponderaciones, requisitos ni fecha de entrega del proyecto final.** Si
> alguien pregunta por ellas, dilo en vez de inventar.

## Conceptos núcleo (referencia rápida)

### El decoder-only, en una frase por paso
Tokens → `e_i = E[t_i]` → `Q, K, V = XW_Q, XW_K, XW_V` → RoPE sobre Q y K → `S = Q̃K̃ᵀ/√d_k` →
máscara causal (`−∞` si `j > i`) → `A = softmax(S + M)` → `y_i = Σ_j a_ij v_j` → concat de cabezas
× `W_O` → `R = X + Attn(Norm(X))` → `X' = R + MLP(Norm(R))` → ×L → `z = Norm(x^L)W_U` →
`p = softmax(z/T)` → muestrear o argmax → repetir.

**Las dos mitades del bloque:** la **atención mezcla posiciones**; la **MLP transforma cada posición
por separado**, con pesos compartidos. El **residual** es el canal común por el que ambas leen y al que
ambas suman.

### Tabla de decisiones de diseño (el mapa mental del módulo 04)
| Dimensión | Qué cambia | Ejemplos |
|---|---|---|
| **Conectividad** | Qué pares (i, j) se calculan | Densa · sliding window (Mistral) · local+global (Longformer) · DSA (DeepSeek) |
| **Memoria y ejecución** | Qué se guarda y cómo se computa | Caché KV · MHA/GQA/MQA · MLA · FlashAttention |
| **Forma de interacción** | Cómo se agrega la información | Softmax densa · atención lineal · gated DeltaNet · Strassen attention |
| **Posición** | Cómo entra el orden | Tabla absoluta · sinusoidal · sesgos (T5, ALiBi) · RoPE |
| **Capacidad** | Cuánto cómputo se activa | Mixture of Experts |

**Dos ejes que no hay que confundir en los embeddings posicionales:** *aprendida/fija* (cómo se obtiene
la señal) ≠ *absoluta/relativa* (qué posición expresa).

### Transferencia: las dos estrategias
| | Feature Extraction | Fine-tuning |
|---|---|---|
| Qué se entrena | solo el cabezal; la red base **congelada** | **todos** los pesos (con lr baja) |
| Dominio | similar al de origen | permite adaptación al dominio |
| Especialización | menos | más |
| Flexibilidad | menos | más |
| Costo computacional | bajo | alto |
| Riesgo de sobreajuste | bajo | alto |
| Catastrophic forgetting | **no hay** riesgo | **sí** hay riesgo |

**La única diferencia en código es si congelas o no la red base.** En PyTorch:
`get_model(..., pretrained=True, frozen=True/False)`.

**Por qué funciona:** *feature extraction* reaprovecha la **alineación entre jerarquías de
características**; *fine-tuning* aprovecha que un **mejor punto de partida** lleva a un mejor óptimo
local.

### Autosupervisión: de dónde sale la señal
**Tarea de pretexto**: un objetivo generado automáticamente desde la estructura intrínseca de los
datos. Tres familias y su ejemplo canónico en el curso:

| Familia | Idea | Ejemplo |
|---|---|---|
| **Generativa** | predecir contenido faltante o futuro | GPT (texto), MAE (visión) |
| **Contrastiva** | lo similar cerca, lo distinto lejos | CLIP (multimodal), SimCLR, MoCo |
| **Adversarial** | tira y afloja de dos redes | GANs |

**El cuello de botella no es el modelo, son las etiquetas:** los modelos escalan, el etiquetado humano
no. La autosupervisión convierte aprendizaje no supervisado en supervisado.

### Interpretabilidad: los siete pasos y su tipo de evidencia
| # | Paso | Herramienta | Tipo de evidencia |
|---|---|---|---|
| 1 | **Observar** | patrones de atención, logit lens | observación |
| 2 | **Proponer** | hipótesis por capa | — |
| 3 | **Demostrar a mano** | pesos escritos sin entrenar | plausibilidad |
| 4 | **Caracterizar** | perfil pos/sym, frecuencias de RoPE | consistencia |
| 5 | **Intervenir** | activation patching, ablación | **causal** |
| 6 | **Descomponer** | PCA, SAE (sin etiquetas) | correlacional |
| 7 | **Confirmar** | probes lineales | correlacional |

> *Cada paso aporta un tipo de evidencia distinto, y solo seguimos si el anterior pasa.* Solo el paso 5
> da evidencia causal; los pasos 6 y 7 muestran que algo es **legible**, no que el modelo lo **use**.

### Ética y seguridad (preámbulo de la clase 1)
El sistema no es solo el modelo: **datos → Transformer → contexto (prompt) → texto que se vuelve acción
→ personas afectadas**. Cada etapa tiene un riesgo y una pregunta de garantía.

> **Inyección de instrucciones:** para el Transformer, **instrucciones y datos son los mismos tokens en
> el mismo contexto**. La atención no distingue su origen y la máscara causal **no es una barrera de
> seguridad**. Los permisos, el aislamiento y la validación **deben vivir fuera del modelo**.

Mapa inspirado en «Responsables» y «Productos» (Godoy, Urrutia y Carvajal, *Ética para la Ciencia de
Datos*, 2023). Referencias: NIST GenAI Profile (2024), NIST Adversarial ML (2025).

## CENIA

«Inteligencia artificial al servicio de las personas». Investigación, transferencia tecnológica,
vinculación con el medio y formación. **Cinco líneas de investigación:** aprendizaje profundo para
visión y lenguaje · IA neuro-simbólica · IA inspirada en el cerebro · aprendizaje automático basado en
la física · IA centrada en las personas (justa, segura, transparente; explicabilidad/XAI).

**Personas:** 10 investigadores(as) principales, 22 asociados, 7 postdoctorados, 6 en ingeniería e
investigación aplicada. 4 de los 5 integrantes del equipo docente son parte de CENIA.

**Iniciativas:** **ILIA 2025** (Índice Latinoamericano de IA, con CEPAL; 19 países, 100 subindicadores)
· **LatamGPT** (lanzado feb. 2026; modelo abierto de 70B sobre Llama 3.1 70B, preentrenamiento continuo
con ~297B tokens y SFT; español, portugués e inglés con foco en variantes latinoamericanas) ·
**Hazlo con IA** (cursos gratuitos para mipymes y sector público) · **GerencIA** (formación ejecutiva) ·
**IA en Corto** (divulgación) · **DashAI** (crear modelos sin programar).

Sitios: `cenia.cl` · `cenia.cl/investigacion` · `plataforma.connect.sciencenia.cl`.

## Bibliografía y referencias citadas en clase

**Arquitectura y posición:** Vaswani et al. (2017) `arxiv.org/abs/1706.03762` · Devlin et al. (BERT,
2018/19) · Raffel et al. (T5, 2019/20) · Llama 2 (2023) y Llama 3 (2024) · Su et al. (RoPE, 2021)
`arxiv.org/abs/2104.09864` · Shaw et al. (2018) · Dai et al. (Transformer-XL, 2019) · Press et al.
(ALiBi, 2021/22).

**Historia de la atención:** Hopfield (1982) · Schmidhuber & Huber (1991), fast weights (1992) ·
Larochelle & Hinton (2010) · Graves (2013), Neural Turing Machines (2014) · Sutskever et al. (2014) ·
Bahdanau et al. (2014/15) · Luong et al. (2015) · Mnih et al. (2014) · Xu et al. (2015) · Sukhbaatar et
al. (2015) · Parikh et al. (2016) · Lin et al. (2017).

**Eficiencia:** Beltagy et al. (Longformer, 2020) · Jiang et al. (Mistral, 2023) · Shazeer (MQA, 2019)
· Ainslie et al. (GQA, 2023) · DeepSeek-V2 (MLA, 2024) · DeepSeek-V3.2 (DSA, 2025) · Native Sparse
Attention (2025) · Katharopoulos et al. (atención lineal, 2020) · Yang et al. (DeltaNet, 2024/25) ·
Kozachinskiy et al. (Strassen attention, 2025) `arxiv.org/abs/2501.19215` · Dao et al.
(FlashAttention, 2022) · Fedus et al. (MoE, 2021/22) · Liu et al. (*lost in the middle*, 2023/24).

**Interpretabilidad:** Elhage et al. (2021), *A Mathematical Framework for Transformer Circuits*,
`transformer-circuits.pub` · Olsson et al. (2022), *In-context Learning and Induction Heads*,
`arxiv.org/abs/2209.11895` · Bricken et al. (2023) · Cunningham et al. (2023) · Gao et al. (2024) ·
Alain & Bengio (2016) · Belinkov (2022) · Meng et al. (2022) · Zhang & Nanda (2023) · Heimersheim &
Nanda (2024) `arxiv.org/abs/2404.15255` · Geiger et al. (2021) · Feng & Steinhardt (2023) · Urrutia et
al. (ICLR 2026, NeurIPS 2026) · Anthropic, *Tracing thoughts in a language model* (2025).

**Casos de estudio de la clase 1:** DeepSeek-AI, R1 (2025) · Google DeepMind, Gemini Robotics 1.5
(2025) · Abramson et al., AlphaFold 3, *Nature* (2024) · AlphaEvolve (2025–2026).

**Skills relacionadas:** `deep-learning` (INF3812, el curso base: MLP, CNN, entrenamiento, RNN,
Transformers introductorios) · `maestria-ia` (índice de todos los cursos) · `pdf-reader` ·
`dla-material` (skill local del directorio `DeepLearningAvanzado/`: dónde está cada archivo y cómo
leerlo).
