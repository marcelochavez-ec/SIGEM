# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

from django.urls import path

from . import views

"""Rutas del aplicativo SIGEM.

Cada path conecta una URL publica con una vista de `views.py`.
"""

# Namespace usado por reverse y etiquetas {% url 'sigem:...' %}.
app_name = "sigem"

urlpatterns = [
    # Endpoint de diagnostico tecnico.
    path("health/", views.health, name="health"),
    # Endpoint JSON para buscar establecimientos desde JavaScript.
    path("api/establecimientos/buscar/", views.api_buscar_establecimientos, name="api_buscar_establecimientos"),
    # Endpoint JSON para obtener detalle de un establecimiento.
    path("api/establecimientos/<str:unicodigo>/", views.api_detalle_establecimiento, name="api_detalle_establecimiento"),
    # Pantalla inicial.
    path("", views.inicio, name="inicio"),
    # Pantalla de gestion de establecimientos.
    path("establecimientos/", views.establecimientos, name="establecimientos"),
    # Pantalla visual de roles y usuarios.
    path("roles-usuarios/", views.roles_usuarios, name="roles_usuarios"),
    # Pantalla de reportes de monitoreo.
    path("reportes-monitoreo/", views.reportes_monitoreo, name="reportes_monitoreo"),
    # Pantalla del manual de usuario.
    path("manual/", views.manual_usuario, name="manual_usuario"),
    # Formulario para crear matriz nueva.
    path("matriz/nueva/", views.nueva_matriz, name="nueva_matriz"),
    # Detalle de una matriz existente.
    path("matriz/<int:pk>/", views.detalle_matriz, name="detalle_matriz"),
    # Edicion de una matriz existente.
    path("matriz/<int:pk>/editar/", views.editar_matriz, name="editar_matriz"),
]

