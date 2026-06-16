import pandas as pd
import numpy as np
from ...etl.models import PacienteClinico

class MedicalStatsService:
    """
    Servicio de analítica de datos médicos para calcular KPIs, estadísticas descriptivas y segmentaciones.
    """

    @staticmethod
    def _get_patients_dataframe():
        """
        Consulta todos los pacientes clínicos de la base de datos y los convierte en un DataFrame.
        """
        queryset = PacienteClinico.objects.all().values()
        if not queryset.exists():
            return pd.DataFrame()
        return pd.DataFrame(list(queryset))

    @classmethod
    def get_kpis(cls):
        """
        Retorna los principales KPIs clínicos del conjunto de pacientes.
        """
        df = cls._get_patients_dataframe()
        if df.empty:
            return {
                "total_pacientes": 0,
                "pacientes_criticos": 0,
                "hipertensos": 0,
                "diabeticos": 0,
                "fumadores": 0,
                "riesgo_promedio": 0.0
            }

        total_pacientes = len(df)
        
        # Pacientes Críticos (Riesgo == 'Crítico')
        criticos = PacienteClinico.objects.filter(riesgo_enfermedad='Crítico').count()
        
        # Hipertensos (Presión Sistólica > 140)
        hipertensos = PacienteClinico.objects.filter(presion_sistolica__gt=140).count()
        
        # Diabéticos (Glucosa > 126)
        diabeticos = PacienteClinico.objects.filter(glucosa__gt=126).count()
        
        # Fumadores (fumador == True)
        fumadores = int(df['fumador'].sum())
        
        # Mapeo de riesgo a escala numérica para promedio
        # Bajo=0, Medio=1, Alto=2, Crítico=3
        mapeo_riesgo = {
            'bajo': 0,
            'medio': 1,
            'alto': 2,
            'critico': 3,
            'crítico': 3
        }
        df['riesgo_num'] = df['riesgo_enfermedad'].str.strip().str.lower().map(mapeo_riesgo).fillna(0)
        riesgo_promedio = float(df['riesgo_num'].mean())

        return {
            "total_pacientes": total_pacientes,
            "pacientes_criticos": criticos,
            "hipertensos": hipertensos,
            "diabeticos": diabeticos,
            "fumadores": fumadores,
            "riesgo_promedio": round(riesgo_promedio, 2)
        }

    @classmethod
    def get_descriptive_stats(cls):
        """
        Retorna la media, mediana, moda y desviación estándar para columnas numéricas.
        """
        df = cls._get_patients_dataframe()
        num_cols = [
            'peso', 'altura', 'IMC', 'presion_sistolica', 
            'presion_diastolica', 'frecuencia_cardiaca', 
            'glucosa', 'colesterol', 'temperatura', 'edad'
        ]

        if df.empty:
            return {col: {"media": 0, "mediana": 0, "moda": 0, "desviacion_estandar": 0} for col in num_cols}

        stats = {}
        for col in num_cols:
            if col in df.columns:
                series = pd.to_numeric(df[col], errors='coerce')
                
                # Moda
                mode_val = series.mode()
                moda = float(mode_val.iloc[0]) if not mode_val.empty else 0.0
                
                stats[col] = {
                    "media": round(float(series.mean()), 2) if not pd.isna(series.mean()) else 0.0,
                    "mediana": round(float(series.median()), 2) if not pd.isna(series.median()) else 0.0,
                    "moda": round(moda, 2),
                    "desviacion_estandar": round(float(series.std()), 2) if not pd.isna(series.std()) else 0.0
                }
            else:
                stats[col] = {"media": 0, "mediana": 0, "moda": 0, "desviacion_estandar": 0}
                
        return stats

    @classmethod
    def get_segmentation(cls):
        """
        Retorna la distribución por categorías (sexo, edad, riesgo, diagnóstico e IMC).
        """
        df = cls._get_patients_dataframe()
        if df.empty:
            return {
                "por_sexo": {},
                "por_rango_edad": {},
                "por_riesgo": {},
                "por_diagnostico": {},
                "por_imc": {}
            }

        # 1. Distribución por Sexo
        dist_sexo = df['sexo'].value_counts().to_dict()

        # 2. Distribución por Rango de Edad (0-18, 19-40, 41-60, 60+)
        bins_edad = [0, 18, 40, 60, 150]
        labels_edad = ['0-18', '19-40', '41-60', '60+']
        df['rango_edad'] = pd.cut(df['edad'], bins=bins_edad, labels=labels_edad, right=True)
        dist_edad = df['rango_edad'].value_counts(sort=False).to_dict()
        # Convertir llaves categóricas a strings
        dist_edad = {str(k): int(v) for k, v in dist_edad.items()}

        # 3. Distribución por Riesgo
        dist_riesgo = df['riesgo_enfermedad'].value_counts().to_dict()

        # 4. Distribución por Diagnóstico
        dist_diag = df['diagnostico_preliminar'].value_counts().to_dict()

        # 5. Distribución por IMC
        # Clasificación clásica:
        # Bajo peso < 18.5, Normal: 18.5-24.9, Sobrepeso: 25-29.9, Obesidad >= 30
        bins_imc = [0, 18.5, 24.99, 29.99, 100]
        labels_imc = ['Bajo peso', 'Normal', 'Sobrepeso', 'Obesidad']
        df['rango_imc'] = pd.cut(df['IMC'], bins=bins_imc, labels=labels_imc, right=True)
        dist_imc = df['rango_imc'].value_counts().to_dict()
        dist_imc = {str(k): int(v) for k, v in dist_imc.items()}

        return {
            "por_sexo": {str(k): int(v) for k, v in dist_sexo.items()},
            "por_rango_edad": dist_edad,
            "por_riesgo": {str(k): int(v) for k, v in dist_riesgo.items()},
            "por_diagnostico": {str(k): int(v) for k, v in dist_diag.items()},
            "por_imc": dist_imc
        }
