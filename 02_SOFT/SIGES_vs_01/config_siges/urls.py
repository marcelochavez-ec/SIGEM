# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

from django.contrib import admin
from django.urls import include, path

"""Rutas raiz del proyecto Django SIGES."""

urlpatterns = [
    # Ruta del panel administrativo Django/Unfold.
    path("admin/", admin.site.urls),
    # Todas las rutas propias del aplicativo se delegan a siges.urls.
    path("", include("siges.urls")),
]
