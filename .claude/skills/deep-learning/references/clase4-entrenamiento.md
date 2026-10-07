# Clase 4 · Entrenamiento de redes neuronales

> *"En teoría, no hay diferencia entre la teoría y la práctica. En la práctica, sí la hay."*

Tras bambalinas, hacer que los modelos de DL funcionen adecuadamente y sean prácticos requiere una
gran cantidad de detalles, organizados en tres preguntas: **¿cómo optimizar?**, **¿cómo controlar el
sobreajuste?** y **¿cómo reutilizar?**

---

# Parte I · ¿Cómo optimizar?

Dado el enfoque de descenso de gradiente, surgen cuatro preguntas:

1. **¿Cómo calculo las derivadas para cada parámetro?** $\;\dfrac{\partial \mathcal{L}}{\partial w},\;\forall w \in W$
2. **¿Cómo desciendo de manera efectiva y eficiente en la función objetivo?**
3. **¿Debo inicializar los pesos y normalizar los datos de manera especial?**
4. **¿Puedo hacerle algo a la arquitectura de la red para facilitar el proceso?**

## 1. Grafo de cómputo y backpropagation

- Un **grafo de cómputo** representa **todas las operaciones realizadas hasta llegar al output**.
- Podemos aprovechar esa estructura junto con la **regla de la cadena** para obtener el gradiente
  completo. **Basta con analizar solo las derivadas locales** en cada nodo.
- Referencia práctica del curso: `micrograd` de Karpathy —
  https://github.com/karpathy/micrograd (y el notebook de backpropagation en Colab).

## 2. El paisaje de optimización

- La función objetivo de una red profunda es, en general, **no convexa**.
- Además puede contener **mesetas**, **regiones mal condicionadas** y **puntos no diferenciables**,
  dependiendo de la activación.
- Referencia: Li et al., *Visualizing the Loss Landscape of Neural Nets*, NeurIPS 2018 · también
  `losslandscape.com`.

**En otras palabras: el descenso de gradiente simple no funciona bien.** Los desafíos concretos son:
- **Costo de cómputo** del gradiente completo.
- **Escapar de puntos críticos** y mínimos locales.
- **Ajuste dinámico del learning rate.**
- **Escala del learning rate para cada parámetro.**

## 3. Stochastic Gradient Descent (SGD)

- Los datos de entrenamiento se dividen en **subconjuntos disjuntos de ejemplos (batches)**.
- Se usa **un batch, no todos los ejemplos**, para calcular el gradiente de cada descenso.
- Una **época** consiste en **recorrer todos los batches** del conjunto de entrenamiento.
- Bajo ciertos supuestos, SGD **puede converger hacia puntos estacionarios**.
- **El ruido de los batches puede ayudar a abandonar** algunas regiones planas o cercanas a puntos
  silla.

## 4. Familia de optimizadores

### Momentum
Aminora el riesgo de quedar pegado en puntos críticos.
$$v_t = \gamma\,v_{t-1} + \eta\,\nabla_\theta J(\theta_t) \qquad \theta_{t+1} = \theta_t - v_t$$
Referencia visual: https://distill.pub/2017/momentum/

### Nesterov Accelerated Gradient (NAG)
Corrige velocidad y trayectoria del momentum **mirando hacia el futuro**: evalúa el gradiente en la
posición a la que el momentum ya está llevando.
$$v_t = \gamma\,v_{t-1} + \eta\,\nabla_\theta J(\theta_t - \gamma\,v_{t-1}) \qquad \theta_{t+1} = \theta_t - v_t$$

### Adagrad
Genera **learning rates adaptativos por parámetro**, usando la **acumulación histórica** de gradientes.
$$g_{t,i} = \nabla_\theta J(\theta_{t,i}) \qquad \theta_{t+1,i} = \theta_{t,i} - \frac{\eta}{\sqrt{G_{t,i} + \epsilon}} \cdot g_{t,i}$$
donde $G_{t,i}$ acumula la suma de cuadrados de los gradientes pasados del parámetro $i$. *Limitación
implícita: esa acumulación nunca decrece, por lo que el learning rate efectivo tiende a cero.*

### RMSProp
Normaliza cada actualización usando un **promedio móvil de gradientes cuadrados recientes** (en vez de
la acumulación histórica completa).
$$E[g^2]_t = \gamma\,E[g^2]_{t-1} + (1-\gamma)\,g_t^2 \qquad \theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{E[g^2]_t + \epsilon}} \cdot g_t$$

### Adadelta
Mejora RMSProp **introduciendo un numerador para hacer calzar las "unidades"**.
$$E[g^2]_t = \gamma\,E[g^2]_{t-1} + (1-\gamma)\,g_t^2 \qquad E[\Delta\theta^2]_t = \gamma\,E[\Delta\theta^2]_{t-1} + (1-\gamma)\,\Delta\theta_t^2$$
$$\theta_{t+1} = \theta_t - \frac{\sqrt{E[\Delta\theta^2]_{t-1} + \epsilon}}{\sqrt{E[g^2]_t + \epsilon}} \cdot g_t$$

### Adam
**Combina momentum con learning rate adaptativo**, con corrección de sesgo.
$$m_t = \beta_1 m_{t-1} + (1-\beta_1)\,g_t \;\;\to\;\; \hat{m}_t = \frac{m_t}{1-\beta_1^t}$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2)\,g_t^2 \;\;\to\;\; \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \cdot \hat{m}_t$$

**Cómo leer la familia completa:** momentum y NAG atacan *escapar de puntos críticos*; Adagrad,
RMSProp y Adadelta atacan *la escala del learning rate por parámetro*; Adam **junta ambas líneas**, y
por eso es el punto de partida razonable por defecto.

## 5. Inicialización de parámetros

**¿Qué pasa si inicializamos todo con ceros?** Todas las neuronas de una capa calculan lo mismo y
reciben el mismo gradiente: nunca se rompe la simetría y la capa colapsa a una sola neurona efectiva.

Lo siguiente sería **inicializar aleatoriamente**, pero el **esquema aleatorio no acotado** genera dos
problemas:
1. **Tiempo de convergencia.**
2. **Desvanecimiento / explosión del gradiente.**

Para reducirlos se corrige la inicialización aleatoria **considerando el tamaño de las capas**:

| Esquema | Escala | Se usa con |
|---|---|---|
| **Kaiming / He** | $\sqrt{2 / \text{fan}_{in}}$ | **ReLU** |
| **LeCun** | $\sqrt{1 / \text{fan}_{in}}$ | — |
| **Xavier / Glorot** | $\sqrt{2 / (\text{fan}_{in} + \text{fan}_{out})}$ | **tanh** |

*(Las láminas escriben "Kaiming/Xe"; es Kaiming/He.)*

## 6. Capas de normalización

- La **escala y variabilidad de las activaciones** influyen en el **condicionamiento del problema** y
  en la **estabilidad de la optimización**.
- Por eso **normalizar las entradas a la red es una buena práctica**. ¿Pero cómo inducimos esto
  **dentro** de la red?

**Batch normalization** es lo más simple: normalizar por batch. Una vez normalizadas las activaciones,
**se escalan y trasladan con parámetros aprendidos** para adecuarlas a la siguiente capa.

## 7. Conexiones residuales (skip connections)

**El fenómeno (2015):** se descubrió algo raro — **más capas no significaba menor pérdida en el
entrenamiento**. No era sobreajuste: la red más profunda rendía peor **incluso en entrenamiento**.

**La hipótesis:** la causa era **la incapacidad de las redes de aprender la función identidad**.

**La solución:** **conexiones residuales o skip connections**, que suman la entrada de un bloque a su
salida, de modo que el bloque solo tiene que aprender el *residuo*. Los resultados mejoran mucho
gracias a un **mejor condicionamiento del problema**.

Referencia: He, K. et al. (2016), *Deep Residual Learning for Image Recognition*, CVPR.

---

# Parte II · ¿Cómo controlar el sobreajuste?

## 8. Dropout

- Las **capas densas del final** suelen concentrar muchos parámetros y son **especialmente propensas a
  sobreajustarse**. La estrategia habitual es aplicar Dropout **principalmente en esas capas**.
- Durante el **entrenamiento**, Dropout **apaga aleatoriamente una fracción de las activaciones**.
- Esto **reduce la coadaptación** entre unidades y favorece **representaciones más robustas**.
- **Dropout puede mejorar la generalización.**
- El curso también lo mira **desde las superficies de optimización**, no solo como regularizador.

> Sutileza evaluada en los ejercicios: en la formulación original, en inferencia se multiplican las
> activaciones por $1-p$ para conservar el valor esperado. **Eso iguala la esperanza a la entrada de
> cada capa, pero no la de la predicción final**, porque la esperanza no conmuta con las no
> linealidades. Ver `ejercicios-resueltos.md` §1.3.

## 9. Regularización explícita

$$\arg\min_W \; J(X,Y;W) = \lambda\,\mathcal{R}(W) + \sum_i^N \mathcal{L}(x_i, y_i; W)$$

$$\ell_2 = \sum_{i,j,k} W_{i,j,k}^2 \qquad\qquad \ell_1 = \sum_{i,j,k} |W_{i,j,k}|$$

> Sutileza evaluada en los ejercicios: **L2 penaliza los parámetros, no la función que la red
> computa**. Dos redes que calculan exactamente la misma función pueden recibir penalizaciones
> distintas. Ver `ejercicios-resueltos.md` §1.1.

## 10. Aumento de datos

Otro de los esquemas más populares de control del sobreajuste: **incrementa el conjunto de datos
"gratuitamente"** aplicando transformaciones que preservan la etiqueta. Visto en detalle en el caso
AlexNet (`clase3-cnn.md` §6).

**Del síntoma a la intervención:** el curso enmarca estas tres herramientas (dropout, regularización
explícita, aumento de datos) como respuestas a diagnosticar qué está fallando, no como recetas fijas.

---

# Parte III · ¿Cómo reutilizar?

## 11. Transfer learning

**La observación.** Los resultados de DL con imágenes son impresionantes, pero resuelven un problema
muy puntual que **no necesariamente se alinea con muchos casos de uso reales**. Afortunadamente, las
redes profundas ya entrenadas **pueden ser usadas o adaptadas con poco esfuerzo en otras tareas**.
Esta propiedad es **consecuencia directa de la habilidad de las redes para aprender features
jerárquicas y composicionales**.

> **La reutilización es la máxima evidencia de generalización.**

**Ejemplo:** si a **AlexNet** se le "corta la cabeza" y se usa como **extractor de características**,
se obtienen excelentes resultados en una gran cantidad de tareas visuales: reconocimiento de escenas,
caras, acciones, personas, etc.

**La idea general:** aprender inicialmente modelos poderosos con sets de datos **abundantes y de buena
calidad**, y luego transferir ese aprendizaje a una nueva tarea, generalmente con un conjunto más
limitado en **cantidad, calidad o seguridad**.

### Dos mecanismos de adaptación
- **Transferencia directa:** las features aprendidas en un dominio se usan **directamente** en otro,
  **sin noción de la existencia de una red neuronal subyacente**.
- **Fine-tuning:** las features aprendidas se **reentrenan "suavemente"** en el nuevo dominio,
  cambiando el clasificador/regresor.

### Ejemplos aplicados citados en clase
- *Estimating Displaced Populations From Overhead*: se usa una CNN entrenada en ImageNet como base
  (**ResNet-50**), se **cambia el clasificador final por un regresor** y se reentrena con **imágenes
  satelitales**.
- *Understanding Network Traffic States using Transfer Learning*: se usa una CNN entrenada en ImageNet
  como base para **extraer features de estados de tráfico codificados como imágenes** y luego
  agruparlos.

### Los desafíos abiertos
- ¿Reentrenamos **todas las capas o algunas**? ¿Cuáles? ¿En qué orden?
- ¿Cuándo decidir entre **fine-tuning** y **entrenamiento desde cero**?
- ¿**Cuán similares** son los dominios?
- ¿Qué rol juega el **learning rate**?

---

## 12. El concepto central de la clase

> Para entrenar redes hay que considerar **muchos elementos prácticos**. Afortunadamente, **no es
> necesario reinventar la rueda** y muchas veces es suficiente basarse en trabajos anteriores.
