# 2. Evidencias del Proceso ETL

## Descripción del Pipeline ETL

El motor ETL (`apps/etl/services/etl_engine.py`) procesa el archivo `dataset_clinico_etl_1800_registros.xlsx` que contiene **1800 registros** de pacientes clínicos. El pipeline sigue 3 fases:

### Fase 1: EXTRACT (Extracción)
- Lee el archivo Excel usando `pandas.read_excel()`
- Registra metadatos: nombre del archivo, tipo, número de filas extraídas, columnas detectadas
- **Resultado:** DataFrame de Pandas con los datos crudos

### Fase 2: TRANSFORM (Transformación)
Aplica 10 pasos de limpieza y transformación:

| Paso | Acción | Detalle |
|---|---|---|
| 1 | Normalización de columnas | Elimina tildes de nombres de columnas (Ej: `presión_sistólica` → `presion_sistolica`) |
| 2 | Eliminación de duplicados | `drop_duplicates(subset=['id_paciente'], keep='first')` |
| 3 | Conversión de edad | `pd.to_numeric()` con imputación de mediana para valores no numéricos |
| 4 | Conversión de presiones | Limpieza de valores no numéricos, imputación con mediana |
| 5 | Estandarización de sexo | `M`, `Masculino`, `Male` → `M`; `F`, `Femenino`, `Female` → `F` |
| 6 | Normalización de diagnósticos | Corrección ortográfica y unificación de términos médicos |
| 7 | Remoción de outliers clínicos | Pesos > 300kg, temperatura <30°C o >42°C, glucosa fuera de rango, etc. |
| 8 | Imputación de nulos | Media para glucosa/colesterol/peso/altura; 36.5°C para temperatura; mediana para saturación |
| 9 | Cálculo de IMC | `IMC = peso / altura²` |
| 10 | Cálculo de riesgo | Algoritmo basado en umbrales clínicos (presión, glucosa, saturación, IMC, fumador) |

### Fase 3: LOAD (Carga)
- Elimina registros previos de `PacienteClinico`
- Inserta los datos transformados usando `bulk_create` (inserción optimizada)
- Genera un registro en `RegistroETL` documentando: fecha, usuario, registros procesados, limpios, duplicados eliminados, tiempo de ejecución, estado y errores

---

## Resultados del Procesamiento

Tras ejecutar el ETL sobre el dataset de 1800 registros:

| Métrica | Valor |
|---|---|
| Registros procesados | **1800** |
| Registros limpios insertados | **1800** |
| Duplicados eliminados | **0** |
| Estado | **Exitoso** |
| Tiempo de ejecución | Variable (~2-5 segundos) |

---

## Capturas de Pantalla (Guía)

Para generar las capturas de pantalla como evidencia visual:

### 1. Módulo ETL (`/etl/`)
- Ingresar con usuario `admin` / `Admin1234`
- Navegar a la sección **ETL** en la barra de navegación
- Hacer clic en **"Ejecutar ETL"**
- **Capturar:** El modal de confirmación "Proceso ETL completado con éxito" y la tabla de historial mostrando la ejecución con estado "Exitoso" y 1800 registros

### 2. Dashboard (`/`)
- Navegar al Dashboard principal
- **Capturar:** Las 4 tarjetas KPI (Total Pacientes: 1800, Pacientes Críticos, Hipertensos, Diabéticos)
- **Capturar:** Las 3 gráficas (Distribución por Riesgo, por Sexo, por Rangos de Edad)
- **Capturar:** La tabla de "Últimos Pacientes Críticos"

### 3. Módulo Pacientes (`/pacientes/`)
- Navegar a la sección **Pacientes**
- **Capturar:** La tabla paginada mostrando los pacientes procesados con su información clínica

### 4. Exportación de Reportes
- Navegar a la sección **Reportes** (`/reportes/`)
- **Capturar:** Las tarjetas de estadísticas globales
- Hacer clic en cada botón de exportación (CSV, Excel, PDF)

---

## Reportes Generados

El sistema permite generar reportes en 3 formatos desde la sección Reportes o Pacientes:

### 1. Reporte CSV (`GET /api/reportes/exportar/?formato=csv`)
- Archivo de texto plano con todos los campos de pacientes
- Delimitado por comas, con cabecera
- Descargable como `pacientes.csv`

### 2. Reporte Excel (`GET /api/reportes/exportar/?formato=excel`)
- Archivo de Excel con los datos completos de pacientes
- Hoja: "Pacientes"
- Descargable como `pacientes.xlsx`

### 3. Reporte PDF Ejecutivo (`GET /api/reportes/exportar/?formato=pdf`)
- Documento PDF profesional con:
  - Título: "Reporte Ejecutivo de Pacientes Clínicos"
  - KPIs principales (Total, Críticos, Hipertensos, Diabéticos, Fumadores, Riesgo Promedio)
  - Tabla de últimos 10 pacientes críticos
- Descargable como `reporte_ejecutivo.pdf`

---

## Verificación de Calidad de Datos

El script `backend/verify_etl.py` realiza 10 validaciones automáticas para garantizar la integridad del ETL:

```python
# Ejemplo de ejecución:
# python manage.py shell < verify_etl.py

1. TOTAL REGISTROS EN BD: 1800
2. REGISTROS CON NULOS: 0
3. VALORES DE SEXO: Solo M y F
4. DIAGNÓSTICOS CON ERRORES ORTOGRÁFICOS: 0
5. PESO OUTLIERS >300kg: 0
6. TEMPERATURA OUTLIERS <30°C o >42°C: 0
7. IDS DUPLICADOS: 0
```

---

## Evidencia de Ejecución en Servidor

El servidor está corriendo actualmente en:
- **URL:** http://localhost:8000
- **Estado:** HTTP 200 OK
- **Puerto:** 8000
- **Base de datos:** SQLite (`backend/db.sqlite3`)
