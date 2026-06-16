import os
import joblib
import pandas as pd
import numpy as np
from django.conf import settings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from ...etl.models import PacienteClinico

MODEL_PATH = os.path.join(settings.BASE_DIR, 'apps', 'ml', 'modelo_entrenado.pkl')

class RiskPredictor:
    """
    Servicio de Machine Learning para predecir el riesgo de enfermedad de pacientes
    utilizando RandomForestClassifier.
    """

    MAPEO_RIESGO = {
        'bajo': 0,
        'medio': 1,
        'alto': 2,
        'critico': 3,
        'crítico': 3
    }
    
    MAPEO_REVERSO = {
        0: 'Bajo',
        1: 'Medio',
        2: 'Alto',
        3: 'Crítico'
    }

    FEATURES_COLS = [
        'IMC', 'edad', 'glucosa', 'colesterol', 
        'presion_sistolica', 'presion_diastolica', 
        'frecuencia_cardiaca', 'fumador'
    ]

    @classmethod
    def entrenar_modelo(cls):
        """
        Entrena el RandomForestClassifier con los datos actuales de PacienteClinico.
        Guarda el modelo entrenado en un archivo .pkl y retorna las métricas de rendimiento.
        """
        queryset = PacienteClinico.objects.all().values()
        if not queryset.exists():
            raise ValueError("No hay datos de pacientes en la base de datos. Por favor, ejecuta primero el proceso ETL.")

        # Cargar a pandas
        df = pd.DataFrame(list(queryset))

        # Renombrar columnas internas de Django a nombres esperados
        df = df.rename(columns={
            'presion_sistolica': 'presion_sistolica',
            'presion_diastolica': 'presion_diastolica',
        })

        # Preprocesamiento
        df['fumador'] = df['fumador'].astype(int)
        
        # Mapear el target (riesgo_enfermedad)
        df['target'] = df['riesgo_enfermedad'].str.strip().str.lower().map(cls.MAPEO_RIESGO)
        # Manejar nulos en target si los hubiera por si acaso
        df = df.dropna(subset=['target'])
        df['target'] = df['target'].astype(int)

        X = df[cls.FEATURES_COLS]
        y = df['target']

        # Verificar que tengamos suficientes datos
        if len(df) < 10:
            raise ValueError(f"Datos insuficientes para entrenar ({len(df)} registros). Se requieren al menos 10 pacientes.")

        # Dividir datos 80/20
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar RandomForest
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluar
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        conf_matrix = confusion_matrix(y_test, y_pred).tolist()

        # Guardar el modelo
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)

        return {
            "accuracy": round(float(accuracy), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "matriz_confusion": conf_matrix,
            "total_registros_entrenamiento": len(df)
        }

    @classmethod
    def predecir_riesgo(cls, data):
        """
        Predice el riesgo y la probabilidad asociada a partir de un JSON de datos de un paciente.
        """
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("El modelo no ha sido entrenado todavía. Por favor, ejecuta el endpoint de entrenamiento primero.")

        # Cargar el modelo
        model = joblib.load(MODEL_PATH)

        # Extraer variables y validar campos
        try:
            input_data = {
                'IMC': float(data['IMC']),
                'edad': int(data['edad']),
                'glucosa': float(data['glucosa']),
                'colesterol': float(data['colesterol']),
                'presion_sistolica': int(data['presion_sistolica']),
                'presion_diastolica': int(data['presion_diastolica']),
                'frecuencia_cardiaca': int(data['frecuencia_cardiaca']),
                'fumador': int(bool(data['fumador']))
            }
        except KeyError as e:
            raise KeyError(f"Falta el campo requerido en los datos de entrada: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Tipo de dato inválido en los campos de entrada: {str(e)}")

        # Convertir a DataFrame manteniendo nombres de columnas para que RandomForest no lance advertencias
        X_pred = pd.DataFrame([input_data])[cls.FEATURES_COLS]

        # Predecir clase
        clase_num = int(model.predict(X_pred)[0])
        clase_texto = cls.MAPEO_REVERSO.get(clase_num, 'Bajo')

        # Predecir probabilidades
        probabilidades = model.predict_proba(X_pred)[0]
        # Obtener la probabilidad correspondiente a la clase predicha
        clase_idx = np.where(model.classes_ == clase_num)[0]
        probabilidad = float(probabilidades[clase_idx[0]]) if len(clase_idx) > 0 else 0.0

        # Crear distribución de probabilidades detallada para valor agregado
        dist_prob = {}
        for idx, prob in enumerate(probabilidades):
            clase_lbl = cls.MAPEO_REVERSO.get(model.classes_[idx], 'Desconocido')
            dist_prob[clase_lbl] = round(float(prob), 4)

        return {
            "riesgo_predicho": clase_texto,
            "probabilidad": round(probabilidad, 4),
            "distribucion_probabilidades": dist_prob
        }
