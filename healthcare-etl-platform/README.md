# Healthcare ETL Platform 🏥📊

Una plataforma integral diseñada con **Django** que unifica la extracción, transformación y carga (ETL) de datos clínicos masivos, análisis estadístico en tiempo real, e inteligencia artificial para la predicción de riesgos de enfermedades, complementada por un Dashboard visual interactivo y documentación automática de API.

---

## 🏗️ Arquitectura del Sistema

El sistema está construido con un Backend robusto en **Django REST Framework** y un Frontend renderizado desde el mismo servidor usando **Django Templates, Bootstrap 5 y Chart.js**. Todo asegurado bajo JWT.

```mermaid
graph TD;
    A[Archivos Crudos (CSV/Excel)] -->|Upload| B(Motor ETL)
    B -->|Limpieza e Imputación| C[(PostgreSQL / SQLite)]
    C -->|Alimenta| D[Módulo Analytics]
    C -->|Entrena| E[Random Forest ML]
    D --> F[REST API Endpoints]
    E --> F
    F -->|Consumo (fetch JS)| G[Frontend Dashboard]
    G -->|Protegido por| H((JWT Auth))
```

---

## 🛠️ Requisitos Previos

- Python 3.9+
- Pip (Gestor de paquetes de Python)
- PostgreSQL (opcional, si decides no usar SQLite)
- Docker y Docker Compose (opcional para despliegue contenerizado)

---

## 🚀 Pasos de Instalación (Entorno Local)

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/healthcare-etl-platform.git
   cd healthcare-etl-platform
   ```

2. **Crear e instalar el entorno virtual**:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   
   cd backend
   pip install -r requirements.txt
   ```

3. **Configurar Variables de Entorno (`.env`)**:
   Renombra `.env.example` a `.env` en la raíz del proyecto.
   Si no tienes PostgreSQL instalado o deseas probar rápidamente, asegúrate de configurar SQLite editando tu `settings.py` temporalmente, o asegúrate de que tu PostgreSQL local concuerda con las credenciales del `.env`.

4. **Correr las Migraciones**:
   ```bash
   python manage.py migrate
   ```

5. **Comando Mágico de Inicialización (Seed)**:
   Prepara la base de datos con un usuario administrador por defecto (`admin` / `admin123`), ejecuta el proceso ETL con el dataset proporcionado y entrena el modelo Random Forest automáticamente:
   ```bash
   python manage.py seed
   ```

6. **Levantar el Servidor**:
    ```bash
    python manage.py runserver
    ```
    *Accede a [http://localhost:8000](http://localhost:8000) en tu navegador.*

---

## Render Deployment

El proyecto queda preparado para desplegarse en Render con PostgreSQL, Gunicorn y WhiteNoise.

### Soporte incluido

- `render.yaml` en la raiz del repositorio para crear el servicio web y la base de datos.
- `DATABASE_URL` en `backend/config/settings.py` para usar PostgreSQL de Render.
- WhiteNoise para servir archivos estaticos en produccion.
- Gunicorn como servidor WSGI.
- `python backend/manage.py seed --skip-if-loaded` para crear usuarios base y cargar el dataset solo si no existen pacientes.

### Pasos en Render

1. En Render, selecciona **New +** y luego **Blueprint**.
2. Conecta el repositorio `ivanch1-23/healthcare`.
3. Render detectara `render.yaml` y creara:
   - servicio web `healthcare-etl-platform`
   - base de datos PostgreSQL `healthcare-etl-db`
4. Antes o despues del primer deploy, configura estas variables con tu dominio real:
   - `CSRF_TRUSTED_ORIGINS=https://tu-servicio.onrender.com`
   - `CORS_ALLOWED_ORIGINS=https://tu-servicio.onrender.com`
5. Ejecuta el deploy.

### Comandos usados por Render

Build command:
```bash
pip install -r backend/requirements.txt && python backend/manage.py collectstatic --noinput
```

Start command:
```bash
python backend/manage.py migrate && python backend/manage.py seed --skip-if-loaded && gunicorn --chdir backend config.wsgi:application --bind 0.0.0.0:$PORT
```

### Credenciales iniciales

- `admin` / `admin123`
- `analista` / `admin123`
- `medico` / `admin123`

---

## 🔗 Endpoints de la API REST

El proyecto cuenta con Swagger UI auto-generado gracias a `drf-spectacular`. Puedes explorar y probar todos los endpoints visitando: **[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)**

| Módulo | Método | Endpoint | Descripción |
| :--- | :--- | :--- | :--- |
| **Auth** | POST | `/api/auth/login/` | Autenticación y obtención de JWT. |
| **Auth** | GET | `/api/auth/me/` | Retorna el rol y datos del usuario actual. |
| **ETL** | POST | `/api/etl/run/` | Ejecuta el ETL sobre el dataset predeterminado. |
| **ETL** | POST | `/api/etl/upload/` | Sube un CSV/Excel e inserta datos clínicos. |
| **ETL** | GET | `/api/etl/pacientes/` | Lista paginada de pacientes con filtros de riesgo. |
| **Analytics**| GET | `/api/analytics/kpis/` | Retorna los indicadores estadísticos clave. |
| **ML** | POST | `/api/ml/entrenar/` | Re-entrena el Random Forest Classifier. |
| **ML** | POST | `/api/ml/predecir/` | Realiza una predicción individual de riesgo. |
| **Reports** | GET | `/api/reportes/exportar/` | Genera CSV, Excel, o PDF Ejecutivo del sistema. |

---

## 📸 Interfaz Frontend

*(Reemplaza los placeholders con tus propias capturas de pantalla)*

### Dashboard Analítico y Tablas Dinámicas
![Dashboard UI](https://via.placeholder.com/800x400?text=Captura+del+Dashboard+Analítico)

### Panel ETL y Machine Learning
![ETL y ML](https://via.placeholder.com/800x400?text=Captura+de+Panel+ETL+e+IA)

---

## 🗄️ Modelo de Base de Datos (ERD ASCII)

```text
+-----------------------+       +-----------------------+       +-----------------------+
|      CustomUser       |       |    RegistroETL        |       |    PacienteClinico    |
+-----------------------+       +-----------------------+       +-----------------------+
| id (PK)               | 1   N | id (PK)               |       | id_paciente (PK)      |
| username              |-------| fecha                 |       | nombres               |
| email                 |       | registros_procesados  |       | apellidos             |
| rol                   |       | registros_limpios     |       | edad                  |
| is_staff              |       | estado                |       | sexo                  |
| is_active             |       | tiempo_ejecucion      |       | glucosa               |
+-----------------------+       | usuario_fk (FK)       |       | presion_sistolica     |
                                +-----------------------+       | riesgo_enfermedad     |
                                                                | diagnostico_preliminar|
                                                                +-----------------------+
```

## 🔄 Flujo del Pipeline ETL

```text
1. EXTRACT 
   └── Lectura de archivo (pandas) 
       └── Captura de métricas iniciales (total filas).
   
2. TRANSFORM
   ├── 2.1 Eliminación de Duplicados (por id_paciente).
   ├── 2.2 Limpieza y Parseo Numérico (Edades de texto a int).
   ├── 2.3 Estandarización Textual (M, Masc -> Masculino).
   ├── 2.4 Imputación de Nulos (Medianas para valores faltantes).
   └── 2.5 Normalización y validación estricta del Schema.
   
3. LOAD
   ├── Inserción optimizada en BD usando `bulk_create`.
   └── Generación de LOG (RegistroETL) documentando el éxito o errores.
```
