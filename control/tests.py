from datetime import date, time, timedelta
from unittest.mock import Mock

from django.test import Client as HttpClient, TestCase
from django.urls import reverse

from .models import Cita, Cliente


class AgendaTests(TestCase):
    def setUp(self):
        self.http = HttpClient()
        self.cliente = Cliente.objects.create(
            nombre="Ana",
            apellido="Pérez",
            correo="ana@example.com",
            dni="12345678",
            telefono="999888777",
        )

    def test_cliente_has_expected_table_and_nullable_contact_fields(self):
        self.assertEqual(Cliente._meta.db_table, "clientes")
        self.assertTrue(Cliente._meta.get_field("telefono").null)
        self.assertEqual(str(self.cliente), "Ana Pérez")
        self.assertIsNotNone(self.cliente.created_at)

    def test_cita_links_to_client_and_defaults_to_pending(self):
        cita = Cita.objects.create(
            client=self.cliente,
            asunto="Consulta",
            fecha=date.today() + timedelta(days=1),
            hora=time(10, 30),
            direccion="Av. Principal 123",
        )
        self.assertEqual(Cita._meta.db_table, "citas")
        self.assertEqual(cita.client, self.cliente)
        self.assertEqual(cita.estado, Cita.Estado.PENDIENTE)

    def test_estado_uses_native_mysql_enum_type(self):
        connection = Mock()
        connection.vendor = "mysql"
        field = Cita._meta.get_field("estado")
        self.assertEqual(
            field.db_type(connection),
            "enum('pendiente', 'confirmada', 'realizada', 'cancelada')",
        )

    def test_dashboard_and_lists_render(self):
        for name in ("inicio", "clientes", "citas"):
            with self.subTest(page=name):
                response = self.http.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_can_create_client_from_form(self):
        response = self.http.post(
            reverse("cliente_crear"),
            {
                "nombre": "Luis",
                "apellido": "García",
                "correo": "luis@example.com",
                "dni": "87654321",
                "telefono": "",
            },
        )
        self.assertRedirects(response, reverse("clientes"))
        self.assertTrue(Cliente.objects.filter(dni="87654321").exists())

    def test_client_form_rejects_invalid_email(self):
        response = self.http.post(
            reverse("cliente_crear"),
            {
                "nombre": "Luis",
                "apellido": "García",
                "correo": "no-es-un-correo",
                "dni": "87654321",
                "telefono": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="form-field has-error"')
        self.assertFalse(Cliente.objects.filter(dni="87654321").exists())

    def test_can_update_client(self):
        response = self.http.post(
            reverse("cliente_editar", args=[self.cliente.pk]),
            {
                "nombre": "Ana María",
                "apellido": "Pérez",
                "correo": "ana@example.com",
                "dni": "12345678",
                "telefono": "",
            },
        )
        self.assertRedirects(response, reverse("clientes"))
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nombre, "Ana María")

    def test_can_create_and_filter_appointment(self):
        response = self.http.post(
            reverse("cita_crear"),
            {
                "client": self.cliente.pk,
                "asunto": "Revisión",
                "fecha": (date.today() + timedelta(days=2)).isoformat(),
                "hora": "11:30",
                "direccion": "Calle Norte 10",
                "referencia": "",
                "notas": "",
                "estado": Cita.Estado.CONFIRMADA,
            },
        )
        self.assertRedirects(response, reverse("citas"))
        cita = Cita.objects.get(asunto="Revisión")
        self.assertEqual(cita.estado, Cita.Estado.CONFIRMADA)

        response = self.http.get(
            reverse("citas"), {"q": "Revisión", "estado": Cita.Estado.CONFIRMADA}
        )
        self.assertContains(response, "Revisión")

    def test_can_update_and_delete_appointment(self):
        cita = Cita.objects.create(
            client=self.cliente,
            asunto="Consulta",
            fecha=date.today() + timedelta(days=1),
            hora=time(10, 30),
            direccion="Av. Principal 123",
        )
        response = self.http.post(
            reverse("cita_editar", args=[cita.pk]),
            {
                "client": self.cliente.pk,
                "asunto": "Consulta actualizada",
                "fecha": cita.fecha.isoformat(),
                "hora": "11:00",
                "direccion": "Av. Principal 123",
                "referencia": "",
                "notas": "",
                "estado": Cita.Estado.REALIZADA,
            },
        )
        self.assertRedirects(response, reverse("citas"))
        cita.refresh_from_db()
        self.assertEqual(cita.estado, Cita.Estado.REALIZADA)

        response = self.http.post(
            reverse("cita_eliminar", args=[cita.pk]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Cita.objects.filter(pk=cita.pk).exists())

    def test_client_with_appointments_cannot_be_deleted(self):
        Cita.objects.create(
            client=self.cliente,
            asunto="Consulta",
            fecha=date.today() + timedelta(days=1),
            hora=time(10, 30),
            direccion="Av. Principal 123",
        )
        response = self.http.post(
            reverse("cliente_eliminar", args=[self.cliente.pk]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Cliente.objects.filter(pk=self.cliente.pk).exists())
        self.assertContains(
            response, "No se puede eliminar este cliente porque tiene citas registradas."
        )
