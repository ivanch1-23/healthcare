import os
import time
import logging
import pandas as pd
from django.utils import timezone
from django.db import transaction
from ..models import PacienteClinico, RegistroETL

logger = logging.getLogger(__name__)

class ETLEngine:
    """
    Motor ETL para la carga, transformación y almacenamiento de registros médicos de pacientes.
    """

    @staticmethod
    def extract(file_path_or_buffer, file_type='excel'):
        """
        FASE EXTRACT: Lee el archivo origen (Excel o CSV) y registra los metadatos iniciales.
        """
        start_time = time.time()
        logger.info(f"=== ETL EXTRACT INICIADO ===")
        logger.info(f"Fuente de datos: {file_path_or_buffer if isinstance(file_path_or_buffer, str) else 'Buffer/Subida externa'}")
        logger.info(f"Tipo de archivo: {file_type}")

        if file_type == 'excel':
            df = pd.read_excel(file_path_or_buffer)
        else:
            df = pd.read_csv(file_path_or_buffer)

        total_rows = len(df)
        logger.info(f"Filas extraídas inicialmente: {total_rows}")
        logger.info(f"Columnas detectadas: {list(df.columns)}")
        
        return df, start_time, total_rows

    @staticmethod
    def transform(df):
        """
        FASE TRANSFORM: Limpieza de duplicados, normalización de campos, imputación de nulos y cálculo de riesgo clínico.
        """
        logger.info(f"=== ETL TRANSFORM INICIADO ===")
        df_clean = df.copy()

        # 0. Normalizar nombres de columnas a minúsculas y sin tildes para simplificar el código
        logger.info("Normalizando nombres de columnas...")
        df_clean.columns = (df_clean.columns.str.replace('á', 'a')
                                           .str.replace('é', 'e')
                                           .str.replace('í', 'i')
                                           .str.replace('ó', 'o')
                                           .str.replace('ú', 'u')
                                           .str.replace('Á', 'A')
                                           .str.replace('É', 'E')
                                           .str.replace('Í', 'I')
                                           .str.replace('Ó', 'O')
                                           .str.replace('Ú', 'U'))
        
        logger.info(f"Nombres de columnas normalizados: {list(df_clean.columns)}")

        # 1. Eliminar filas completamente duplicadas o con id_paciente duplicado
        filas_antes = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=['id_paciente'], keep='first')
        duplicados = filas_antes - len(df_clean)
        logger.info(f"Filas duplicadas eliminadas: {duplicados}")

        # 2. Convertir edad a numérico (si dice 'Treinta' -> NaN y rellenar con mediana)
        logger.info("Transformando campo 'edad'...")
        df_clean['edad'] = pd.to_numeric(df_clean['edad'], errors='coerce')
        mediana_edad = df_clean['edad'].median()
        if pd.isna(mediana_edad):
            mediana_edad = 40.0
        df_clean['edad'] = df_clean['edad'].fillna(mediana_edad).astype(int)
        logger.info(f"Edad procesada (Mediana de imputación: {mediana_edad})")

        # 3. Convertir presiones a numérico (si dice 'Alta' -> NaN y rellenar con mediana)
        logger.info("Transformando presiones sistólica y diastólica...")
        df_clean['presion_sistolica'] = pd.to_numeric(df_clean['presion_sistolica'], errors='coerce')
        df_clean['presion_diastolica'] = pd.to_numeric(df_clean['presion_diastolica'], errors='coerce')
        
        mediana_sist = df_clean['presion_sistolica'].median()
        if pd.isna(mediana_sist):
            mediana_sist = 120.0
        mediana_diast = df_clean['presion_diastolica'].median()
        if pd.isna(mediana_diast):
            mediana_diast = 80.0
            
        df_clean['presion_sistolica'] = df_clean['presion_sistolica'].fillna(mediana_sist).astype(int)
        df_clean['presion_diastolica'] = df_clean['presion_diastolica'].fillna(mediana_diast).astype(int)
        logger.info(f"Presiones procesadas. Medianas de imputación: Sistólica={mediana_sist}, Diastólica={mediana_diast}")

        # 4. Estandarizar sexo (Masculino -> 'M', Femenino -> 'F')
        logger.info("Estandarizando sexo...")
        def clean_sexo(val):
            if not isinstance(val, str):
                return 'M'
            val_clean = val.strip().lower()
            if val_clean in ['m', 'masculino', 'male']:
                return 'M'
            elif val_clean in ['f', 'femenino', 'female']:
                return 'F'
            return 'M'
        df_clean['sexo'] = df_clean['sexo'].apply(clean_sexo)

        # 5. Estandarizar diagnóstico preliminar (normalizar tildes, corregir ortografía)
        logger.info("Normalizando diagnósticos preliminares...")
        def clean_diagnostico(val):
            if not isinstance(val, str):
                return 'Paciente Sano'
            
            s = val.strip().lower()
            s = s.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            
            correcciones = {
                'diabetes tipo 2': 'Diabetes Tipo 2',
                'paciente sano': 'Paciente Sano',
                'riesgo cardiovascular': 'Riesgo Cardiovascular',
                'obesidad': 'Obesidad',
                'hipertension': 'Hipertensión',
                'hipertenson': 'Hipertensión',
                'hipertencion': 'Hipertensión',
                'prehipertension': 'Prehipertensión',
                'prehipertencion': 'Prehipertensión',
                'cardiopatia': 'Cardiopatía',
                'diabtes': 'Diabetes Tipo 2'
            }
            
            for key, clean_val in correcciones.items():
                if key in s:
                    return clean_val
            
            return val.strip().title()
        
        df_clean['diagnostico_preliminar'] = df_clean['diagnostico_preliminar'].apply(clean_diagnostico)

        # 6. Validar rangos clínicos y marcar outliers como nulos para imputarlos
        logger.info("Identificando y removiendo outliers clínicos...")
        
        # Outliers a nulos
        df_clean.loc[(df_clean['peso'] < 1) | (df_clean['peso'] > 300), 'peso'] = pd.NA
        df_clean.loc[(df_clean['temperatura'] < 30) | (df_clean['temperatura'] > 42), 'temperatura'] = pd.NA
        df_clean.loc[(df_clean['glucosa'] < 50) | (df_clean['glucosa'] > 600), 'glucosa'] = pd.NA
        df_clean.loc[(df_clean['saturacion_oxigeno'] < 50) | (df_clean['saturacion_oxigeno'] > 100), 'saturacion_oxigeno'] = pd.NA
        df_clean.loc[(df_clean['presion_sistolica'] < 60) | (df_clean['presion_sistolica'] > 250), 'presion_sistolica'] = pd.NA

        # 7. Rellenar nulos numéricos (glucosa, colesterol, peso, altura -> media; temperatura -> 36.5; saturación_oxígeno -> mediana)
        logger.info("Imputando valores nulos...")
        
        # Glucosa, Colesterol, Peso, Altura -> media
        for col in ['glucosa', 'colesterol', 'peso', 'altura']:
            media = pd.to_numeric(df_clean[col], errors='coerce').mean()
            if pd.isna(media):
                media = 70.0  # Fallback
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(media)

        # Temperatura -> 36.5
        df_clean['temperatura'] = pd.to_numeric(df_clean['temperatura'], errors='coerce').fillna(36.5)

        # Saturación de oxígeno -> mediana
        sat_mediana = pd.to_numeric(df_clean['saturacion_oxigeno'], errors='coerce').median()
        if pd.isna(sat_mediana):
            sat_mediana = 95.0
        df_clean['saturacion_oxigeno'] = pd.to_numeric(df_clean['saturacion_oxigeno'], errors='coerce').fillna(sat_mediana)

        # 8. Recalcular IMC = peso / altura² y reclasificar
        logger.info("Recalculando IMC...")
        df_clean['IMC'] = df_clean['peso'] / (df_clean['altura'] ** 2)

        # 9. Calcular/asignar riesgo_enfermedad
        logger.info("Calculando riesgo de enfermedad...")
        def calc_riesgo(row):
            sistolica = row['presion_sistolica']
            glucosa = row['glucosa']
            sat = row['saturacion_oxigeno']
            imc = row['IMC']
            fumador = bool(row['fumador'])
            diag = str(row['diagnostico_preliminar']).strip()
            
            # Regla especial para Paciente Sano:
            if diag == 'Paciente Sano':
                # Solo crítico si valores son realmente extremos
                if (sistolica > 200) or (glucosa > 400) or (sat < 70):
                    return 'Crítico'
                elif (sistolica > 160) or (glucosa > 250) or (imc > 40) or (row.get('frecuencia_cardiaca', 0) > 120):
                    return 'Alto'
                elif (imc > 25) or (fumador is True) or (row.get('colesterol', 0) > 240):
                    return 'Medio'
                else:
                    return 'Bajo'

            # Umbrales normales
            if (sistolica > 180) or (glucosa > 300) or (sat < 85):
                return 'Crítico'
            elif (sistolica > 140) or (glucosa > 200) or (imc > 35) or (row.get('frecuencia_cardiaca', 0) > 100):
                return 'Alto'
            elif (imc > 25) or (fumador is True) or (row.get('colesterol', 0) > 240):
                return 'Medio'
            else:
                return 'Bajo'
                
        df_clean['riesgo_enfermedad'] = df_clean.apply(calc_riesgo, axis=1)

        # 10. Estandarizar fecha_consulta
        df_clean['fecha_consulta'] = pd.to_datetime(df_clean['fecha_consulta']).dt.date

        logger.info(f"Proceso de transformación completado. Filas resultantes: {len(df_clean)}")
        return df_clean, duplicados

    @staticmethod
    def load(df_clean, usuario, start_time, source_name, total_rows, duplicados):
        """
        FASE LOAD: Inserta los registros procesados en la BD y guarda el log de ejecución.
        """
        logger.info(f"=== ETL LOAD INICIADO ===")
        estado = 'exitoso'
        errores_msg = ''
        registros_limpios = len(df_clean)
        
        try:
            with transaction.atomic():
                # Limpiamos los registros existentes de pacientes para evitar solapamiento en carga completa
                PacienteClinico.objects.all().delete()
                logger.info("Registros anteriores de PacienteClinico eliminados para carga limpia.")

                pacientes = []
                for _, row in df_clean.iterrows():
                    pacientes.append(PacienteClinico(
                        id_paciente=int(row['id_paciente']),
                        nombres=row['nombres'],
                        apellidos=row['apellidos'],
                        edad=int(row['edad']),
                        sexo=row['sexo'],
                        peso=float(row['peso']),
                        altura=float(row['altura']),
                        IMC=float(row['IMC']),
                        presion_sistolica=int(row['presion_sistolica']),
                        presion_diastolica=int(row['presion_diastolica']),
                        frecuencia_cardiaca=int(row['frecuencia_cardiaca']),
                        glucosa=float(row['glucosa']),
                        colesterol=float(row['colesterol']),
                        saturacion_oxigeno=float(row['saturacion_oxigeno']),
                        temperatura=float(row['temperatura']),
                        antecedentes_familiares=bool(row['antecedentes_familiares']),
                        fumador=bool(row['fumador']),
                        consumo_alcohol=bool(row['consumo_alcohol']),
                        actividad_fisica=row['actividad_fisica'],
                        diagnostico_preliminar=row['diagnostico_preliminar'],
                        riesgo_enfermedad=row['riesgo_enfermedad'],
                        fecha_consulta=row['fecha_consulta']
                    ))
                
                PacienteClinico.objects.bulk_create(pacientes)
                logger.info(f"Se insertaron correctamente {len(pacientes)} registros clínicos en PostgreSQL.")

        except Exception as e:
            estado = 'fallido'
            errores_msg = str(e)
            logger.error(f"Error durante la inserción en base de datos: {errores_msg}")

        end_time = time.time()
        tiempo_ejecucion = end_time - start_time
        logger.info(f"Tiempo de ejecución ETL: {tiempo_ejecucion:.4f} segundos.")

        # Guardar log en RegistroETL
        log_etl = RegistroETL.objects.create(
            usuario_fk=usuario,
            registros_procesados=total_rows,
            registros_limpios=registros_limpios,
            duplicados_eliminados=duplicados,
            tiempo_ejecucion=tiempo_ejecucion,
            estado=estado,
            errores=errores_msg if errores_msg else None
        )
        logger.info(f"RegistroETL id={log_etl.id} creado con estado '{estado}'.")

        return log_etl
