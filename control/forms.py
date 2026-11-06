from django import forms

from .models import Cita, Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "apellido", "correo", "dni", "telefono"]
        labels = {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "correo": "Correo electrónico",
            "dni": "DNI",
            "telefono": "Teléfono",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "apellido": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "correo": forms.EmailInput(attrs={"autocomplete": "email"}),
            "dni": forms.TextInput(attrs={"autocomplete": "off"}),
            "telefono": forms.TextInput(
                attrs={"autocomplete": "tel", "type": "tel"}
            ),
        }


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = [
            "client",
            "asunto",
            "fecha",
            "hora",
            "direccion",
            "referencia",
            "notas",
            "estado",
        ]
        labels = {
            "client": "Cliente",
            "asunto": "Asunto",
            "fecha": "Fecha",
            "hora": "Hora",
            "direccion": "Dirección",
            "referencia": "Referencia",
            "notas": "Notas",
            "estado": "Estado",
        }
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "referencia": forms.TextInput(
                attrs={"placeholder": "Piso, oficina u otra referencia"}
            ),
            "notas": forms.Textarea(attrs={"rows": 4}),
        }
