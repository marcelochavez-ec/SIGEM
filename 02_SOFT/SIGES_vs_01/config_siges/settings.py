# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

import json
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
from django.urls import reverse_lazy

"""Configuracion principal del proyecto Django SIGES.

Este archivo define ambiente, base de datos, aplicaciones instaladas,
templates, estaticos y configuracion visual de Unfold. No contiene vistas,
modelos ni reglas de negocio.
"""

# BASE_DIR apunta a la raiz del proyecto SIGES.
BASE_DIR = Path(__file__).resolve().parent.parent
# Conda guarda variables persistentes del ambiente msp_01 en este archivo.
MSP_CONDA_STATE = Path(r"C:\ProgramData\anaconda3\envs\msp_01\conda-meta\state")


def cargar_variables_msp_01():
    """Carga variables persistidas en Conda msp_01 sin usar archivos .env."""
    # Si el archivo de estado no existe, no se puede cargar nada.
    if not MSP_CONDA_STATE.exists():
        return

    # Se abre el archivo JSON de estado del ambiente Conda.
    with MSP_CONDA_STATE.open("r", encoding="utf-8") as archivo:
        estado = json.load(archivo)

    # Cada variable se copia al ambiente del proceso si aun no existe.
    for clave, valor in estado.get("env_vars", {}).items():
        os.environ.setdefault(clave, str(valor))


# Se cargan variables antes de leer configuracion sensible.
cargar_variables_msp_01()

# SIGES - configuracion Django para PostgreSQL institucional.

# SECRET_KEY usa valor de ambiente si existe; el valor por defecto solo sirve en desarrollo.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "SIGES-01-dev-change-this-key-before-production")
# DEBUG queda activo por defecto para desarrollo local.
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"
# ALLOWED_HOSTS permite controlar hosts autorizados por variable.
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")
# FORCE_SCRIPT_NAME permite publicar SIGES bajo una ruta base de Nginx, por ejemplo /siges.
FORCE_SCRIPT_NAME = os.getenv("DJANGO_FORCE_SCRIPT_NAME") or None
# USE_X_FORWARDED_HOST respeta el host publico enviado por el proxy institucional.
USE_X_FORWARDED_HOST = os.getenv("DJANGO_USE_X_FORWARDED_HOST", "true").lower() == "true"

# Aplicaciones instaladas en Django.
INSTALLED_APPS = [
    # Unfold debe declararse antes de admin para reemplazar la interfaz administrativa.
    "unfold",  # Debe ir antes de django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "siges.apps.SigesConfig",
]

# Middleware ejecutado en cada peticion HTTP.
MIDDLEWARE = [
    # Seguridad base de Django.
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise permite servir estaticos de forma simple en desarrollo/control.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Sesiones para conservar borradores S01/S02 temporalmente.
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # Proteccion CSRF para formularios POST.
    "django.middleware.csrf.CsrfViewMiddleware",
    # Autenticacion Django, necesaria para admin aunque el aplicativo aun no use login propio.
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Mensajes temporales para avisos al usuario.
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Archivo raiz de rutas del proyecto.
ROOT_URLCONF = "config_siges.urls"

# Configuracion de templates Django.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Carpeta global de templates institucionales.
        "DIRS": [BASE_DIR / "templates"],
        # Permite que Django busque templates dentro de apps instaladas.
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # request permite usar request dentro de templates si se requiere.
                "django.template.context_processors.request",
                # auth entrega usuario/permisos al admin y templates.
                "django.contrib.auth.context_processors.auth",
                # messages entrega mensajes temporales.
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Puntos de entrada WSGI/ASGI del proyecto.
WSGI_APPLICATION = "config_siges.wsgi.application"
ASGI_APPLICATION = "config_siges.asgi.application"

# Schema funcional usado por SIGES.
DB_SCHEMA = os.getenv("SIGES_DB_SCHEMA", "siges")
# La clave debe venir del ambiente Conda; no se escribe en codigo.
DB_PASSWORD = os.getenv("SIGES_DB_PASSWORD")

if not DB_PASSWORD:
    # Se detiene Django temprano si falta la clave, evitando errores confusos de conexion.
    raise ImproperlyConfigured(
        "Falta SIGES_DB_PASSWORD en el ambiente Conda msp_01. "
        "Configure la variable con: conda env config vars set SIGES_DB_PASSWORD=\"su_clave\""
    )

# Configuracion de PostgreSQL institucional.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # Base institucional definida para el aplicativo.
        "NAME": os.getenv("SIGES_DB_NAME", "productos_bm"),
        # Usuario PostgreSQL leido desde ambiente o valor de desarrollo.
        "USER": os.getenv("SIGES_DB_USER", "marcelo_chavez"),
        # Password obligatorio cargado desde msp_01.
        "PASSWORD": DB_PASSWORD,
        # Host institucional de PostgreSQL.
        "HOST": os.getenv("SIGES_DB_HOST", "10.64.100.191"),
        # Puerto estandar PostgreSQL.
        "PORT": os.getenv("SIGES_DB_PORT", "5432"),
        # Mantiene conexiones abiertas por 60 segundos para mejorar rendimiento local.
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            # search_path asegura que las tablas SIGES se consulten en schema siges.
            "options": f"-c search_path={DB_SCHEMA},public",
        },
    },
}

# Validadores estandar de contrasena Django para admin.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Idioma, zona horaria e internacionalizacion.
LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

# Configuracion de archivos estaticos.
# STATIC_URL cambia automaticamente cuando el aplicativo se publica bajo una ruta base.
STATIC_URL = f"{FORCE_SCRIPT_NAME.rstrip('/')}/static/" if FORCE_SCRIPT_NAME else "static/"
# Carpeta destino para collectstatic.
STATIC_ROOT = BASE_DIR / "staticfiles"
# Carpetas fuente de estaticos propios e imagenes institucionales.
STATICFILES_DIRS = [BASE_DIR / "static", BASE_DIR / "img"]
# Almacenamiento comprimido para estaticos servidos por WhiteNoise.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Tipo por defecto para llaves primarias generadas por Django.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuracion visual y navegacion del admin Unfold.
UNFOLD = {
    "THEME": "light",
    "SITE_TITLE": "SIGES",
    "SITE_HEADER": "SIGES",
    "SITE_SUBHEADER": "Sistema de Información para la Gestión de Establecimientos de Salud",
    "SITE_URL": reverse_lazy("siges:inicio"),
    "SITE_SYMBOL": "health_and_safety",
    "SITE_ICON": {
        "light": "health_and_safety",
        "dark": "health_and_safety",
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "href": lambda request: static("msp_favicon.png"),
            "type": "image/png",
        },
        {
            "rel": "shortcut icon",
            "href": lambda request: static("msp_favicon.png"),
            "type": "image/png",
        },
        {
            "rel": "apple-touch-icon",
            "href": lambda request: static("msp_favicon.png"),
        },
    ],
    "SITE_LOGO": {
        "light": lambda request: static("logo_msp.png"),
        "dark": lambda request: static("logo_msp.png"),
    },
    "SITE_DROPDOWN": [
        {
            "title": "Inicio SIGES",
            "icon": "home",
            "link": reverse_lazy("siges:inicio"),
        },
        {
            "title": "Establecimientos",
            "icon": "local_hospital",
            "link": reverse_lazy("siges:establecimientos"),
        },
        {
            "title": "Roles y usuarios",
            "icon": "manage_accounts",
            "link": reverse_lazy("siges:roles_usuarios"),
        },
    ],
    "STYLES": [
        lambda request: static("siges/css/unfold_admin.css"),
    ],
    "SCRIPTS": [
        lambda request: static("siges/js/unfold_admin.js"),
    ],
    "BORDER_RADIUS": "8px",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "SHOW_BACK_BUTTON": True,
    "COLORS": {
        "primary": {
            "50": "#eef8ff",
            "100": "#d8f0ff",
            "200": "#b9e4ff",
            "300": "#86d3ff",
            "400": "#45b8ff",
            "500": "#087bff",
            "600": "#006fd6",
            "700": "#0056a8",
            "800": "#073e76",
            "900": "#052c57",
            "950": "#031d38",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Aplicativo SIGES",
                "separator": True,
                "items": [
                    {
                        "title": "Inicio del aplicativo",
                        "icon": "home",
                        "link": reverse_lazy("siges:inicio"),
                    },
                    {
                        "title": "Establecimientos",
                        "icon": "local_hospital",
                        "link": reverse_lazy("siges:establecimientos"),
                    },
                    {
                        "title": "Nueva matriz",
                        "icon": "post_add",
                        "link": reverse_lazy("siges:nueva_matriz"),
                    },
                ],
            },
            {
                "title": "Roles y usuarios",
                "separator": True,
                "items": [
                    {
                        "title": "Usuarios",
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Crear usuario",
                        "icon": "person_add",
                        "link": reverse_lazy("admin:auth_user_add"),
                    },
                    {
                        "title": "Roles / grupos",
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": "Matriz SIGES",
                "separator": True,
                "items": [
                    {
                        "title": "Formularios registrados",
                        "icon": "assignment",
                        "link": reverse_lazy("admin:siges_sigesformulario_changelist"),
                    },
                    {
                        "title": "Secciones",
                        "icon": "view_list",
                        "link": reverse_lazy("admin:siges_formularioseccion_changelist"),
                    },
                    {
                        "title": "Variables",
                        "icon": "data_object",
                        "link": reverse_lazy("admin:siges_formulariovariable_changelist"),
                    },
                    {
                        "title": "Opciones",
                        "icon": "fact_check",
                        "link": reverse_lazy("admin:siges_formularioopcion_changelist"),
                    },
                ],
            },
        ],
    },
}


