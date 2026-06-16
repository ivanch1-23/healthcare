# 2. Evidencias del Proceso ETL

El proceso de Extracción, Transformación y Carga (ETL) fue diseñado para consumir el archivo `healthcare_dataset.csv` de manera robusta y limpia.

## 1. Capturas de Pantalla (Instrucciones)
Para recopilar tus capturas de pantalla para el entregable, te recomendamos tomar capturas de las siguientes secciones:
1. **Módulo ETL (`/etl/`)**: Captura la pantalla después de presionar "Ejecutar ETL", mostrando la tabla del historial con estado "Exitoso" y la métrica de *1800 registros creados*.
2. **Dashboard (`/`)**: Toma captura de los KPIs principales (Total: 1800) y de las gráficas (Riesgo, Sexo) con su nuevo diseño profesional.
3. **Módulo Pacientes (`/pacientes/`)**: Muestra la paginación y la tabla final procesada, demostrando que los datos están estructurados correctamente.

## 2. Reportes Generados
El ETL limpió los siguientes datos en su última ejecución:
- **Total Registros Procesados:** 1800
- **Limpieza Ejecutada:** 
  - Corrección de valores nulos o atípicos.
  - Normalización de textos y cálculos de nuevos campos como el `IMC` en base a altura y peso.
  - Generación de la columna calculada `riesgo_enfermedad` aplicando las reglas de negocio médicas estrictas (presión, glucosa, saturación).

## 3. Descarga de Evidencias Físicas
Dirígete a la pestaña **Reportes (`/reportes/`)** y utiliza los botones interactivos (CSV, Excel o PDF) para descargar la base de datos completa ya transformada. Ese archivo en formato PDF o Excel sirve como evidencia física generada por el sistema.
