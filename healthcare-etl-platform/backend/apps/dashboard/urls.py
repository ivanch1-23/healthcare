from django.urls import path
from .views import DashboardView, ETLView, PacientesView, MLView, LoginView, ReportesView, UsuariosView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_page'),
    path('', DashboardView.as_view(), name='dashboard_page'),
    path('etl/', ETLView.as_view(), name='etl_page'),
    path('pacientes/', PacientesView.as_view(), name='pacientes_page'),
    path('ml/', MLView.as_view(), name='ml_page'),
    path('reportes/', ReportesView.as_view(), name='reportes_page'),
    path('usuarios/', UsuariosView.as_view(), name='usuarios_page'),
]
