from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class ETLView(TemplateView):
    template_name = 'etl.html'

class PacientesView(TemplateView):
    template_name = 'pacientes.html'

class MLView(TemplateView):
    template_name = 'ml.html'

class LoginView(TemplateView):
    template_name = 'login.html'

class ReportesView(TemplateView):
    template_name = 'reportes.html'

class UsuariosView(TemplateView):
    template_name = 'usuarios.html'
