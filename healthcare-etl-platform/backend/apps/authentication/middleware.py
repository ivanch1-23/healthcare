from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class RoleRequiredMiddleware:
    """
    Middleware que asocia el usuario del JWT al request clásico de Django
    y opcionalmente restringe rutas basadas en el rol.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Autenticar usuario vía JWT para vistas estándar de Django
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            try:
                token_str = auth_header.split(' ')[1]
                access_token = AccessToken(token_str)
                user_id = access_token.payload.get('user_id')
                if user_id:
                    request.user = User.objects.get(id=user_id)
            except Exception:
                pass  # Dejar que DRF maneje la autenticación en sus endpoints

        # 2. Validación de permisos por rol a nivel de Middleware HTTP
        # Si se accede a rutas marcadas como restringidas (ejemplo conceptual para la API)
        if request.path.startswith('/api/admin-only/') and (not request.user.is_authenticated or request.user.rol != 'administrador'):
            return JsonResponse(
                {"detail": "Acceso denegado: Requiere rol de administrador."},
                status=403
            )

        response = self.get_response(request)
        return response
