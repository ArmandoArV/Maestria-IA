# Ejercicios resueltos del curso

Fuente: `DeepLearning/SolucionEjercicios/solucion-ejercicios-dl.tex` (y su PDF), autoría de Armando
Arredondo Valle, septiembre de 2026. Está escrito en el **estilo LaTeX de la casa** (portada tikz
azul/dorado UC, `titlesec`, `fancyhdr`), con un entorno `enunciado` que separa la pregunta de la
respuesta.

Estos ejercicios son la mejor señal disponible sobre **el tipo de pregunta que el curso evalúa**: no
piden calcular, piden **razonar sobre supuestos arquitectónicos y sus consecuencias**. Tres bloques:
preguntas de teoría, diseño de arquitecturas y un caso extendido de detección de anomalías.

---

## 1. Preguntas de teoría

### 1.1 Invarianza al reescalado y regularización L2
**Enunciado.** Red sin sesgos $f(\mathbf{x}) = W_2\,\mathrm{ReLU}(W_1\mathbf{x})$. Para $\alpha > 0$ se
reemplaza $W_1$ por $\alpha W_1$ y $W_2$ por $W_2/\alpha$. ¿Cambian las predicciones? ¿Cambia el efecto
de una regularización L2 sobre ambas matrices?

**Las predicciones no cambian.** La ReLU es **positivamente homogénea**:
$\mathrm{ReLU}(\alpha z) = \alpha\,\mathrm{ReLU}(z)$ para todo $\alpha > 0$, porque multiplicar por una
constante positiva no altera el signo de $z$. Entonces
$$\frac{W_2}{\alpha}\,\mathrm{ReLU}(\alpha W_1\mathbf{x}) = \frac{W_2}{\alpha}\,\alpha\,\mathrm{ReLU}(W_1\mathbf{x}) = f(\mathbf{x}).$$

**El efecto de L2 sí cambia.** La penalización pasa de $\|W_1\|_F^2 + \|W_2\|_F^2$ a
$\alpha^2\|W_1\|_F^2 + \alpha^{-2}\|W_2\|_F^2$, que **depende de $\alpha$ aunque la función
representada sea idéntica**. Entre infinitas redes que calculan la misma función, **L2 prefiere la
configuración de normas balanceadas**.

> **La lección:** **L2 penaliza los parámetros, no directamente la función que la red computa.**

**El $\alpha$ óptimo.** Con $a = \|W_1\|_F^2$, $b = \|W_2\|_F^2$ y $g(\alpha) = \alpha^2 a + b/\alpha^2$:
$$g'(\alpha) = 2\alpha a - \frac{2b}{\alpha^3} = 0 \;\Longrightarrow\; \alpha^4 = \frac{b}{a} \;\Longrightarrow\; \alpha^\star = \left(\frac{b}{a}\right)^{1/4} = \sqrt{\frac{\|W_2\|_F}{\|W_1\|_F}}$$
Es un mínimo porque $g''(\alpha) = 2a + 6b/\alpha^4 > 0$. Sustituyendo,
$\|\alpha^\star W_1\|_F^2 = \|W_2/\alpha^\star\|_F^2 = \sqrt{ab}$: **ambas capas quedan con igual
norma**, y la penalización mínima vale $2\|W_1\|_F\|W_2\|_F$. Sin cálculo diferencial, la desigualdad
aritmético-geométrica da lo mismo: $\alpha^2 a + b/\alpha^2 \ge 2\sqrt{ab}$, con igualdad si y solo si
$\alpha^2 a = b/\alpha^2$.

### 1.2 Permutación aleatoria de píxeles: CNN vs. MLP
**Enunciado.** Todas las imágenes se transforman con la **misma** permutación aleatoria de píxeles,
aplicada en entrenamiento y evaluación. ¿Qué modelo se ve más afectado?

**La CNN se ve más afectada; el MLP no se ve afectado.**

- **MLP:** trata la entrada como un **vector plano sin estructura**; no incorpora ningún supuesto sobre
  el orden de las componentes. Permutar los píxeles equivale a **permutar las columnas de la matriz de
  pesos de la primera capa**, de modo que para cada solución del problema original existe una solución
  **exactamente equivalente** en el problema permutado. Su clase de hipótesis es **invariante al
  reordenamiento** de la entrada.
- **CNN:** incorpora dos sesgos inductivos sobre la estructura espacial — **localidad** (los píxeles
  cercanos están correlacionados y forman patrones locales capturables con filtros pequeños) y
  **equivarianza a la traslación** (un mismo patrón puede aparecer en cualquier posición, lo que
  justifica compartir los pesos del filtro, junto con el pooling). **Una permutación destruye
  precisamente esa estructura.**

> **La lección:** la información **sigue presente** (no se pierde nada), pero **la arquitectura ya no
> puede explotarla**. La CNN pierde justamente la ventaja que la hace superior en imágenes naturales.

### 1.3 Dropout y valor esperado de la predicción
**Enunciado.** En la formulación original de Dropout, en inferencia se multiplican las activaciones por
$1-p$ para conservar el valor esperado del entrenamiento. ¿Por qué igualar la esperanza de las
activaciones intermedias **no** implica igualar la esperanza de la predicción final?

El escalamiento por $1-p$ garantiza la igualdad **a la entrada de cada capa**: si
$m \sim \mathrm{Bernoulli}(1-p)$, entonces $\mathbb{E}[m \cdot a] = (1-p)\,a$. Pero esa activación pasa
luego por **transformaciones no lineales** $g$ (ReLU, sigmoide, softmax), y **la esperanza no conmuta
con una función no lineal**:
$$\mathbb{E}[g(z)] \neq g(\mathbb{E}[z])$$
(Para funciones convexas o cóncavas, la **desigualdad de Jensen** indica incluso la dirección del
sesgo.)

Durante el entrenamiento la predicción es una variable aleatoria $f(\mathbf{x}, m)$ y lo que se
quisiera reproducir en inferencia es **el promedio del ensamble** $\mathbb{E}_m[f(\mathbf{x}, m)]$,
tomado sobre **exponencialmente muchas subredes**. La regla de escalar introduce la esperanza
**dentro** de las no linealidades, capa por capa; en cada capa se comete un error de aproximación que
además **se propaga y se compone** a través de la red.

> **La lección:** la regla de inferencia de Dropout es **solo una aproximación** al verdadero promedio
> del ensamble, exacta únicamente si la red fuera lineal.

### 1.4 Una convolución de 7×7 vs. tres de 3×3
**Enunciado.** CNN con $C$ canales en todas las capas, stride 1, sin sesgo. Comparar una convolución
de $7\times7$ con tres de $3\times3$: campo receptivo, parámetros y capacidad no lineal.

| Criterio | Una conv. $7\times7$ | Tres conv. $3\times3$ |
|---|---|---|
| Campo receptivo | $7\times7$ | $7\times7$ |
| Parámetros | $7\cdot7\cdot C\cdot C = 49C^2$ | $3\cdot(3\cdot3\cdot C\cdot C) = 27C^2$ |
| No linealidades | 1 | 3 |

- **Campo receptivo: idéntico.** Con stride 1, cada $3\times3$ adicional expande el campo receptivo en
  **2 píxeles por lado**: $3 \to 5 \to 7$.
- **Parámetros:** $27C^2$ frente a $49C^2$, una **reducción cercana al 45 %**, con el consiguiente
  ahorro de memoria y cómputo y **menor riesgo de sobreajuste**.
- **Capacidad no lineal:** si entre las convoluciones se intercalan ReLU, la secuencia **compone tres
  transformaciones no lineales** sobre el mismo campo receptivo. **Sin activaciones intermedias, las
  tres $3\times3$ colapsarían en una única transformación lineal** equivalente a una $7\times7$ (de
  rango restringido): la ventaja expresiva **depende de las no linealidades**.

> **Conclusión:** apilar convoluciones de $3\times3$ **domina en ambos ejes**. Este es el principio de
> diseño introducido por **VGG**.

---

## 2. Diseño de arquitecturas

El patrón de estas preguntas: dado un problema con datos heterogéneos, **proponer una arquitectura
justificando cada decisión**. La estructura de respuesta que funciona es siempre la misma:
**representación de cada tipo de entrada → agregación a tamaño fijo → combinación y salida/pérdida**.

### 2.1 Estimación de precios en comercio electrónico
**Enunciado.** Estimar el precio de publicación de productos. Hay variables numéricas, categóricas de
**alta cardinalidad** (marca, vendedor) y un conjunto de **etiquetas descriptivas de número variable**;
en operación **pueden aparecer categorías no vistas en entrenamiento**.

**Representación de cada tipo de variable:**
- **Numéricas:** normalizar (estandarización; **transformación logarítmica** para las sesgadas) e
  ingresar directamente.
- **Categóricas de alta cardinalidad:** **embeddings aprendidos**, una tabla que asigna a cada
  categoría un vector denso de dimensión moderada. El **one-hot sería inviable** por la cardinalidad y
  **no capturaría similitud** entre categorías.
- **Categorías nuevas en operación:** un token **UNK** por campo, cuyo embedding se entrena
  **reemplazando aleatoriamente una fracción de las categorías durante el entrenamiento**;
  alternativamente **feature hashing**, que mapea cualquier cadena a un número fijo de buckets.

**Entrada de tamaño fijo desde las etiquetas.** Cada etiqueta se embebe con una misma tabla y el
conjunto $\{\mathbf{e}_1,\dots,\mathbf{e}_k\}$ (con $k$ variable) se agrega con una operación
**invariante al orden e independiente de $k$**: promedio o suma (estilo **Deep Sets**) o,
preferentemente, **attention pooling**, que aprende un peso por etiqueta.

**Combinación y salida.** Concatenar numéricas + embedding de marca + embedding de vendedor + vector
agregado de etiquetas → **MLP** con salida escalar. Entrenar como **regresión** (**MSE o Huber**),
idealmente prediciendo $\log(\text{precio})$ por la distribución fuertemente sesgada de los precios.

### 2.2 Severidad de accidentes con múltiples fotografías
**Enunciado.** Clasificar la gravedad de un accidente con las fotos del lugar. **Número variable** de
imágenes, **sin orden determinado**, y **no todas igualmente relevantes**.

El problema tiene la estructura de **multiple instance learning sobre un conjunto** (no una secuencia).
Tres etapas:

1. **Procesamiento por fotografía.** Un **mismo encoder** (CNN o ViT preentrenado en ImageNet, **con
   pesos compartidos**) convierte cada imagen en $\mathbf{z}_i$.
2. **Representación única del accidente.** Agregar $\{\mathbf{z}_1,\dots,\mathbf{z}_N\}$ con una
   operación **invariante a permutaciones e independiente de $N$**. La opción más adecuada es
   **attention pooling**: $\mathbf{z} = \sum_i \alpha_i \mathbf{z}_i$ con $\alpha_i$ aprendido, porque
   responde directamente a que **no todas las fotos son igualmente relevantes**. (Promedio o máximo
   también son válidos, pero tratan todas las imágenes por igual o consideran solo la más activada.)
3. **Salida.** Capa densa con softmax sobre las clases de severidad, entrenada con **entropía
   cruzada**. Como la severidad es **ordinal** (leve < moderada < grave), una alternativa razonable es
   **regresión ordinal**, que penaliza más los errores entre clases lejanas.

---

## 3. Caso extendido: detección de anomalías en piezas mecánicas

**Enunciado.** Muchas fotografías de piezas que **superaron** los controles de calidad. Los defectos
son **poco frecuentes, muy diversos y cambiantes**, por lo que **no existe un conjunto representativo
de imágenes defectuosas ni categorías de falla definidas**. Se quiere un sistema que indique si una
pieza nueva **se aleja de lo normal**.

### 3.1 Formulación del problema de aprendizaje
Dado que solo hay imágenes normales y los defectos son raros y cambiantes (lo que **hace inviable un
clasificador supervisado**), el problema se formula como **detección de anomalías** o clasificación
**one-class**: **modelar la distribución de la apariencia normal** y señalar lo que se desvíe.

- **Regularidades a aprender:** textura, geometría, color y estructura típicos de las piezas buenas.
- **Señal de entrenamiento:** proviene de **las propias imágenes, sin etiquetas externas**; el objetivo
  se construye a partir de la entrada (por ejemplo, reconstruirla).
- **Paradigma:** aprendizaje **no supervisado** (en su variante **auto-supervisada**), del tipo
  *one-class learning*.

### 3.2 Modelo, entrenamiento y prevención de soluciones triviales
**Modelo: un autoencoder convolucional.** Un encoder CNN comprime la imagen a un **código latente de
baja dimensión** y un decoder la reconstruye.
- **Entrada:** la fotografía normalizada (opcionalmente **por parches**, lo que además permite
  **localizar** el defecto).
- **Salida:** la reconstrucción $\hat{\mathbf{x}}$.
- **Pérdida:** error de reconstrucción, p. ej. **MSE por píxel** $\|\mathbf{x}-\hat{\mathbf{x}}\|^2$, o
  una pérdida basada en **SSIM**, que captura mejor la estructura local.

**El riesgo central: aprender la función identidad.** Si el modelo tiene capacidad para copiar
cualquier imagen, **también reconstruirá perfectamente las piezas defectuosas** y el error dejará de
discriminar. Se evita con:
- un **cuello de botella latente suficientemente pequeño**, que obliga a comprimir y retener solo las
  regularidades de las piezas normales;
- variantes que **rompen la copia trivial por construcción**: **denoising autoencoder** (reconstruir
  desde una versión corrompida) o **inpainting** (reconstruir regiones ocultas);
- **regularización del espacio latente** y verificación en validación de que el error sobre piezas
  normales **no se anule trivialmente**.

### 3.3 Puntaje de anomalía, umbral y caso de falla
**Puntaje.** Pasar la imagen por el autoencoder y calcular un **mapa de error por píxel**
$|\mathbf{x}-\hat{\mathbf{x}}|^2$, agregado a un escalar — por ejemplo el **máximo o el promedio de los
$K$ píxeles con mayor error**, criterio **más sensible a defectos pequeños y localizados** que el
promedio global. El mapa de error, además, **localiza espacialmente** el defecto para el inspector.

**Criterio de decisión.** Calcular la distribución del puntaje sobre un conjunto de validación de
piezas normales **no vistas en entrenamiento** y fijar el umbral en un **percentil alto** (p. ej. 95 a
99) o en $\mu + k\sigma$. **La elección es una decisión de costos:** umbral bajo → más falsas alarmas
(revisiones innecesarias); umbral alto → defectos que pasan. **En control de calidad usualmente se
prefiere tolerar falsas alarmas antes que despachar piezas defectuosas.**

**Cuándo falla el sistema.** Cuando el defecto **resulta fácil de reconstruir** para el modelo:
- un **defecto sutil y de baja frecuencia espacial** (leve cambio de tono, deformación suave) que el
  autoencoder reconstruye casi a la perfección porque **localmente se parece a texturas normales**;
- un **defecto estructural o global** (una perforación faltante, un componente mal posicionado) en el
  que **cada parche local luce perfectamente normal**: si el puntaje se basa en apariencia local, la
  pieza pasa aunque su **configuración global** sea inválida;
- más en general, un **autoencoder con demasiada capacidad** puede generalizar en exceso y **"reparar"**
  patrones defectuosos.

> **La limitación de fondo:** un error de reconstrucción bajo es solo un **proxy de normalidad**, no una
> garantía de ella.

---

## 4. Cómo razonar en este tipo de preguntas

Patrones que se repiten en las cuatro preguntas de teoría y en los dos diseños:

1. **Separa "qué función computa la red" de "qué parámetros la computan".** Es el eje de 1.1 y aparece
   siempre que se habla de regularización o reparametrización.
2. **Nombra el sesgo inductivo explícitamente** y pregúntate si los datos lo satisfacen. Es el eje de
   1.2 y de todo el curso.
3. **Cuidado con intercambiar esperanzas y no linealidades.** Es el eje de 1.3 y reaparece en cualquier
   argumento sobre ensambles o aproximaciones.
4. **Cuenta los parámetros y el campo receptivo.** Es el eje de 1.4 y la forma estándar de justificar
   una elección arquitectónica con números.
5. **Para entradas de tamaño variable, usa agregación invariante al orden** (suma, promedio, máximo o
   attention pooling). Es el eje de 2.1 y 2.2.
6. **Para categorías no vistas, planifica el token UNK o el hashing desde el entrenamiento**, no como
   parche de inferencia.
7. **Cuando no hay etiquetas de la clase de interés, reformula como one-class / autosupervisado**, y
   anticipa explícitamente **la solución trivial** que haría inútil al modelo.
