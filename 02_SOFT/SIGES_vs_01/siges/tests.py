from django.test import TestCase

from .forms import S02AccesoMovilizacionForm
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


class S02TiempoTrasladoFormTest(TestCase):
    def setUp(self):
        self.seccion = FormularioSeccion.objects.create(
            codigo="s02",
            nombre="Acceso y Movilizacion",
            orden=2,
        )
        for orden, codigo in enumerate(["s02_am01", "s02_am02", "s02_am03", "s02_am04_unidad", "s02_am05", "s02_am06"], 1):
            variable = FormularioVariable.objects.create(
                seccion=self.seccion,
                codigo=codigo,
                etiqueta=codigo,
                tipo_control="radio" if codigo in ["s02_am01", "s02_am04_unidad", "s02_am05"] else "select",
                tipo_dato="catalogo",
                orden=orden,
            )
            if codigo == "s02_am01":
                FormularioOpcion.objects.create(variable=variable, codigo=1, descripcion="Si", orden=1)
                FormularioOpcion.objects.create(variable=variable, codigo=2, descripcion="No", orden=2)
            elif codigo == "s02_am04_unidad":
                FormularioOpcion.objects.create(variable=variable, codigo=1, descripcion="Horas", orden=1)
                FormularioOpcion.objects.create(variable=variable, codigo=2, descripcion="Minutos", orden=2)
            elif codigo == "s02_am05":
                FormularioOpcion.objects.create(variable=variable, codigo=1, descripcion="Urbano", orden=1)
                FormularioOpcion.objects.create(variable=variable, codigo=2, descripcion="Rural", orden=2)
            else:
                FormularioOpcion.objects.create(variable=variable, codigo=1, descripcion=f"Opcion {codigo}", orden=1)

    def payload_base(self, unidad, tiempo):
        return {
            "s02_am01": "Si",
            "s02_am02": FormularioOpcion.objects.get(variable__codigo="s02_am02").pk,
            "s02_am03": FormularioOpcion.objects.get(variable__codigo="s02_am03").pk,
            "s02_am04": tiempo,
            "s02_am04_unidad": unidad,
            "s02_am05": "Urbano",
            "s02_am06": FormularioOpcion.objects.get(variable__codigo="s02_am06").pk,
        }

    def test_horas_admite_decimal_desde_uno(self):
        form = S02AccesoMovilizacionForm(data=self.payload_base("Horas", "1.65"))
        self.assertTrue(form.is_valid(), form.errors)

    def test_horas_rechaza_cero(self):
        form = S02AccesoMovilizacionForm(data=self.payload_base("Horas", "0"))
        self.assertFalse(form.is_valid())
        self.assertIn("s02_am04", form.errors)

    def test_minutos_admite_hasta_cincuenta_y_nueve(self):
        form = S02AccesoMovilizacionForm(data=self.payload_base("Minutos", "59"))
        self.assertTrue(form.is_valid(), form.errors)

    def test_minutos_rechaza_sesenta(self):
        form = S02AccesoMovilizacionForm(data=self.payload_base("Minutos", "60"))
        self.assertFalse(form.is_valid())
        self.assertIn("s02_am04", form.errors)

    def test_minutos_rechaza_decimal_mayor_a_cincuenta_y_nueve(self):
        form = S02AccesoMovilizacionForm(data=self.payload_base("Minutos", "59.5"))
        self.assertFalse(form.is_valid())
        self.assertIn("s02_am04", form.errors)
