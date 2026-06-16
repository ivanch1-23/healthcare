# 1. Codificación y Base de Datos

## Repositorio de Código Fuente

El código fuente de la plataforma se encuentra alojado y es completamente funcional de manera local.
Para subirlo a un repositorio remoto de GitHub, ejecuta los siguientes comandos desde la raíz del proyecto (`healthcare-etl-platform/`):

```bash
git init
git add .
git commit -m "Primera versión: ETL Platform"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

## Script SQL de la Base de Datos

El script SQL que contiene el modelo relacional generado se ha exportado exitosamente.

**Ubicación del archivo:** `backend/entregables_script.sql`

Este archivo contiene la definición DDL de las tablas principales, incluyendo `etl_pacienteclinico`, así como las tablas de autenticación de Django (`auth_user`, etc.). Puedes ejecutar este archivo en cualquier gestor de bases de datos compatible para regenerar la estructura.
