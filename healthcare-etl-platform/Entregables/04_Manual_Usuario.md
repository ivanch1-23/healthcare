# 4. Manual de Usuario

## Credenciales de Acceso
El sistema cuenta con 3 perfiles de acceso mediante un sistema de inicio de sesión seguro en `/login/`.
La contraseña predeterminada y unificada para todas las pruebas de evaluación es: `admin123`.

1. **Administrador**
   - Usuario: `admin`
   - Permisos: Acceso total al Dashboard, Proceso ETL, Pacientes, Reportes, Machine Learning y Usuarios.
2. **Analista**
   - Usuario: `analista`
   - Permisos: Uso enfocado al procesamiento de datos (Sección ETL) y Analítica (Dashboard y Reportes).
3. **Médico**
   - Usuario: `medico`
   - Permisos: Acceso clínico a Pacientes, Machine Learning (predicción) y Dashboards.

## Uso del Dashboard (`/`)
El panel de control interactivo despliega en tiempo real:
- Tarjetas clínicas indicadoras del volumen total de pacientes, y grupos patológicos.
- Gráfico de barras identificando los 4 niveles de riesgo.
- Gráfico de pastel identificando la demografía por género.

## Proceso ETL (`/etl/`)
1. Inicie sesión en el sistema con rol de *Admin* o *Analista*.
2. Navegue al apartado "Procesos ETL" en la barra superior.
3. Para procesar el archivo maestro (1800 registros), simplemente pulse el botón azul **"Ejecutar ETL"**.
4. Si desea subir un archivo personalizado (.csv o .xlsx), use el formulario del lado derecho **"Carga Manual"**, escoja su archivo y presione subir. 
5. El sistema purificará los datos, asignará automáticamente los diagnósticos clínicos faltantes, e insertará todo en la Base de Datos, reportando "Éxito" en el Historial de Ejecuciones.

## Reportes y Pacientes
En la pestaña de **Pacientes**, puede buscar registros clínicos exactos mediante la barra de filtrado por Edad o Riesgo.
Puede pulsar en cualquier momento los botones de exportación (`CSV`, `Excel`, `PDF`) en la esquina superior derecha para generar de inmediato un archivo físico filtrado con los datos mostrados.
