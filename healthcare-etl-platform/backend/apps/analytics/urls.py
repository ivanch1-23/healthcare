from django.urls import path
from .views import KPIsView, EstadisticasView, SegmentacionView

urlpatterns = [
    path('kpis/', KPIsView.as_view(), name='analytics_kpis'),
    path('estadisticas/', EstadisticasView.as_view(), name='analytics_estadisticas'),
    path('segmentacion/', SegmentacionView.as_view(), name='analytics_segmentacion'),
]
