# Clase 4 (10/11/2026) · Interpretabilidad en Transformers

Docente: **Felipe Urrutia**. 49 diapositivas. Tema del día: **cabezas de inducción en un Transformer de
juguete**.

> **Entender qué aprendió un modelo para resolver una tarea: proponer un mecanismo y ponerlo a prueba.**

El archivo del repo se llama `clase-2.pdf` (nombre heredado) y es **un PDF sin capa de texto**: las
diapositivas son imágenes. Ver `dla-material` para cómo leerlo.

---

## 01 · Motivación

### La pregunta
Tenemos una tarea y un modelo entrenado **que acierta**. La pregunta genuina es: **¿cómo usa la entrada
para producir la salida?**

```
entrada  →  embedding → atención·capa 1 → atención·capa 2 → unembedding  →  ŷ = x_{n+1}
                         ¿a qué posiciones mira?  ¿a qué posiciones mira?
            flujo residual h_i: ¿qué información guarda cada posición?
```

### De observar a confirmar: siete pasos

> **Cada paso aporta un tipo de evidencia distinto, y solo seguimos si el anterior pasa.**

| # | Paso | Pregunta | Tipo de evidencia |
|---|---|---|---|
| 1 | **Observar** — patrones de atención | ¿a qué mira cada capa? | observación |
| 2 | **Proponer** — hipótesis por capa | ¿qué calcula cada capa? | observación |
| 3 | **Demostrar a mano** — pesos sin entrenar | ¿puede resolver la tarea? | **plausibilidad** |
| 4 | **Caracterizar** — perfil pos/sym, frecuencias | ¿cada capa tiene su perfil? | **consistencia** |
| 5 | **Intervenir** — *activation patching* | ¿cambia como se predijo? | **evidencia causal** |
| 6 | **Descomponer** — PCA · SAE, sin etiquetas | ¿aparecen las variables? | correlacional |
| 7 | **Confirmar** — *probing* lineal | ¿las lee un clasificador? | correlacional |

El flujo: 1 → 2 → 3 (*si es plausible*) → 4 (*si los perfiles calzan, intervenimos*) → 5 → 6 → 7.

### Qué comportamiento estudiamos: empezamos por uno simple

| Comportamiento | En | ¿Sabemos qué debe calcular? | ¿Podemos mirar el modelo entero? | ¿Aparece en LLMs? |
|---|---|---|---|---|
| Razonar en varios pasos («¿En qué país nació el autor de …?») | un LLM | en parte | ✘ | ✔ |
| Asociar atributos a entidades («el auto es rojo, la casa es azul … el auto es») | un LLM | ✔ | ✘ | ✔ |
| Copiar desde el contexto («… Alexis Sánchez … Alexis» → «Sánchez») | un LLM | ✔ | ✘ | ✔ |
| **Copiar desde el contexto («… σ τ … σ» → «τ»), 8 tokens** | **Transformer de 2 capas** | ✔ | ✔ | ✔ |

> **Hoy: copiar desde el contexto en un Transformer de juguete. La regla es exacta, el modelo es chico
> y el mismo circuito aparece en LLMs.**

### Inducción: «… σ τ … σ → τ»
Un **mecanismo abstracto**, independiente de qué signifiquen σ y τ. Sirve para cualquier tarea cuya
respuesta se pueda leer en el contexto. Tres pasos:
1. **buscar la última aparición del token actual σ**;
2. **mirar a su derecha**;
3. **copiar**.

| Tarea | σ (lo que se busca) | τ (lo que se copia) |
|---|---|---|
| Historia | «Alexis» | «Sánchez» |
| Lista de objetos | «auto es» | «rojo» |
| Tarea de juguete | un símbolo de Σ = {A, B, C, D, E, F, G, H} | el que lo siguió **la vez más reciente** |

## 02 · Una predicción

### La tarea, el modelo y la predicción que seguiremos: «D»

**La regla:** si el token actual ya apareció, **copiar lo que lo siguió la vez MÁS RECIENTE**.

- Alfabeto de **8 símbolos**, **32 posiciones**.
- Con probabilidad **0.25** la regla se interrumpe con un token al azar, **así los pares se
  sobrescriben**.
- La respuesta está definida en el **60 % de las posiciones**; ahí se mide la exactitud.
- **El modelo:** **2 capas de atención, 1 cabeza cada una, sin MLP ni LayerNorm, d = 64, RoPE**, con
  flujo residual `tokens → (+capa 1) → (+capa 2) → logits`.
- Formalmente: `x_{i+1} = x_k`, con `k = max{ k ≤ i : x_{k−1} = x_i }`.
- En el ejemplo, «C» fue seguido de «B» y, más tarde, de «D»: el modelo predice **«D»**. **Esta
  predicción se sigue toda la clase.**

### Entrenamiento: 100 % con 2 capas, 72 % con 1

| Ítem | Valor |
|---|---|
| Entrenamiento | 128 × 3.000 = **384.000 secuencias nuevas** |
| Secuencias | **32 tokens · 8 símbolos** |
| Curvas | 500 de test, cada 50 pasos |
| Resultado final | 2.000 de test (nunca vistas) |
| Pérdida | entropía cruzada **donde hay respuesta** |
| Optimizador | **AdamW · lr 0.001 · wd 0.01** |
| Tasa | sube a 0.001 en 150 pasos (5 %), luego baja en coseno a ~0 |
| Modelo | **17.408 parámetros · d = 64** |

- **2 capas: 100 %** · **1 capa: 72 %**.
- La regla «primera aparición» acierta **63 %**; el azar, **1/8**.
- **Posiciones ambiguas:** el token ya tuvo sucesores distintos (p. ej. candidatos B antiguo y D
  reciente; la regla exige D). **39 % de las posiciones con respuesta son así.**

## 03 · Observar (pasos 1 y 2)

> Solo analizamos **lo que el modelo entrenado ya hace**: sus patrones de atención. A partir de ellos
> proponemos un mecanismo, capa por capa, con su salida idealizada. **Todavía es una hipótesis: la
> atención muestra a dónde mira una cabeza, no qué usa.**

**Pregunta del bloque:** ¿a qué posiciones mira cada capa, y qué mecanismo explicaría esos patrones?

### Herramienta: patrones de atención
Dos estructuras visibles en toda la secuencia:
- **Capa 1:** cada línea sube **un paso a la izquierda**, al **token previo**.
- **Capa 2:** **saltos largos hacia atrás**.

### Hipótesis para la capa 1: cada posición copia su token previo
Desde «D» (posición 15), la capa 1 mira a «C», justo antes (**85 %**, contra 14 % al siguiente). Salida
idealizada: **`y_i = (x_{i−1}, x_i)`** — arriba el previo, abajo el actual.
`y₁₅ = (C, D)`: *«vengo después de C»*.

### Hipótesis para la capa 2: buscar el par («C», ·) más reciente y copiar
La query «C» (posición 23) compara su token con el **previo** de cada `y_k`. Entre las que coinciden
(6 posiciones en el ejemplo), **elige la más reciente** (**82 %**, contra 14 % a la más antigua) y
**copia su token actual, «D»**.

`k* = max{ k < i : prev(y_k) = x_i }`, `ŷ = act(y_{k*})`.

### Hipótesis completa: las dos capas componen un circuito
**La capa 2 solo puede buscar por «previo» porque la capa 1 lo escribió antes**: una **composición de
cabezas** en tres pasos.

1. **capa 1 · token previo:** cada posición lee la anterior y escribe el par `y_i = (x_{i−1}, x_i)`.
2. **capa 2 · matching:** la query «C» busca keys cuyo previo sea «C»; **prefiere la más reciente**.
3. **capa 2 · copia:** el value de esa key es su propio token, «D».

`k* = max{ k ≤ i : x_{k−1} = x_i }`, `salida = x_{k*}`.

## 04 · Demostrar a mano (paso 3)

> **Antes de abrir el modelo entrenado, comprobamos que la hipótesis basta:** la escribimos directamente
> en los pesos, **sin entrenar**, y medimos su exactitud. **Si falla, no tiene sentido buscarla en el
> modelo; si funciona, sabemos qué ingrediente es indispensable.**

**Pregunta del bloque:** ¿puede el mecanismo propuesto, construido a mano, resolver la tarea?

### Arquitectura propuesta: 7 dimensiones y dos cabezas escritas a mano
Cada símbolo es un **vértice del octágono** (máxima separación en el plano). El residual guarda
`x_n`, una constante y **dos subespacios libres** donde las capas escriben:

| bloque | dims |
|---|---|
| x | 2 |
| 1 (constante) | 1 |
| z (el token previo) | 2 |
| salida | 2 |

| Capa | Logit (qué posición i lee la query n) | Value | Resultado |
|---|---|---|---|
| **Capa 1** · token previo | `q = R(−θ₁)u`, `k = u` (leen la constante); `β₁ cos((n − 1 − i)θ₁)` | `x_i →` bloque z | `z_n ≈ x_{n−1}` |
| **Capa 2** · matching + recencia | Q lee `x_n`, K lee `z_i`; otro par con RoPE lee la constante; `β₂⟨x_n, z_i⟩ + c cos((n − i)θ₂)` | `x_i →` bloque salida | `ŷ =` vértice más cercano a la salida (≈ `x_{k*}`) |

### Capa 1 a mano: con RoPE basta para mirar al token previo
La capa 1 **solo necesita posición**. RoPE gira la key de la posición i en `iθ₁`; como `q = R(−θ₁)u`, la
query de la posición n queda girada en `(n−1)θ₁`: **coincide exactamente con la key n − 1**.

`qᵀ R((i − n)θ₁) k = β₁ cos((n − 1 − i)θ₁)`

Con softmax de `β₁ = 1000` la atención es **100 %** al token previo. Barrido de θ₁: **se elige 10°**
(≈ 360°/32); para θ₁ muy pequeño o cuando `cos(kθ₁)` vuelve a valer 1 con `k ≠ 0`, falla.

### Capa 2 a mano: matching simbólico + recencia → 100 %
Q lee `x_n` y K lee `z_i`: el producto `⟨x_n, z_i⟩` **vale 1 solo si `z_i` es el mismo vértice**. Otro
par con RoPE suma `c·cos((n−i)θ₂)`, que **decrece con la distancia**: **entre las coincidencias, gana la
más reciente**.

`logit₂(n, i) = β₂⟨x_n, z_i⟩ + c cos((n − i)θ₂)`

**Resultado del paso 3:** 7 dimensiones bastan para **100 %**; **sin el término de recencia (c = 0) solo
33 % en las ambiguas**. La recencia es el ingrediente indispensable.

## 05 · Caracterizar (paso 4)

> Antes de intervenir, una prueba más barata: la hipótesis dice que la **capa 1 solo usa posición** y la
> **capa 2 compara símbolos**, con algo de posición para la recencia. Medimos ese perfil en el modelo
> **entrenado**.

**Pregunta del bloque:** ¿es la capa 1 posicional y la capa 2 simbólica, como pide el mecanismo?

### Frecuencias de RoPE
Cada par de dimensiones de q y k es un vector 2D que RoPE gira con su propio ángulo `θ_p` por paso de
posición. Con base 100 y `d = 64`:

`θ_p = 100^(−2p/d)`, `p = 0, …, 15` — de **57°** por posición (plano más rápido) a **0,8°** (el más lento).

- **Planos rápidos:** el coseno cambia mucho de una distancia a la siguiente → **distinguen posiciones
  vecinas**.
- **Planos lentos:** casi no rotan en el rango de la secuencia → **comparan contenido**.

`qᵀ R((j − i)θ) k = Σ_p q^(p)ᵀ R((j − i)θ_p) k^(p)`

**Medición** (fracción de `‖q^(p)‖·‖k^(p)‖` por plano, promediada sobre los pares query–key visibles de
300 secuencias de test):

> **La capa 1 vive en los planos rápidos (57°, 43°, 32°, 24°…); la capa 2, en los lentos (4,3° y
> menores).** Exactamente lo que exige el mecanismo.

### Pos / Sym: ¿manda la posición o el contenido?
Urrutia et al. (**ICLR 2026**) caracterizan cada cabeza con **dos puntajes**, con definición formal:

```
φ = arctan e^{λ₂ − λ₁}          β = arctan e^{λ'₂ − λ'₁}
pos = cos(φ − β)                sym = sin(φ + β)
```
donde `λ₁, λ₂` son los logits de dos keys `j₁ < j₂` para una query, y `λ'` los mismos con el
**contenido** de las keys intercambiado (posiciones fijas).

- **pos = 1:** el intercambio **no cambia la preferencia** → **manda la posición**.
- **sym = 1:** la preferencia **se invierte** → **manda el símbolo**.

Promediando sobre pares, cada cabeza es un punto (pos, sym).

**Resultado:** **capa 1 → media (0.89, 0.35)** (posicional) · **capa 2 → media (0.29, 0.83)**
(simbólica). La hipótesis predecía capa 1 → pos ≈ 1 y capa 2 → sym ≈ 1. ✔

> **Desafío abierto planteado en clase:** ¿cómo se relaciona el aprendizaje de las cabezas de inducción
> con la emergencia de cabezas posicionales y simbólicas? Medir (pos, sym) a lo largo del entrenamiento
> y correlacionarlo con la aparición de la inducción (como en Urrutia et al., NeurIPS 2026).

## 06 · Intervenir (paso 5)

> **Que el modelo tenga los perfiles correctos no significa que use esa información.** Trasplantamos
> activaciones de una secuencia **donante** a una **receptora**; la hipótesis **predice qué token
> saldrá**. Si la salida cambia como se predice, tenemos **evidencia causal**.

**Pregunta del bloque:** ¿usa el modelo entrenado el mecanismo que propusimos?

**Herramienta: *activation patching* donante → receptor.** Cada escenario aísla **una pieza** del
circuito. n = 400 casos por escenario.

| # | Escenario | Qué se parcha | Qué afirma | Resultado |
|---|---|---|---|---|
| **1** | Key nueva · salida de capa 1 | copiar la **salida completa de la capa 1 en k**, el par (E, B) | **capa 2 · value:** copia el token actual de la key ganadora | **95 %** |
| **2** | Key nueva · solo atención de capa 1 | copiar **solo la atención de la capa 1 en k** (el previo, E) | **capa 1 · atención en la key:** escribe el previo con el que la key es reconocida (**composición K**) | **89 %** |
| **3** | Query · salida de capa 1 | copiar la salida de la capa 1 **en la query**, el par (B, C) | **capa 2 · query:** busca la key cuyo previo es su token actual | **100 %** |
| **4** | Query · solo atención de capa 1 | copiar solo la atención de la capa 1 **en la query** (el previo, G) | **capa 1 en la query:** su previo **no participa** en la búsqueda | **100 %** (sin cambio) |

**Cuándo no se cumple** (los casos interesantes):
- Escenario 1, **5 %**: esperado «G», el modelo parchado dio «E» (sin cambio). Atención de la capa 2:
  56 % a la key esperada, 44 % a otra posición; probabilidades: «G» 34 %, «E» 66 %.
- Escenario 2, **11 %**: esperado «D», dio «A» (sin cambio). Atención de la capa 2: 7 % a la key
  esperada, 91 % a otra posición.

> **Cuatro predicciones, cuatro aciertos: evidencia causal del mecanismo.** Juntas cubren el recorrido
> completo: la query, la key, cómo se reconocen y qué se copia.

## 07 · Leer representaciones (pasos 6 y 7)

> La hipótesis predice **a priori** qué variables deben existir tras la capa 1: el par `(x_{i−1}, x_i)`.
> Las buscamos **primero sin etiquetas** (PCA lineal, SAE no lineal) y **luego con ellas** (probes
> lineales). Es **evidencia correlacional: complementa al patching, no lo reemplaza.**

**Pregunta del bloque:** ¿cómo codifica el flujo residual las variables que el mecanismo necesita?

### Herramienta: PCA
`Σ = (1/N) Σ_n (h_n − μ)(h_n − μ)ᵀ`, `Σw_j = λ_j w_j` con `λ₁ ≥ λ₂ ≥ …`,
`z = (w₁ᵀ(h − μ), …, w_kᵀ(h − μ)) ∈ ℝᵏ`.

**Objetivo:** ver si la capa 1 escribe el par `(x_{i−1}, x_i)` **sin usar etiquetas** → esperamos
**64 grupos** (8 × 8), no 8.

**Resultados:**
- **PCA-2: los pares (σ, τ) se agrupan.** PC1 explica 20 % y PC2 17 % — **solo 37 % de la varianza**,
  pero **separan los 64 pares con 96 %** de exactitud al clasificar por el centroide más cercano en ese
  mismo plano.
- **Dos niveles:** restando a cada centroide el centro de su grupo σ, **los 8 grupos caen uno sobre
  otro**: la disposición local de los τ es la misma en todos. En el plano, el par se escribe como una
  **suma**: `z(σ, τ) ≈ g + a(σ) + b(τ)`.

### De PCA a un autoencoder disperso (SAE)
PCA separa los pares, pero **cada par es solo un punto en un plano compartido**: decir «qué par es»
exige comparar con los 64 centroides, un paso **no lineal fuera de la PCA**. **Un SAE mete ese paso en
el propio código.**

| | **PCA: comprimir** | **SAE: expandir y elegir** |
|---|---|---|
| codificar | `z = Wᵀ(h − μ)` | `z = TopK(W_enc(h − b))` |
| reconstruir | `ĥ = μ + Wz` | `ĥ = b + W_dec z` |
| objetivo | `min_W Σ_n ‖h_n − ĥ_n‖²` | `min_{W_enc, W_dec, b} Σ_n ‖h_n − ĥ_n‖²` |
| dimensión | `W ∈ ℝ^{d×k}`, `k < d`, `WᵀW = I` | `W_dec ∈ ℝ^{d×K}`, `‖z‖₀ = k ≪ K` |

**¿Qué es un código del SAE?**
```
z_c = w_cᵀ(h − b)  si c ∈ TopK ;  0 si no
ĥ = b + Σ_c z_c d_c   ──(k=1)──►  ĥ = b + z_c d_c
```
Un **código = un detector `w_c`** (fila de `W_enc`: ¿cuánto se parece h?) **+ una dirección `d_c`**
(columna de `W_dec`: qué escribe). **El índice c es arbitrario: lo que significa un código se lee en las
muestras (x, i) que lo activan**, `T_c = top_{(x,i)} z_c(h_i(x))`.

**Resultados del barrido (SAE TopK sobre la salida de la capa 1):**

| Config. | FVE | Lectura |
|---|---|---|
| **k = 1, K = 64 = \|Σ\|²** | — | **63 códigos vivos; las 20 muestras más activas de cada uno comparten un mismo par.** El SAE encontró los pares **sin etiquetas**. 64 de 64 pares con exactamente 1 código |
| **k = 1, K = 48** | 96 % | **37 pares conservan su código propio**; los demás se juntan **dentro del mismo σ** (11 códigos compartidos) |
| **k = 1, K = 8** | 72 % | Sin espacio para los pares, **cada código junta casi una fila completa: «el token previo es σ»**. 0 pares con código propio |
| **k = 2, K = 16 = 2\|Σ\|** | 99,7 % | **Cada código lee un solo token: el previo σ o el actual τ.** Cada posición activa uno de cada rol |
| **k = 2, soportes** | — | El **soporte** `S(h) = {c : z_c(h) ≠ 0} = {c_i, c_j}` **predice el par en 95 %** de las posiciones. 72 de 136 soportes usados; `#soportes = C(K,2) + K = 136` con K = 16 |

- **Con k = 1 un concepto es *una coordenada*; con k = 2 puede ser *una coordenada* (una parte, p. ej. σ)
  o *un soporte* `{c_i, c_j}` (la combinación).**
- **Capacidad:** con k = 1 recién `K = 64` reconstruye todo. Con k = 2 la reconstrucción se completa ya
  en `K = 16 = 2|Σ|`.
- **FVE** (*fraction of variance explained*): `FVE = 1 − Σ‖h_n − ĥ_n‖² / Σ‖h_n − h̄‖²`.
- **Par recuperado:** `(1/N) Σ_n 1[(σ_n, τ_n) = π(c_n)]`, donde `π(c)` es el par más frecuente del código
  c. Vale 100 % si cada código lee un solo par.
- **Umbral:** `S_t(h) = { c : z_c(h) > t · max_{c'} z_{c'}(h) }` con `t = 0.1`. Descarta las coordenadas
  que TopK deja encendidas por muy poco. **En K = 64 el segundo activo es ≈ 0 en 71 % de las posiciones:
  con umbral, par recuperado = 100 %.**

> **TopK activa *a lo más* k códigos: con códigos de sobra vuelve a un código por par, y el segundo es
> ruido.**

### Herramienta: probing lineal (paso 7)
**Ahora sí usamos etiquetas:** un clasificador lineal **por variable y por punto del residual**,
entrenado en 3.000 secuencias y evaluado en 1.000 nuevas.

`p(y | h) = softmax(Wh + b)`, `min_{W,b} −Σ_n log p(y_n | h_n) + λ‖W‖²`

Puntos del residual: `h⁰` (embedding), `h¹` (tras capa 1), `h²` (tras capa 2). Variables: `x_i` (token
actual), `x_{i−1}` (token previo), el par `(x_{i−1}, x_i)`, `x_{i+1}` (respuesta).

**Esperado:** el previo aparece **tras la capa 1**; la respuesta, **solo tras la capa 2**.

| Variable | `h⁰` embedding | `h¹` tras capa 1 | `h²` tras capa 2 | azar |
|---|---|---|---|---|
| token actual `x_i` | **100 %** | **100 %** | **100 %** | 1/8 |
| token previo `x_{i−1}` | 19 % | **100 %** | **100 %** | 1/8 |
| par `(x_{i−1}, x_i)` | 19 % | **100 %** | **100 %** | 1/64 |
| respuesta `x_{i+1}` | 24 % | 48 % | **100 %** | 1/8 |

> **Cada variable aparece exactamente donde el mecanismo dice.** Advertencia metodológica: el probe mide
> si la variable **se puede leer**, **no si el modelo la usa**.

## 08 · Resumen: siete técnicas, una explicación

**El mecanismo:** la capa 1 escribe el par `(x_{i−1}, x_i)` en cada posición; la capa 2 busca el par más
reciente cuyo previo es el token actual y **copia lo que siguió**.

| # | Paso | Herramienta | Lo que se vio | Evidencia |
|---|---|---|---|---|
| 1 | Observar | patrones de atención | capa 1 → token previo (**79 %**); capa 2 → key más reciente (**93 %**) | observación |
| 2 | Proponer | hipótesis por capa | capa 1 escribe el par; capa 2 busca el más reciente y copia | observación |
| 3 | Demostrar | construcción a mano (RoPE) | **7 dimensiones bastan: 100 %**; sin recencia, **33 % en ambiguas** | plausibilidad |
| 4 | Caracterizar | pos/sym y frecuencias | capa 1 **posicional (pos 0.89)**, capa 2 **simbólica (sym 0.83)** | consistencia |
| 5 | Intervenir | activation patching | 4 escenarios: el desenlace predicho en **89 %–100 %** de los casos | **causal** |
| 6 | Descomponer | PCA y SAE | PCA-2 recupera el par en **96 %**; SAE: **63 códigos = pares**, **16 = previo + actual** | correlacional |
| 7 | Confirmar | probing lineal | previo legible desde la capa 1 (**100 %**); respuesta solo tras la capa 2 (**100 %**) | correlacional |

## Referencias citadas en las diapositivas
Olsson et al. (2022) · Elhage et al. (2021) · Brown et al. (2020) · Bricken et al. (2023) ·
Cunningham et al. (2023) · Gao et al. (2024) · Alain & Bengio (2016) · Belinkov (2022) ·
Meng et al. (2022) · Zhang & Nanda (2023) · Heimersheim & Nanda (2024) · Geiger et al. (2021) ·
Su et al. (2021, RoPE) · Feng & Steinhardt (2023) · Urrutia et al. (ICLR 2026) ·
Urrutia et al. (NeurIPS 2026).

## Material práctico asociado
- `binding-colab.ipynb` — **los mismos siete pasos en un LLM abierto** (Qwen2.5-1.5B-Instruct) sobre
  *entity binding*. Detalle en `practicos-y-codigo.md`.
- **Laboratorio 1** (entrega 24/11/2026) — los siete pasos sobre **la tarea del puntero**, una variante
  distinta de la inducción. Detalle en `practicos-y-codigo.md`.
