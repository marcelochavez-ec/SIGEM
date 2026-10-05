from django.core.management.base import BaseCommand
from django.db import connection, transaction

from siges.models import (
    FormularioOpcion,
    FormularioSeccion,
    FormularioValidacion,
    FormularioVariable,
)

"""Comando Django para cargar catalogos iniciales de SIGES.

El comando crea o actualiza secciones, variables, reglas obligatorias y
opciones base. Usa `update_or_create` para evitar duplicados y para que se
pueda ejecutar mas de una vez sin perder consistencia.
"""

# Definicion inicial de secciones y variables del formulario.
SECCIONES = [
    {
        # Codigo funcional de la seccion de datos generales.
        "codigo": "s01",
        "nombre": "Datos Generales",
        "descripcion": "Datos generales del establecimiento y responsable.",
        "orden": 1,
        # Cada tupla define codigo, etiqueta, control HTML y tipo de dato.
        "variables": [
            ("s01_dg01", "Unicodigo", "text", "texto"),
            ("s01_dg02", "Establecimiento de Salud", "text", "texto"),
            ("s01_dg03", "Tipologia", "text", "texto"),
            ("s01_dg04", "Institucion", "text", "texto"),
            ("s01_dg05", "Direccion Provincial", "text", "texto"),
            ("s01_dg06", "Canton", "text", "texto"),
            ("s01_dg07", "Parroquia", "text", "texto"),
            ("s01_dg08", "Direccion del Establecimiento", "text", "texto"),
            ("s01_dg09", "Permiso de funcionamiento", "text", "texto"),
            ("s01_dg10", "Estado del predio", "text", "texto"),
            ("s01_dg11", "Nombres completos del Responsable", "text", "texto"),
            ("s01_dg12", "Movil del Responsable", "text", "texto"),
            ("s01_dg13", "Cedula de identidad del Responsable", "text", "texto"),
        ],
    },
    {
        # Codigo funcional de la seccion de acceso y movilizacion.
        "codigo": "s02",
        "nombre": "Acceso y Movilización",
        "descripcion": "Acceso y movilización del establecimiento.",
        "orden": 2,
        "variables": [
            ("s02_am01", "Frontera", "radio", "catalogo"),
            ("s02_am02", "Medio de movilizacion", "select", "catalogo"),
            ("s02_am03", "Frecuencia del transporte publico", "select", "catalogo"),
            ("s02_am04", "Tiempo hasta el Establecimiento de Salud", "number", "decimal"),
            ("s02_am04_unidad", "Unidad del tiempo de traslado", "radio", "catalogo"),
            ("s02_am05", "Categoria de accesibilidad", "radio", "catalogo"),
            ("s02_am06", "Tipo de via", "select", "catalogo"),
        ],
    },
]


# Opciones de catalogo asociadas a variables tipo select.
OPCIONES = {
    # Catalogo dicotomico de frontera.
    "s02_am01": [
        (1, "Si", ""),
        (2, "No", ""),
    ],
    # Catalogo de medio de movilizacion.
    "s02_am02": [
        (1, "Terrestre", "Alta accesibilidad"),
        (2, "Fluvial", "Media accesibilidad"),
        (3, "Aereo", "Baja accesibilidad"),
    ],
    # Catalogo de frecuencia de transporte publico.
    "s02_am03": [
        (1, "Diaria", "Alta accesibilidad"),
        (2, "2 veces al dia", "Media accesibilidad"),
        (3, "1-2 veces por semana", "Baja accesibilidad"),
        (4, "Nunca", "Muy baja accesibilidad"),
    ],
    # Catalogo de unidad para el tiempo de traslado.
    "s02_am04_unidad": [
        (1, "Horas", ""),
        (2, "Minutos", ""),
    ],
    # Catalogo urbano/rural para categoria de accesibilidad.
    "s02_am05": [
        (1, "Urbano", "Alta accesibilidad"),
        (2, "Rural", "Media accesibilidad"),
    ],
    # Catalogo de tipo de via.
    "s02_am06": [
        (1, "Primer orden", "Alta accesibilidad"),
        (2, "Segundo orden", "Media accesibilidad"),
        (3, "Tercer orden", "Baja accesibilidad"),
    ],
}


SECCIONES_OBSOLETAS = ["s03"]
OBJETOS_OBSOLETOS_SQL = [
    ("VIEW", "vw_catalogo_s03"),
    ("TABLE", "respuesta_s03"),
]


class Command(BaseCommand):
    """Comando ejecutable mediante `python manage.py cargar_catalogos_siges`."""

    # Texto que Django muestra en la ayuda del comando.
    help = "Crea o actualiza secciones, variables y opciones iniciales de SIGES."

    @transaction.atomic
    def handle(self, *args, **options):
        """Ejecuta la carga idempotente de catalogos."""
        # Primero se eliminan secciones obsoletas para que no aparezcan en administracion.
        for codigo_obsoleto in SECCIONES_OBSOLETAS:
            # La eliminacion de FormularioSeccion borra variables, opciones y validaciones por cascada.
            FormularioSeccion.objects.filter(codigo__iexact=codigo_obsoleto).delete()

        # Luego se retiran objetos fisicos heredados de S03 si existen en el schema activo.
        with connection.cursor() as cursor:
            # La vista se elimina antes que la tabla para evitar dependencias.
            for tipo_objeto, nombre_objeto in OBJETOS_OBSOLETOS_SQL:
                # DROP IF EXISTS evita errores cuando el objeto ya fue retirado.
                cursor.execute(f"DROP {tipo_objeto} IF EXISTS {nombre_objeto} CASCADE")

        # La transaccion garantiza que se cargue todo o no se confirme nada.
        for seccion_cfg in SECCIONES:
            # Crea o actualiza la seccion por codigo institucional.
            seccion, _ = FormularioSeccion.objects.update_or_create(
                codigo=seccion_cfg["codigo"],
                defaults={
                    "nombre": seccion_cfg["nombre"],
                    "descripcion": seccion_cfg["descripcion"],
                    "orden": seccion_cfg["orden"],
                    "activo": True,
                },
            )

            # Recorre variables de la seccion preservando orden de captura.
            for orden, (codigo, etiqueta, tipo_control, tipo_dato) in enumerate(seccion_cfg["variables"], start=1):
                # Crea o actualiza la variable dentro de la seccion.
                variable, _ = FormularioVariable.objects.update_or_create(
                    seccion=seccion,
                    codigo=codigo,
                    defaults={
                        "etiqueta": etiqueta,
                        "tipo_control": tipo_control,
                        "tipo_dato": tipo_dato,
                        "unidad_medida": None,
                        "obligatorio": True,
                        "orden": orden,
                        "activo": True,
                    },
                )

                # Documenta que la variable es obligatoria para esta etapa.
                FormularioValidacion.objects.update_or_create(
                    variable=variable,
                    regla="obligatorio",
                    defaults={
                        "detalle": "Campo obligatorio de la matriz SIGES.",
                        "parametros_json": None,
                        "activo": True,
                    },
                )

                # Lista de opciones que deben quedar activas para la variable actual.
                codigos_activos = []
                for opcion_orden, (opcion_codigo, descripcion, nivel) in enumerate(OPCIONES.get(codigo, []), start=1):
                    # Se registra el codigo como activo.
                    codigos_activos.append(opcion_codigo)
                    # Crea o actualiza la opcion de catalogo.
                    FormularioOpcion.objects.update_or_create(
                        variable=variable,
                        codigo=opcion_codigo,
                        defaults={
                            "descripcion": descripcion,
                            "nivel_accesibilidad": nivel,
                            "orden": opcion_orden,
                            "activo": True,
                        },
                    )

                if codigos_activos:
                    # Opciones antiguas no presentes en la definicion se desactivan sin borrar.
                    variable.opciones.exclude(codigo__in=codigos_activos).update(activo=False)

        # Mensaje final visible en consola.
        self.stdout.write(self.style.SUCCESS("Catalogos SIGES cargados/actualizados correctamente."))


