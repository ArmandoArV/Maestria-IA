# Práctica: PyTorch y Colab

> **Advertencia de procedencia.** Las láminas dicen repetidamente *"Vamos a Colab…"*, pero **esos
> notebooks no están en el repositorio**: `DeepLearning/` contiene únicamente los 7 PDFs y la carpeta
> `SolucionEjercicios`. Lo que sigue es **PyTorch estándar alineado a las decisiones conceptuales del
> curso**, no una transcripción del código de clase. Si alguien pide "el código de la clase X", dilo.

## 1. Las decisiones del curso

- **Framework: PyTorch.** *"Aunque los conceptos son independientes del framework, preferentemente
  usaremos PyTorch y Colab para los ejemplos."*
- **Entorno: Google Colab**, con GPU.
- **Qué se evalúa:** *"siempre consideraremos las implementaciones como parte fundamental de los
  contenidos del curso (**pero no el código en sí**)"*. En las tareas se evalúa el **criterio de
  diseño y el análisis**, no la sintaxis.

## 2. Esqueleto mínimo, mapeado al vocabulario del curso

Cada pieza del esquema general de ML (ver SKILL.md) tiene su contraparte directa en PyTorch:

| Concepto del curso | En PyTorch |
|---|---|
| Modelo predictivo $f(\cdot;W)$ | `nn.Module` con sus capas |
| Parámetros $W$ | `model.parameters()` |
| Función de pérdida $\mathcal{L}$ | `nn.CrossEntropyLoss()`, `nn.MSELoss()`, … |
| Regularizador $\mathcal{R}(W)$ (L2) | `weight_decay` del optimizador |
| Técnica de búsqueda | `torch.optim.SGD`, `torch.optim.Adam` |
| Grafo de cómputo + backprop | `autograd`, `loss.backward()` |
| Batch / época | `DataLoader` / el bucle externo |

## 3. Preparación del entorno

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader

# Dispositivo: en Colab, Entorno de ejecución → Cambiar tipo → GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device, torch.__version__)

# Reproducibilidad (relativa): fija la semilla antes de construir el modelo
torch.manual_seed(42)
```

## 4. Datos: Fashion-MNIST, el ejemplo de la clase 2

```python
from torchvision import datasets, transforms

# Normalizar las entradas es "una buena práctica" explícita del curso (clase 4).
# Los valores son la media y desviación estándar del conjunto de entrenamiento.
tf = transforms.Compose([
    transforms.ToTensor(),                 # [0,255] uint8 -> [0,1] float, shape (1,28,28)
    transforms.Normalize((0.2860,), (0.3530,)),
])

train_ds = datasets.FashionMNIST(root="./data", train=True,  download=True, transform=tf)
test_ds  = datasets.FashionMNIST(root="./data", train=False, download=True, transform=tf)

train_dl = DataLoader(train_ds, batch_size=128, shuffle=True,  num_workers=2)
test_dl  = DataLoader(test_ds,  batch_size=256, shuffle=False, num_workers=2)
```

**60.000 de entrenamiento y 10.000 de test, imágenes 28×28 en escala de grises, 10 categorías** — las
cifras exactas que da la clase 2.

> **Separación de conjuntos.** El curso trabaja con train/test, pero para tomar decisiones de
> arquitectura o hiperparámetros hay que **partir el train en train/validación** y dejar el test
> intocado hasta el final. Usar el test para elegir hiperparámetros es filtrar información.

## 5. Un MLP, tal como lo plantea el curso

$f = \sigma(W_3\,\sigma(W_2\,\sigma(W_1 x)))$, con **softmax en la salida** y **cross-entropy** como
pérdida.

```python
class MLP(nn.Module):
    def __init__(self, d_in=28*28, hidden=(256, 128), n_classes=10, p_drop=0.5):
        super().__init__()
        capas, d = [], d_in
        for h in hidden:
            capas += [nn.Linear(d, h), nn.ReLU(), nn.Dropout(p_drop)]
            d = h
        capas += [nn.Linear(d, n_classes)]     # salida SIN softmax: ver nota
        self.red = nn.Sequential(*capas)

    def forward(self, x):
        x = x.flatten(1)                        # (B,1,28,28) -> (B,784)
        return self.red(x)                      # logits

model = MLP().to(device)
```

**Dos avisos que evitan errores clásicos:**

1. **No pongas `softmax` en la última capa.** `nn.CrossEntropyLoss` ya aplica `log_softmax`
   internamente y espera **logits**. Aplicarlo dos veces aplana los gradientes y la red entrena mal.
   Conceptualmente el curso sí describe softmax + cross-entropy; en PyTorch vienen fusionados por
   estabilidad numérica.
2. **`nn.CrossEntropyLoss` espera etiquetas como índices enteros** (`long`), no one-hot.

### Inicialización (clase 4)
PyTorch inicializa `nn.Linear` con un esquema tipo Kaiming uniforme por defecto, lo que suele bastar.
Para aplicar explícitamente el criterio del curso (**Kaiming/He con ReLU**):

```python
def init_kaiming(m):
    if isinstance(m, (nn.Linear, nn.Conv2d)):
        nn.init.kaiming_normal_(m.weight, nonlinearity="relu")   # std = sqrt(2 / fan_in)
        if m.bias is not None:
            nn.init.zeros_(m.bias)

model.apply(init_kaiming)
```
Con **tanh** corresponde `nn.init.xavier_normal_` (Xavier/Glorot). **Nunca inicializar los pesos en
cero**: no se rompe la simetría y toda la capa colapsa a una neurona efectiva.

## 6. Pérdida y optimizador

```python
criterio = nn.CrossEntropyLoss()

# Adam: "combina momentum con learning rate adaptativo". Punto de partida razonable.
optim = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)

# Alternativa fiel a SGD + momentum de la clase 4:
# optim = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9,
#                         nesterov=True, weight_decay=1e-4)
```

**`weight_decay` es la regularización $\ell_2$** del curso: el término $\lambda\,\mathcal{R}(W)$ con
$\mathcal{R}(W) = \sum W_{i,j,k}^2$. **$\ell_1$ no tiene parámetro nativo**: hay que sumarla a mano a
la pérdida.

## 7. Bucle de entrenamiento

```python
def entrenar_una_epoca(model, dl, criterio, optim, device):
    model.train()                      # activa dropout y usa estadísticas de batch en BatchNorm
    total, aciertos, suma_loss = 0, 0, 0.0
    for x, y in dl:
        x, y = x.to(device), y.to(device)
        optim.zero_grad()              # los gradientes se ACUMULAN: hay que limpiarlos
        logits = model(x)
        loss = criterio(logits, y)
        loss.backward()                # backprop sobre el grafo de cómputo
        optim.step()                   # un paso de descenso

        suma_loss += loss.item() * y.size(0)
        aciertos  += (logits.argmax(1) == y).sum().item()
        total     += y.size(0)
    return suma_loss / total, aciertos / total


@torch.no_grad()                       # sin grafo de cómputo: más rápido y menos memoria
def evaluar(model, dl, criterio, device):
    model.eval()                       # desactiva dropout y congela BatchNorm
    total, aciertos, suma_loss = 0, 0, 0.0
    for x, y in dl:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        suma_loss += criterio(logits, y).item() * y.size(0)
        aciertos  += (logits.argmax(1) == y).sum().item()
        total     += y.size(0)
    return suma_loss / total, aciertos / total


historial = []
for epoca in range(1, 21):             # una "época" = recorrer todos los batches
    tr_loss, tr_acc = entrenar_una_epoca(model, train_dl, criterio, optim, device)
    te_loss, te_acc = evaluar(model, test_dl, criterio, device)
    historial.append((tr_loss, tr_acc, te_loss, te_acc))
    print(f"época {epoca:2d} | train loss {tr_loss:.4f} acc {tr_acc:.4f} "
          f"| test loss {te_loss:.4f} acc {te_acc:.4f}")
```

**Los cuatro errores más frecuentes en este bucle:**
1. Olvidar `optim.zero_grad()` → los gradientes se acumulan entre batches.
2. Olvidar `model.eval()` al evaluar → dropout sigue activo y las métricas salen ruidosas y peores.
3. Olvidar `model.train()` al volver a entrenar → dropout y BatchNorm quedan desactivados.
4. Usar `loss` en vez de `loss.item()` al acumular → se retiene el grafo y la memoria explota.

## 8. Diagnóstico: las dos curvas del curso

El curso monitorea **Loss** y **Accuracy**. La lectura conjunta de train vs. test es lo que da el
diagnóstico:

| Síntoma | Diagnóstico | Intervención (clase 4) |
|---|---|---|
| Train loss baja, test loss sube | **Sobreajuste** | Dropout, $\ell_2$ (`weight_decay`), **aumento de datos**, red más pequeña, early stopping |
| Train loss no baja | **Subajuste** u optimización mal condicionada | Más capacidad, más épocas, revisar learning rate, normalizar entradas, revisar inicialización |
| Loss = `nan` | Gradientes explotando o `log(0)` | Bajar el learning rate, **gradient clipping**, revisar que no haya softmax duplicado |
| Loss oscila mucho | Learning rate demasiado alto o batch muy chico | Bajar `lr`, subir `batch_size`, usar scheduler |
| Loss se estanca muy pronto | Learning rate muy bajo o saturación de activaciones | Subir `lr`, revisar inicialización, usar ReLU |

```python
# Gradient clipping (clase 5): limita las explosiones, NO recupera gradientes desvanecidos
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)   # entre backward() y step()
```

## 9. Las otras arquitecturas del curso, en una línea cada una

### CNN (clase 3)
```python
class CNN(nn.Module):
    def __init__(self, n_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.head = nn.Sequential(nn.Flatten(), nn.Dropout(0.5), nn.Linear(64*7*7, n_classes))

    def forward(self, x):
        return self.head(self.features(x))
```
Nota el orden del curso: **convolucionales → pooling → fully connected**, con **dropout en las capas
densas del final**, que son "las especialmente propensas a sobreajustarse".

**Tamaño de salida:** $O = \lfloor (I - K + 2P)/S \rfloor + 1$. Con `kernel=3, padding=1, stride=1` el
tamaño se conserva, y cada `MaxPool2d(2)` lo divide por dos: 28 → 14 → 7.

### Embeddings categóricos para datos tabulados (clase 2)
```python
# Un embedding es "one-hot x matriz = seleccionar una fila", entrenado junto con el predictor
emb_marca = nn.Embedding(num_embeddings=n_marcas + 1, embedding_dim=16)  # +1 para el token UNK
# forward: torch.cat([emb_marca(idx_marca), emb_vendedor(idx_vend), x_numericas], dim=1) -> MLP
```

### RNN / LSTM / GRU (clase 5)
```python
self.rnn = nn.LSTM(input_size=d_in, hidden_size=128, num_layers=2,
                   batch_first=True, bidirectional=False, dropout=0.2)
salida, (h_n, c_n) = self.rnn(x)   # x: (B, T, d_in)
```
**`bidirectional=True` solo si toda la secuencia está disponible al predecir** — la regla de diseño de
la clase 5. Para clasificación de secuencia se usa `h_n[-1]`; para una salida por paso, `salida`.

### Transfer learning (clase 4)
```python
from torchvision import models

base = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

for p in base.parameters():          # transferencia directa: congelar el extractor
    p.requires_grad = False

base.fc = nn.Linear(base.fc.in_features, n_clases)   # cabeza nueva, entrenable
# Fine-tuning: descongelar las últimas capas y usar un learning rate MUCHO menor (p. ej. 1e-4)
```

## 10. Checklist antes de entrenar la primera red

1. **¿Qué tarea es?** Clasificación → `CrossEntropyLoss` + logits. Regresión → `MSELoss` (o `HuberLoss`
   si hay outliers).
2. **¿Qué sesgo inductivo corresponde a los datos?** Tabla → MLP + embeddings. Imagen → CNN. Secuencia
   → RNN/LSTM o Transformer. *Esta es la pregunta que el curso evalúa.*
3. **¿Están normalizadas las entradas?**
4. **¿Hay un conjunto de validación separado del test?**
5. **Sobreajusta a propósito un batch pequeño** (10-20 ejemplos) hasta loss ≈ 0. Si no lo logra, hay un
   bug: no es un problema de hiperparámetros.
6. **Parte simple:** modelo pequeño, sin dropout, learning rate por defecto. Agrega regularización
   cuando veas sobreajuste, no antes.
7. **Guarda las curvas** de train y test por época: son la evidencia que piden las tareas.
