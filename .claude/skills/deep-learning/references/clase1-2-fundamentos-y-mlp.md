# Clases 1-2 · Fundamentos y arquitecturas neuronales básicas

## 1. De la IA tradicional al aprendizaje de representaciones

- **≈1990:** explosión digital, empezamos a usar computadores en vez de papel para guardar datos.
- **IA tradicional:** buscaba máquinas tan inteligentes como un humano **en todo**.
- **Machine Learning:** máquinas **especializadas** que aprenden **inductivamente**, y pueden **superar
  a los humanos** en la(s) tarea(s) asignada(s).

### El esquema común a todos los sistemas de ML
Cuatro piezas que interactúan:

| Pieza | Qué aporta |
|---|---|
| **Modelo predictivo** | Espacio de hipótesis + sesgo inductivo |
| **Datos de entrenamiento** | Los datos y sus etiquetas |
| **Función de pérdida** | Cuantifica el error del modelo en los datos |
| **Técnica de búsqueda** | Recorre el espacio de hipótesis |

$$\arg\min_W \; J(X,Y;W) \;=\; \lambda\,\mathcal{R}(W) \;+\; \sum_{i}^{N} \mathcal{L}\big(f(x_i;W),\,y_i\big)$$

- **Etiqueta:** el valor a predecir (define la tarea).
- **Parámetros** $W$: viven en el espacio de hipótesis del modelo.
- **Regularizador** $\mathcal{R}(W)$: función que induce sesgo inductivo **a través de los parámetros**.
- El conjunto es un **problema de optimización**: una búsqueda sobre el espacio de hipótesis.

### El problema de las features diseñadas a mano
En muchos pipelines tradicionales la **representación se diseña por separado** y el modelo aprende
principalmente la **regla de predicción**. Esas *handcrafted features* / *feature engineering* tienen
que ver con el conocimiento experto que tengamos (o no) del problema. No es ideal por tres motivos:

1. **Un experto es caro** y nada asegura que su conocimiento sea óptimo.
2. Para **datos no estructurados** no son evidentes las mejores características ni las
   especificaciones de modelo.
3. No siempre es evidente **cómo combinar distintos tipos de datos** para extraer información, ni qué
   relaciones hay entre ellos.

> La clave para enfrentar esto es pensar las **features y el modelo predictivo como un modelo/problema
> conjunto**. Buscamos mecanismos de aprendizaje suficientemente **poderosos y generales**, que
> permitan capturar aspectos complejos y eventualmente desconocidos (para nosotros) de los datos.

## 2. La neurona y el modelo de una capa

Una **unidad neuronal** aplica una **transformación lineal** y, cuando corresponde, una **activación**.

El problema de aprendizaje, dada la estructura de una red: *¿cómo ajustar los parámetros de las
neuronas (nodos, unidades) para que al ingresar un vector de entrada obtengamos la salida deseada?*
(Ejemplo del curso: cuando la red recibe la imagen de un 4, su codificación de salida debe indicar 4.)

**Modelo de una capa.** Queremos aproximar el mapeo $g(x) = y$. Con suficientes pares $(x_i, y_i)$
muestreados de ese mapeo podemos construir una función que mida cuán buena es la estimación. Sea

$$f(x;w) \;=\; \sigma\!\left(\sum_{i=1}^{m} w^{(i)} x^{(i)}\right) \;=\; \sigma(w \cdot x)$$

Buscamos que $g(x) \approx f(x;w)$. Una posible función de pérdida (o costo, o error):

$$J(w) \;=\; \frac{1}{n}\sum_{i=1}^{n}\big(f(x_i;w) - y_i\big)^2$$

**Propiedad clave:** en modelos de **una capa** con una pérdida apropiada (casi todas), el objetivo es
**convexo** respecto de los parámetros, y en esos casos el **descenso de gradiente puede alcanzar un
óptimo global** bajo condiciones adecuadas.

**Límite:** un modelo de una capa representa **funciones afines o fronteras de decisión lineales**.

## 3. El MLP

Al agregar una **capa oculta** se capturan **features intermedias** entre entrada y salida, que
permiten separar más fácilmente los datos. Esas representaciones **se aprenden junto con la tarea**.

Un **Multilayer Perceptron (MLP)** combina transformaciones afines y activaciones no lineales en
múltiples capas. También se conoce como **red feedforward profunda** o **Deep Feed Forward Network
(DFF)**.

**Sin glamour, un MLP es una composición de funciones:**

| Profundidad | Función |
|---|---|
| Modelo de 1 capa | $f = \sigma(W_1 x)$ |
| MLP de 2 capas | $f = \sigma(W_2\,\sigma(W_1 x))$ |
| MLP de 3 capas | $f = \sigma(W_3\,\sigma(W_2\,\sigma(W_1 x)))$ |

con $\sigma(z)$ la función de activación. **Nuevas capas aumentan el poder discriminativo** y amplían
la clase de funciones representables.

### Teorema de aproximación universal
- Bajo determinadas condiciones, una red con **una capa oculta suficientemente ancha** puede aproximar
  funciones continuas sobre dominios compactos con **precisión arbitraria**.
- **El resultado NO garantiza** que esa red sea fácil de entrenar, eficiente en parámetros, ni capaz de
  generalizar con pocos datos.
- La "mostración" vista en clase construye la aproximación con escalones: se aumenta $w$ (1 → 10 →
  100) para que la sigmoide se aproxime a un escalón, se desplaza con $b$ ($b = 100, 0, -100$), y se
  **restan** pares de escalones para formar "torres" que aproximan la función por tramos.
- Resumen: siempre es posible construir un MLP que estime una función continua con precisión
  arbitraria con esta metodología, pero **la cantidad de neuronas por capa depende del problema** y
  puede ser potencialmente muy grande. La metodología **no es práctica** y es **distinta de entrenar**
  un MLP, pero da una idea de una **cota superior** para su tamaño.

## 4. Clasificación de imágenes con MLP: MNIST y Fashion-MNIST

### MNIST
- Imágenes de **dígitos escritos a mano** en escala de grises.
- Cada imagen muestra un dígito entre 0 y 9, resolución **28×28 = 784 píxeles**.
- **60.000** ejemplos de entrenamiento y **10.000** de prueba.

### De las salidas a una pérdida
Para construir una función de pérdida adecuada, el primer paso es que las salidas del MLP sean las
**probabilidades** de que la entrada $x$ corresponda a cada una de las $K = 10$ categorías,
$P(Y = k \mid X = x)$. Esto se logra con la activación **softmax** después de la capa de salida.

Como pérdida se usa **Cross Entropy** (entropía cruzada), que **penaliza adecuadamente las
probabilidades incorrectamente asignadas**.

Se monitorean dos curvas: **Loss** y **Accuracy**.

### Fashion-MNIST
- Sucesor de MNIST con **mayor dificultad** (pero tampoco tanto más).
- Cada imagen muestra **una prenda** de una de diez categorías, escala de grises, **28×28**.
- **60.000** de entrenamiento y **10.000** de test.

**Resultado:** un MLP idéntico al de MNIST rinde notoriamente peor. *Quizá los MLP no andan bien con
imágenes y aprenden patrones que no son muy generales* — la explicación completa llega en la clase de
CNN (ver `clase3-cnn.md`).

## 5. MLP sobre datos tabulados

Las **filas de una tabla** pueden verse de manera natural como los vectores de entrada, así que
parecería el dominio natural del MLP. **Pero tampoco le va muy bien.** Dos problemas principales:

### Problema 1: heterogeneidad de tipos y escalas
- Los datos tabulares combinan variables **numéricas y categóricas** con unidades, escalas y
  cardinalidades distintas.
- Pueden contener **valores faltantes** y **categorías raras**.
- Estas diferencias requieren **representaciones y preprocesamiento explícitos**.

### Problema 2: distribución y correlación
- Las columnas presentan generalmente **alta correlación**, por lo que basta un **subconjunto pequeño**
  de variables para predecir.
- Hay habitualmente **alto desbalance** en las clases a predecir.
- Todo esto es **campo fértil para el sobreajuste**.

### La relación con el teorema de aproximación universal
> Los MLP **no tienen restricción** en lo que pueden aprender, por lo que les sale **más fácil usar
> correlaciones entre el ruido en los datos y la etiqueta**. Gran parte del arte de Deep Learning es
> utilizar arquitecturas que **sesguen** el aprendizaje de la red en base a la **estructura de los
> datos**, de modo que aprendan representaciones útiles.

## 6. Embeddings categóricos (solución al problema 1)

El primer problema se relaciona con la **incapacidad de los MLP de trabajar con datos que no sean
numéricos (continuos) y bien distribuidos**. Los datos categóricos son el ejemplo típico.

**En vez de adaptar los MLP para que funcionen con datos categóricos, se aprenden transformaciones que
muevan los datos categóricos a un espacio numérico.** Esa transformación es un **embedding**, y es
*"de los aspectos más importantes y generales de Deep Learning"*.

### Qué es un embedding
- Asigna **cada elemento discreto a un vector continuo** que **se aprende para una tarea**.
- La **cercanía entre vectores** puede capturar **similitudes útiles** para el predictor.
- **No necesariamente reduce dimensionalidad**: su dimensión la define previamente el experto.

### Cómo se implementa
**One-hot × matriz equivale a seleccionar una fila** de la matriz de embeddings. La **matriz de
embeddings se entrena junto con el predictor**: embeddings y MLP se entrenan **conjuntamente**.

En datos tabulados los embeddings categóricos actúan **solamente al inicio del procesamiento**; luego
se concatenan con las variables numéricas y todo entra al MLP.

### Caso histórico: Entity Embeddings (Guo y Berkhahn, 2016)
*Entity Embeddings of Categorical Variables.*
- Objetivo: predecir **ventas diarias** de cada tienda de la cadena **Rossmann**.
- **2,5 años** de datos para **1.115 tiendas**.
- **1.017.210 registros**, divididos en **90 % entrenamiento / 10 % test**.
- **No se utilizó feature engineering.**
- Compara redes neuronales con embeddings categóricos frente a **XGBoost, Random Forest y KNN**.

## 7. Dropout (mitigación del problema 2)

- La observación principal: **haga lo que se haga, las capas densas de un MLP son altamente propensas
  a sobreajustarse**.
- Dropout **"apaga" aleatoriamente neuronas** en esas capas **durante el entrenamiento**, con una
  probabilidad previamente definida (p. ej. **0,5**).
- **Efecto neto:** las neuronas **no pueden "confiar" en las otras**, por lo que aprenden
  representaciones **más robustas**.
- **Dropout puede mejorar la generalización.**

Más detalle (incluida la regla de inferencia y la perspectiva desde las superficies de optimización)
en `clase4-entrenamiento.md`.

### Lo que embeddings y dropout NO resuelven
Los problemas de **alta correlación entre variables** y **alto desbalance de clases** son
**transversales a todas las técnicas de Deep Learning**. Las técnicas para enfrentarlos se cubren en
otros capítulos, al revisar los modelos donde fueron originalmente aplicadas; aunque hayan sido
propuestas en otro contexto, siguen siendo aplicables a datos tabulados. Dos ejemplos citados:
- **TabNet: Attentive Interpretable Tabular Learning** — https://arxiv.org/pdf/1908.07442.pdf
- **Neural Oblivious Decision Ensembles for Deep Learning on Tabular Data** —
  https://arxiv.org/abs/1909.06312

## 8. Conceptos centrales de estas dos clases

- El ML moderno se centra en el **aprendizaje de representaciones**.
- La fortaleza de DL es el aprendizaje de **features jerárquicas composicionales**.
- El proceso requiere **grandes cantidades de datos y cómputo**.
- Los **MLP** presentan teóricamente un esquema **altamente poderoso** para reconocer patrones, pero
  su uso es **complejo debido a su rápido sobreajuste**.
- Para **datos tabulados**, restringir el dominio mediante **embeddings** y usar **dropout** alivia
  gran parte de los problemas.
