from django.urls import path
from .views import ExportReportView

urlpatterns = [
    path('exportar/', ExportReportView.as_view(), name='exportar'),
]
