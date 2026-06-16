# 5. Diagramas del Sistema

Los siguientes diagramas están codificados en formato Mermaid para que GitHub los renderice nativamente como diagramas visuales en su visor web o en tu editor si cuenta con previsualización.

## 1. Arquitectura del Sistema (Cliente-Servidor)

```mermaid
graph TD
    A[Navegador del Usuario] -->|Peticiones HTTP/Fetch| B(Servidor Web Django)
    B -->|Manejo de Rutas y Permisos| C{Controlador / Vistas}
    C -->|Consultas ORM| D[(Base de Datos SQLite/PostgreSQL)]
    C -->|Servicios ML| E[Motor Scikit-Learn]
    C -->|Datos JSON| A
    E -->|Modelo Joblib| F(Archivo modelo.pkl)
    B -->|Renderiza HTML| A
```

## 2. Flujo del Proceso ETL

```mermaid
flowchart LR
    A[Archivo Excel / CSV] -->|Subida HTTP o Archivo Local| B(Extracción: Pandas)
    B --> C{Transformación: Limpieza}
    C -->|Eliminación de Nulos| D[Imputación]
    D -->|Conversión de Tipos| E[Cálculo de Variables: IMC]
    E -->|Motor Clínico| F[Clasificación: Riesgo Enfermedad]
    F -->|Mapeo Django ORM| G[(Carga a BD: bulk_create)]
    G --> H[Registro de Historial ETL Exitoso]
```

## 3. Modelo Entidad-Relación (Base de Datos)

```mermaid
erDiagram
    USUARIOS {
        int id PK
        string username
        string password
        string rol "admin, medico, analista"
    }
    
    PACIENTE_CLINICO {
        int id_paciente PK
        string nombres
        string apellidos
        int edad
        string sexo
        float peso
        float altura
        float IMC
        float glucosa
        int presion_sistolica
        int presion_diastolica
        string riesgo_enfermedad "Crítico, Alto, Medio, Bajo"
        string diagnostico_preliminar
    }
    
    HISTORIAL_ETL {
        int id PK
        datetime fecha_ejecucion
        int registros_procesados
        string estado "Exitoso, Fallido"
        int usuario_id FK
    }

    USUARIOS ||--o{ HISTORIAL_ETL : "Ejecuta"
```
