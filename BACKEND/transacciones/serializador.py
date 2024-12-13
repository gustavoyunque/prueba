from rest_framework import serializers
from .models import Transaccion  

class SerializadorTransaccion(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = [
            'id',  
            'cuenta_origen', 
            'cuenta_destino', 
            'tipo', 
            'monto', 
            'estado', 
            'descripcion', 
            'fecha_transaccion'
        ]