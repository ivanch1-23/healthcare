# 4. Manual de Usuario

## Credenciales de Acceso

El sistema cuenta con **3 perfiles de usuario** con diferentes niveles de acceso:

| Rol | Usuario | Contraseña | Permisos |
|---|---|---|---|
| **Administrador** | `admin` | `Admin1234` | Acceso total: Dashboard, ETL, Pacientes, ML, Reportes, Usuarios, Admin Django |
| **Analista** | *(creación manual)* | *(definida por admin)* | Procesamiento ETL, Dashboard, Reportes (sin ML ni Usuarios) |
| **Médico** | *(creación manual)* | *(definida por admin)* | Dashboard, Pacientes, Predicción ML (sin ETL ni Reportes) |

### Cómo Iniciar Sesión

1. Abrir el navegador en **http://localhost:8000**
2. Será redirigido automáticamente a la página de login
3. Ingresar **Usuario** y **Contraseña**
4. Hacer clic en **"Ingresar"**
5. El sistema redirigirá al Dashboard principal

**Nota:** Si las credenciales son incorrectas, aparecerá un mensaje de error en rojo.

### Gestión de Roles

- **Administrador:** Acceso completo. Puede crear, editar y eliminar usuarios desde `/usuarios/`
- **Analista:** Acceso a ETL, Dashboard y Reportes. No puede ver Pacientes ni ML
- **Médico:** Acceso a Dashboard, Pacientes y ML (solo predicción). No puede ejecutar ETL

---

## Uso del Dashboard (`/`)

El Dashboard es la página principal del sistema y muestra un resumen analítico de todos los pacientes procesados.

### Tarjetas KPI (Indicadores Clave)

En la parte superior se muestran 4 tarjetas con los indicadores principales:

| Tarjeta | Descripción | Color |
|---|---|---|
| **Total Pacientes** | Número total de registros en la BD | Azul |
| **Pacientes Críticos** | Cantidad de pacientes con riesgo "Crítico" | Rojo |
| **Hipertensos** | Pacientes con presión sistólica > 140 mmHg | Naranja |
| **Diabéticos** | Pacientes con glucosa > 126 mg/dL | Púrpura |

### Gráficas Interactivas

1. **Distribución por Riesgo** (Gráfico de Barras)
   - Muestra cuántos pacientes hay en cada nivel: Bajo, Medio, Alto, Crítico
   - Colores: Verde (Bajo), Amarillo (Medio), Naranja (Alto), Rojo (Crítico)

2. **Distribución por Sexo** (Gráfico de Pastel)
   - Proporción de pacientes Masculinos vs Femeninos
   - Colores: Azul y Púrpura

3. **Distribución por Rangos de Edad** (Gráfico de Líneas)
   - Muestra la población en rangos: 0-18, 19-40, 41-60, 60+
   - Color: Púrpura con área sombreada

### Tabla de Pacientes Críticos

En la parte inferior se muestra una tabla con los últimos 10 pacientes clasificados como "Crítico", incluyendo: ID, Nombre, Edad, Sexo, Diagnóstico y Riesgo.

---

## Proceso ETL (`/etl/`)

La sección ETL permite gestionar el pipeline de extracción, transformación y carga de datos clínicos.

### Ejecutar ETL (Dataset Predeterminado)

1. Navegar a **ETL** en el menú superior
2. Hacer clic en el botón **"Ejecutar ETL"**
3. El sistema procesará los 1800 registros del dataset predeterminado
4. Al finalizar, aparecerá un modal con el mensaje "Proceso ETL completado con éxito"
5. La tabla de **Historial de Ejecuciones** se actualizará automáticamente

### Carga Manual (Archivo CSV/Excel)

1. En la sección "Carga Manual", hacer clic en **"Seleccionar archivo"**
2. Elegir un archivo CSV (`.csv`) o Excel (`.xlsx`) con la estructura clínica esperada
3. Hacer clic en **"Subir y Procesar"**
4. El sistema ejecutará el pipeline ETL sobre el archivo subido
5. El resultado se mostrará en el historial

### Historial de Ejecuciones

La tabla de historial muestra:

| Columna | Descripción |
|---|---|
| Fecha | Fecha y hora de la ejecución |
| Usuario | Usuario que ejecutó el proceso |
| Registros Leídos | Total de filas en el archivo original |
| Registros Limpios | Filas insertadas después de la limpieza |
| Duplicados | Número de duplicados eliminados |
| Tiempo (s) | Duración del proceso en segundos |
| Estado | **Exitoso** (verde) o **Fallido** (rojo) |
| Errores | Ícono de advertencia si hubo errores |

---

## Módulo de Pacientes (`/pacientes/`)

### Visualización de Pacientes

- Tabla paginada (20 pacientes por página) con todos los registros clínicos
- Columnas: ID, Nombre, Edad, Sexo, IMC, Glucosa, Presión (Sistólica/Diastólica), Riesgo
- Los niveles de riesgo tienen colores distintivos:
  - **Crítico:** Rojo
  - **Alto:** Naranja
  - **Medio:** Amarillo
  - **Bajo:** Verde

### Filtros

1. Seleccionar **Riesgo** (Bajo, Medio, Alto, Crítico o Todos)
2. Seleccionar **Sexo** (Masculino, Femenino o Todos)
3. Hacer clic en **"Filtrar"**
4. La tabla se actualizará con los resultados filtrados

### Exportación de Datos

Botones disponibles en la parte superior derecha:
- **CSV** - Exportar todos los registros a un archivo CSV
- **Excel** - Exportar a formato Excel
- **PDF** - Exportar reporte ejecutivo en PDF

---

## Machine Learning (`/ml/`)

### Entrenamiento del Modelo

1. Hacer clic en **"Entrenar Modelo Random Forest"**
2. El sistema entrenará el modelo con los datos de pacientes en la BD
3. Al finalizar, se mostrarán las métricas de rendimiento:
   - **Accuracy** (Exactitud)
   - **Precision** (Precisión)
   - **Recall** (Exhaustividad)
   - **F1-Score**

### Predicción Individual de Riesgo

1. Completar el formulario con los datos del paciente:
   - Edad, IMC, Presión Sistólica, Presión Diastólica
   - Glucosa, Colesterol, Frecuencia Cardíaca
   - Indicar si es fumador (interruptor)
2. Hacer clic en **"Predecir Riesgo"**
3. El sistema mostrará:
   - **Nivel de riesgo predicho** (Bajo, Medio, Alto, Crítico) con color indicativo
   - **Probabilidad** de la predicción en porcentaje

---

## Reportes (`/reportes/`)

### Estadísticas Globales

Tres tarjetas informativas:
1. **Total Pacientes** - Conteo global
2. **Distribución por Riesgo** - Desglose por nivel (Bajo, Medio, Alto, Crítico)
3. **Promedios Generales** - Edad promedio, Glucosa promedio, Presión Sistólica promedio

### Exportación Global

Tres botones para exportar la base de datos completa:
- **CSV** - Formato de datos abierto
- **Excel** - Hoja de cálculo formateada
- **PDF** - Documento ejecutivo profesional con KPIs y tabla de críticos

---

## Gestión de Usuarios (`/usuarios/`) - Solo Admin

### Lista de Usuarios

Tabla con todos los usuarios del sistema: ID, Username, Rol, Activo, Acciones.

### Crear Nuevo Usuario

1. Hacer clic en **"+ Nuevo Usuario"**
2. Completar el formulario:
   - **Username:** Nombre de usuario
   - **Password:** Contraseña inicial
   - **Rol:** Administrador, Médico o Analista
3. Hacer clic en **"Guardar"**

### Editar Usuario

1. Hacer clic en el botón **"Editar"** junto al usuario
2. Modificar los campos deseados
3. Dejar la contraseña en blanco para no cambiarla
4. Hacer clic en **"Guardar"**

### Eliminar Usuario

1. Hacer clic en el botón **"Eliminar"** junto al usuario
2. Confirmar la eliminación en el diálogo
3. El usuario será eliminado permanentemente

---

## Solución de Problemas Comunes

| Problema | Causa Posible | Solución |
|---|---|---|
| No carga el Dashboard | Token expirado | Cerrar sesión y volver a iniciar |
| Error "401 Unauthorized" | Token inválido o expirado | Hacer login nuevamente |
| No se ven secciones | El rol no tiene permisos | Contactar al administrador |
| ETL falla | Archivo de dataset no encontrado | Verificar que el Excel existe en `datasets/` |
| ML no predice | Modelo no entrenado | Ejecutar "Entrenar Modelo" primero |
| Error al exportar PDF | ReportLab no instalado | Ejecutar `pip install reportlab` |
