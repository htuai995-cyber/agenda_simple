from django.contrib import admin

from .models import Cita, Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "correo", "dni", "telefono")
    search_fields = ("nombre", "apellido", "correo", "dni")


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("asunto", "client", "fecha", "hora", "estado")
    list_filter = ("estado", "fecha")
    search_fields = ("asunto", "client__nombre", "client__apellido", "direccion")
    date_hierarchy = "fecha"
