import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from apps.etl.models import PacienteClinico, RegistroETL
from apps.etl.services.etl_engine import ETLEngine
from apps.ml.services.predictor import RiskPredictor

class Command(BaseCommand):
    help = 'Inicializa la base de datos con el usuario admin por defecto y corre el pipeline ETL con datos semilla.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando proceso de seeding...'))
        
        # 1. Crear Usuario Administrador
        User = get_user_model()
        admin_email = 'admin@healthanalytics.com'
        admin_pass = 'Admin1234'
        admin_username = 'admin'

        if not User.objects.filter(username=admin_username).exists():
            admin_user = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_pass,
                rol='administrador'
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario administrador creado: {admin_email} / {admin_pass}'))
        else:
            admin_user = User.objects.get(username=admin_username)
            self.stdout.write(self.style.SUCCESS('Usuario administrador ya existe.'))

        # 2. Correr el proceso ETL
        excel_path = os.path.join(settings.BASE_DIR.parent, 'datasets', 'dataset_clinico_etl_1800_registros.xlsx')
        
        if not os.path.exists(excel_path):
            self.stdout.write(self.style.ERROR(f'No se encontró el dataset en {excel_path}'))
            return

        self.stdout.write(self.style.WARNING('Ejecutando ETL (Extracción y Transformación)...'))
        try:
            df, start_time, total_rows = ETLEngine.extract(excel_path, file_type='excel')
            df_clean, duplicados = ETLEngine.transform(df)
            
            # Limpiar datos previos
            PacienteClinico.objects.all().delete()
            RegistroETL.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Se limpiaron los registros previos de la base de datos.'))
            
            log_etl = ETLEngine.load(
                df_clean=df_clean,
                usuario=admin_user,
                start_time=start_time,
                source_name='dataset_clinico_etl_1800_registros.xlsx',
                total_rows=total_rows,
                duplicados=duplicados
            )
            self.stdout.write(self.style.SUCCESS(f'ETL completado. Registros insertados: {log_etl.registros_limpios}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante el ETL: {str(e)}'))
            return

        # 3. Entrenar el modelo de ML
        self.stdout.write(self.style.WARNING('Entrenando el modelo de Machine Learning (Random Forest)...'))
        try:
            metrics = RiskPredictor.entrenar_modelo()
            self.stdout.write(self.style.SUCCESS(f"Modelo entrenado. Accuracy: {metrics['accuracy']}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al entrenar el modelo: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('¡Seeding completado con éxito!'))
