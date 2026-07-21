# R Code Examples — EPG4001 Aprendizaje Supervisado

This file contains detailed R code examples from the course complementary materials.
Use these as reference when the user asks for R code or needs to solve lab exercises.

---

## 1. Package Installation and Loading

```r
# Installation (run once)
install.packages("ISLR")
install.packages("MASS")
install.packages("tree")
install.packages("class")
install.packages("e1071")
install.packages("mlbench")
install.packages("pROC")
install.packages("caret")
install.packages("car")
install.packages("nortest")
install.packages("tseries")
install.packages("lmtest")
install.packages("faraway")
install.packages("glmnet")
install.packages("boot")
install.packages("Metrics")
install.packages("rpart")
install.packages("rpart.plot")
install.packages("randomForest")
install.packages("naivebayes")
install.packages("themis")

# Loading (every session)
library(ISLR)
library(MASS)
library(tree)
library(class)
library(e1071)
library(mlbench)
library(pROC)
library(caret)
library(car)
library(nortest)
library(tseries)
library(lmtest)
library(faraway)
```

---

## 2. Linear Regression — Complete Workflow

### 2.1 Simple Linear Regression (Investment/Return example)

```r
# Create dataset
data.inversion <- data.frame(
  inversion = c(11, 14, 16, 15, 16, 18, 20, 21, 14, 20, 19, 11),
  rendimiento = c(2, 3, 5, 6, 5, 3, 7, 10, 6, 10, 5, 6)
)

# Fit model
m1 <- lm(rendimiento ~ inversion, data = data.inversion)

# ANOVA table
anova(m1)

# Summary (coefficients, SE, significance, R²)
summary(m1)

# Results: β̂₀ = -1.6823, β̂₁ = 0.4522, R²_adj = 0.3202
# F(1,10) = 6.181, p = 0.0322
```

### 2.2 Prediction with Confidence Bands

```r
# Grid for predictions
newdata <- data.frame(
  inversion = seq(min(data.inversion$inversion),
                  max(data.inversion$inversion),
                  length.out = 200)
)

# Confidence intervals at different levels
pred90 <- predict(m1, newdata, interval = "confidence", level = 0.90)
pred95 <- predict(m1, newdata, interval = "confidence", level = 0.95)
pred99 <- predict(m1, newdata, interval = "confidence", level = 0.99)

# Plot
plot(rendimiento ~ inversion, data = data.inversion, pch = 16,
     xlab = "Inversión", ylab = "Rendimiento",
     main = "Valores Predichos con Bandas de Confianza")
grid()

# Add confidence bands
lines(newdata$inversion, pred99[, "lwr"], lty = 2, col = "red")
lines(newdata$inversion, pred99[, "upr"], lty = 2, col = "red")
lines(newdata$inversion, pred95[, "lwr"], lty = 2, col = "blue")
lines(newdata$inversion, pred95[, "upr"], lty = 2, col = "blue")
lines(newdata$inversion, pred90[, "lwr"], lty = 2, col = "darkgreen")
lines(newdata$inversion, pred90[, "upr"], lty = 2, col = "darkgreen")

# Fitted line
lines(newdata$inversion, pred95[, "fit"], lwd = 2, col = "black")

# Legend
legend("topleft",
       legend = c("Fitted line", "90% CI", "95% CI", "99% CI"),
       col = c("black", "darkgreen", "blue", "red"),
       lty = c(1, 2, 2, 2), lwd = c(2, 1, 1, 1))
```

---

## 3. Model Selection — Polynomial Regression

### 3.1 Global Warming Data

```r
data(globwarm)  # from faraway
globwarm2 <- subset(globwarm, year >= 1880)

# Plot time series
plot(globwarm2$year, globwarm2$nhtemp, type = "l", lwd = 2,
     xlim = c(1880, 2000), xlab = "Year", ylab = "Temperature",
     main = "Northern Hemisphere Temperature")
abline(h = 0, col = "red")
grid()

# Fit polynomial models
mod.lin   <- lm(nhtemp ~ year, data = globwarm2)
mod.quad  <- lm(nhtemp ~ year + I(year^2), data = globwarm2)
mod.cubic <- lm(nhtemp ~ year + I(year^2) + I(year^3), data = globwarm2)

# Compare summaries
summary(mod.lin)
summary(mod.quad)
summary(mod.cubic)

# ANOVA comparison (nested models)
anova(mod.lin, mod.quad, mod.cubic)

# Comparison table
data.frame(
  Model = c("M1", "M2", "M3"),
  AIC = c(AIC(mod.lin), AIC(mod.quad), AIC(mod.cubic)),
  BIC = c(BIC(mod.lin), BIC(mod.quad), BIC(mod.cubic)),
  Adj_R2 = c(summary(mod.lin)$adj.r.squared,
             summary(mod.quad)$adj.r.squared,
             summary(mod.cubic)$adj.r.squared)
)

# Plot with fitted lines
plot(globwarm2$year, globwarm2$nhtemp, type = "l", lwd = 2,
     xlim = c(1880, 2000), xlab = "Year", ylab = "Temperature",
     main = "Northern Hemisphere Temperature")
abline(h = 0, col = "red"); grid()
lines(globwarm2$year, predict(mod.lin), col = "blue", lwd = 2)
lines(globwarm2$year, predict(mod.quad), col = "darkgreen", lwd = 2)
lines(globwarm2$year, predict(mod.cubic), col = "purple", lwd = 2)
legend("topleft",
       legend = c("Observed", "Linear", "Quadratic", "Cubic"),
       col = c("black", "blue", "darkgreen", "purple"), lwd = 2)
```

---

## 4. Diagnostics — Checking Assumptions

### 4.1 VIF (Multicollinearity)

```r
data("PimaIndiansDiabetes")
datos.pima <- PimaIndiansDiabetes

# Fit model
m4 <- lm(glucose ~ age + mass + triceps, data = datos.pima)
summary(m4)

# Check VIF
vif(m4)  # from car package
# age: 1.02, mass: 1.19, triceps: 1.21 → all < 10, no collinearity
```

### 4.2 Autocorrelation Tests

```r
# Durbin-Watson test
dwtest(m4)       # from lmtest

# Breusch-Godfrey test
bgtest(m4)       # from lmtest

# Ljung-Box test
Box.test(residuals(m4), type = "Ljung-Box")  # base R
```

### 4.3 Homoscedasticity Tests

```r
# Visual: Ŷ vs residuals
plot(fitted(m4), residuals(m4), xlab = "Fitted", ylab = "Residuals")
abline(h = 0, col = "red")

# Goldfeld-Quandt test
gqtest(m4)       # from lmtest

# Breusch-Pagan test
bptest(m4)       # from lmtest
```

### 4.4 Normality Tests

```r
# QQ-Plot
qqnorm(residuals(m4))
qqline(residuals(m4))

# Shapiro-Wilk
shapiro.test(residuals(m4))

# Kolmogorov-Smirnov
ks.test(residuals(m4), "pnorm",
        mean = mean(residuals(m4)), sd = sd(residuals(m4)))

# Lilliefors (nortest)
lillie.test(residuals(m4))

# Anderson-Darling (nortest)
ad.test(residuals(m4))

# Jarque-Bera (tseries)
jarque.bera.test(residuals(m4))
```

---

## 5. Logistic Regression

### 5.1 Link Functions Visualization

```r
x <- seq(-5, 5, length = 500)
logit   <- plogis(x)
probit  <- pnorm(x)
cloglog <- 1 - exp(-exp(x))

plot(x, logit, type = "l", lwd = 2, col = "black",
     ylim = c(0, 1), xlab = "", ylab = "p",
     main = "Funciones de Enlace")
lines(x, probit, col = "#E95A74", lwd = 2)
lines(x, cloglog, col = "dodgerblue", lwd = 2)
abline(v = 0, lty = 2); abline(h = 0.5, lty = 2)
legend("bottomright",
       legend = c("Logit", "Probit", "CLogLog"),
       col = c("black", "#E95A74", "dodgerblue"),
       lwd = 2, bty = "o", cex = 1.2)
```

### 5.2 Simple Logistic Regression (chd ~ cigs)

```r
library(faraway)
data <- wcgs

modelo <- glm(chd ~ cigs, family = binomial(link = "logit"), data = data)
summary(modelo)

# Odds ratio
exp(coef(modelo))
# cigs OR = 1.0235 → 2.35% more risk per cigarette
```

### 5.3 Logistic Regression with Default Data

```r
datos1 <- Default

# Simple model
modelo_1 <- glm(default ~ income, family = binomial(link = "logit"), data = datos1)
summary(modelo_1)

# Multiple model
modelo_2 <- glm(default ~ income + student + balance,
                family = binomial(link = "logit"), data = datos1)
summary(modelo_2)
```

### 5.4 ROC Curve and Optimal Cutoff

```r
pred_m2 <- predict(modelo_2, type = "response")
roc_m2 <- roc(datos1$default, pred_m2)

plot(roc_m2, print.auc = TRUE, print.thres = "best",
     main = "Curva ROC para el Modelo Logístico",
     col = "blue", lwd = 2,
     xlab = "1-Especificidad", ylab = "Sensibilidad")
# Optimal cutoff: 0.031, AUC: 0.950
```

### 5.5 Confusion Matrix

```r
# Apply optimal cutoff
pred_op <- ifelse(pred_m2 > 0.031, "Yes", "No")
pred_op <- factor(pred_op, levels = c("No", "Yes"))
real <- factor(datos1$default, levels = c("No", "Yes"))

# Basic confusion matrix
table(Predicho = pred_op, Real = real)

# Manual sensitivity and specificity
mconf <- table(Predicho = pred_op, Real = real)
sens <- mconf[2, 2] / (mconf[2, 2] + mconf[1, 2])  # 0.9039
esp  <- mconf[1, 1] / (mconf[1, 1] + mconf[2, 1])   # 0.8605

# Using caret (detailed output)
confusionMatrix(pred_op, real, positive = "Yes")
```

---

## 6. Loading Datasets — Summary

```r
# ISLR datasets (load directly)
datos <- Default
datos <- Smarket

# mlbench datasets (require data() first)
data("PimaIndiansDiabetes")
datos <- PimaIndiansDiabetes

data("Vehicle")
datos <- Vehicle

# faraway datasets
data(globwarm)
data <- wcgs

# Quick exploration
head(datos)
summary(datos)
str(datos)
dim(datos)
```

---

## 7. Métricas y Validación Cruzada (Clase 4)

```r
library(boot)      # cv.glm
library(caret)     # trainControl, train, confusionMatrix
library(Metrics)   # rmse, mae, mse, f1, precision, recall
library(pROC)      # roc, auc

# --- Clasificación: métricas sobre regresión logística (Default) ---
modelo_logit <- glm(default ~ balance + income + student,
                    data = Default, family = binomial)
prob  <- predict(modelo_logit, type = "response")
y_pred <- ifelse(prob > 0.5, "Yes", "No")
y      <- Default$default

confusionMatrix(factor(y_pred), y, positive = "Yes")   # Accuracy, Sens, Espec
precision_val <- Metrics::precision(y, as.numeric(y_pred == "Yes"))
recall_val    <- Metrics::recall(y,    as.numeric(y_pred == "Yes"))
f1_val        <- 2 * precision_val * recall_val / (precision_val + recall_val)

roc_obj <- roc(y, prob)
plot(roc_obj, main = paste("Curva ROC | AUC =", round(auc(roc_obj), 3)))

# --- K-Fold con caret ---
ctrl_kfold <- trainControl(method = "cv", number = 10)
fit_kf <- train(default ~ balance + income + student, data = Default,
                method = "glm", family = binomial, trControl = ctrl_kfold)

# --- cv.glm: K-Fold y LOOCV directos sobre un glm ---
# costo basado en deviance media para clasificación
cv_loocv  <- cv.glm(Default, modelo_logit, K = nrow(Default))  # LOOCV
cv_10fold <- cv.glm(Default, modelo_logit, K = 10)             # 10-Fold
cv_10fold$delta   # delta[1] = raw, delta[2] = bias-corrected

# --- Regresión: RMSE / MAE / R2 (Advertising) ---
modelo_lm <- lm(sales ~ TV + radio + newspaper, data = Advertising)
y_hat <- predict(modelo_lm)
Metrics::rmse(Advertising$sales, y_hat)
Metrics::mae(Advertising$sales, y_hat)

# Hold-Out 70/30
set.seed(1)
idx   <- sample(nrow(Advertising), 0.7 * nrow(Advertising))
train_ad <- Advertising[idx, ]; test_ad <- Advertising[-idx, ]
m_tr  <- lm(sales ~ TV + radio + newspaper, data = train_ad)
y_pred_hold <- predict(m_tr, newdata = test_ad)
Metrics::rmse(test_ad$sales, y_pred_hold)

# Bootstrap 0.632 con caret
ctrl_boot632 <- trainControl(method = "boot632", number = 200)
```

---

## 8. Análisis Discriminante y Naive Bayes (Clase 5)

```r
library(MASS)        # lda(), qda()
library(e1071)       # naiveBayes()
library(naivebayes)  # naive_bayes()
library(caret)

datos <- data.frame(
  y  = factor(c(1,0,0,1,1,1,1,1,0,0)),
  x1 = c(9,6,1,3,3,1,9,9,4,6),
  x2 = c(6,2,6,9,7,9,8,2,6,4))

# --- Naive Bayes (e1071) ---
mod_nb <- naiveBayes(y ~ x1 + x2, data = datos)
predict(mod_nb, datos, type = "raw")          # probabilidades posteriores
predict(mod_nb, data.frame(x1 = 4, x2 = 8))   # clasifica (4,8)

# --- Naive Bayes (naivebayes) ---
mod_nb2 <- naive_bayes(y ~ x1 + x2, data = datos)

# --- LDA ---
mod_lda <- lda(y ~ x1 + x2, data = datos)
p_lda   <- predict(mod_lda, data.frame(x1 = 4, x2 = 8))
p_lda$class       # clase predicha
p_lda$posterior   # P(G=k|x)

# --- QDA ---
mod_qda <- qda(y ~ x1 + x2, data = datos)
predict(mod_qda, data.frame(x1 = 4, x2 = 8))$posterior

# --- Aplicación a Default con comparación de AUC ---
set.seed(1)
idx <- sample(nrow(Default), 0.7 * nrow(Default))
train <- Default[idx, ]; test <- Default[-idx, ]

mod_lda_def <- lda(default ~ balance + income + student, data = train)
mod_qda_def <- qda(default ~ balance + income + student, data = train)
mod_nb_def  <- naiveBayes(default ~ balance + income + student, data = train)

# AUC de cada clasificador
prob_lda <- predict(mod_lda_def, test)$posterior[, "Yes"]
roc_lda  <- pROC::roc(test$default, prob_lda)
pROC::auc(roc_lda)

# k-Fold comparando clasificadores con caret
ctrl_kf <- trainControl(method = "cv", number = 10,
                        classProbs = TRUE, summaryFunction = twoClassSummary)
fit_nb  <- train(default ~ balance + income + student, data = train,
                 method = "naive_bayes", trControl = ctrl_kf, metric = "ROC")
```

---

## 9. Árboles de Decisión y Random Forest (Clase 6)

```r
library(rpart)
library(rpart.plot)
library(randomForest)
library(mlbench)

data("PimaIndiansDiabetes")
datos <- PimaIndiansDiabetes
set.seed(1)
idx   <- sample(nrow(datos), 0.7 * nrow(datos))
train <- datos[idx, ]; test <- datos[-idx, ]

# --- Árbol de CLASIFICACIÓN ---
tree_class <- rpart(diabetes ~ ., data = train, method = "class")
rpart.plot(tree_class, type = 2, extra = 104)
pred_class <- predict(tree_class, test, type = "class")
caret::confusionMatrix(pred_class, test$diabetes, positive = "pos")

# Poda por complejidad de costes (elige cp por CV)
printcp(tree_class)                      # tabla de cp y xerror (CV)
cp_opt <- tree_class$cptable[which.min(tree_class$cptable[, "xerror"]), "CP"]
tree_pruned <- prune(tree_class, cp = cp_opt)

# --- Árbol de REGRESIÓN ---
tree_reg <- rpart(glucose ~ pregnant + pressure + triceps + mass + age,
                  data = train, method = "anova")
rpart.plot(tree_reg, type = 2, fallen.leaves = TRUE)

# --- Random Forest ---
rf <- randomForest(diabetes ~ ., data = train, ntree = 500, importance = TRUE)
rf                                  # OOB error
varImpPlot(rf)                      # importancia de variables
pred_rf <- predict(rf, test)
caret::confusionMatrix(pred_rf, test$diabetes, positive = "pos")
```

---

## 10. SVM, Clases Desbalanceadas y KNN (Clase 7)

```r
library(e1071)   # svm(), tune()
library(class)   # knn()
library(caret)   # confusionMatrix, trainControl, train
library(themis)  # SMOTE (via recipes / caret sampling)
library(pROC)

# --- SVM lineal ---
mod_svm_lin <- svm(y ~ x1 + x2, data = dat_svm,
                   kernel = "linear", cost = 1, scale = TRUE,
                   probability = TRUE)
pred <- predict(mod_svm_lin, dat_svm)

# Selección del costo C por CV (tune)
tune_lin <- tune(svm, y ~ x1 + x2, data = dat_svm,
                 kernel = "linear",
                 ranges = list(cost = c(0.01, 0.1, 1, 5, 10)),
                 tunecontrol = tune.control(cross = 5))
tune_lin$best.parameters      # mejor C
mod_best <- tune_lin$best.model

# --- SVM kernel radial (RBF): ajusta cost y gamma ---
tune_rbf <- tune(svm, y ~ x1 + x2, data = dat_circ,
                 kernel = "radial",
                 ranges = list(cost = c(0.1, 1, 10), gamma = c(0.5, 1, 2)),
                 tunecontrol = tune.control(cross = 5))
tune_rbf$best.parameters

# SVM con caret (kernel radial)
ctrl_svm <- trainControl(method = "cv", number = 5,
                         classProbs = TRUE, summaryFunction = twoClassSummary)
fit_svm <- train(y ~ ., data = train, method = "svmRadial",
                 trControl = ctrl_svm, metric = "ROC")

# --- Clases desbalanceadas: SMOTE dentro de la CV (solo en train) ---
ctrl_smote <- trainControl(method = "cv", number = 5,
                           classProbs = TRUE, summaryFunction = twoClassSummary,
                           sampling = "smote")   # "up" / "down" también disponibles
set.seed(123)
mod_smote <- train(default ~ balance + income, data = train_d,
                   method = "glm", family = binomial(),
                   trControl = ctrl_smote, metric = "ROC")
pi_smote  <- predict(mod_smote, newdata = test_d, type = "prob")[, "Yes"]

# --- Probabilidad de corte óptima (igualar sensibilidad y especificidad) ---
roc_obj <- roc(y_test_bin, pi_smote)
coords(roc_obj, "best", best.method = "closest.topleft")  # umbral, sens, espec

# --- KNN ---
# Estandarizar predictores (escalas distintas)
train_X <- scale(train[, c("x1", "x2")])
test_X  <- scale(test[,  c("x1", "x2")],
                 center = attr(train_X, "scaled:center"),
                 scale  = attr(train_X, "scaled:scale"))
pred_k1 <- knn(train = train_X, test = test_X, cl = train$y, k = 1)
pred_k5 <- knn(train = train_X, test = test_X, cl = train$y, k = 5)

# Elegir k por CV con caret
ctrl_knn <- trainControl(method = "cv", number = 5)
fit_knn <- train(y ~ ., data = train, method = "knn",
                 trControl = ctrl_knn,
                 tuneGrid = data.frame(k = c(5, 10, 15, 20, 30)))
fit_knn$bestTune
```
