# Generated by Django 5.1.4 on 2024-12-13 04:00

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cuentas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('deposito', 'Depósito'), ('retiro', 'Retiro'), ('transferencia', 'Transferencia'), ('pago', 'Pago'), ('cobro', 'Cobro')], max_length=15, verbose_name='Tipo de Transacción')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Monto')),
                ('estado', models.CharField(choices=[('procesando', 'Procesando'), ('completada', 'Completada'), ('fallida', 'Fallida'), ('revertida', 'Revertida')], default='procesando', max_length=15, verbose_name='Estado de Transacción')),
                ('descripcion', models.TextField(blank=True, max_length=300, null=True, verbose_name='Descripción')),
                ('fecha_transaccion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Transacción')),
                ('cuenta_destino', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transacciones_recibidas', to='cuentas.cuenta', verbose_name='Cuenta de Destino')),
                ('cuenta_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacciones_realizadas', to='cuentas.cuenta', verbose_name='Cuenta de Origen')),
            ],
            options={
                'verbose_name': 'Transacción',
                'verbose_name_plural': 'Transacciones',
                'ordering': ['-fecha_transaccion'],
            },
        ),
    ]
