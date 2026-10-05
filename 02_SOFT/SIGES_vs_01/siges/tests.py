from django.test import TestCase

from .models import FormularioOpcion, FormularioSeccion, FormularioVariable


class ModeloCatalogoTest(TestCase):
    def test_relacion_seccion_variable_opcion(self):
        seccion = FormularioSeccion.objects.create(
            codigo="s02",
            nombre="Acceso y Movilizacion",
            orden=2,
        )
        variable = FormularioVariable.objects.create(
            seccion=seccion,
            codigo="s02_am02",
            etiqueta="Medio de movilizacion",
            tipo_control="select",
            tipo_dato="catalogo",
            orden=1,
        )
        opcion = FormularioOpcion.objects.create(
            variable=variable,
            codigo=1,
            descripcion="Terrestre",
            nivel_accesibilidad="Alta accesibilidad",
            orden=1,
        )
        self.assertEqual(opcion.variable.seccion.codigo, "s02")
