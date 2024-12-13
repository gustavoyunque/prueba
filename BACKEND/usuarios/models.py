from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Usuario(AbstractUser):
    TIPOS_USUARIO = (
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
        ('administrador', 'Administrador'),
    )

    tipo_usuario = models.CharField(
        max_length=15, 
        choices=TIPOS_USUARIO, 
        default='cliente',
        verbose_name='Tipo de Usuario'
    )
    
    documento_identidad = models.CharField(
        max_length=8, 
        unique=True,
        verbose_name='Documento de Identidad',
        validators=[
            RegexValidator(
                regex=r'^\d{8}$', 
                message='El documento de identidad debe contener 8 dígitos'
            )
        ]
    )
    
    telefono = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name='Teléfono',
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$', 
                message='Número de teléfono inválido'
            )
        ]
    )
    
    direccion = models.TextField(
        max_length=300, 
        blank=True, 
        null=True,
        verbose_name='Dirección'
    )
    
    fecha_nacimiento = models.DateField(
        blank=True, 
        null=True,
        verbose_name='Fecha de Nacimiento'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualización')

    def __str__(self):
        return f"{self.username} - {self.get_tipo_usuario_display()}"

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']