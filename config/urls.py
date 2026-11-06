"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from control import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.inicio, name="inicio"),
    path("clientes/", views.ClienteListView.as_view(), name="clientes"),
    path("clientes/nuevo/", views.ClienteCreateView.as_view(), name="cliente_crear"),
    path(
        "clientes/<int:pk>/editar/",
        views.ClienteUpdateView.as_view(),
        name="cliente_editar",
    ),
    path("clientes/<int:pk>/eliminar/", views.cliente_eliminar, name="cliente_eliminar"),
    path("citas/", views.CitaListView.as_view(), name="citas"),
    path("citas/nueva/", views.CitaCreateView.as_view(), name="cita_crear"),
    path("citas/<int:pk>/editar/", views.CitaUpdateView.as_view(), name="cita_editar"),
    path(
        "citas/<int:pk>/eliminar/",
        views.CitaDeleteView.as_view(),
        name="cita_eliminar",
    ),
]
