from django.db import models
from django.core.validators import MinValueValidator
from cuentas.models import Cuenta

class Transaccion(models.Model):
    TIPOS_TRANSACCION = (
        ('deposito', 'Depósito'),
        ('retiro', 'Retiro'),
        ('transferencia', 'Transferencia'),
        ('pago', 'Pago'),
        ('cobro', 'Cobro')
    )

    ESTADOS_TRANSACCION = (
        ('procesando', 'Procesando'),
        ('completada', 'Completada'),
        ('fallida', 'Fallida'),
        ('revertida', 'Revertida')
    )

    cuenta_origen = models.ForeignKey(
        Cuenta, 
        on_delete=models.CASCADE,
        related_name='transacciones_realizadas',
        verbose_name='Cuenta de Origen'
    )

    cuenta_destino = models.ForeignKey(
        Cuenta, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transacciones_recibidas',
        verbose_name='Cuenta de Destino'
    )

    tipo = models.CharField(
        max_length=15, 
        choices=TIPOS_TRANSACCION,
        verbose_name='Tipo de Transacción'
    )

    monto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Monto'
    )

    estado = models.CharField(
        max_length=15, 
        choices=ESTADOS_TRANSACCION, 
        default='procesando',
        verbose_name='Estado de Transacción'
    )

    descripcion = models.TextField(
        max_length=300, 
        blank=True, 
        null=True,
        verbose_name='Descripción'
    )

    fecha_transaccion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Transacción'
    )

    def __str__(self):
        return f"{self.tipo} - {self.monto} - {self.estado}"

    def procesar_transaccion(self):
        """
        Método para procesar la transacción
        """
        try:
            if self.tipo == 'deposito':
                self.cuenta_origen.actualizar_saldo(self.monto)
            elif self.tipo == 'retiro':
                if self.cuenta_origen.saldo >= self.monto:
                    self.cuenta_origen.actualizar_saldo(-self.monto)
                    self.estado = 'completada'
                else:
                    self.estado = 'fallida'
            elif self.tipo == 'transferencia':
                if self.cuenta_origen.saldo >= self.monto:
                    self.cuenta_origen.actualizar_saldo(-self.monto)
                    self.cuenta_destino.actualizar_saldo(self.monto)
                    self.estado = 'completada'
                else:
                    self.estado = 'fallida'
            
            self.save()
        except Exception as e:
            self.estado = 'fallida'
            self.save()
            raise e

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha_transaccion']