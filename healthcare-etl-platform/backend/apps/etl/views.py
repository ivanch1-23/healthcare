import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.authentication.permissions import IsAdminOrAnalista
from django.conf import settings
from .services.etl_engine import ETLEngine
from .serializers import RegistroETLSerializer, PacienteClinicoSerializer
from .models import RegistroETL, PacienteClinico
from rest_framework.pagination import PageNumberPagination

class BaseETLView(APIView):
    """
    Vista base.
    """
    permission_classes = [IsAdminOrAnalista]

    def check_rol_permiso(self, user):
        return user.rol in ['administrador', 'analista']


class ETLRunView(BaseETLView):
    """
    POST /api/etl/run/
    Ejecuta el motor ETL sobre el dataset clínico predeterminado (Excel).
    """
    def post(self, request):

        # Ruta del archivo Excel clínico predeterminado
        excel_path = os.path.join(settings.BASE_DIR.parent, 'datasets', 'dataset_clinico_etl_1800_registros.xlsx')
        
        if not os.path.exists(excel_path):
            # Fallback en caso de que esté corriendo en otro contexto de directorios
            excel_path = os.path.join(settings.BASE_DIR, 'datasets', 'dataset_clinico_etl_1800_registros.xlsx')

        if not os.path.exists(excel_path):
            return Response(
                {"detail": f"Archivo de dataset no encontrado en la ruta: {excel_path}"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # 1. EXTRACT
            df, start_time, total_rows = ETLEngine.extract(excel_path, file_type='excel')
            
            # 2. TRANSFORM
            df_clean, duplicados = ETLEngine.transform(df)
            
            # 3. LOAD
            log_etl = ETLEngine.load(
                df_clean=df_clean,
                usuario=request.user,
                start_time=start_time,
                source_name='dataset_clinico_etl_1800_registros.xlsx',
                total_rows=total_rows,
                duplicados=duplicados
            )
            
            serializer = RegistroETLSerializer(log_etl)
            return Response(
                {
                    "message": "Proceso ETL completado con éxito.",
                    "log": serializer.data
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"detail": f"Fallo al ejecutar el proceso ETL: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ETLUploadView(BaseETLView):
    """
    POST /api/etl/upload/
    Permite subir un archivo CSV externo y ejecutar el pipeline ETL sobre él.
    """
    def post(self, request):

        if 'file' not in request.FILES:
            return Response(
                {"detail": "No se proporcionó ningún archivo en el campo 'file'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = request.FILES['file']
        
        # Validar extensión del archivo
        if not uploaded_file.name.endswith('.csv') and not uploaded_file.name.endswith('.xlsx'):
            return Response(
                {"detail": "Formato de archivo no soportado. Debe ser un archivo CSV o Excel (.xlsx)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_type = 'excel' if uploaded_file.name.endswith('.xlsx') else 'csv'

        try:
            # 1. EXTRACT (Pasamos el buffer del archivo en memoria)
            df, start_time, total_rows = ETLEngine.extract(uploaded_file, file_type=file_type)
            
            # 2. TRANSFORM
            df_clean, duplicados = ETLEngine.transform(df)
            
            # 3. LOAD
            log_etl = ETLEngine.load(
                df_clean=df_clean,
                usuario=request.user,
                start_time=start_time,
                source_name=uploaded_file.name,
                total_rows=total_rows,
                duplicados=duplicados
            )
            
            serializer = RegistroETLSerializer(log_etl)
            return Response(
                {
                    "message": f"Proceso ETL para {uploaded_file.name} completado con éxito.",
                    "log": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": f"Fallo al ejecutar el proceso ETL del archivo subido: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ETLHistorialView(APIView):
    """
    GET /api/etl/historial/
    Retorna el historial de ejecuciones del pipeline ETL.
    """
    permission_classes = [IsAdminOrAnalista]

    def get(self, request):
        logs = RegistroETL.objects.all().order_by('-fecha')
        serializer = RegistroETLSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PacientesPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class PacientesListView(APIView):
    """
    GET /api/etl/pacientes/
    Retorna la lista de pacientes con paginación y filtros por sexo y riesgo.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = PacienteClinico.objects.all().order_by('id_paciente')
        
        sexo = request.query_params.get('sexo', None)
        if sexo:
            queryset = queryset.filter(sexo__iexact=sexo)
            
        riesgo = request.query_params.get('riesgo', None)
        if riesgo:
            queryset = queryset.filter(riesgo_enfermedad__iexact=riesgo)
            
        paginator = PacientesPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PacienteClinicoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
