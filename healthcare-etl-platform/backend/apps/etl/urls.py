from django.urls import path
from .views import ETLRunView, ETLUploadView, ETLHistorialView, PacientesListView

urlpatterns = [
    path('run/', ETLRunView.as_view(), name='etl_run'),
    path('upload/', ETLUploadView.as_view(), name='etl_upload'),
    path('historial/', ETLHistorialView.as_view(), name='etl_historial'),
    path('pacientes/', PacientesListView.as_view(), name='etl_pacientes'),
]
