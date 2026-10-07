# Clases 5-7 · Secuencias: RNN, modelos de lenguaje y Transformers

En esta segunda parte del curso el foco son los esquemas que permiten **aprender sobre secuencias de
datos**: series de tiempo, texto, videos, etc. Tres líneas:
- **Recurrencia** para capturar el estado de una secuencia: **RNN, LSTM, GRU**.
- **Aprendizaje de representaciones** basadas en coocurrencia y contexto: **word2vec, seq2seq**.
- **Aprendizaje general sobre secuencias**: **Transformer**.

---

# Parte I · Redes Neuronales Recurrentes (clase 5)

## 1. Qué es una RNN

- Propuestas en la **década de los 80**.
- Trabajan de manera **secuencial**, procesando **uno a uno** los elementos de la secuencia o serie.
- A diferencia de las redes feedforward, las RNN **mantienen un estado**, es decir, **"tienen
  memoria"**.
- **Cómo se maneja esa memoria** es lo que caracteriza a los distintos tipos de redes recurrentes
  (RNN, LSTM, GRU).

### Formalización
$$h_t = g\big(f_1(x_t),\, f_2(h_{t-1})\big)$$

- $t$: paso de la secuencia; usualmente tiene significado temporal, **pero puede representar cualquier
  relación de orden** (espacio, ranking, etc.).
- $x_t$: vector que codifica el paso $t$ de la secuencia de entrada.
- $h_t$: **vector de estado oculto**, que codifica **la historia relevante de la entrada hasta ese
  momento** (algo así como un vector de features).
- $f_1$ y $f_2$: **funciones paramétricas entrenables**; entre las dos forman una **neurona
  recurrente**.

**Configuración típica:** sigmoide y funciones lineales combinadas aditivamente:
$$h_t = \sigma\big(W_{xh}\,x_t + W_{hh}\,h_{t-1}\big)$$

### La propiedad clave
El **tamaño del grafo de cómputo** depende del largo de la secuencia, **pero el número de parámetros
no**. Al igual que en una CNN pura, el tamaño de la entrada **no afecta** el número de parámetros.
Mejor aún: al usar una capa recurrente, **el estado puede depender de entradas arbitrariamente
lejanas** sin aumentar la complejidad del modelo — *aunque aprender esas dependencias puede ser
difícil*.

### Las RNN como elementos de memoria
Las RNN **aprenden a usar el estado oculto $h_t$ como una feature** que representa lo relevante de las
entradas hasta el paso $t$ para la tarea a resolver. Esto permite capturar la **estructura
secuencial/temporal** de la entrada, **análogamente a como las convoluciones capturan la estructura
espacial** en una CNN.

## 2. Configuraciones

- La **salida** puede adecuarse a la tarea: una salida por cada valor de la secuencia, una sola al
  final, etc.
- La **cantidad de capas** también: al agregar más capas se incrementa la capacidad de abstracción.
  Las RNN multicapa requieren **pasar la secuencia completa de estados ocultos entre capas**, y **el
  costo de esto es bastante alto** comparado con una red no recurrente.
- **RNN bidireccional:** cuando el análisis se hace sobre la frase completa (p. ej. predicción de
  sentimiento) se puede capturar más información recorriendo la secuencia en ambos sentidos.

> **Regla de diseño fundamental:** *la arquitectura no debe utilizar información que estará ausente al
> predecir*. Antes de elegir bidireccional o no, hay que preguntarse **qué información estará
> disponible al momento de predecir**.

**Aplicaciones conceptualizadas en clase:** seguimiento en videos · predicción de sentimiento (con y
sin bidireccionalidad) · generación de texto.

## 3. Caso de estudio: image captioning (Karpathy y Fei-Fei Li, 2015)

*Automated Image Captioning with ConvNets and Recurrent Nets.* Combina **CNN + RNN** aprovechando las
fortalezas de cada una: la CNN codifica la imagen en un vector $V$ y la RNN genera el texto.

La modificación concreta sobre la recurrencia estándar es inyectar $V$ en el primer paso:
$$h_1 = \sigma(W_{xh}x_1 + W_{hh}h_0) \quad\longrightarrow\quad h_1 = \sigma(W_{xh}x_1 + W_{hh}h_0 + W_{ih}V)$$

## 4. Por qué necesitamos recurrencia (el argumento de cierre)

- Los **MLP** solo pueden aplicarse a problemas donde **entrada y salida tienen largo fijo**.
- Las **CNN** pueden procesar entradas de tamaño variable y producir salidas cuyas dimensiones dependen
  de la entrada, **pero no generar secuencias cuya longitud se decide durante la generación**.
- La estructura de una **RNN** permite transformar la información de una secuencia de **tamaño
  arbitrario** en un **vector de tamaño fijo**; y además la salida puede generarse **secuencialmente**,
  lo que permite salidas de **largo arbitrario**.

## 5. Entrenamiento: BPTT

Las operaciones de una RNN se descomponen en **tres bloques de parámetros**:
1. Desde la **entrada** hasta el estado oculto: $W_{xh}$
2. Desde el **estado oculto anterior** al nuevo: $W_{hh}$
3. Desde el **estado oculto a la salida**: $W_{hy}$

El entrenamiento requiere una **función de pérdida adecuada a la tarea** (cross-entropy, ranking, MSE,
etc.) y se minimiza con algún esquema basado en **SGD**. Dado que **una RNN desenrollada es un grafo
de cómputo**, para calcular los gradientes **basta aplicar backpropagation tal cual como antes**: esta
técnica se llama **backpropagation through time (BPTT)**.

Mecánica: se calcula **hacia adelante** a través de la secuencia completa para obtener la pérdida, y
luego se propaga la señal de error **hacia atrás** a través de la secuencia, **calculando y acumulando
los gradientes** — los **pesos son compartidos entre pasos** $t$. Con múltiples capas esto se complica
aún más.

### Problema 1: secuencias largas y tiempo de cómputo
Dada la estructura recursiva, el cálculo del gradiente es **excesivamente demandante en recursos**.
Una **solución burdamente simple** es **truncarlo** en cierto $t < T$ (**truncated backprop**). Así el
modelo se centra más en **dependencias cercanas** que lejanas. En la práctica funciona muy bien, **pero
solo en problemas donde las dependencias son acotadas**.

### Problema 2: exploding y vanishing gradients
- El gradiente **atraviesa un producto de Jacobianos** a lo largo de la secuencia.
- Ese producto puede **reducir o amplificar fuertemente** la señal de aprendizaje.
- **Cambiar la activación no garantiza resolver el problema.**
- **Gradient clipping limita las explosiones, pero no recupera gradientes desvanecidos.**

## 6. GRU y LSTM

**El diagnóstico conceptual:** revisando la regla de actualización de una RNN, para cada instante $t$
la memoria $h_t$ es **completamente recalculada**, quedando (casi) completamente **a merced del efecto
de $x_t$**.

> **El desafío es conservar información y aprender cuándo utilizarla.** GRU y LSTM incorporan
> **mecanismos (compuertas) que facilitan conservar y actualizar información**.

### GRU (Gated Recurrent Unit)
- Elemento principal: una **compuerta aprendible de actualización** de la memoria.
- Esa compuerta controla **cuánto se "olvida" y cuánto se agrega** a la memoria.
- Lo que se "agrega" está a su vez modulado por una **compuerta de reset**: qué cosas de la memoria son
  necesarias para actualizar el estado.

### LSTM (Long Short-Term Memory)
- Extiende la idea de compuertas, **pero son cronológicamente previas a las GRU**.
- **Separan explícitamente memoria de estado.**
- Esto les permite tener un **flujo del gradiente menos accidentado**: la memoria puede mantenerse
  entre pasos, ya que las compuertas **aprenden cuándo conservar y cuándo actualizar**.
- **Analogía explícita del curso:** *como en las conexiones residuales, una **ruta de conservación**
  facilita el entrenamiento.*

## 7. Conceptos centrales de la clase 5

- Las redes recurrentes permiten modelar **secuencias de largo arbitrario**.
- **Compartir parámetros** de manera profunda a través de conexiones recurrentes les entrega gran
  poder.
- Su **flexibilidad y versatilidad** les permite usarse en muchos dominios y **acoplarse fácilmente con
  otras redes**.
- Las **secuencias largas generan problemas en el flujo del gradiente**; GRU y LSTM permiten
  controlarlo.
- LSTM y GRU son alternativas recurrentes con **mecanismos explícitos de control de memoria**.

**Lecturas recomendadas por el profesor:**
- *Understanding LSTM Networks* — http://colah.github.io/posts/2015-08-Understanding-LSTMs/
- *Exploring LSTMs* — http://blog.echen.me/2017/05/30/exploring-lstms/
- *Visualizing memorization in RNNs* — https://distill.pub/2019/memorization-in-rnns/
- *The Unreasonable Effectiveness of Recurrent Neural Networks* —
  http://karpathy.github.io/2015/05/21/rnn-effectiveness/

---

# Parte II · Modelos de lenguaje (clase 6)

## 8. El lenguaje como codificación y decodificación

El lenguaje puede verse como un **proceso secuencial (ordenado) de codificación y decodificación
jerárquica de información**. La clase cubre dos aspectos: **cómo codificar y decodificar (generar)
lenguaje de manera simple y con muchos datos**, y **cómo mejorar este enfoque integrando codificación
y decodificación en un proceso recurrente**.

## 9. Bag of Words y sus límites

Pipeline: **creación de vocabulario** → **codificación de documentos** → **representación vectorial
con BoW**.

**Dos problemas:**
1. **No genera un espacio semántico continuo:** vectores cercanos **no son necesariamente similares
   semánticamente**.
2. **No considera el orden** de los elementos (letras, palabras, etc.).

El primer enfoque (word embeddings) ataca el **primer** problema; el segundo (seq2seq) ataca el
**segundo**.

## 10. Modelos de lenguaje neuronales y word embeddings

- Como primer paso, las palabras se representan con **codificación one-hot** en la entrada: cada
  palabra es un vector binario con un único 1 en la posición que la representa.
- **La suma de las representaciones one-hot de cada palabra de una frase equivale a la codificación
  BoW de esta.**
- Arquitectura: **producto de la matriz de embedding con cada vector one-hot** → **concatenación**
  (para generación) o **promedio** (para codificación) de los vectores resultantes → **MLP común y
  corriente**.

> Si lo que se busca es la **codificación**, al terminar el entrenamiento **el producto esencial es la
> matriz de embedding $M_\theta$**.

- La matriz de embedding entrega, para cada palabra del vocabulario, una **representación vectorial**.
- Esa representación es buena para predecir el token faltante **y además captura un espacio semántico**.
- Esto es **consecuencia directa de la función de pérdida y de los contextos observados**: palabras
  similares en sentido (o función) tienen representaciones similares.
- Técnicas más populares: **word2vec, GloVe y fastText**.

### La formulación
Los esquemas típicos usan **el contexto para predecir la palabra central**, o **la palabra central para
predecir el contexto**. Para cada palabra en la posición $t = 1,\dots,T$ se busca predecir las palabras
alrededor en una **ventana de tamaño $m$**; se plantea la **verosimilitud** y la pérdida es su
**negative log-likelihood**. La probabilidad se define con un softmax sobre el vocabulario:

$$P(w_i \mid w_c; \theta) = \frac{\exp(u_i \cdot u_c)}{\sum_{j \in V} \exp(u_j \cdot u_c)}, \qquad u_k = M_\theta \cdot \text{onehot}_k$$

### Qué captura el espacio de embeddings
- Genera **"vecindades semánticas"**: palabras conceptualmente similares quedan cercanas.
- Captura **relaciones a través de operaciones vectoriales** (la aritmética de analogías).
- Ejemplo práctico usado en clase: Embedding Projector — https://projector.tensorflow.org/
- Aplicaciones en sistemas urbanos citadas: *Additive Compositionality in Urban Area Embeddings Based
  on Human Mobility Patterns* · *A framework for extracting urban functional regions based on
  multiprototype word embeddings using points-of-interest data*.

### El límite
Al **no considerar explícitamente la información secuencial**, la matriz de embedding genera
codificaciones **para palabras, pero no para frases** de manera directa. Para codificar una frase se
requiere un paso extra (sumar o promediar), **lo que descarta la información secuencial**.

## 11. Encoder-decoder y seq2seq

- Para capturar más información contextual, los modelos **encoder-decoder** usan redes neuronales para
  **codificar la entrada** y luego **decodificar la salida**.
- Si se usan **redes recurrentes para ambas partes**, hablamos de un modelo **seq2seq**:
  - Un **encoder recurrente** procesa la secuencia de entrada y genera una **representación vectorial
    (estado oculto)** que captura la información relevante.
  - Un **decoder recurrente** usa esa representación para generar una secuencia de salida adecuada.
- Ambas redes se entrenan **de manera conjunta**.
- **El esquema es completamente general**, lo que lo hace aplicable a **cualquier tipo de secuencia**.

### Por qué tiene sentido
- Al usar una **representación latente intermedia**, las secuencias de entrada y salida pueden tener
  **largos distintos**.
- Esa representación **codifica la información relevante** de la entrada.
- Al usar secuencias, **considera el orden de las palabras**, a diferencia de BoW o de un promedio de
  vectores.

### La configuración más simple
Un encoder que genera **un único vector contextual $C$**, que es típicamente **el último estado oculto
del encoder** luego de procesar la secuencia. La entrada no son las palabras en sí ni su one-hot/BoW,
sino **los embeddings de cada una**.

> El esquema es **muy similar al generador de captions**: la diferencia es que allí el codificador es
> una **CNN**. Se puede ver ese sistema como **un traductor del "lenguaje" visual al escrito**.

### Ejemplo real: traducción automática (Sutskever et al., 2014)
- Basado en encoder-decoder; **ambos implementados con LSTM de 4 capas**.
- El **vector de contexto** entregado al decoder es el **último estado oculto del encoder**.
- Para terminar una secuencia se usa el símbolo especial **`<EOS>`**.
- Durante el **entrenamiento**, los valores reales de la traducción se usan como entrada al decoder:
  **teacher forcing**. En **inferencia** se usan los **outputs del paso anterior**.
- Al graficar en 2D (**PCA**) el vector de contexto para distintas frases, se ve que **captura
  información semántica y es sensible al orden de las palabras**.

### Las tres limitaciones de seq2seq
1. **Exposure bias.** En entrenamiento el decoder recibe el token correcto, pero en inferencia usa sus
   propias predicciones. Esa diferencia genera exposure bias y **los errores pueden acumularse porque
   el modelo no aprendió a recuperarse**. **Scheduled sampling** lo enfrenta mezclando tokens
   correctos y predicciones durante el entrenamiento.
2. **Estrategia de decodificación.** **Greedy search** (elegir siempre la palabra más probable) frente
   a **beam search** (explorar varias secuencias en paralelo). Trade-off: **calidad vs. costo
   computacional**.
3. **Tamaño del vector de contexto.** Toda la entrada **se comprime en un único vector $C$**; el
   decoder recibe únicamente ese vector, y **su dimensión no cambia al crecer la secuencia**, lo que
   genera efectos importantes en secuencias largas.

> Esta tercera limitación, junto con **el procesamiento secuencial de la entrada**, fueron los
> **principales puntos de mejora introducidos por la arquitectura Transformer**.

## 12. Conceptos centrales de la clase 6

- **Word embeddings** capturan **similitud semántica de palabras individuales**.
- **seq2seq** (encoder-decoder con RNN) permite transformar secuencias en otras secuencias de
  **longitud distinta**.
- El **vector de contexto** actúa como un **"resumen comprimido"** de la entrada.
- Las **limitaciones prácticas** de seq2seq derivaron en la creación del **Transformer**.

---

# Parte III · Transformers (clase 7)

## 13. Dos perspectivas

Más allá de los detalles arquitectónicos, el curso propone mirar los Transformers desde dos ángulos:
1. **El qué**, que es en realidad bien tradicional en el contexto de DL.
2. **El cómo**, mucho más interesante y conceptualmente enriquecedor.

> Quizá lo más llamativo al verlo de esta forma es que queda claro que, **al momento de su aparición,
> nadie sabía lo que iba a ocurrir**.

## 14. El origen: atención sobre seq2seq

**La reflexión inicial:** *¿tiene sentido pasar un único mensaje estático entre encoder y decoder?*

- Los modelos seq2seq dependen completamente de que el contexto esté bien representado en $C$, ya que
  **es la única conexión** entre encoder y decoder.
- Más aún, **asumen que todos los pasos pueden basarse en el mismo contexto**. El problema es que un
  **contexto fijo le da una importancia fija a cada parte de la entrada**.

**La solución: contextos adaptativos.** Un **mecanismo de atención** es esencialmente **una nueva capa
que pondera, en cada paso, la relevancia de cada estado del encoder** y, por consiguiente, de la
secuencia de entrada. Esto **reduce la carga de conocimiento que debe almacenar el vector $C$** y lo
**especializa de acuerdo con el paso particular** del proceso.

El **mapa de atención** muestra gráficamente el proceso. Ejemplo citado: **image captioning
revisitado** (Xu et al., 2015), donde se ve a qué región de la imagen atiende el modelo al generar
cada palabra.

## 15. El "qué": por qué nace el Transformer

Los modelos **seq2seq con atención acarrean muchos de los problemas de las RNN**. Aplicarlos a
conjuntos de datos masivos es complejo debido a:
- **Baja eficiencia computacional** dada por la **restricción secuencial** de las RNN.
- **Problemas de predicción con secuencias muy largas.**

> En resumen, **subutilizan la infraestructura computacional existente**. *(¿Quién podría estar
> especialmente interesado en resolver esto? — Google.)*

**La arquitectura Transformer:**
- **Completamente basada en atención** (distinta de la atención recién vista, pero con la misma idea
  subyacente).
- **Su gran aporte fue poder realizar el cómputo en paralelo** (no hay recurrencia alguna), permitiendo
  su **potencial escalamiento a enormes volúmenes de datos**.
- Sigue formado por encoders y decoders, pero **estos no son recurrentes**: son **combinaciones de
  auto-atención y capas densas**.

## 16. El "cómo": por qué funciona en texto

- Desde el inicio, el foco del Transformer fueron las **tareas relacionadas al texto**, como la
  traducción, donde rápidamente demostró **rendimiento superior en un contexto supervisado**.
- ¿Qué características del texto explota esta arquitectura?
  - **Las dependencias pueden ser extremadamente largas.** Ejemplo del curso: *"Crecí en Francia, donde
    pasé la mayor parte de los veranos. Hablo de manera fluida el _____"*. **La atención de los modelos
    seq2seq no logra esto, al estar limitada por la recurrencia.**
  - **La atención debe fijarse en múltiples elementos, con distinta fuerza.**
  - Y, *si algo nos ha enseñado DL durante estos años, es que **tener múltiples capas ayuda***.

## 17. Auto-atención

- La atención en Transformers **no es igual** a la de un modelo seq2seq. Aquí se usa **auto-atención**,
  que indica **para cada elemento de una secuencia su dependencia con otros elementos de la misma**.
- A partir de esa atención **se genera un nuevo embedding para cada elemento** de la secuencia.

**La analogía del curso:** la auto-atención es parecida a **un diccionario en Python (memoria
asociativa)**: dada una **consulta**, buscamos la **llave** que coincida con ella y retornamos el
**valor** almacenado. En la práctica, a cada vector de entrada se le aplican **tres operadores de
transformación: Query, Key y Value**, que se combinan para generar el embedding de cada elemento en
cada capa.

**Multi-head:** la auto-atención puede ser **multifocal** — muchas atenciones distintas, **análogo a la
existencia de múltiples filtros por capa en una CNN** — porque **pueden existir múltiples tipos de
dependencia entre tokens**.

## 18. Los detalles que completan la arquitectura

- **¿Qué pasa con el orden de las secuencias?** Como no hay recurrencia, el orden **se incluye a través
  de un embedding posicional/temporal**.
- **Conexiones residuales y normalización** dentro de cada bloque.
- **Conexiones con el decoder** (cross-attention entre encoder y decoder).
- **Máscara causal.** En el entrenamiento el decoder **procesa todas las posiciones a la vez para ser
  eficiente**. Si esto se hace sin control, **la atención puede tomar información de tokens que
  deberían generarse a futuro**. Para evitarlo se aplica una **máscara causal antes de calcular el
  softmax** de la atención.

Referencia visual del curso: *The Illustrated Transformer* —
https://jalammar.github.io/illustrated-transformer/

## 19. Del Transformer a los modelos fundacionales

- Si bien la arquitectura fue muy novedosa, **su proceso de entrenamiento es tradicional**: se entrena
  con una tarea **supervisada** (traducción) y luego se hace **fine-tuning** para llevar el
  conocimiento a otras tareas.
- **Esto es problemático:** los **datos rotulados no son suficientes** para sacarle todo el provecho.
  Dicho de otra manera, **la arquitectura es tan general y efectiva que, hacia 2016, la limitante para
  escalar su rendimiento venía desde los datos**.
- **2021:** un amplio grupo de investigadores de **Stanford** crea el **Centro de Investigación de
  Modelos Fundacionales**, acompañado de un paper muy extenso donde se discuten estos modelos.
- **El aprendizaje supervisado no es suficiente** para modelos de esta capacidad → el **aprendizaje
  autosupervisado** permite aprovechar **datos sin etiqueta a gran escala**. **BERT** fue uno de los
  primeros en capitalizar sobre esta idea.
- **Un ingrediente importante para el éxito es el alineamiento.**
- Extensiones arquitectónicas mencionadas: **posición y eficiencia**.

## 20. Conceptos finales sobre los Transformers

- **Arquitectura neuronal general de alta capacidad.**
- **Al inicio, nadie sabía en qué se iba a convertir.**
- El **sesgo inductivo de la atención** permite **integrar información de distintas posiciones**.
- Es la **arquitectura base en los modelos fundacionales actuales**.
