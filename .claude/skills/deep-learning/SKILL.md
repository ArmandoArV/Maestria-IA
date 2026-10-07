---
name: deep-learning
description: >
  Expert knowledge base for the INF3812 Deep Learning course (Magíster en IA, PUC Chile, Prof. Hans
  Löbel). Covers the full course: aprendizaje de representaciones y sesgo inductivo, el esquema general
  de un modelo de ML (modelo predictivo, función de pérdida, regularizador, técnica de búsqueda),
  neurona artificial y perceptrón, MLP y teorema de aproximación universal, softmax y cross-entropy,
  MNIST y Fashion-MNIST, datos tabulados con embeddings categóricos y dropout; redes convolucionales
  (convolución, campo receptivo, pooling, equivarianza a la traslación, AlexNet, ImageNet, aumento de
  datos); entrenamiento de redes (grafo de cómputo, backpropagation, regla de la cadena, SGD, momentum,
  NAG, Adagrad, RMSProp, Adadelta, Adam, inicialización Kaiming/He, LeCun y Xavier/Glorot, batch
  normalization, conexiones residuales y skip connections, dropout, regularización L1 y L2, transfer
  learning y fine-tuning); redes recurrentes (RNN, estado oculto, BPTT, truncated backprop, exploding y
  vanishing gradients, gradient clipping, LSTM, GRU, RNN bidireccional, image captioning); modelos de
  lenguaje (BoW, one-hot, word embeddings, word2vec, GloVe, fastText, seq2seq encoder-decoder, vector
  de contexto, teacher forcing, exposure bias, greedy y beam search); y Transformers (atención,
  auto-atención, Query/Key/Value, multi-head, embedding posicional, máscara causal, modelos
  fundacionales, aprendizaje autosupervisado, BERT). Incluye el uso práctico de PyTorch y Colab y los
  ejercicios resueltos del curso. Use for any INF3812 question — controles, tareas, slides, syllabus,
  o para construir y entrenar redes neuronales siguiendo las convenciones del curso. Also trigger on
  deep learning, aprendizaje profundo, red neuronal, neural network, MLP, perceptrón multicapa,
  feedforward, capa oculta, función de activación, ReLU, sigmoide, tanh, softmax, cross entropy,
  entropía cruzada, backpropagation, retropropagación, descenso de gradiente, SGD, momentum, Adam,
  learning rate, época, batch, minibatch, sobreajuste, overfitting, dropout, batch normalization,
  inicialización de pesos, Xavier, Glorot, Kaiming, He, conexión residual, skip connection, ResNet,
  CNN, convolución, filtro, kernel, stride, padding, pooling, campo receptivo, AlexNet, VGG, ImageNet,
  aumento de datos, data augmentation, transfer learning, fine-tuning, RNN, LSTM, GRU, BPTT, secuencia,
  serie de tiempo, embedding, word2vec, seq2seq, encoder-decoder, atención, attention, self-attention,
  Transformer, query key value, multi-head, positional encoding, BERT, PyTorch, torch, Colab, autograd,
  nn.Module, DataLoader, tensor, GPU, or the course code (INF3812).
  Respond in Spanish when the user writes in Spanish.
---

# Deep Learning (INF3812)

Knowledge base for **INF3812 – Deep Learning**, Pontificia Universidad Católica de Chile, Escuela de
Ingeniería, Departamento de Ciencia de la Computación. Profesor **Hans Löbel** (`halobel@uc.cl`),
Dpto. de Ingeniería de Transporte y Logística + Dpto. de Ciencia de la Computación.

> *"Este es un curso conceptual-teórico-práctico, pero no porque sí."* Las implementaciones se
> consideran parte fundamental de los contenidos, **pero no el código en sí**: lo que se evalúa es el
> criterio de diseño, no la sintaxis.

## Cómo usar esta skill

1. **Lee el archivo de `references/` que corresponda** antes de responder algo más allá del resumen de
   abajo. SKILL.md es el mapa; los archivos de referencia tienen las fórmulas, las cifras de los casos
   de estudio y los ejercicios resueltos.
2. **Responde en español.** El curso es en español.
3. **Razona siempre desde el sesgo inductivo.** Es el hilo conductor del curso completo: un MLP no
   asume nada sobre la entrada, una CNN asume localidad y equivarianza a la traslación, una RNN asume
   orden secuencial, un Transformer asume que la relevancia entre posiciones se puede aprender. Cuando
   te pregunten por qué una arquitectura funciona o falla en un dominio, la respuesta casi siempre está
   en el calce o descalce entre ese supuesto y la estructura real de los datos.
4. **Usa PyTorch**, no Keras ni TensorFlow, y asume ejecución en Colab. Es la elección explícita del
   curso. Ver `references/pytorch-practica.md`.
5. **Precaución sobre el código del curso:** las láminas dicen repetidamente "Vamos a Colab…", pero
   **esos notebooks no están en el repositorio** (solo hay 7 PDFs y la carpeta `SolucionEjercicios`).
   Los patrones de código de esta skill son PyTorch estándar alineado a los conceptos del curso, **no
   transcripciones del código de clase**. Dilo si alguien pide "el código de la clase X".
6. **Integridad académica:** los controles son **individuales**. Usa esta skill para explicar, resolver
   ejemplos análogos y revisar razonamiento; no para entregar las respuestas del control.

## Mapa del curso

| Sesión | Fecha | Tema | Reference |
|--------|-------|------|-----------|
| 1 | 04/08 | Fundamentos de Deep Learning | `references/clase1-2-fundamentos-y-mlp.md` |
| 2 | 11/08 | Arquitecturas neuronales fundamentales (MLP, embeddings, dropout) | `references/clase1-2-fundamentos-y-mlp.md` |
| 3 | 18/08 | Redes Convolucionales | `references/clase3-cnn.md` |
| 4 | 25/08 | Entrenamiento de Redes Neuronales | `references/clase4-entrenamiento.md` |
| 5 | 01/09 | **Evaluaciones 1** (Control 1 + consultas Tarea 1) | — |
| 6 | 08/09 | Redes Recurrentes | `references/clase5-7-secuencias-y-transformers.md` |
| 7 | 22/09 | Modelos de lenguaje | `references/clase5-7-secuencias-y-transformers.md` |
| 8 | 29/09 | Arquitectura Transformer | `references/clase5-7-secuencias-y-transformers.md` |
| 9 | 06/10 | **Evaluaciones 2** (Control 2 + consultas Tarea 2) | — |

Práctica en PyTorch: `references/pytorch-practica.md`.
Ejercicios resueltos del curso: `references/ejercicios-resueltos.md`.

Material: `DeepLearning/` (7 PDFs de clase) y `DeepLearning/SolucionEjercicios/`.

## Evaluación

- **2 controles individuales** (sesiones 5 y 9), **25 % cada uno**. El Control 1 cubre hasta la sesión
  4; el Control 2, hasta la sesión 8. Duran aproximadamente las **primeras 2 horas** de la sesión y
  esas sesiones son **remotas**.
- **2 tareas grupales** (grupos de hasta 3), **25 % cada una**. Los enunciados se publican después de
  las sesiones 4 y 8; cubren los aspectos **prácticos** (programación y análisis).
- La entrega es el **domingo subsiguiente** a la publicación: Tarea 1 el **domingo 6 de septiembre**,
  Tarea 2 el **domingo 11 de octubre**.
- Después de cada control hay una **sesión de consultas** para la tarea.

**Canales oficiales:** **Canvas** para todo (programa, videos, slides, ejemplos) · **Teams** para
sesiones y comunicación sincrónica · el **foro del curso** para dudas de materia · el correo
`halobel@uc.cl` solo para temas administrativos.

## Conceptos núcleo (referencia rápida)

### El esquema general de cualquier sistema de Machine Learning
> Buscamos, en el **espacio de hipótesis** del modelo, aquella hipótesis con mejor rendimiento (menor
> pérdida) en los datos de entrenamiento, apoyándonos en el **sesgo inductivo** del modelo.

Cuatro piezas: **modelo predictivo** (espacio de hipótesis + sesgo inductivo) · **datos de
entrenamiento** · **función de pérdida** · **técnica de búsqueda**. Matemáticamente:

$$\arg\min_W \; J(X,Y;W) \;=\; \lambda\,\mathcal{R}(W) \;+\; \sum_{i}^{N} \mathcal{L}\big(f(x_i;W),\,y_i\big)$$

- **Modelo predictivo** $f(\cdot;W)$: función parametrizada que mapea del espacio de los datos al de
  las etiquetas. Sus **parámetros viven en el espacio de hipótesis**.
- **Función de pérdida** $\mathcal{L}$: cuantifica el error del modelo en los datos de entrenamiento.
- **Regularizador** $\mathcal{R}(W)$: induce sesgo inductivo **a través de los parámetros**.
- Todo junto es un **problema de optimización**: una búsqueda sobre el espacio de hipótesis.

### Qué es Deep Learning
Área de la IA centrada en **redes neuronales de múltiples capas**, entrenadas para aprender
**representaciones y resolver la tarea de manera conjunta**.
- Sus capas aprenden representaciones (**features**) **composicionales y jerárquicas**, además de las
  necesarias para la tarea.
- Las unidades son **diferenciables** y se entrenan conjuntamente con una **función objetivo común**.
- *"Principal diferencia con las redes neuronales previas: ahora sí funcionan."*

**Representaciones composicionales y jerárquicas:** se organizan de bajo a alto nivel de abstracción y
permiten describir infinitas configuraciones a partir de un número acotado de elementos. Sonidos →
fonemas → sílabas → palabras · Pixeles → bordes → partes → objetos → escenas · Caracteres → palabras →
grupos → cláusulas → frases.

**Capas bajas:** features genéricas y locales (bordes, fonemas), bloques de construcción.
**Capas altas:** features especializadas y globales, más robustas a variaciones (independientes del
hablante o del punto de vista).

### Por qué recién ahora funcionan: tres elementos centrales
1. **Estructura y entrenamiento** — distintos grupos mantuvieron y desarrollaron las bases técnicas
   durante décadas, incluso cuando el foco dominante estaba en otras técnicas.
2. **Bases de datos órdenes de magnitud mayores** — datos para reconocimiento visual y para NLP.
3. **GPUs y aceleradores** — cuando crecen datos y modelos, la CPU se vuelve cuello de botella; los
   aceleradores y las arquitecturas paralelas o distribuidas hacen viable el entrenamiento a escala.

### El problema con las features diseñadas a mano
Las técnicas tradicionales de ML usan *handcrafted features*, que dependen del conocimiento experto.
No es ideal por tres motivos: (i) un experto es **caro** y nada asegura que su conocimiento sea
óptimo; (ii) para **datos no estructurados** no son evidentes las mejores características; (iii) no es
evidente **cómo combinar distintos tipos de datos** ni qué relaciones hay entre ellos.
**La clave es pensar las features y el modelo predictivo como un problema conjunto.**

### El MLP y su límite
Un **MLP** compone transformaciones afines y activaciones no lineales en múltiples capas:
$f = \sigma(W_3\,\sigma(W_2\,\sigma(W_1 x)))$ para 3 capas.

**Teorema de aproximación universal:** bajo ciertas condiciones, una red con **una capa oculta
suficientemente ancha** puede aproximar funciones continuas sobre dominios compactos con precisión
arbitraria. **Pero el resultado no garantiza** que esa red sea fácil de entrenar, eficiente en
parámetros ni capaz de generalizar con pocos datos.

**La consecuencia práctica, que es la tesis del curso:**
> Como los MLP no tienen restricción en lo que pueden aprender, les sale más fácil usar correlaciones
> entre el **ruido** y la etiqueta. **Gran parte del arte de Deep Learning es usar arquitecturas que
> sesguen el aprendizaje en base a la estructura de los datos**, de modo que aprendan representaciones
> útiles.

### Tabla de sesgos inductivos (el mapa mental del curso)
| Arquitectura | Qué asume sobre los datos | Cuándo falla |
|---|---|---|
| **MLP** | Nada; entrada como vector plano | Imágenes (demasiados parámetros, sin equivarianza), datos tabulados correlacionados (sobreajuste) |
| **CNN** | Localidad + equivarianza a la traslación | Si se destruye la estructura espacial (p. ej. permutar píxeles) |
| **RNN / LSTM / GRU** | Orden secuencial, estado que resume el pasado | Dependencias muy largas; cómputo inherentemente secuencial |
| **Transformer** | La relevancia entre posiciones se aprende; sin recurrencia | Requiere muchísimos datos y cómputo; el orden hay que inyectarlo |

### Las cuatro preguntas del entrenamiento (clase 4)
1. **¿Cómo calculo las derivadas para cada parámetro?** → grafo de cómputo + regla de la cadena +
   backpropagation.
2. **¿Cómo desciendo de manera efectiva y eficiente?** → SGD y sus variantes (momentum, NAG, Adagrad,
   RMSProp, Adadelta, Adam).
3. **¿Debo inicializar los pesos y normalizar los datos de manera especial?** → Kaiming/He, LeCun,
   Xavier/Glorot; batch normalization.
4. **¿Puedo hacerle algo a la arquitectura para facilitar el proceso?** → conexiones residuales.

Y, en paralelo: **¿cómo controlar el sobreajuste?** (dropout, L1/L2, aumento de datos) y **¿cómo
reutilizar?** (transfer learning, fine-tuning).

### El concepto central de la clase 4
> Para entrenar redes hay que considerar muchos elementos prácticos. Afortunadamente, **no es
> necesario reinventar la rueda** y muchas veces basta con basarse en trabajos anteriores.

## Bibliografía del curso

- **Goodfellow, Bengio y Courville**, *Deep Learning* — https://www.deeplearningbook.org/
- **Zhang et al.**, *Dive into Deep Learning* (D2L) — https://d2l.ai/

**Recursos de visualización y lectura citados en clase:** CNN Explainer
(`poloclub.github.io/cnn-explainer/`) · Adam Harley, visualización 3D de redes
(`adamharley.com/nn_vis/`) · `micrograd` de Karpathy (`github.com/karpathy/micrograd`) ·
*The Illustrated Transformer* (`jalammar.github.io/illustrated-transformer/`) · *Understanding LSTM
Networks* de Colah · *The Unreasonable Effectiveness of RNNs* de Karpathy · Distill sobre momentum y
sobre memorización en RNNs · `losslandscape.com` · Embedding Projector
(`projector.tensorflow.org`) · Papers With Code (SOTA en ImageNet).
