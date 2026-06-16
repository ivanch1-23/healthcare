from django.urls import path
from .views import MLEntrenarView, MLPredecirView

urlpatterns = [
    path('entrenar/', MLEntrenarView.as_view(), name='ml_entrenar'),
    path('predecir/', MLPredecirView.as_view(), name='ml_predecir'),
]
