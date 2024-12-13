from django.db import models
from django.core.validators import MinValueValidator
from usuarios.models import Usuario
from cuentas.models import Cuenta

class Tarjeta(models.Model):
    TIPOS_TARJETA = (
        ('credito', 'Tarjeta de Crédito'),
        ('debito', 'Tarjeta de Débito')
    )

    ESTADOS_TARJETA = (
        ('activa', 'Activa'),
        ('bloqueada', 'Bloqueada'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada')
    )

    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        verbose_name='Titular',
        related_name='tarjetas'
    )

    cuenta_asociada = models.ForeignKey(
        Cuenta,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tarjetas_asociadas',
        verbose_name='Cuenta Asociada'
    )

    numero_tarjeta = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='Número de Tarjeta'
    )

    tipo_tarjeta = models.CharField(
        max_length=10,
        choices=TIPOS_TARJETA,
        verbose_name='Tipo de Tarjeta'
    )

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS_TARJETA,
        default='activa',
        verbose_name='Estado de la Tarjeta'
    )

    fecha_emision = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de Emisión'
    )

    fecha_vencimiento = models.DateField(
        verbose_name='Fecha de Vencimiento'
    )

    cvv = models.CharField(
        max_length=4,
        verbose_name='Código de Seguridad'
    )

    limite_credito = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.00)],
        verbose_name='Límite de Crédito'
    )

    saldo_disponible = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)],
        verbose_name='Saldo Disponible'
    )

    def generar_numero_tarjeta(self):
        """
        Método para generar un número de tarjeta único
        """
        import random
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])

    def validar_tarjeta(self):
        """
        Método para validar el estado de la tarjeta
        """
        from django.utils import timezone
        
        if timezone.now().date() > self.fecha_vencimiento:
            self.estado = 'vencida'
            self.save()

    def __str__(self):
        return f"{self.tipo_tarjeta.upper()} - {self.numero_tarjeta} - {self.estado}"

    def save(self, *args, **kwargs):
        if not self.numero_tarjeta:
            self.numero_tarjeta = self.generar_numero_tarjeta()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'
        ordering = ['-fecha_emision']