# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

import os
import sys
from pathlib import Path

import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.utils import autoreload

"""Lanzador local del aplicativo SIGEM.

Este archivo permite iniciar el sistema con un solo comando:
`python deploy_sigem.py`. Su responsabilidad es validar Django y levantar
el servidor WSGI local en el puerto institucional 8036. No crea bases, no
borra datos y no modifica estructuras PostgreSQL.
"""

# Carpeta raiz del proyecto SIGEM.
BASE_DIR = Path(__file__).resolve().parent
# Ruta esperada del archivo manage.py.
MANAGE_PY = BASE_DIR / "manage.py"
# Host 0.0.0.0 permite acceso local y desde red autorizada.
HOST = "0.0.0.0"
# Puerto oficial de trabajo local solicitado para SIGEM.
PORT = "8036"
# Hilos WSGI para atender HTML, CSS, JS e imagenes sin saturar la cola local.
WAITRESS_THREADS = int(os.getenv("SIGEM_WAITRESS_THREADS", "16"))
# Limite de conexiones concurrentes aceptadas por Waitress.
WAITRESS_CONNECTION_LIMIT = int(os.getenv("SIGEM_WAITRESS_CONNECTION_LIMIT", "200"))
# Tiempo maximo de canal inactivo antes de cerrar conexiones pendientes.
WAITRESS_CHANNEL_TIMEOUT = int(os.getenv("SIGEM_WAITRESS_CHANNEL_TIMEOUT", "120"))
# Autoreload permite refrescar cambios de templates/static/Python durante desarrollo.
AUTO_RELOAD = os.getenv("SIGEM_AUTORELOAD", "true").lower() == "true"


def validar_dependencias_servidor():
    """Verifica que Waitress exista en el ambiente Python activo."""
    try:
        # Waitress sirve la aplicacion WSGI sin mostrar el warning de runserver.
        from waitress import serve
    except ImportError as error:
        # Mensaje claro para instalar dependencias sin exponer detalles internos.
        mensaje = (
            "Falta la dependencia 'waitress' en el ambiente msp_01.\n\n"
            "Ejecute una sola vez:\n"
            "pip install -r requirements.txt\n\n"
            "Luego vuelva a iniciar:\n"
            "python deploy_sigem.py"
        )
        raise SystemExit(mensaje) from error

    # Se devuelve la funcion serve para usarla al levantar el servidor.
    return serve


def registrar_carpetas_autoreload(sender=None, **kwargs):
    """Registra carpetas que deben disparar recarga automatica."""
    # Django entrega el reloader como sender cuando inicia autoreload.
    reloader = sender
    if reloader is None:
        return

    # Carpetas que normalmente cambian durante desarrollo local.
    carpetas = [
        BASE_DIR / "templates",
        BASE_DIR / "static",
        BASE_DIR / "img",
        BASE_DIR / "sigem",
        BASE_DIR / "config_sigem",
    ]

    for carpeta in carpetas:
        # Solo se registra la carpeta si existe fisicamente.
        if carpeta.exists():
            reloader.watch_dir(carpeta, "**/*")


def mostrar_encabezado():
    """Muestra informacion de inicio y ejecuta `check` de Django."""
    print("=" * 60, flush=True)
    print("SIGEM", flush=True)
    print("Sistema de Gestion de Informacion Hospitalaria", flush=True)
    print("=" * 60, flush=True)
    print("Validando configuracion Django...", flush=True)
    # check valida settings, modelos, apps y configuracion general.
    call_command("check")
    print("Entorno Django: OK", flush=True)
    print("Aplicacion: SIGEM", flush=True)
    print("Servidor WSGI: Waitress", flush=True)
    print(f"Waitress threads: {WAITRESS_THREADS}", flush=True)
    print(f"Waitress connection_limit: {WAITRESS_CONNECTION_LIMIT}", flush=True)
    print(f"Autoreload: {'Activo' if AUTO_RELOAD else 'Inactivo'}", flush=True)
    print(f"Puerto: {PORT}", flush=True)
    print("", flush=True)
    print("Acceso local:", flush=True)
    print(f"http://127.0.0.1:{PORT}", flush=True)
    print("", flush=True)
    print("Servidor:", flush=True)
    print(f"http://{HOST}:{PORT}", flush=True)
    print("=" * 60, flush=True)


def levantar_servidor(serve):
    """Inicializa Django y levanta Waitress."""
    # Inicializa apps, modelos y configuracion Django.
    django.setup()
    # Registra carpetas para recarga cuando el servidor corre con autoreload.
    registrar_carpetas_autoreload()
    # Imprime informacion operativa antes de servir.
    mostrar_encabezado()

    # Obtiene la aplicacion WSGI configurada en config_sigem.
    aplicacion = get_wsgi_application()
    # Levanta el servidor en host y puerto definidos.
    serve(
        aplicacion,
        host=HOST,
        port=int(PORT),
        threads=WAITRESS_THREADS,
        connection_limit=WAITRESS_CONNECTION_LIMIT,
        channel_timeout=WAITRESS_CHANNEL_TIMEOUT,
    )


def main():
    """Punto principal del lanzador."""
    # Se evita iniciar si el usuario no esta en la raiz correcta del proyecto.
    if not MANAGE_PY.exists():
        raise SystemExit("No se encontro manage.py en la raiz del proyecto SIGEM.")

    # Define el settings module si no venia definido desde el ambiente.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config_sigem.settings")
    # Verifica Waitress antes de intentar iniciar.
    serve = validar_dependencias_servidor()

    if AUTO_RELOAD:
        # Conecta el registro de carpetas al ciclo de autoreload.
        autoreload.autoreload_started.connect(registrar_carpetas_autoreload)
        # Ejecuta el servidor bajo el reloader de Django.
        autoreload.run_with_reloader(levantar_servidor, serve)
    else:
        # Ejecuta una instancia directa cuando autoreload esta desactivado.
        levantar_servidor(serve)


if __name__ == "__main__":
    try:
        # Inicia el flujo principal.
        main()
    except KeyboardInterrupt:
        # Mensaje limpio cuando el usuario detiene con Ctrl+C.
        raise SystemExit("\nServidor SIGEM detenido por el usuario.")


