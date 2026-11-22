# Clase 1 (20/10/2026) · Panorama de modelos avanzados + Introducción a Transformers

Docente: **Felipe Urrutia**. Dos partes, con descanso entre medio. El material son **dos presentaciones
HTML autocontenidas con demos interactivas** (no PDFs): `clase-1-parte-1.html` y `clase-1-parte-2.html`.

---

# Parte 1 · Advanced models overview

Tres bloques: **(1) Bienvenida y el curso**, **(2) Contenidos**, **(3) Casos de ejemplo**.

## Bloque 1 · El curso
Equipo docente, CENIA, calendario y evaluación: ver la tabla correspondiente en `SKILL.md`.

## Bloque 2 · Los contenidos (ocho módulos)

Cada módulo se presenta con una figura o demo y **una pregunta**.

| # | Módulo | Subtítulo | Contenido | Pregunta |
|---|---|---|---|---|
| 01 | Transformers | Arquitectura y flujo de información | Atención, MLPs y conexiones residuales. Distinción encoder/decoder y relación entre arquitectura y tarea. | ¿Cómo describimos un Transformer, en particular un GPT? |
| 02 | Transfer learning | Reutilizar conocimiento | Fundamentos y tipos de transferencia; extracción de características, fine-tuning y adaptación eficiente con PEFT, como LoRA. | ¿Qué parte del modelo conviene adaptar? |
| 03 | Self-supervision | Aprender de los propios datos | Familias de objetivos autosupervisados: GPT en texto, MAE en visión, CLIP en multimodal. | ¿De dónde viene la señal de aprendizaje? |
| 04 | Interpretabilidad | De las activaciones a los mecanismos | Patching, ablación, probes y steering; SAEs, superposición y monosemántica; transcoders y crosscoders. | ¿Qué información está representada y qué componentes importan causalmente? |
| 05 | GNNs | Aprender sobre relaciones | Introducción a Graph Neural Networks y Laboratorio 2. | ¿Cómo representar un problema con nodos y relaciones? |
| 06 | Integración | Advanced Techniques | *Everything all together all at once* (Nico), semana del 1 de diciembre. | ¿Cómo combinar las herramientas de los módulos anteriores en un sistema? |
| 07 | RL | Aprender a decidir | MDPs, políticas, valor, Bellman, programación dinámica, SARSA, Q-learning y exploración. Opción de policy gradients o fine-tuning de LLMs como caso de RL. | ¿Cómo elegir acciones para maximizar el retorno esperado? |
| 08 | Proyecto final | Integrar lo aprendido | Trabajo las semanas del 1 y 8 de diciembre; Q&A la del 15. | — |

**Demos interactivas de esta parte** (todas entrenan modelos pequeños **en vivo en el navegador**):
- *Transformers*: generación autorregresiva con un predictor de trigramas (capas y atención ilustrativas).
- *Transfer learning*: red 2 → H → H(W + ΔW, ΔW = BA) → 1, preentrenada en «anillos» y adaptada a
  Círculos / Lunas / XOR / Espiral con tres estrategias: **solo cabeza**, **LoRA de rango r** o
  **fine-tuning completo**. Compara precisión vs. parámetros entrenables. La capa 1 es estrecha y el
  preentrenamiento usa weight decay, así que «solo cabeza» funciona en Círculos pero **no** en Lunas,
  XOR ni Espiral.
- *Self-supervision*: tres señales en pestañas — GPT (el texto genera sus propios pares contexto →
  siguiente token, sin modelo), MAE (autoencoder MLP 272 → 128 → 256 que reconstruye parches ocultos de
  figuras 16×16) y CLIP (dos codificadores pequeños con pérdida contrastiva; dos combinaciones
  forma–color nunca aparecen en entrenamiento, para mostrar recuperación zero-shot).
- *Interpretabilidad*: MLP 768 → 16 (ReLU) → 4 entrenado al cargar la página para reconocer la **forma**
  de figuras de colores 16×16; luego probes lineales sobre las 16 activaciones (forma, tamaño, lado,
  color) e intervenciones: **ablación** (apagar neuronas), **patching** (copiar neuronas desde otra
  imagen) y **steering** (sumar una dirección de concepto).
- *GNNs*: GCN real con `H' = ReLU( media{ h_u : u ∈ N(v) ∪ {v} } · W )`, es decir `Â = D⁻¹(A + I)`,
  entrenada sobre el club de karate de Zachary (1977) con **solo dos nodos etiquetados**. Con k capas
  cada nodo ve hasta k saltos; los nodos lejos de toda etiqueta quedan grises.
- *RL*: Q-learning y SARSA tabulares en un gridworld editable.
  - Q-learning (off-policy): `Q(s,a) ← Q(s,a) + α[r + γ·max_{a'} Q(s',a') − Q(s,a)]`
  - SARSA (on-policy): `Q(s,a) ← Q(s,a) + α[r + γ·Q(s',a') − Q(s,a)]`, con `a'` elegida por la misma
    política ε-greedy.
  - En el acantilado, Q-learning aprende el camino al borde y SARSA uno más seguro (porque explora con
    ε > 0).

## Bloque 3 · Cinco casos de estudio

Cada caso trae **problema · método · módulos del curso · una limitación para discutir · una pregunta**.

### DeepSeek-R1 — Razonamiento y aprendizaje por refuerzo (2025)
- **Problema:** resolver problemas de matemáticas y código con un LM adaptado para razonar.
- **Método:** R1 combina SFT inicial, RL de razonamiento, nuevos datos para SFT y RL final. R1-Zero
  explora RL **sin SFT previo** sobre un modelo base preentrenado.
- **Módulos:** Transformers (base DeepSeek-V3, decoder-only con MoE) · transferencia (SFT de arranque y
  SFT con nuevos datos; luego destilación a modelos más pequeños) · autosupervisión (el base se
  preentrena prediciendo el siguiente token) · RL (**GRPO** con recompensas por reglas: exactitud de la
  respuesta y formato del razonamiento) · interpretabilidad como *contraste*.
- **Límite:** la calidad de la recompensa y la evaluación delimitan qué mejora se está midiendo.
- **Pregunta:** ¿entrenar con RL significa que el modelo aprendió desde cero? **No.** R1-Zero parte de un
  modelo base preentrenado; elimina el SFT preliminar, **no el preentrenamiento**.
- Fuente: `arxiv.org/html/2501.12948v1`.

### Gemini Robotics — De visión y lenguaje a acciones físicas (2025)
- **Problema:** clasificar objetos siguiendo una instrucción y completar una tarea física de varios pasos.
- **Método:** *Robotics-ER 1.5* planifica y usa herramientas; *Robotics 1.5*, un modelo
  **vision-language-action (VLA)**, convierte instrucciones y observaciones en acciones. Ambos
  especializan modelos Gemini mediante **fine-tuning**.
- **Módulos:** multimodal · transferencia · integración (dos modelos en un sistema). Las decisiones
  secuenciales son un **puente conceptual** hacia RL, no RL.
- **Límite:** el éxito en las tareas y robots evaluados no demuestra generalización a cualquier entorno.
- **Pregunta:** ¿comprender una instrucción basta para ejecutarla? **No.** También hace falta percepción
  espacial, control y observaciones de la ejecución para comprobar el progreso.

### AlphaFold 3 — Predicción de interacciones biomoleculares (2024)
- **Problema:** predecir la estructura conjunta de complejos con proteínas, ADN, ARN y moléculas pequeñas.
- **Método:** **Pairformer** procesa representaciones individuales y de pares; un módulo de **difusión**
  elimina ruido de coordenadas atómicas para generar la estructura 3D.
- **Módulos:** atención (Pairformer) · reconstrucción (como MAE, pero con estructuras experimentales) ·
  representaciones relacionales (los pares funcionan como aristas) · integración. **Difusión es una
  técnica adicional al programa.**
- **Límite:** una estructura predicha no demuestra función biológica; el artículo analiza estructuras
  plausibles pero incorrectas.
- **Pregunta:** ¿una estructura visualmente plausible valida la predicción? **No**: hay que analizar
  confianza, geometría y evidencia experimental.
- Fuente: Abramson et al., *Nature* (2024).

### Circuit tracing en Claude — Examinar mecanismos internos (2025)
- **Problema:** investigar cómo Claude 3.5 Haiku planifica una rima o comparte conceptos entre idiomas.
- **Método:** *circuit tracing* con características interpretables y **grafos de atribución**; las
  intervenciones sobre características comprueban hipótesis.
- **Módulos:** representaciones · características dispersas · transcoders (entrenados sin etiquetas,
  reconstruyendo las salidas de las MLPs) · causalidad. **Contraste importante:** un grafo de atribución
  es un grafo, pero **no es una GNN**: describe el cómputo, no aprende sobre él.
- **Límite:** el método captura una fracción de la computación y puede introducir artefactos.
- **Pregunta:** ¿la explicación que escribe el modelo describe su mecanismo interno? **No
  necesariamente.** El texto generado y el mecanismo deben contrastarse.
- Fuentes: `anthropic.com/research/tracing-thoughts-language-model` ·
  `transformer-circuits.pub/2025/attribution-graphs/methods.html`.

### AlphaEvolve — Agentes para descubrir y optimizar algoritmos (2025–2026)
- **Problema:** encontrar programas que resuelvan mejor un problema con una métrica evaluable.
- **Método:** modelos Gemini (Flash y Pro) proponen código; **evaluadores automáticos** verifican y
  puntúan; un proceso **evolutivo** conserva y reutiliza programas prometedores.
- **Módulos:** Transformers · integración · diseño de evaluación. **Contraste:** el ciclo de búsqueda
  evolutiva **no equivale a entrenar mediante RL**.
- **Límite:** depende de un evaluador útil y fiable; optimizar su puntuación no garantiza resolver un
  objetivo mal definido.
- **Pregunta:** ¿por qué el evaluador es tan importante como el generador? Porque **define qué candidatos
  sobreviven**: si no mide la propiedad deseada, la búsqueda mejora una puntuación sin mejorar el
  resultado.
- Fuentes: `arxiv.org/abs/2506.13131` · `deepmind.google/blog/alphaevolve-impact/`.

### Cierre de la parte 1
> Una arquitectura, un objetivo de aprendizaje, un método de adaptación y una pregunta de
> interpretabilidad **pueden formar parte del mismo sistema**.

---

# Parte 2 · Introducción a Transformers

Cuatro momentos, más un preámbulo.

## Preámbulo · ¿Por qué entender Transformers? Ética y seguridad

> Comprender el *backbone* de muchos LLMs ayuda a decidir **qué confiarles, qué verificar y qué no
> delegar**.

Mapa del sistema (inspirado en «Responsables»/*Liability* y «Productos»/*Warranty*, Godoy, Urrutia y
Carvajal, *Ética para la Ciencia de Datos*, 2023):

| Etapa | Quién | Riesgo | Garantía | Qué aporta entender el Transformer |
|---|---|---|---|---|
| **Datos de entrenamiento** | curaduría y etiquetado | sesgos, datos personales, derechos de autor | ¿sabemos con qué datos aprendió? | el modelo aprende patrones estadísticos de su corpus: lo que falta o está sesgado reaparece en sus predicciones |
| **Transformer** | entrenamiento y evaluación | errores plausibles, sesgos, opacidad | ¿es justo? ¿es robusto si el mundo cambia? | predice el siguiente token: **una respuesta probable no es necesariamente verdadera** |
| **Contexto (prompt)** | usuario y documentos externos | **inyección de instrucciones** | ¿quién controla lo que entra al contexto? | **instrucciones y datos son los mismos tokens en el mismo contexto**; la atención no distingue su origen y la máscara causal **no es una barrera de seguridad** |
| **Texto → acción** | integración con herramientas | el texto generado puede enviar correos, ejecutar código o mover dinero | ¿quién autorizó la acción? | permisos, aislamiento y validación **deben vivir fuera del modelo** |
| **Personas afectadas** | terceros | decisiones que afectan a quienes no usaron el sistema | si hay impacto negativo, ¿quién responde? | entender el mecanismo ayuda a decidir qué confiar, qué verificar y qué no delegar |

Referencias: NIST · GenAI Profile (2024) · NIST · Adversarial ML (2025) · Anthropic, *Faithfulness* (2025).

## Momento 01 · Decoder-only, paso a paso

**Referencia moderna: un decoder-only tipo Llama** — pre-normalización, **RoPE**, **GQA** y una MLP con
compuerta (**SwiGLU**). Advertencias explícitas de la clase:
- RoPE **rota Q y K**; **no** añade un vector al embedding.
- En esta familia se usa **RMSNorm** (no LayerNorm) y **SwiGLU**.
- **No es un diseño universal**: las variantes de posición, atención y MLP se comparan en el momento 04.
- El recorrido numérico usa un **modelo de juguete** de la misma estructura: **d = 8, 2 cabezas, 2 capas,
  |V| = 34, MHA en lugar de GQA**. Todos los números mostrados son valores intermedios reales de una
  sola pasada.

El orden dentro de la capa (lo que la diapositiva «Decoder-only moderno» traza para un token):
`xˡ` (residual de entrada) → `RMSNorm(xˡ)` (escala por 1/rms y ganancia aprendida) → atención causal
(actualización que se suma) → `r = xˡ + atención` (**primera suma residual**) → `MLP SwiGLU(RMSNorm(r))`
(actualización por posición) → `xˡ⁺¹ = r + MLP` (**segunda suma residual**).

### 1. Tokens
`t_i ∈ {0, …, |V| − 1}`. La separación por palabras es **solo ilustrativa**: un token puede ser parte de
palabra, puntuación o bytes. **El tokenizer no es la capa de embedding.**

### 2. Embeddings
`e_i = E[t_i] ∈ ℝᵈ`. Con n tokens, `X` tiene n filas y d columnas. En las ecuaciones matriciales de este
momento, **cada token es un vector fila**.

### 3. Q, K, V
`Q = XW_Q`, `K = XW_K`, `V = XW_V`. Las tres proyecciones son **paralelas** y parten de la **X ya
normalizada**. La *query* busca; la *key* permite comparar; el *value* aporta contenido.

### 4. Posición: RoPE
`q̃_i = RoPE(q_i, i)`, `k̃_i = RoPE(k_i, i)`. **Primero se proyecta, luego se rota.** El embedding inicia
el residual; la **posición se incorpora dentro de cada bloque de atención**. **V no se rota.**

RoPE actúa en **pares de dimensiones**: cada par es un vector 2D que se gira un ángulo proporcional a la
posición, con frecuencia propia `θ_k = base^(−2k/d_k)`. La demo permite interpolar λ de **NoPE** (λ = 0,
sin rotación: el score es `q·k` y no depende de i ni j) a **RoPE** (λ = 1), y desplazar ambas posiciones
en Δ: el score **no cambia**, porque depende de `j − i`.

### 5. Afinidades
`S = Q̃K̃ᵀ / √d_k ∈ ℝⁿˣⁿ`. El escalado controla la magnitud típica de los productos punto. **En GQA, cada
cabeza de query usa las keys del grupo al que pertenece.**

### 6. Máscara causal
`M_ij = 0` si `j ≤ i`; `M_ij = −∞` si `j > i`. Se aplica **antes** de softmax (`e^{−∞} = 0`). Permite
**entrenar todas las posiciones en paralelo** sin filtrar la respuesta futura. Con n posiciones hay
`n(n−1)/2` pares con `j > i`.

### 7. Pesos de atención
`A = softmax(S + M)`, con `Σ_j a_ij = 1`. Cada fila es un **destino**. Sin dividir por `√d_k` los scores
son `√d_k` veces mayores y la fila se concentra. **Los pesos de atención no son por sí solos una
explicación causal.**

### 8. Mezcla de values
`y_i = Σ_j a_ij v_j`; en forma matricial `Y = AV`. Ejemplo mínimo a mano: `¼[2,0] + ¾[0,4] = [0.5, 3]`;
los scores `[0, ln 3]` producen exactamente los pesos `[¼, ¾]`.

### 9. Multi-head
`Attention(X) = Concat(h₁, …, h_H) W_O`. Cada cabeza aprende sus propias proyecciones y opera sobre el
contexto permitido; `W_O` devuelve al ancho `d` del residual. **Una cabeza no tiene necesariamente una
función semántica única y estable.**

### 10. Residual y MLP
`R = X + Attention(Norm(X))` · `X' = R + MLP(Norm(R))`.
**Atención mezcla posiciones; la MLP transforma cada posición por separado**, con pesos compartidos.

### MLP por dentro: SwiGLU
`MLP(x_i) = (SiLU(x_i W_g) ⊙ x_i W_u) W_d`, sin sesgos, tipo Llama. Dos proyecciones **paralelas** se
combinan con una multiplicación elemento a elemento. **La compuerta introduce no linealidad sin mezclar
posiciones**; el contexto ya llega incorporado en `x_i`.

### 11. Apilar bloques
`Xˡ⁺¹ = Blockˡ(Xˡ)`. La profundidad permite **componer** operaciones. **Por sí sola no garantiza
razonamiento** ni mejor desempeño en cualquier tarea.

> **Lente de logits (*logit lens*):** leer cada residual intermedio con la normalización final y `U`
> permite ver cómo se forma la predicción **capa a capa**.

### 12. Logits
`z_i = Norm(x_iᴸ) W_U + b_U ∈ ℝ^{|V|}`. **El unembedding no es la inversa del embedding**; usar sesgo o
compartir pesos depende del modelo.

### 13. Probabilidades
`p(t_{i+1} | t_{≤i}) = softmax(z_i / T)`. **T < 1 concentra, T > 1 aplana; el orden de los tokens no
cambia.** La probabilidad **no garantiza verdad**. La demo muestra además la **entropía** en bits.

### 14. Generar
`p(t₁…t_n) = ∏_i p(t_i | t_{<i})`. **Argmax y muestreo son estrategias distintas.** El **caché KV** evita
recalcular keys y values pasados en cada paso; **no elimina su costo de almacenamiento**. Tras el
*prefill*, en cada paso solo el último par (k, v) es nuevo.

### Entrenar y generar: el mismo modelo, dos flujos
`ℒ = −Σ_i log p_θ(t_{i+1} | t_{≤i})`.
- **Entrenamiento:** todas las posiciones a la vez; los pesos se actualizan.
- **Generación:** una posición por paso; la generación estándar mantiene los pesos fijos.

## Momento 02 · Tres familias de Transformers

> **«LLM» no equivale estrictamente a decoder-only.** GPT es la familia dominante en generación
> autorregresiva, no todo Transformer.

| Familia | Contexto | Objetivo | Uso típico |
|---|---|---|---|
| **Decoder-only · GPT** | prefijo causal | `p(y \| x) = ∏_i p(y_i \| x, y_{<i})` | continuar / generar: texto, código, diálogo |
| **Encoder-only · BERT** | entrada bidireccional | `p(t_masked \| t_resto)` (**masked language modeling**, y NSP en el diseño original) | representar / clasificar: clasificación, extracción de entidades |
| **Encoder-decoder · T5** | entrada + prefijo de salida | cross-attention: **Q del decoder; K, V del encoder** | transformar una secuencia en otra: traducción, resumen |

T5 usa formato **texto-a-texto** y preentrenamiento de *denoising*. **La familia es una decisión de
diseño, no una lista de tareas permitidas**: una clasificación también puede formularse como generación.
También importan objetivo de entrenamiento, datos, escala y adaptación; esta taxonomía de tres familias
**no describe todas las variantes posibles**.

## Momento 03 · Historia: atención y posición

> **La atención no comienza en 2017.** Convergen varias líneas: memoria asociativa, selección visual y
> alineamiento de secuencias. Es una historia de hitos y líneas de trabajo, **no una atribución a un
> único artículo**.

| Período | Hito | Qué aportó |
|---|---|---|
| **1982–2013** | Antecedentes | Memoria por contenido (Hopfield), control del foco (Schmidhuber & Huber 1991, Larochelle & Hinton 2010), *fast weights* (1992), alineamiento suave (Graves 2013) |
| **2014–2015** | Atención diferenciable | Traducción (Sutskever; Bahdanau; Luong), visión (Mnih; Xu), memorias externas (NTM; Sukhbaatar) |
| **2016–2017** | Self-attention y Transformer | Parikh et al. (2016, atención descomponible con extensión intra-oración); Lin et al. (mar. 2017, self-attention estructurada sobre un BiLSTM); Vaswani et al. (2017) |

- **1982 · Hopfield:** `s_i ← sign(Σ_j w_ij s_j)`, `W = (1/N) Σ_u pᵘ(pᵘ)ᵀ`. Antecedente de memoria
  asociativa, **no la self-attention softmax de 2017**; la conexión formal con Hopfield modernos llega
  mucho después.
- **2014 · El cuello de botella:** en seq2seq recurrente básico, `h_t = R h_{t−1} + e(x_t)`, `c = h_n`:
  un estado de **tamaño fijo** conecta encoder y decoder. Bahdanau et al. cuestionan ese cuello de
  botella, sobre todo en secuencias largas.
- **2016–2017:** atención sin recurrencia y self-attention tienen precedentes. **Lin et al. aún usan un
  BiLSTM: self-attention no significa automáticamente «sin RNN».**
- **2017 · Vaswani:** `Attention(Q,K,V) = softmax(QKᵀ/√d_k)V`. La contribución **no es inventar la
  atención**: es una **arquitectura completa paralelizable** (atención + MLPs + posiciones + residuales +
  normalización, sin RNN ni convoluciones), evaluada originalmente en traducción.

### Embeddings posicionales: dos ejes

> **Aprendida/fija ≠ absoluta/relativa.** Un eje pregunta **cómo se obtiene** la señal; el otro, **qué
> posición expresa**.

| Método | Parámetros de posición | Señal posicional |
|---|---|---|
| Tabla absoluta | aprendidos | índice i |
| Sinusoidal aditiva | fijos | índice i |
| Sesgo T5 | aprendidos | *bucket* de `j − i` |
| RoPE base | frecuencias fijas | rotación por i; **score relativo** |

- **Absolutas aprendidas:** `x_i = E[t_i] + P[i]`. BERT las usa. Una tabla finita **no provee vectores
  entrenados para índices fuera de su rango**; extenderla exige decisiones adicionales.
- **Sinusoidales:** `p_{i,2r} = sin(i ω_r)`, `p_{i,2r+1} = cos(i ω_r)`, con `ω_r = 10000^(−2r/d)`. Se
  **suma** `p_i` al embedding: sigue siendo **absoluta**. Poder calcularla para cualquier i **no
  garantiza generalizar a cualquier longitud**. El término *Fourier-like* describe el uso de senos,
  cosenos y fases; **no** significa aplicar una FFT al texto.
- **Relativas (Shaw et al.):** `s_ij = q_i · (k_j + r_{j−i}) / √d_k` — embeddings relativos aprendidos
  con distancias recortadas; también modifican los values. Transformer-XL desarrolla otra formulación
  relativa, compatible con su memoria recurrente.
- **Sesgos de distancia:** `s_ij = q_i · k_j / √d_k + b_h(i,j)`. **T5** aprende los sesgos de sus
  *buckets* (uno por cabeza, compartido entre capas); **ALiBi** fija pendientes por cabeza
  (`−m_h(i − j)` en causal). *Relativo* **no** significa necesariamente *aprendido* ni *periódico*.
- **RoPE:** `q'_i = R(i)q_i`, `k'_j = R(j)k_j` (aquí con vectores columna). La **fase relativa** aparece
  en el score: `(R(i)q_i)ᵀ(R(j)k_j) = q_iᵀ R(j − i) k_j`. Desplazar ambos índices igual conserva el score
  si el contenido se mantiene fijo. RoPE **no suma una PE al residual**; los vectores de contenido siguen
  siendo aprendidos.
- **La evolución no es una sustitución cronológica simple ni una escala universal de superioridad:**
  cambian los parámetros, el sesgo inductivo y la generalización a nuevas longitudes.

## Momento 04 · Arquitecturas y eficiencia

> Tres preguntas distintas: **¿qué conexiones calcular?** (ventanas, patrones dispersos, selección
> aprendida) · **¿cómo guardar y computar?** (caché KV, GQA, MLA, FlashAttention) · **¿qué interacción
> representar?** (atención lineal, memorias recurrentes, atención de orden superior).
>
> **Eficiencia y exactitud no mejoran automáticamente juntas.** Cada propuesta se evalúa en tareas,
> longitudes y hardware concretos.

### El costo de la base
Con n posiciones, cada cabeza produce una matriz n × n durante *prefill* o entrenamiento:
**O(n²d)** con anchos fijos. **No es el costo total del modelo** (proyecciones y MLP también cuentan).
Durante *decode* con caché KV, un token nuevo compara con **O(n)** posiciones pasadas.

### Conectividad
| Método | Regla | Costo | Nota |
|---|---|---|---|
| **Sliding window** | `i − w < j ≤ i` | O(nwd) | Mistral 7B v0.1 usa SWA. La información lejana puede propagarse **entre capas**, pero el acceso directo está limitado |
| **Local + global** | ventana w + g tokens globales | O(n(w + g)d) | Longformer (2020), en contexto **bidireccional**: no trasladar su máscara sin cambios a un decoder causal |
| **DeepSeek Sparse Attention (DSA)** | `S_i = TopK(I_{i,≤i})`, `y_i = Attention(q_i, KV[S_i])` | — | Un *lightning indexer* puntúa el historial; la atención principal usa solo los top-k. En DeepSeek-V3.2 (2025) se integra con MLA. **La selección depende del contenido; no es una ventana fija** |

### Forma de interacción
- **Atención lineal** (Katharopoulos et al., 2020). Una similitud factorizable permite acumular el pasado
  en un **estado de tamaño fijo** (vectores columna):
  `S_i = Σ_{j≤i} φ(k_j)v_jᵀ`, `z_i = Σ_{j≤i} φ(k_j)`; lectura `y_iᵀ = φ(q_i)ᵀS_i / (φ(q_i)ᵀz_i)`.
  Lineal en n para dimensiones fijas, **sin materializar una matriz n × n**. **No es la misma función que
  softmax densa**: puede perder detalle al comprimir el historial.
- **Memorias e híbridos:** *gating* para controlar retención y actualizaciones más selectivas (Gated
  DeltaNet); combinar memoria comprimida con acceso explícito a algunos tokens. **Mejoras en sus
  benchmarks no implican superioridad universal ni equivalencia a softmax.**
- **Strassen attention** (Kozachinskiy et al., 2025): de pares a **tripletes**,
  `s_ijk = (f_i·g_j + g_j·h_k + h_k·f_i)/√d`; el contenido combina `v_j ⊙ v_k`. Busca **capacidad
  composicional**, no simplemente dispersar la atención. Teóricamente **O(n^ω d)** con ω < 3, evitando
  enumerar los tripletes. **No significa ser más barata que la atención cuadrática estándar**, ni prueba
  una mejora general en LLMs grandes: la evidencia del artículo son separaciones de capacidad en una capa
  y experimentos sintéticos composicionales.

### Memoria y ejecución
- **FlashAttention** (Dao et al., 2022): reorganiza el cálculo **por bloques** para aprovechar la SRAM de
  la GPU, con softmax *online*. Atención softmax **exacta** salvo redondeo. **Reduce tráfico de memoria;
  el trabajo aritmético denso sigue siendo cuadrático en n. No es atención dispersa.**
- **MHA / GQA / MQA:** `H_kv = H_q` es MHA; `1 < H_kv < H_q` es **GQA**; `H_kv = 1` es **MQA**. Cada
  cabeza conserva su proyección de query; un grupo comparte K y V: `Y_h = softmax(Q_h(Kᵍ)ᵀ/√d_k + M)Vᵍ`.
  **Compartir el historial proyectado no obliga a compartir la distribución de atención.** GQA conserva
  el acceso causal al historial: **reduce cabezas KV, no posiciones**. Es un cambio de arquitectura
  entrenado o adaptado, **no un interruptor de inferencia**.
- **Caché KV:** `Bytes KV = 2 × L × B × n × H_kv × d_head × b`. Cálculo **ilustrativo** con L = 32, B = 1,
  n = 8192, H_q = 32, d_head = 128, b = 2 bytes, sin overhead:

  | Ejemplo | H_kv | Caché KV |
  |---|---|---|
  | MHA | 32 | 4 GiB |
  | GQA | 8 | 1 GiB |
  | MQA | 1 | 128 MiB |

  **4× menos caché no significa 4× más velocidad ni 4× menos trabajo total.**
- **MLA** (DeepSeek-V2, 2024): comprime el caché en un **espacio latente**. **Ahorrar memoria KV no es
  seleccionar tokens**: es otra dimensión de diseño, combinable con otros mecanismos.

### Capacidad: Mixture of Experts
Un *router* activa una fracción de expertos, normalmente en subcapas feed-forward (Fedus et al.,
2021/22). Aumenta capacidad con cómputo activo selectivo, pero **añade memoria y comunicación**.
**La sparsity de expertos no es sparsity de tokens.**

### Síntesis del momento
| Qué cambia | Ejemplos |
|---|---|
| **Conectividad** | Ventanas / DSA: menos pares explícitos |
| **Memoria y ejecución** | GQA / MLA / FlashAttention: almacenamiento o implementación |
| **Forma de interacción** | Linear / Strassen: otra agregación o mayor orden |

> **La arquitectura ofrece posibilidades; entrenamiento, datos y hardware determinan cuánto de ellas se
> obtiene. Exactitud y eficiencia deben medirse por separado.**
