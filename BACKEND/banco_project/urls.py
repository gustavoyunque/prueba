from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.views import UserViewSet
from cuentas.views import AccountViewSet
from transacciones.views import TransactionViewSet
from prestamos.views import LoanViewSet
from tarjetas.views import CardViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'cuentas', AccountViewSet)
router.register(r'transacciones', TransactionViewSet)
router.register(r'prestamos', LoanViewSet)
router.register(r'tarjetas', CardViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]