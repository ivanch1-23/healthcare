from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services.predictor import RiskPredictor

from apps.authentication.permissions import IsAdminOrAnalista

class MLEntrenarView(APIView):
    """
    POST /api/ml/entrenar/
    Entrena el modelo de RandomForestClassifier a partir de los datos clínicos de la BD
    y responde con las métricas de rendimiento obtenidas.
    """
    permission_classes = [IsAdminOrAnalista]

    def post(self, request):
        try:
            metrics = RiskPredictor.entrenar_modelo()
            return Response(
                {
                    "message": "Modelo entrenado y guardado correctamente.",
                    "metrics": metrics
                },
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Error inesperado al entrenar el modelo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MLPredecirView(APIView):
    """
    POST /api/ml/predecir/
    Recibe los datos clínicos de un paciente y retorna la predicción de riesgo junto con su probabilidad.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if not data:
            return Response(
                {"detail": "No se proporcionaron datos de entrada para la predicción."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            prediction = RiskPredictor.predecir_riesgo(data)
            return Response(prediction, status=status.HTTP_200_OK)
            
        except FileNotFoundError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except (KeyError, ValueError) as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Error al realizar la predicción: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
