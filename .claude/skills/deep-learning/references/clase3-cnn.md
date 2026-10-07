# Clase 3 · Redes Neuronales Convolucionales (CNN)

## 1. Por qué los MLP fracasan con imágenes

Los MLP **fracasan catastróficamente** en conjuntos de datos visuales más desafiantes que MNIST. Por
ejemplo, Fashion-MNIST presenta **mayor variación intraclase**, en parte dada por un **posicionamiento
no constante** de los patrones visuales principales.

### El argumento de los parámetros
Imagen de **640×480 a colores**, **128 neuronas** en la primera capa:

$$640 \times 480 \times 3 \times 128 \;\approx\; 120\,\text{millones de parámetros solo en la primera capa}$$

### El argumento estructural (el más importante)
- **Cada neurona ve todo simultáneamente**, lo que genera una cantidad excesiva de parámetros.
- **No hay equivarianza** respecto de la posición de los elementos visuales: un patrón aprendido en una
  posición no se reconoce en otra.

## 2. La inspiración biológica: Hubel y Wiesel

Hubel y Wiesel (**década de 1960**) investigaron los patrones de estímulo visual en mamíferos y
mostraron que:
- Los patrones básicos de estímulo visual son detectados por **células (neuronas) específicas,
  altamente localizadas**.
- Las neuronas responden a **patrones locales** y se organizan de manera **jerárquica**, aumentando
  progresivamente el nivel de abstracción de los patrones detectados.

> La evidencia biológica **valida el esquema de construcción** de las CNN, aunque las CNN **no son un
> modelo de la corteza visual**.

## 3. Qué debe incluir una red que procese datos visuales

La respuesta se construye en clase en tres pasos:
1. **Representación composicional jerárquica**
2. **Profundidad**
3. **Detección de patrones / embeddings locales, equivariantes a la ubicación**

### Cómo capturarlo
- **Neuronas locales con parámetros compartidos** que cubran la entrada (**ventana deslizante**).
- Proveen una **reducción significativa** en el número de parámetros (que **no depende de la
  conectividad** con toda la entrada).
- Dado su tamaño, permiten **capturar patrones locales en cualquier posición**.
- Como la **salida de esta operación es también una imagen**, no hay problema en apilar **múltiples
  capas secuenciales** que operen de la misma manera.

## 4. La convolución

- Modela neuronas como **filtros locales** aplicados en toda la imagen, **de manera independiente en
  cada posición**.
- Intuitivamente, **miden cuánto se parece el filtro al sector de la imagen** sobre el cual se aplica.
- La salida de una neurona convolucional entrega un **mapa** (antes era un número), que indica **dónde
  se podría encontrar el patrón** capturado por la neurona.

### Qué resuelve realmente una convolución
- **Reduce drásticamente la cantidad de parámetros.**
- **Obliga a buscar patrones locales.**
- **Permite detectar el mismo patrón en muchas posiciones.**
- A diferencia de un MLP, **no rompe la estructura espacial** de las imágenes, al trabajar sobre ellas
  **sin aplanarlas**.

### Comparación numérica hecha en clase
- Imagen de **32×32**, capa **fully connected** de **10 neuronas con bias** → **10.250 parámetros**.
- *"La situación es en realidad aún peor para los MLP"*: con una imagen algo más grande (p. ej.
  **256×256**), el número de parámetros de la **primera capa convolucional no cambiaría**, pero la de
  un MLP **se elevaría por sobre el medio millón**.

## 5. La arquitectura CNN

- Están formadas (generalmente) por capas **convolucionales**, de **pooling** y **fully connected**.
- **Disminuyen drásticamente el número de parámetros** en comparación con los MLP.
- Son **menos propensas al sobreajuste**, gracias a su **sesgo inductivo**.

**Herramientas de visualización usadas en clase:**
- CNN Explainer — https://poloclub.github.io/cnn-explainer/
- Visualización 3D de Adam Harley — https://adamharley.com/nn_vis/
- Diagramas de Andrej Karpathy (CS231n)

## 6. Caso de estudio: AlexNet (Krizhevsky, Sutskever y Hinton, NeurIPS 2012)

*ImageNet Classification with Deep Convolutional Neural Networks.*

AlexNet fue **uno de los primeros ejemplos exitosos de ConvNets**. Además de usar convoluciones,
introdujo una serie de **"trucos" muy útiles** para el entrenamiento. **El gran diferenciador fue ser
capaz de aprender efectivamente de un set de datos órdenes de magnitud mayor** que los existentes.

### ImageNet: la primera base de datos visual práctica de gran escala
- Más de **15M de imágenes** divididas en **22K categorías**.
- Las imágenes están relacionadas por una **estructura de grafo** que captura relaciones entre ellas.
- Recolectadas de la web y rotuladas usando **Amazon Mechanical Turk**.

**ILSVRC-XXXX** (el subconjunto usado para entrenar AlexNet, donde XXXX es el año):
- **1K categorías**, **1,2M imágenes** de entrenamiento (≈1,2K por categoría).
- **50K** imágenes de validación y **150K** de test.
- Imágenes RGB de distintas resoluciones, **escaladas a 256×256**.
- Métricas de error **top-1** y **top-5**.

### Tamaño y cómputo
Entrenada con **SGD** en **dos Nvidia GTX 580 con 3 GB de VRAM** durante **una semana**:
- ≈ **650K neuronas**
- ≈ **60M de parámetros**
- ≈ **630M de conexiones**

### Los tres "trucos"
1. **ReLU.** Uno de los primeros trabajos en cambiar las no linealidades clásicas por ReLU, lo que
   permitió que el entrenamiento fuera **varias veces más rápido**.
2. **Dropout** (introducido en 2012), aplicado a las **capas densas** del final, que son igualmente
   propensas a sobreajustarse. Apaga aleatoriamente neuronas durante el entrenamiento; el efecto neto
   es que las neuronas no pueden "confiar" en las otras y aprenden representaciones más robustas.
3. **Aumento de datos.** Si bien el set es grande, **el tamaño de la red obliga a aumentarlo aún más**:
   - Por cada imagen se tomaron **5 subimágenes de 224×224** (4 esquinas y el centro).
   - El proceso se repite para el **reflejo** de cada imagen.
   - Con esto se aumentó **10 veces** el tamaño efectivo del dataset.
   - Finalmente, a cada imagen se le **resta la media de cada canal de color**.

> **El aumento de datos puede verse como otra forma de controlar la complejidad de una red.**

### Resultados
| Métrica | Valor |
|---|---|
| Error **top-5** | **15,3 %** |
| Error **top-1** | **26,2 %** |
| Error **humano** | aprox. **8 %** |

### El estado del arte después
En la actualidad las arquitecturas para reconocimiento visual son bastante **más profundas (cientos de
capas)**. Los mejores métodos tienen alrededor de **89 % top-1** y **99 % top-5**. Referencia:
https://paperswithcode.com/sota/image-classification-on-imagenet

## 7. Conceptos centrales de la clase

- Las redes convolucionales (en 2012) permitieron **resolver los problemas que tenían los MLP** gracias
  al uso de convoluciones (y otros detalles más).
- El aspecto central de las CNN es el **aprendizaje de features locales en un esquema composicional
  jerárquico profundo**.
- Si bien **no son un modelo de la corteza visual**, la evidencia biológica **valida** su esquema de
  construcción.
- Su **simplicidad y buenos resultados** las llevaron a ser las redes más utilizadas durante bastante
  tiempo.

## 8. Nota sobre lo que no quedó en el texto de las láminas

Buena parte de la clase 3 son **diagramas sin texto extraíble** (mecánica de la convolución paso a
paso, stride, padding, pooling, el cálculo del tamaño de salida y los diagramas de Karpathy). Si una
pregunta depende de esos detalles numéricos, conviene abrir directamente
`DeepLearning/03 - Redes Neuronales Convolucionales.pdf`. Las fórmulas estándar que el curso usa y que
no aparecen transcritas en las láminas son:

- **Tamaño de salida de una convolución:** $O = \left\lfloor \dfrac{I - K + 2P}{S} \right\rfloor + 1$,
  con $I$ el tamaño de entrada, $K$ el del kernel, $P$ el padding y $S$ el stride.
- **Parámetros de una capa convolucional:** $(K_h \cdot K_w \cdot C_{in} + 1) \cdot C_{out}$ contando
  el bias.
- **Campo receptivo:** con stride 1, cada convolución de $3\times 3$ adicional lo expande en 2 píxeles
  por lado ($3 \to 5 \to 7$). Este punto sí está desarrollado en los ejercicios resueltos, ver
  `ejercicios-resueltos.md` §1.4.
