from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CitaForm, ClienteForm
from .models import Cita, Cliente


def inicio(request: HttpRequest) -> HttpResponse:
    hoy = timezone.localdate()
    citas = Cita.objects.select_related("client").filter(fecha__gte=hoy)[:8]
    return render(
        request,
        "control/inicio.html",
        {
            "citas": citas,
            "total_clientes": Cliente.objects.count(),
            "total_citas": Cita.objects.count(),
            "citas_hoy": Cita.objects.filter(fecha=hoy).count(),
        },
    )


class ClienteListView(ListView):
    model = Cliente
    template_name = "control/clientes/lista.html"
    context_object_name = "clientes"

    def get_queryset(self):
        queryset = super().get_queryset()
        busqueda = self.request.GET.get("q", "").strip()
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda)
                | Q(apellido__icontains=busqueda)
                | Q(correo__icontains=busqueda)
                | Q(dni__icontains=busqueda)
                | Q(telefono__icontains=busqueda)
            )
        return queryset


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "control/formulario.html"
    success_url = reverse_lazy("clientes")
    extra_context = {"titulo": "Registrar cliente", "volver_url": "clientes"}

    def form_valid(self, form):
        messages.success(self.request, "El cliente se registró correctamente.")
        return super().form_valid(form)


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "control/formulario.html"
    success_url = reverse_lazy("clientes")
    extra_context = {"titulo": "Editar cliente", "volver_url": "clientes"}

    def form_valid(self, form):
        messages.success(self.request, "Los datos del cliente se actualizaron.")
        return super().form_valid(form)


def cliente_eliminar(request: HttpRequest, pk: int) -> HttpResponse:
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        if cliente.citas.exists():
            messages.error(
                request,
                "No se puede eliminar este cliente porque tiene citas registradas.",
            )
            return redirect("clientes")
        cliente.delete()
        messages.success(request, "El cliente se eliminó correctamente.")
        return redirect("clientes")
    return render(request, "control/clientes/eliminar.html", {"cliente": cliente})


class CitaListView(ListView):
    model = Cita
    template_name = "control/citas/lista.html"
    context_object_name = "citas"

    def get_queryset(self):
        queryset = Cita.objects.select_related("client")
        busqueda = self.request.GET.get("q", "").strip()
        estado = self.request.GET.get("estado", "").strip()
        if busqueda:
            queryset = queryset.filter(
                Q(asunto__icontains=busqueda)
                | Q(client__nombre__icontains=busqueda)
                | Q(client__apellido__icontains=busqueda)
                | Q(direccion__icontains=busqueda)
            )
        if estado in Cita.Estado.values:
            queryset = queryset.filter(estado=estado)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = Cita.Estado.choices
        context["estado_actual"] = self.request.GET.get("estado", "")
        return context


class CitaCreateView(CreateView):
    model = Cita
    form_class = CitaForm
    template_name = "control/formulario.html"
    success_url = reverse_lazy("citas")
    extra_context = {"titulo": "Agendar cita", "volver_url": "citas"}

    def form_valid(self, form):
        messages.success(self.request, "La cita se agendó correctamente.")
        return super().form_valid(form)


class CitaUpdateView(UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = "control/formulario.html"
    success_url = reverse_lazy("citas")
    extra_context = {"titulo": "Editar cita", "volver_url": "citas"}

    def form_valid(self, form):
        messages.success(self.request, "La cita se actualizó correctamente.")
        return super().form_valid(form)


class CitaDeleteView(DeleteView):
    model = Cita
    template_name = "control/citas/eliminar.html"
    success_url = reverse_lazy("citas")

    def form_valid(self, form):
        messages.success(self.request, "La cita se eliminó correctamente.")
        return super().form_valid(form)
