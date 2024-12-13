from django.db import models
from django.core.validators import MinValueValidator
from usuarios.models import Usuario
from cuentas.models import Cuenta

class Prestamo(models.Model):
    ESTADOS_PRESTAMO = (
        ('solicitado', 'Solicitado'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('activo', 'Activo'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido')
    )

    TIPOS_PRESTAMO = (
        ('personal', 'Préstamo Personal'),
        ('hipotecario', 'Préstamo Hipotecario'),
        ('vehicular', 'Préstamo Vehicular'),
        ('empresarial', 'Préstamo Empresarial')
    )

    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        related_name='prestamos'
    )

    cuenta_asociada = models.ForeignKey(
        Cuenta,
        on_delete=models.SET_NULL,
        null=True,
        related_name='prestamos_asociados',
        verbose_name='Cuenta Asociada'
    )

    monto_solicitado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(100.00)],
        verbose_name='Monto Solicitado'
    )

    monto_aprobado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Monto Aprobado'
    )

    tipo_prestamo = models.CharField(
        max_length=20,
        choices=TIPOS_PRESTAMO,
        verbose_name='Tipo de Préstamo'
    )

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS_PRESTAMO,
        default='solicitado',
        verbose_name='Estado del Préstamo'
    )

    tasa_interes = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        verbose_name='Tasa de Interés (%)'
    )

    plazo_meses = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Plazo en Meses'
    )

    fecha_solicitud = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Solicitud'
    )

    fecha_aprobacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Aprobación'
    )

    fecha_primer_pago = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha del Primer Pago'
    )

    def calcular_cuota_mensual(self):
        """
        Calcula la cuota mensual del préstamo
        """
        if not self.monto_aprobado or not self.tasa_interes or not self.plazo_meses:
            return None
        
        tasa_mensual = self.tasa_interes / 100 / 12
        cuota = (self.monto_aprobado * tasa_mensual * (1 + tasa_mensual)**self.plazo_meses) / ((1 + tasa_mensual)**self.plazo_meses - 1)
        return round(cuota, 2)

    def __str__(self):
        return f"Préstamo {self.id} - {self.usuario.username} - {self.estado}"

    class Meta:
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        ordering = ['-fecha_solicitud']