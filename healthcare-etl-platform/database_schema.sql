-- ====================================================================
-- Esquema de Base de Datos para healthcare_etl_platform (PostgreSQL 15)
-- ====================================================================

-- 1. Tabla de Usuarios Personalizados (authentication_customuser)
CREATE TABLE IF NOT EXISTS authentication_customuser (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'analista'
);

-- Índice para búsquedas rápidas de username
CREATE INDEX IF NOT EXISTS authentication_customuser_username_idx 
    ON authentication_customuser (username);

-- 2. Tabla de Pacientes Clínicos (etl_pacienteclinico)
CREATE TABLE IF NOT EXISTS etl_pacienteclinico (
    id BIGSERIAL PRIMARY KEY,
    id_paciente INTEGER UNIQUE NOT NULL,
    nombres VARCHAR(150) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    edad INTEGER NOT NULL,
    sexo VARCHAR(20) NOT NULL,
    peso DOUBLE PRECISION NOT NULL,
    altura DOUBLE PRECISION NOT NULL,
    "IMC" DOUBLE PRECISION NOT NULL,
    "presión_sistólica" INTEGER NOT NULL,
    "presión_diastólica" INTEGER NOT NULL,
    frecuencia_cardiaca INTEGER NOT NULL,
    glucosa DOUBLE PRECISION NOT NULL,
    colesterol DOUBLE PRECISION NOT NULL,
    "saturación_oxígeno" DOUBLE PRECISION NOT NULL,
    temperatura DOUBLE PRECISION NOT NULL,
    antecedentes_familiares BOOLEAN NOT NULL,
    fumador BOOLEAN NOT NULL,
    consumo_alcohol BOOLEAN NOT NULL,
    "actividad_física" VARCHAR(100) NOT NULL,
    "diagnóstico_preliminar" VARCHAR(250) NOT NULL,
    riesgo_enfermedad VARCHAR(50) NOT NULL,
    fecha_consulta DATE NOT NULL
);

-- Índice para búsqueda por id de paciente
CREATE INDEX IF NOT EXISTS etl_pacienteclinico_id_paciente_idx 
    ON etl_pacienteclinico (id_paciente);

-- 3. Tabla de Registros ETL (etl_registroetl)
CREATE TABLE IF NOT EXISTS etl_registroetl (
    id BIGSERIAL PRIMARY KEY,
    fecha TIMESTAMP WITH TIME ZONE NOT NULL,
    registros_procesados INTEGER NOT NULL,
    registros_limpios INTEGER NOT NULL,
    duplicados_eliminados INTEGER NOT NULL,
    tiempo_ejecucion DOUBLE PRECISION NOT NULL,
    estado VARCHAR(20) NOT NULL,
    errores TEXT NULL,
    usuario_fk_id BIGINT NOT NULL,
    CONSTRAINT etl_registroetl_usuario_fk_id_fkey 
        FOREIGN KEY (usuario_fk_id) 
        REFERENCES authentication_customuser (id) 
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED
);

-- Índice para optimizar búsquedas de logs ETL por usuario
CREATE INDEX IF NOT EXISTS etl_registroetl_usuario_fk_id_idx 
    ON etl_registroetl (usuario_fk_id);
