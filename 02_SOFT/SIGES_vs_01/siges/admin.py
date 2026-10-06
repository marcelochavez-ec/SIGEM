# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    FormularioOpcion,
    FormularioSeccion,
    FormularioValidacion,
    FormularioVariable,
    RespuestaS01,
    RespuestaS02,
    SigesFormulario,
)

"""Configuracion del panel administrativo Django/Unfold para SIGES.

Este archivo define como se visualizan y administran modelos en `/admin/`.
No implementa reglas de negocio del formulario publico; solo organiza la
administracion tecnica y catalogos.
"""


class FormularioVariableInline(TabularInline):
    """Permite editar variables dentro de una seccion desde el admin."""

    # Modelo hijo que se muestra dentro de FormularioSeccion.
    model = FormularioVariable
    # No muestra filas vacias adicionales por defecto.
    extra = 0
    # Campos visibles en la tabla inline.
    fields = ("codigo", "etiqueta", "tipo_control", "tipo_dato", "obligatorio", "orden", "activo")
    # Permite abrir la variable completa desde el inline.
    show_change_link = True


@admin.register(FormularioSeccion)
class FormularioSeccionAdmin(ModelAdmin):
    """Administra secciones del formulario SIGES."""

    # Columnas visibles en el listado.
    list_display = ("codigo", "nombre", "orden", "activo")
    # Campos por los que se puede buscar.
    search_fields = ("codigo", "nombre")
    # Filtro lateral por estado.
    list_filter = ("activo",)
    list_filter_submit = True
    list_fullwidth = True
    # Agrupa campos del formulario administrativo.
    fieldsets = (
        ("Identificacion de la seccion", {"fields": ("codigo", "nombre", "descripcion")}),
        ("Orden y estado", {"fields": ("orden", "activo")}),
    )
    # Muestra variables relacionadas dentro de la seccion.
    inlines = [FormularioVariableInline]


@admin.register(FormularioVariable)
class FormularioVariableAdmin(ModelAdmin):
    """Administra variables/campos del formulario."""

    list_display = ("codigo", "etiqueta", "seccion", "tipo_control", "tipo_dato", "obligatorio", "orden", "activo")
    search_fields = ("codigo", "etiqueta")
    list_filter = ("seccion", "tipo_control", "tipo_dato", "obligatorio", "activo")
    list_filter_submit = True
    list_fullwidth = True
    autocomplete_fields = ("seccion",)
    fieldsets = (
        ("Trazabilidad SIGES", {"fields": ("seccion", "codigo", "etiqueta")}),
        ("Definicion del campo", {"fields": ("tipo_control", "tipo_dato", "unidad_medida", "obligatorio")}),
        ("Orden y estado", {"fields": ("orden", "activo")}),
    )


@admin.register(FormularioOpcion)
class FormularioOpcionAdmin(ModelAdmin):
    """Administra opciones de catalogo por variable."""

    list_display = ("variable", "codigo", "descripcion", "nivel_accesibilidad", "orden", "activo")
    search_fields = ("variable__codigo", "descripcion")
    list_filter = ("variable__seccion", "variable", "nivel_accesibilidad", "activo")
    list_filter_submit = True
    list_fullwidth = True
    autocomplete_fields = ("variable",)
    fieldsets = (
        ("Variable asociada", {"fields": ("variable",)}),
        ("Opcion", {"fields": ("codigo", "descripcion", "nivel_accesibilidad")}),
        ("Orden y estado", {"fields": ("orden", "activo")}),
    )


@admin.register(FormularioValidacion)
class FormularioValidacionAdmin(ModelAdmin):
    """Administra reglas documentables de validacion."""

    list_display = ("variable", "regla", "activo")
    search_fields = ("variable__codigo", "regla", "detalle")
    list_filter = ("activo", "regla")
    list_filter_submit = True
    autocomplete_fields = ("variable",)
    fieldsets = (
        ("Variable validada", {"fields": ("variable",)}),
        ("Regla", {"fields": ("regla", "detalle", "parametros_json", "activo")}),
    )


class RespuestaS01Inline(TabularInline):
    """Muestra respuesta S01 dentro de la cabecera del formulario."""

    model = RespuestaS01
    extra = 0
    max_num = 1
    can_delete = False


class RespuestaS02Inline(TabularInline):
    """Muestra respuesta S02 dentro de la cabecera del formulario."""

    model = RespuestaS02
    extra = 0
    max_num = 1
    can_delete = False


@admin.register(SigesFormulario)
class SigesFormularioAdmin(ModelAdmin):
    """Administra cabeceras de matrices SIGES."""

    list_display = ("id_formulario", "unicodigo", "nivel_atencion", "usuario", "estado", "version", "fecha_registro")
    search_fields = ("id_formulario", "unicodigo", "nivel_atencion", "usuario__username")
    list_filter = ("nivel_atencion", "estado", "version", "fecha_registro")
    list_filter_submit = True
    list_fullwidth = True
    readonly_fields = ("id_formulario", "fecha_registro", "fecha_actualizacion")
    fieldsets = (
        ("Identificacion", {"fields": ("id_formulario", "unicodigo", "nivel_atencion", "estado", "version")}),
        ("Auditoria", {"fields": ("usuario", "fecha_registro", "fecha_actualizacion")}),
    )
    inlines = [RespuestaS01Inline, RespuestaS02Inline]


@admin.register(RespuestaS01)
class RespuestaS01Admin(ModelAdmin):
    """Administra respuestas S01 de forma directa."""

    list_display = ("id_respuesta_s01", "formulario", "s01_dg01", "s01_dg02", "actualizado_en")
    search_fields = ("formulario__id_formulario", "formulario__unicodigo", "s01_dg01", "s01_dg02")
    list_fullwidth = True
    autocomplete_fields = ("formulario",)
    fieldsets = (
        ("Formulario", {"fields": ("formulario",)}),
        (
            "Datos institucionales",
            {
                "fields": (
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
                )
            },
        ),
        ("Responsable", {"fields": ("s01_dg11", "s01_dg12", "s01_dg13")}),
    )


@admin.register(RespuestaS02)
class RespuestaS02Admin(ModelAdmin):
    """Administra respuestas S02 de forma directa."""

    list_display = (
        "id_respuesta_s02",
        "formulario",
        "s02_am01",
        "s02_am04",
        "s02_am04_unidad",
        "s02_am04_horas",
        "s02_am04_minutos",
        "actualizado_en",
    )
    search_fields = ("formulario__id_formulario", "formulario__unicodigo", "s02_am01", "s02_am05")
    list_fullwidth = True
    autocomplete_fields = ("formulario", "s02_am02", "s02_am03", "s02_am06")
    fieldsets = (
        ("Formulario", {"fields": ("formulario",)}),
        (
            "Acceso y movilidad",
            {
                "fields": (
                    "s02_am01",
                    "s02_am02",
                    "s02_am03",
                    "s02_am04",
                    "s02_am04_unidad",
                    "s02_am04_horas",
                    "s02_am04_minutos",
                    "s02_am05",
                    "s02_am06",
                )
            },
        ),
    )


