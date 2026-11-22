# Clase 3 (03/11/2026) · Modelos Autosupervisados

Docente: **Felipe del Río** (CENIA). 61 diapositivas.
Agenda: **1. Motivación · 2. Aprendizaje Autosupervisado · 3. Texto: GPT · 4. Visión: MAE ·
5. Multimodal: CLIP.**

> **Ojo con el material:** la portada del PDF dice «Clase 2», pero la agenda y el contenido son los de
> la **clase 3**. Es un error de la diapositiva de título.

## 1 · Motivación

Recordemos el paradigma de **modelos fundacionales** con que cerró la clase 2.

- El éxito del aprendizaje profundo se debe a **grandes conjuntos de datos etiquetados** (ImageNet,
  corpus de textos anotados…).
- El **etiquetado humano es costoso, lento y no escala bien**.
- Los **datos sin etiquetar crecen exponencialmente**: imágenes, texto, videos y datos de sensores en
  internet.

> **Cuello de botella de datos: los modelos pueden escalar, pero los datos etiquetados no.**

**IA escalable = aprovechar grandes cantidades de datos sin etiquetar.** Pero, ¿cómo aprendemos
directamente de los propios datos? El aprendizaje **no supervisado** aprende la **estructura intrínseca**
de los datos.

## 2 · Self-Supervised Learning (SSL)

**Definición básica:** utilizar **tareas de pretexto** para aprender representaciones significativas
**sin etiquetas manuales**.

> Nos permite **transformar aprendizaje no supervisado en supervisado**: obtenemos las **señales de
> supervisión directamente de los datos**.

**Aprendizaje de representación:** capturar la **estructura semántica**.

**Tareas de pretexto:** objetivos generados **automáticamente** a partir de la estructura intrínseca de
los datos. Por ejemplo:
- Predicción de **partes ocultas**.
- **Reconstrucción** de entradas.
- **Alineación** de modalidades.

Difieren de las aplicaciones reales, **pero proporcionan conocimiento transferible** (es decir, se
conectan directamente con el transfer learning de la clase 2).

**Por qué importa el SSL:**
- **Escalabilidad:** aprovechar datos sin etiquetar.
- **Robustez:** aprender patrones en diferentes dominios.
- **Modelos fundacionales:** una nueva generación de modelos.

### Las tres familias de objetivos

| Familia | Idea | Ejemplo en la clase |
|---|---|---|
| **Aprendizaje generativo** | predecir contenido **faltante o futuro** | GPT, MAE |
| **Aprendizaje contrastivo** | elementos **similares cerca, diferentes lejos** | CLIP, SimCLR, MoCo |
| **Aprendizaje adversarial** | **tira y afloja** de dos redes (G y D) | GANs |

## 3 · Texto: GPT

### Modelamiento de lenguaje
Un objetivo autosupervisado **simple pero potente**. Modelos **autorregresivos**: predecir cada token
dados **todos los anteriores**.

```
P(x) = P(x_t | x_<t) = P(x_t | x_{t−1}, x_{t−2}, …, x_0)
```

**Ejemplos de modelos:** serie **GPT** (GPT-1 a GPT-5) · **LLaMA** (alternativas abiertas) ·
**Mistral** (enfoques de mezcla de expertos) · **LatamGPT**, entre otros.

### El Transformer (visto desde SSL)
Procesa secuencias de manera eficiente. **Decoder-only** con:
- **Multi-head auto-atención**
- **Capas feedforward**
- **Conexiones residuales**

**Enmascaramiento causal:** solo se consideran los tokens anteriores. Permite la **generación de texto
coherente** y un **entrenamiento e inferencia eficientes**.

### Escala y generalización
- **Scaling laws:** los modelos siguen **leyes de escalamiento predecibles**.
- **GPT-3:** usando **few-shot**, logra rendimiento similar a los mejores modelos que usan
  **fine-tuning**.

### Prompting
Interactuar con modelos mediante **instrucciones en lenguaje natural** que guíen su comportamiento.

> **Idea principal:** usar el **conocimiento preentrenado** del modelo para realizar **nuevas tareas
> mediante instrucciones**, en lugar de reentrenarlo.

**Tipos de prompts:**
- **Zero-shot:** sin ejemplos, solo la instrucción.
- **Few-shot:** contiene algunos ejemplos.
- **Chain-of-Thought:** se pide que incluya **pasos de razonamiento**.

| Ventajas | Limitaciones |
|---|---|
| No requiere entrenamiento | **Sensible a la redacción y el formato** |
| Adaptación rápida a nuevos dominios o tareas | Adaptación limitada frente a fine-tuning |
| Control sencillo e interpretable del comportamiento | Puede requerir *prompt engineering* |

> **Una diferencia importante: ChatGPT no es solo un modelo de lenguaje.** (Hay SFT, alineamiento y
> producto alrededor del LM.)

### ¿Por qué el modelamiento de lenguaje permite generalizar?
Es una **propiedad emergente**: el modelo aprende a **continuar patrones** en contextos arbitrarios y a
**interpretar las instrucciones y ejemplos que aparecen en el texto**. El objetivo lo fuerza a aprender
un **amplio conjunto de habilidades y capacidades de reconocimiento de patrones**: sintaxis, semántica,
tópicos, etcétera.

## 4 · Visión: MAE

### Vision Transformers (ViT)
Podemos usar un Transformer para visión **dividiendo la imagen en parches**.

### Autoencoders
Redes entrenadas para **reconstruir su propia entrada** (`x → z → x̂`, con pérdida RMSE).
**Objetivo:** aprender **representaciones latentes comprimidas e informativas**.

**Variantes:**
- **Denoising AE:** reconstruye datos limpios a partir de entradas corruptas.
- **Sparse AE:** fomenta representaciones *sparse*.
- **Variational AE (VAE):** agrega estructura probabilística para tareas generativas.

### Masked Autoencoders (MAE)
Variante de autoencoder **autosupervisado**. **Masked:** parte de la entrada se oculta y el modelo
aprende a **reconstruir el contenido faltante**.

> **Idea principal:** esta tarea **obliga al modelo a aprender representaciones semánticas de alto
> nivel.**

**Arquitectura, en cuatro pasos:**
1. **Enmascaramiento aleatorio:** se elimina el **75 %** de los parches **antes de la codificación**.
2. **Encoder completo:** procesa **solo los parches visibles** con un ViT. → **se ahorra cómputo.**
3. **Decoder ligero:** reconstruye **todos** los parches enmascarados.
4. **Reconstrucción de píxeles:** pérdida **MSE solo en los parches enmascarados**.

La clase muestra reconstrucciones con **75 %, 85 % y 95 %** de enmascaramiento.

### Otras técnicas de preentrenamiento
Otros objetivos autosupervisados muy exitosos: **SimCLR · MoCo · BYOL · DINO y DINOv2.**

## 5 · Multimodal: CLIP

**CLIP = Contrastive Language–Image Pre-training.** Aprendizaje de modelos visuales **transferibles** a
partir de la **supervisión del lenguaje natural**.

**Ideas:**
- Entrenar con **grandes conjuntos de datos web** que combinan imágenes y texto.
- Usar el **texto como una etiqueta más flexible** para abordar otras tareas.
- Realizar **aprendizaje sin ejemplos (zero-shot)** usando lenguaje natural.
- Aprender una **representación vinculada al lenguaje**.

### Datos: WebImageText (WIT)
- **400 millones** de pares imagen–texto, recopilados de diversas fuentes de internet.
- Mejorado **buscando pares a partir de un conjunto de consultas**.
- La lista de consultas se construyó con **todas las palabras que aparecen al menos 100 veces en
  Wikipedia**.
- Hasta **20.000 pares imagen–texto por consulta**.

### Entrenamiento
Dado un conjunto de **N pares imagen–texto**, CLIP se entrena para **predecir cuál de las N × N
combinaciones posibles se produjo**: la **diagonal** son los elementos relacionados, el resto no.

**Objetivo contrastivo:** los elementos relacionados deben estar **más cerca entre sí en el espacio de
características** que los no relacionados.

> **¿Por qué contrastivo?** Para **evitar intentar predecir las palabras exactas**, y porque es **más
> eficiente**.

### Espacio latente
Se entrena para que las representaciones de **texto e imagen se agrupen por similitud semántica** en un
**espacio compartido**.

### Zero-shot
CLIP **compara un texto y una imagen** asignando una **puntuación de similitud**. Para clasificación
zero-shot se usa la consulta **«A photo of a {class}»**.

### Otros modelos multimodales
- **BLIP / BLIP-2:** preentrenamiento con lenguaje e imágenes para **generación y descripción
  automática**.
- **Flamingo:** **pregunta-respuesta visual** con pocos ejemplos, **intercalando** visión y lenguaje.

## Práctico asociado
`Práctico_Aprendizaje_Autosupervisado.ipynb` — **CLIP ViT-B/32** en clasificación zero-shot sobre
**Food101** y **Stanford Cars**, con templates de consulta propios y visualización PCA 3D de embeddings
de texto e imagen. Detalle en `practicos-y-codigo.md`.
