import os
import django
import sys

# Ajustar el path para que encuentre el módulo config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.etl.services.etl_engine import ETLEngine
from apps.ml.services.predictor import RiskPredictor
from django.conf import settings

def main():
    User = get_user_model()
    admin = User.objects.get(username='admin')

    excel_path = os.path.join(settings.BASE_DIR.parent, 'datasets', 'dataset_clinico_etl_1800_registros.xlsx')

    if not os.path.exists(excel_path):
        print(f"Dataset no encontrado en {excel_path}")
        return

    print("=== Iniciando ETL ===")
    df, start_time, total_rows = ETLEngine.extract(excel_path, file_type='excel')
    df_clean, duplicados = ETLEngine.transform(df)
    log_etl = ETLEngine.load(
        df_clean=df_clean,
        usuario=admin,
        start_time=start_time,
        source_name='dataset_clinico_etl_1800_registros.xlsx',
        total_rows=total_rows,
        duplicados=duplicados
    )
    print(f"ETL completo. Registros cargados: {log_etl.registros_limpios}")

    print("=== Entrenando modelo ML ===")
    metrics = RiskPredictor.entrenar_modelo()
    print("Modelo entrenado exitosamente.")
    print(metrics)

if __name__ == '__main__':
    main()
