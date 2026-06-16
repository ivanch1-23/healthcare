from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services.stats import MedicalStatsService

class KPIsView(APIView):
    """
    GET /api/analytics/kpis/
    Retorna los KPIs principales de la tabla de pacientes.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        kpis = MedicalStatsService.get_kpis()
        return Response(kpis, status=status.HTTP_200_OK)


class EstadisticasView(APIView):
    """
    GET /api/analytics/estadisticas/
    Retorna las estadísticas descriptivas para cada variable numérica.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = MedicalStatsService.get_descriptive_stats()
        return Response(stats, status=status.HTTP_200_OK)


class SegmentacionView(APIView):
    """
    GET /api/analytics/segmentacion/
    Retorna las distribuciones por categorías.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        segmentation = MedicalStatsService.get_segmentation()
        return Response(segmentation, status=status.HTTP_200_OK)
