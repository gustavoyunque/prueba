from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanViewSet

router = DefaultRouter()
router.register(r'', LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('activos/', LoanViewSet.as_view({'get': 'prestamos_activos'}), name='prestamos-activos'),
    path('<int:pk>/cambiar-estado/', LoanViewSet.as_view({'put': 'cambiar_estado'}), name='cambiar-estado-prestamo')
]