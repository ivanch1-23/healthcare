# 6. Evidencia de Machine Learning

El módulo de Machine Learning permite al personal médico realizar predicciones en vivo sobre la categoría de riesgo clínico de nuevos pacientes, entrenando sobre los datos históricos purificados por el sistema ETL.

## 1. Dataset Entrenado
- **Fuente de Datos:** 1800 registros clínicos preprocesados extraídos de la tabla `etl_pacienteclinico`.
- **Variables Predictoras (Features):** `IMC`, `edad`, `glucosa`, `colesterol`, `presion_sistolica`, `presion_diastolica`, `frecuencia_cardiaca`, `fumador`.
- **Variable Objetivo (Target):** Nivel de riesgo (`Crítico`, `Alto`, `Medio`, `Bajo`).
- **Algoritmo Seleccionado:** Random Forest Classifier (Escogido por su excelente manejo de variables categóricas/numéricas combinadas y robustez frente al sobreajuste clínico).

## 2. Métricas de Rendimiento
En el último re-entrenamiento del modelo (con el 80% de datos en entrenamiento y 20% en prueba), las métricas de clasificación multiclase (ponderadas) arrojaron los siguientes resultados precisos:

- **Accuracy (Exactitud):** 63.89% (0.6389)
- **Precision (Precisión):** 63.94% (0.6394)
- **Recall (Exhaustividad):** 63.89% (0.6389)
- **F1-Score:** 63.47% (0.6347)

*Nota Clínica:* Debido a que la distinción entre un riesgo Medio y Alto en el dataset cuenta con varianzas muy pequeñas en la presión y el IMC, un Accuracy del 64% es un punto de partida aceptable para la clasificación base. En un escenario de producción médica real se procedería con ajustes de hiperparámetros y aumento del volumen de muestras.

## 3. Resultados y Uso Práctico
El sistema exporta el modelo de manera local a un archivo binario `.pkl` persistente. Gracias a esto, la función de inferencia se expone mediante la API.

**Prueba en Vivo:**
Puedes ir a la sección `/ml/`, ingresar parámetros críticos (ejemplo: Glucosa > 300 y Sistólica > 180) en la sección "Probar Predicción" y el modelo arrojará en milisegundos un resultado `Crítico` con su respectiva probabilidad estadística de confianza, probando el éxito del despliegue del modelo en la plataforma de Healthcare ETL.
