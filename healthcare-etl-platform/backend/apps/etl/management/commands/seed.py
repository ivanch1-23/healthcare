import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.etl.models import PacienteClinico, RegistroETL
from apps.etl.services.etl_engine import ETLEngine
from apps.ml.services.predictor import RiskPredictor


class Command(BaseCommand):
    help = 'Inicializa usuarios base, carga el dataset clinico y entrena el modelo ML.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Recarga pacientes e historial ETL aunque ya existan datos.',
        )
        parser.add_argument(
            '--skip-if-loaded',
            action='store_true',
            help='No recarga el dataset si ya hay pacientes cargados.',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando proceso de seeding...'))
        force = options['force']
        skip_if_loaded = options['skip_if_loaded']

        admin_user = self._crear_usuarios_base()

        if skip_if_loaded and PacienteClinico.objects.exists() and not force:
            self.stdout.write(self.style.WARNING('Ya existen pacientes cargados; se omite el ETL.'))
            self._train_if_possible()
            self.stdout.write(self.style.SUCCESS('Seeding finalizado sin recargar datos.'))
            return

        excel_path = os.path.join(settings.BASE_DIR.parent, 'datasets', 'dataset_clinico_etl_1800_registros.xlsx')
        if not os.path.exists(excel_path):
            self.stdout.write(self.style.ERROR(f'No se encontro el dataset en {excel_path}'))
            return

        self.stdout.write(self.style.WARNING('Ejecutando ETL...'))
        try:
            df, start_time, total_rows = ETLEngine.extract(excel_path, file_type='excel')
            df_clean, duplicados = ETLEngine.transform(df)

            if force or not PacienteClinico.objects.exists():
                PacienteClinico.objects.all().delete()
                RegistroETL.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('Se limpiaron registros previos.'))

            log_etl = ETLEngine.load(
                df_clean=df_clean,
                usuario=admin_user,
                start_time=start_time,
                source_name='dataset_clinico_etl_1800_registros.xlsx',
                total_rows=total_rows,
                duplicados=duplicados,
            )
            self.stdout.write(self.style.SUCCESS(f'ETL completado. Registros insertados: {log_etl.registros_limpios}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error durante el ETL: {exc}'))
            return

        self._train_if_possible()
        self.stdout.write(self.style.SUCCESS('Seeding completado con exito.'))

    def _crear_usuarios_base(self):
        User = get_user_model()
        usuarios_base = [
            {
                'username': 'admin',
                'email': 'admin@healthanalytics.com',
                'password': 'admin123',
                'rol': 'administrador',
                'is_superuser': True,
                'is_staff': True,
            },
            {
                'username': 'analista',
                'email': 'analista@healthanalytics.com',
                'password': 'admin123',
                'rol': 'analista',
                'is_superuser': False,
                'is_staff': False,
            },
            {
                'username': 'medico',
                'email': 'medico@healthanalytics.com',
                'password': 'admin123',
                'rol': 'medico',
                'is_superuser': False,
                'is_staff': False,
            },
        ]

        creados = []
        for data in usuarios_base:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'rol': data['rol'],
                    'is_staff': data['is_staff'],
                    'is_superuser': data['is_superuser'],
                },
            )
            if created:
                user.set_password(data['password'])
                user.save()
                creados.append(f"{data['username']} / {data['password']}")

        if creados:
            self.stdout.write(self.style.SUCCESS('Usuarios creados: ' + ', '.join(creados)))
        else:
            self.stdout.write(self.style.SUCCESS('Usuarios base ya existen.'))

        return User.objects.get(username='admin')

    def _train_if_possible(self):
        self.stdout.write(self.style.WARNING('Entrenando modelo de Machine Learning...'))
        try:
            metrics = RiskPredictor.entrenar_modelo()
            self.stdout.write(self.style.SUCCESS(f"Modelo entrenado. Accuracy: {metrics['accuracy']}"))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error al entrenar el modelo: {exc}'))
