# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

from django.db import transaction

from .forms import datos_s01_desde_establecimiento
from .forms import NIVELES_ATENCION_PERMITIDOS
from .forms import normalizar_tiempo_traslado
from .models import EstablecimientoIngresado, RespuestaS01, RespuestaS02
from .models import SigesFormulario


"""Servicios de negocio reutilizables del aplicativo SIGES.

Este archivo separa consultas y persistencia para que `views.py` no se
convierta en un archivo demasiado grande. No contiene HTML ni logica visual.
"""


NIVELES_ATENCION_VALIDOS = {codigo for codigo, _ in NIVELES_ATENCION_PERMITIDOS}


def buscar_establecimientos(termino, nivel_atencion=None, limite=10):
    """Busca establecimientos por unicodigo y, si no hay resultados, por nombre."""
    # Se normaliza el termino para evitar busquedas con espacios innecesarios.
    termino = (termino or "").strip()
    # Se normaliza el nivel para filtrar solo los niveles funcionales permitidos.
    nivel_atencion = (nivel_atencion or "").strip()
    # Se exige un minimo de caracteres para no cargar demasiados registros.
    if len(termino) < 2 or nivel_atencion not in NIVELES_ATENCION_VALIDOS:
        return []

    # Primero se busca por unicodigo porque es el identificador principal.
    consulta = (
        EstablecimientoIngresado.objects
        .filter(uni_codigo__icontains=termino, nivel_atencion=nivel_atencion)
        # only reduce columnas traidas desde PostgreSQL.
        .only("uni_codigo", "uni_nombre", "establecimiento", "can_descripcion", "prv_descripcion", "nivel_atencion")
        .order_by("uni_codigo")
    )
    # Si no se encuentran codigos, se permite busqueda por nombre.
    if not consulta.exists():
        consulta = (
            EstablecimientoIngresado.objects
            .filter(uni_nombre__icontains=termino, nivel_atencion=nivel_atencion)
            .only("uni_codigo", "uni_nombre", "establecimiento", "can_descripcion", "prv_descripcion", "nivel_atencion")
            .order_by("uni_codigo")
        )

    # Se construye una lista JSON simple para el navegador.
    resultados = []
    for establecimiento in consulta[:limite]:
        resultados.append(
            {
                "unicodigo": establecimiento.uni_codigo,
                "nombre": establecimiento.uni_nombre or establecimiento.establecimiento or "",
                "ubicacion": " / ".join(
                    valor
                    for valor in [establecimiento.prv_descripcion, establecimiento.can_descripcion]
                    if valor
                ),
                "nivel_atencion": establecimiento.nivel_atencion or "",
            }
        )
    return resultados


def obtener_datos_establecimiento(unicodigo, nivel_atencion=None):
    """Obtiene datos institucionales de un establecimiento por unicodigo."""
    # Sin nivel valido no se autocompleta, porque cada nivel tendra formulario propio.
    nivel_atencion = (nivel_atencion or "").strip()
    if nivel_atencion not in NIVELES_ATENCION_VALIDOS:
        return None
    # Se recupera el primer registro que coincida con el unicodigo.
    filtros = {"uni_codigo": unicodigo, "nivel_atencion": nivel_atencion}
    establecimiento = EstablecimientoIngresado.objects.filter(**filtros).first()
    # Si no existe, la vista devolvera un 404 controlado.
    if not establecimiento:
        return None
    # Se transforma el modelo institucional a nombres de campos S01.
    return datos_s01_desde_establecimiento(establecimiento)


@transaction.atomic
def guardar_matriz_siges(*, cleaned_data, usuario, instancia=None):
    """Guarda cabecera, S01 y S02 de una matriz SIGES en una transaccion."""
    # Si no se recibe instancia, se crea una nueva cabecera de formulario.
    if instancia is None:
        instancia = SigesFormulario(usuario=usuario)

    # El unicodigo principal proviene de S01.
    instancia.unicodigo = cleaned_data["s01_dg01"].strip()
    # El nivel de atencion queda en cabecera para trazabilidad y formularios futuros por nivel.
    instancia.nivel_atencion = cleaned_data["nivel_atencion"].strip()
    # En esta etapa, guardar S02 marca la matriz como enviada.
    instancia.estado = "ENVIADO"
    # Se guarda o actualiza la cabecera.
    instancia.save()

    # update_or_create permite editar una matriz sin duplicar la respuesta S01.
    RespuestaS01.objects.update_or_create(
        formulario=instancia,
        defaults={
            # Se copian exclusivamente los campos de la seccion S01.
            campo: cleaned_data[campo]
            for campo in [
                "s01_dg01",
                "s01_dg02",
                "s01_dg03",
                "s01_dg04",
                "s01_dg05",
                "s01_dg06",
                "s01_dg07",
                "s01_dg08",
                "s01_dg09",
                "s01_dg10",
                "s01_dg11",
                "s01_dg12",
                "s01_dg13",
            ]
        },
    )

    # El tiempo capturado se transforma a horas y minutos operativos.
    horas_traslado, minutos_traslado = normalizar_tiempo_traslado(
        cleaned_data["s02_am04"],
        cleaned_data["s02_am04_unidad"],
    )

    # update_or_create permite guardar o reemplazar la respuesta S02 de la misma matriz.
    respuesta_s02, _ = RespuestaS02.objects.update_or_create(
        formulario=instancia,
        defaults={
            # Se asignan campos S02 ya validados por el formulario.
            "s02_am01": cleaned_data["s02_am01"],
            "s02_am02": cleaned_data["s02_am02"],
            "s02_am03": cleaned_data["s02_am03"],
            "s02_am04": cleaned_data["s02_am04"],
            "s02_am04_unidad": cleaned_data["s02_am04_unidad"],
            "s02_am04_horas": horas_traslado,
            "s02_am04_minutos": minutos_traslado,
            "s02_am05": cleaned_data["s02_am05"],
            "s02_am06": cleaned_data["s02_am06"],
        },
    )
    # full_clean ejecuta validaciones del modelo, incluida pertenencia de opciones.
    respuesta_s02.full_clean()
    # Se guarda luego de validar reglas del modelo.
    respuesta_s02.save()

    # Se devuelve la cabecera para redirigir al detalle.
    return instancia


