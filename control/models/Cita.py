from django.db import models

from ..fields import EnumCharField
from .Cliente import Cliente


class Cita(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADA = "confirmada", "Confirmada"
        REALIZADA = "realizada", "Realizada"
        CANCELADA = "cancelada", "Cancelada"

    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="citas",
        db_column="client_id",
    )
    asunto = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.TimeField()
    direccion = models.CharField(max_length=255)
    referencia = models.CharField(max_length=255, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    estado = EnumCharField(
        max_length=20,
        choices=Estado.choices,
        null=True,
        blank=True,
        default=Estado.PENDIENTE,
    )
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        db_table = "citas"
        ordering = ["fecha", "hora"]
        verbose_name = "cita"
        verbose_name_plural = "citas"

    def __str__(self):
        return f"{self.asunto} — {self.fecha:%d/%m/%Y} {self.hora:%H:%M}"