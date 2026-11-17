# Clase 05 — Eficiencia paralela (Amdahl, Gustafson, escalabilidad)

**IMT3870**, Prof. Ignacio Labarca. Fuente: `Presentaciones/clase05.pdf` (35 láminas), lunes 2 de
noviembre.

**Agenda:** ¿cómo analizar el rendimiento de un algoritmo paralelo? Speedup, eficiencia y overhead ·
Ley de Amdahl · Ejemplo: reducción paralela · Ley de Gustafson · Escalabilidad fuerte y débil.

**Motivación:**
- Un algoritmo **casi nunca es 100 % paralelizable**.
- En la práctica la **eficiencia normalmente baja** con más procesos o hilos.
- ¿Qué tan eficiente es el algoritmo paralelo? ¿Cómo elegir el número de procesos o hilos a usar?

---

## 1. ¿Qué es un *worker*?

Un **worker** es la **unidad de ejecución paralela**. Depende del contexto:
- Un **proceso**: `multiprocessing`, `joblib`.
- Un **hilo**: librerías compiladas como **NumPy**.
- Un **nodo completo** de un clúster.

> En **joblib, p corresponde a `n_jobs`**.

**Las métricas de rendimiento son las mismas en todos los casos.**

---

## 2. Speedup y eficiencia

Con un solo worker el tiempo es **T₁**. En el **caso ideal**, p workers reparten el trabajo
equitativamente:

```
T_p^ideal = T₁ / p
```

En la práctica **T_p > T₁/p**. El speedup y la eficiencia miden **qué tan lejos estamos del ideal**.

**Speedup (aceleración):**
```
S_p = T₁ / T_p
```

**Eficiencia:**
```
E_p = S_p / p = T₁ / (p · T_p)
```

> **E_p es la fracción del tiempo en que cada worker hace trabajo útil.**

Nos gustaría que con p procesadores el programa sea p veces más rápido (**S_p = p**), lo que
corresponde a **eficiencia del 100 %** (**E_p = 1**). Esto **no es cierto en la práctica**: en general

```
S_p ≤ p
```

y de hecho **el speedup suele ser mucho menor**.

**Analogía de clase:** nos demoramos 8 horas en terminar una tarea difícil; repartiendo el trabajo
entre **dos** personas tardamos 5 horas; repartiéndolo entre **10** podríamos demorarnos **más de un
día**.

### 2.1 Speedup superlineal
Excepcionalmente se observa **S_p > p**:
- Con **p = 1**, el problema completo **no cabe en caché**.
- Con **p workers**, cada **subproblema es p veces más pequeño**.
- Cada subproblema **sí cabe en caché**.
- Los accesos a memoria **se aceleran más que linealmente**.

### 2.2 Advertencia metodológica
Speedup y eficiencia son **medidas crudas**, porque influyen varios efectos: **capacidad de
almacenamiento**, **transferencia de datos**, **arquitectura de computadores** y **optimizaciones
algorítmicas**.

> **T₁ debe medirse con el mejor código secuencial disponible.** (Si no, el speedup se infla.)

---

## 3. Overhead paralelo

Si el speedup no es perfecto, el **tiempo total de los p workers supera al trabajo serial**. El
**overhead paralelo** es

```
T₀ = p · T_p − T₁  ≥ 0
```

- **T₀ = 0**: caso **ideal**, todo es trabajo útil.
- **T₀ > 0**: tiempo perdido en **coordinación, esperas y trabajo redundante**.

Un algoritmo es **cost-optimal** si **p·T_p = O(T₁)**.

### ¿Qué limita el speedup?
- **Parte serial:** lo que no se paraleliza **impone un techo**.
- **Comunicación y sincronización:** su **costo crece con p**.
- **Desbalance de carga:** los workers rápidos **esperan al más lento**.

### 3.1 Balance de carga
Si el trabajo se reparte de forma desigual:
- Algunos workers **terminan antes y quedan ociosos**.
- **El tiempo total lo determina el worker más lento.**
- **La eficiencia cae aunque haya speedup.**

---

## 4. Ley de Amdahl

**Supuesto clave: el tamaño del problema es fijo.**

Todo programa tiene una **fracción serial f** que **no puede paralelizarse**. El tiempo serial se
divide en una parte serial y una paralelizable:

```
T₁ = f·T₁ + (1 − f)·T₁
```

El tiempo paralelo es **al menos**

```
T_p ≥ f·T₁ + (1 − f)·T₁ / p
```

**La ley de Amdahl acota el speedup:**

```
            1
S_p ≤ ───────────────
      f + (1 − f)/p
```

### 4.1 El límite asintótico
Cuando **p → ∞**:

```
S_∞ ≤ 1 / f
```

**Existe un límite para la aceleración.** Con **f = 5 %**:

| p | S_p |
|---|-----|
| 10 | ≈ 6,9 |
| 100 | ≈ 16,8 |
| 1000 | ≈ 19,6 |

> **El speedup nunca supera 20×, sin importar p.**

### 4.2 Amdahl con comunicación
Si agregamos el costo de comunicación:

```
T_p = T₁ · ( f + (1 − f)/p ) + T_com
```

- **T_com suele crecer con p.**
- **El speedup puede *disminuir* al agregar procesadores.**
- **Existe un número óptimo de procesadores.**

### 4.3 Ejemplo: recurrencia (f = 1)

```python
x = np.empty(n)
x[0] = 1.0
for i in range(1, n):
    x[i] = 0.99 * x[i - 1] + 1.0
```
**Cada iteración depende de la anterior** → la fracción serial es **f = 1**. Para cualquier p:
**S_p ≤ 1**.

### 4.4 Ejemplo: inicialización + cómputo (f → 0)

```python
x = np.empty(n)
x[0] = 1.0
for i in range(1, n):
    x[i] = 0.99 * x[i - 1] + 1.0

for i in range(n):
    for j in range(n):
        A[i, j] = x[i] + x[j]
```

- **Inicialización:** n operaciones **seriales**.
- **Cómputo de A:** n² operaciones **paralelizables**.

```
f = n / (n + n²) = 1 / (1 + n)
```

**Para n grande, f → 0 y S_p puede acercarse a p.**

### 4.5 Lecciones
- **Reducir la fracción serial importa más que agregar workers.**
- **Pequeñas porciones seriales limitan el speedup global.**
- **La ley de Amdahl es pesimista:** asume **tamaño de problema fijo**.

---

## 5. Ejemplo central: la reducción paralela

Tenemos un arreglo `x` de largo n:

```python
total = 0.0
for i in range(n):
    total += x[i]
```

¿Es esto paralelizable? **Cada suma depende del valor anterior de `total`** → es necesario **modificar
el algoritmo**.

**Idea:** cada worker suma **n/p** elementos y luego **se combinan las sumas parciales**.

```
x0..x3  → worker 0 → s0 ┐
x4..x7  → worker 1 → s1 ├─ Etapa 2: p − 1 sumas  → s0+s1+s2+s3
x8..x11 → worker 2 → s2 │
x12..x15→ worker 3 → s3 ┘
         Etapa 1: n/p sumas
```

**Análisis:** cada worker suma n/p elementos; **uno solo acumula los p resultados**.

```
T₁  = n
T_p = n/p + (p − 1)
```

> **Notar que la fracción serial depende de p.** (Amdahl con f constante no aplica directamente.)

```
              n                              1
S_p = ───────────────        E_p = ────────────────────
       n/p + p − 1                  1 + p(p − 1)/n
```

**¿Cuándo hay eficiencia constante?** ⇒ **p² ≈ n**, es decir **p ≈ √n**.

---

## 6. Escalabilidad paralela y Ley de Gustafson

**Observación:** los problemas **a gran escala** suelen tener **más posibilidades de paralelizar**. La
**parte escalable** de un código a menudo es **más fácil de paralelizar**:
- **Código secuencial:** entrada, salida, etc.
- **Código paralelo:** álgebra lineal, ordenar, etc.

### 6.1 El cambio de pregunta
- **Amdahl:** fijo el trabajo y aumento p ⇒ **speedup acotado**.
- En la práctica, **la fracción serial depende del tamaño del problema**.
- **Gustafson:** fijo el **tiempo T_p** y **aumento el tamaño con p**. *¿Cuánto más puedo resolver en
  el mismo tiempo?*

### 6.2 Derivación

Sea **T_p** el tiempo **medido con p procesadores**:
- **f**: fracción de **ese** tiempo en la parte serial → **T_ser = f·T_p**
- **1 − f**: fracción en la parte paralela → **T_par = (1 − f)·T_p**

Con **un solo procesador**, la parte paralela tardaría **p veces más**:

```
T₁ = f·T_p + p·(1 − f)·T_p
```

**Speedup para el problema escalado:**

```
S_p = T₁/T_p = ( f·T_p + p(1 − f)·T_p ) / T_p = p − (p − 1)·f
```

Cuando **p → ∞**: **S_p = O(p)**, **E_p = O(1)**.

**Comparación con f = 5 % y p = 100:**
- **Gustafson: S_p ≈ 95**
- **Amdahl: S_p ≈ 16,8**

### 6.3 Las dos leyes, lado a lado

| | Dirección | Tamaño | S_p | E_p |
|---|---|---|---|---|
| **Amdahl** | código para **1** procesador → tiempo en **p** | **fijo** | **O(1)** | **O(1/p)** |
| **Gustafson** | código para **p** procesadores → tiempo en **1** | **crece con p** | **O(p)** | **O(1)** |

> **Escalar el problema junto con p permite mantener la eficiencia.**

---

## 7. Escalabilidad fuerte y débil

**Escalabilidad fuerte (*strong scaling*):**
- Mantener el **tamaño del problema fijo** y **aumentar p**.
- Es el escenario de la **ley de Amdahl**.
- Hay escalabilidad fuerte si **N ≡ const, p → ∞ ⇒ E_p ≈ const**.

**Escalabilidad débil (*weak scaling*):**
- Mantener el **trabajo por procesador fijo** y aumentar p.
- Es el escenario de la **ley de Gustafson**.
- Hay escalabilidad débil si **N/p ≡ const, p → ∞ ⇒ E_p ≈ const**.

**Problema práctico de medición:** medir E_p en escalabilidad débil **requeriría correr el problema
completo con 1 procesador**. En la práctica se mide la **eficiencia débil**:

```
E_débil = T₁(N/p) / T_p(N) ≈ 1
```

---

## Resumen de la clase
- **Speedup, eficiencia y overhead paralelo.**
- **Fracción serial, comunicación y desbalance de carga.**
- **Ley de Amdahl:** tamaño fijo, speedup acotado por **1/f**.
- **Ley de Gustafson:** tamaño crece con p.
- **Escalabilidad fuerte y débil.**

**Próxima clase:** acceso a memoria paralela y localidad de datos.
