# Clase 2 (27/10/2026) · Transferencia de Conocimiento

Docente: **Felipe del Río** (CENIA). 62 diapositivas.
Agenda: **1. Motivación · 2. Transfer Learning · 3. ¿Cómo? · 4. Panorama general.**

## 1 · Motivación

Hasta ahora el curso base cubrió el **modelo** (tipos de redes, arquitecturas, funciones de activación)
y la **optimización** (regularizadores, optimizadores). Pero queda **el elefante en la habitación: los
datos**.

> En general se asume que se cuenta con **grandes volúmenes de datos** para entrenar redes desde cero.
> Con pocos datos los modelos **no es que no funcionen, pero no brillarán**.

El escenario real de la clase:
1. Tenemos una tarea que nos interesa.
2. **No existe** un modelo entrenado para nuestra tarea.
3. **No tenemos muchos datos** de entrenamiento.

Las tres preguntas de la clase: **¿qué técnicas existen? ¿por qué funcionan? ¿cómo lo hacemos en la
práctica?**

## 2 · Transfer Learning

**Transfer learning = transferencia de conocimiento** desde una **tarea de origen** a una **tarea de
destino**, usando una red neuronal como vehículo.

### Los dos datasets

| | **Dataset de origen** | **Dataset de destino** |
|---|---|---|
| Qué es | donde se aprende la tarea de origen | la tarea que nos interesa resolver |
| Debe ser | **masivo**, **diverso** (dominios, habilidades, modalidades) y **rico en semántica** | **relevante**, **diverso**, **similar a la tarea de origen** y **suficientemente grande** |

### Tipos de transferencia
1. **Adaptación de tarea** — cambia la tarea, mismo tipo de datos.
2. **Adaptación de dominio** — misma tarea, otro dominio.
3. **Adaptación de clases** — mismo tipo de tarea, otro conjunto de clases.
4. **Transferencia de modalidad** — cambia la modalidad (p. ej. imagen → video).
5. Otros.

## 3 · ¿Cómo? Dos estrategias

### Paso 0 · Pre-training
Hay que **contar con un modelo pre-entrenado**. Pre-entrenar = entrenar un modelo en un **dataset
masivo**; **requiere mucha ingeniería**. El modelo adquiere **conocimiento, habilidades y sesgo
inductivo**. (La clase 3 se dedica a este proceso.)

### Estrategia 1 · Feature Extraction

**Vector de características (*embedding*):** vector n-dimensional que representa un ejemplo, extraído
con una red neuronal. Permite reaprovechar el pre-entrenamiento: **el conocimiento aprendido y los
sesgos inductivos**.

**Dos formas de usarlo, equivalentes en espíritu:**
- (a) **Precomputar** las representaciones → entrenar un clasificador sobre ellas.
- (b) **Congelar** los pesos de la red → **reemplazar y entrenar el cabezal de salida**.

```python
# Feature extraction (PyTorch, tipo del práctico)
model = models.resnet18(weights="IMAGENET1K_V1")
for p in model.parameters():
    p.requires_grad = False            # congelamos la red base
model.fc = nn.Linear(512, n_classes)   # nuevo cabezal (entrenable)
```

**En la práctica:** API de *vector embeddings* de OpenAI · embeddings de texto e imágenes en Google
Cloud · modelos en Hugging Face · **Torch FX** (para extraer activaciones intermedias).

**Aplicaciones de los embeddings:**
- **Búsqueda semántica** — buscar por *similitud de contenido*, no por palabras clave ni metadatos
  (p. ej. «perros en la playa»).
- **Recomendación.**
- **Otros usos:** detección de anomalías, clustering, medir diversidad.
- **Bases de datos vectoriales:** almacenar y consultar información vectorial, **búsqueda aproximada de
  vecinos cercanos (ANN)** y asociar metadata a los vectores.

### Estrategia 2 · Fine-Tuning

Similar a feature extraction, **pero actualizamos los pesos de la red base**. Permite **adaptar las
representaciones aprendidas**, reaprovechando igual el conocimiento y los sesgos inductivos del
pre-entrenamiento.

```python
# Fine-tuning
model = models.resnet18(weights="IMAGENET1K_V1")
model.fc = nn.Linear(512, n_classes)   # nuevo cabezal
# no congelamos nada: se entrenan todos los pesos (con lr baja)
```

> **La única diferencia es si congelamos o no la red base.** En el notebook del práctico:
> `get_model(..., pretrained=True, frozen=True / False)`.

**En la práctica:** fine-tuning en OpenAI · fine-tuning en Google Cloud · modelos en Hugging Face ·
**Hugging Face PEFT** (*Parameter-efficient Fine-tuning*).

### Catastrophic forgetting (olvido catastrófico)

Al actualizar **todos** los pesos para la tarea de destino, la red **puede olvidar lo aprendido en el
pre-entrenamiento**.

```
Antes:   tarea de origen ✔ · tarea de destino ✘
            ↓ fine-tuning agresivo
Después: tarea de destino ✔ · tarea de origen ✘
```

**Es más probable con pocos datos, learning rates altas o muchas épocas.**

**Cómo mitigarlo:**
- **Learning rate baja** (p. ej. 10× menor que entrenando desde cero).
- **Entrenar primero el cabezal** y luego toda la red.
- **Congelar las primeras capas** o descongelarlas de a poco.
- **Métodos PEFT como LoRA**: los pesos originales **no cambian**.

### LoRA · Low-Rank Adaptation

Personalizar modelos grandes en tareas específicas usando **adaptadores ligeros** en lugar de un ajuste
completo.

```
        x ──► A ──► B ──┐
                        ⊕ ──► h          W = W₀ + AB
  W₀ (preentrenado) ────┘
     d×d        d×r, r×d
```

- **Hipótesis:** el cambio necesario para adaptar el modelo (**ΔW**) tiene **rango bajo**, así que basta
  con `BA`.
- **Inicio:** `A` aleatoria y `B = 0`, entonces `ΔW = BA = 0` y **el modelo parte idéntico al
  pre-entrenado**.
- **Al final:** se fusiona `W = W₀ + BA`, **sin costo extra en inferencia**. `W₀` no cambia: **un
  adaptador por tarea**.

**Cuánto ahorra** (matriz de 4096 × 4096):

| | Parámetros a actualizar |
|---|---|
| ΔW completo | **16,8 M** |
| LoRA con r = 8 | **65,5 mil** → `2 · 4096 · 8` = **0,4 %** del total |

### Casos de fine-tuning mostrados
- **Image captioning.**
- **Tareas de video** (p. ej. features I3D).
- **ChatGPT:** *supervised fine-tuning* (SFT) sobre un modelo de lenguaje, siguiendo el esquema de
  *instruction following* de OpenAI.

## 4 · Panorama general

### ¿Por qué funciona?
- **Transfer learning:** **alineación entre las jerarquías de características**. Reutilizamos
  características aprendidas en una tarea para otra.
- **Fine-tuning:** **un mejor punto de partida** permite encontrar **un mejor óptimo local** cuando
  buscamos en el espacio de hipótesis.

### Comparación (tabla literal de la clase)

| Feature Extraction | Fine-tuning |
|---|---|
| Dominio similar | Adaptación al dominio |
| Menos especialización | Más especialización |
| Menos flexible | Más flexible |
| Bajo costo computacional | Alto costo computacional |
| Bajo riesgo de sobreajuste | Alto riesgo de sobreajuste |
| **No hay riesgo de catastrophic forgetting** | **Riesgo de catastrophic forgetting** |

### El paradigma: Foundation Models
**Posibilitado por el transfer learning y los entrenamientos a gran escala.** Es el puente directo con
la clase 3 (autosupervisión), que explica **cómo** se pre-entrenan esos modelos.

## Práctico asociado
`Practico - Transferencia de Conocimiento.ipynb` — ResNet18 sobre el dataset *flowers*: modelo base vs.
feature extraction vs. fine-tuning, t-SNE de embeddings, k-NN y búsqueda semántica. Detalle en
`practicos-y-codigo.md`.
