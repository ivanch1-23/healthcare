# 3. Documentación Técnica

## Arquitectura del Sistema
El proyecto está implementado bajo un patrón de arquitectura **Cliente-Servidor (MVC/MVT)** usando el framework Django.
- **Backend (API + Vistas):** Desarrollado en Python con Django. Expone servicios RESTful y sirve plantillas HTML del lado del servidor utilizando el sistema de plantillas integrado.
- **Base de Datos:** SQLite / PostgreSQL (según entorno).
- **Frontend:** Implementado utilizando HTML5, CSS3, JavaScript Vainilla y Bootstrap 5 para garantizar responsividad. Utiliza *Fetch API* nativo para comunicarse asíncronamente con los microservicios y *Chart.js* para renderizar las métricas.
- **Machine Learning:** `scikit-learn` corriendo en Python, el cual lee los registros desde el ORM de Django, entrena un Random Forest y guarda el modelo serializado mediante `joblib`.

## Despliegue en la Nube (Guía)
Para desplegar este proyecto en una plataforma gratuita (Platform-as-a-Service) como Render o Heroku:

1. **Configurar Entorno de Producción (`settings.py`)**:
   - Cambiar `DEBUG = False`.
   - Modificar `ALLOWED_HOSTS = ['tu-app.onrender.com']`.
   - Configurar la base de datos para usar variables de entorno `DATABASE_URL`.
2. **Requisitos Adicionales**:
   - Instalar `gunicorn` (servidor de producción): `pip install gunicorn`.
   - Instalar `whitenoise` para servir archivos estáticos.
3. **Archivo de Despliegue**:
   - Si usas Render, crear un archivo `build.sh`:
     ```bash
     pip install -r requirements.txt
     python manage.py collectstatic --no-input
     python manage.py migrate
     ```
   - Iniciar comando en el panel de control: `gunicorn backend.wsgi:application`.

## Documentos y APIs
El sistema expone diversos endpoints utilizados asíncronamente:
- `POST /api/etl/run/`: Dispara el motor ETL para cargar los 1800 registros de Excel a BD.
- `POST /api/etl/upload/`: Procesa y carga archivos CSV/Excel externos enviados por el usuario.
- `GET /api/analytics/kpis/`: Retorna conteos globales y distribución por riesgo.
- `GET /api/analytics/estadisticas/`: Entrega promedios clínicos (Glucosa, Presión).
- `POST /api/ml/train/`: Entrena el modelo Random Forest en vivo.
- `POST /api/ml/predict/`: Predice en tiempo real el riesgo clínico de un paciente en base a parámetros json.
