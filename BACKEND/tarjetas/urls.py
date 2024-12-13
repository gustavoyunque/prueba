from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CardViewSet

router = DefaultRouter()
router.register(r'', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('activas/', CardViewSet.as_view({'get': 'tarjetas_activas'}), name='tarjetas-activas'),
    path('<int:pk>/bloquear/', CardViewSet.as_view({'put': 'bloquear_tarjeta'}), name='bloquear-tarjeta')
]