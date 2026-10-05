# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

from decimal import Decimal

from django import forms

from .models import EstablecimientoIngresado, FormularioOpcion


"""Formularios Django de la matriz SIGES.

Este archivo concentra campos, widgets y validaciones de entrada. La regla
del proyecto es que las validaciones del formulario vivan aqui y no se
concentren dentro de las vistas.
"""


def texto(valor):
    """Normaliza valores nulos o vacios para evitar errores al autocompletar."""
    return (valor or "").strip()


NIVELES_ATENCION_PERMITIDOS = [
    ("I NIVEL DE ATENCION", "I Nivel de atención"),
    ("II NIVEL DE ATENCION", "II Nivel de atención"),
    ("III NIVEL DE ATENCION", "III Nivel de atención"),
]


def datos_s01_desde_establecimiento(establecimiento):
    """Convierte un establecimiento institucional en datos iniciales S01."""
    # Se prioriza el nombre oficial y se usa `establecimiento` como respaldo.
    nombre = texto(establecimiento.uni_nombre) or texto(establecimiento.establecimiento)
    # La direccion base proviene de la fuente institucional.
    direccion = texto(establecimiento.uni_direccion)
    # Algunas fuentes pueden incluir una referencia adicional.
    referencia = texto(getattr(establecimiento, "direcc_referencia", ""))
    # Si la referencia existe y no esta incluida, se concatena para no perder informacion.
    if referencia and referencia not in direccion:
        direccion = f"{direccion} - {referencia}".strip(" -")

    # El diccionario devuelto usa los mismos nombres de campos del formulario S01.
    return {
        "s01_dg01": texto(establecimiento.uni_codigo),
        "s01_dg02": nombre or "No registra",
        "s01_dg03": texto(establecimiento.tipologia) or "No registra",
        "s01_dg04": texto(establecimiento.igu_descripcion) or "No registra",
        "s01_dg05": texto(establecimiento.dp_descripcion) or texto(establecimiento.prv_descripcion) or "No registra",
        "s01_dg06": texto(establecimiento.can_descripcion) or "No registra",
        "s01_dg07": texto(establecimiento.par_descripcion) or "No registra",
        "s01_dg08": direccion or "No registra",
        "s01_dg09": texto(establecimiento.estado) or "No registra",
        "s01_dg10": texto(establecimiento.dificilacceso) or "No registra",
        "s01_dg11": texto(establecimiento.represen_legal),
        "s01_dg12": texto(establecimiento.tlf_movil),
        "s01_dg13": texto(establecimiento.ced_ident_rep_legal),
    }


class BaseSigesForm(forms.Form):
    """Clase base para aplicar estilos comunes a formularios SIGES."""

    def aplicar_estilos(self):
        """Agrega clases CSS/Unfold a cada widget del formulario."""
        for campo in self.fields.values():
            # Clase comun para inputs de texto, numero y textarea.
            clase = "form-control unfold-input"
            # Los grupos de radio usan una clase propia porque no son cajas de texto.
            if isinstance(campo.widget, forms.RadioSelect):
                campo.widget.attrs.setdefault("class", "radio-options")
                campo.widget.attrs.setdefault("data-unfold-field", "true")
                continue
            # Los campos select reciben clases adicionales de selector.
            if isinstance(campo.widget, forms.Select):
                clase += " form-select unfold-select"
            # setdefault conserva clases definidas manualmente si existieran.
            campo.widget.attrs.setdefault("class", clase)
            # Atributo semantico para identificar campos del formulario desde CSS/JS.
            campo.widget.attrs.setdefault("data-unfold-field", "true")


class S01DatosGeneralesForm(BaseSigesForm):
    """Formulario de la seccion S01: Datos Generales."""

    # Nivel funcional usado para filtrar unicodigos antes de capturar S01.
    nivel_atencion = forms.ChoiceField(
        label="Nivel de atención del establecimiento de salud",
        choices=[("", "Seleccione nivel de atención...")] + NIVELES_ATENCION_PERMITIDOS,
        help_text="Seleccione si la matriz corresponde a un establecimiento de I, II o III nivel antes de buscar el unicódigo.",
    )
    # Campo clave que identifica al establecimiento.
    s01_dg01 = forms.CharField(
        label="Unicodigo",
        max_length=20,
        help_text="Código único institucional del establecimiento de salud seleccionado.",
    )
    # Campos institucionales que se autocompletan desde PostgreSQL.
    s01_dg02 = forms.CharField(label="Establecimiento de Salud", max_length=255, help_text="Nombre oficial del establecimiento registrado en la fuente institucional.")
    s01_dg03 = forms.CharField(label="Tipologia", max_length=150, help_text="Clasificación funcional o tipológica del establecimiento.")
    s01_dg04 = forms.CharField(label="Institucion", max_length=150, help_text="Institución responsable o administradora del establecimiento.")
    s01_dg05 = forms.CharField(label="Direccion Provincial", max_length=150, help_text="Dirección Provincial de Salud asociada al establecimiento.")
    s01_dg06 = forms.CharField(label="Canton", max_length=150, help_text="Cantón donde se ubica territorialmente el establecimiento.")
    s01_dg07 = forms.CharField(label="Parroquia", max_length=150, help_text="Parroquia registrada para la ubicación del establecimiento.")
    s01_dg08 = forms.CharField(label="Direccion del Establecimiento", max_length=255, help_text="Dirección física o referencia principal del establecimiento.")
    s01_dg09 = forms.CharField(label="Permiso de funcionamiento", max_length=150, help_text="Estado del permiso o habilitación funcional registrada.")
    s01_dg10 = forms.CharField(label="Estado del predio", max_length=150, help_text="Condición institucional reportada para el predio del establecimiento.")
    s01_dg11 = forms.CharField(label="Nombres completos del Responsable", max_length=255, help_text="Nombre de la persona responsable del establecimiento o de la información registrada.")
    s01_dg12 = forms.CharField(label="Movil del Responsable", max_length=30, help_text="Número móvil de contacto del responsable.")
    s01_dg13 = forms.CharField(label="Cedula de identidad del Responsable", max_length=20, help_text="Número de identificación del responsable.")

    def __init__(self, *args, **kwargs):
        """Configura atributos visuales y comportamiento de campos S01."""
        super().__init__(*args, **kwargs)
        # El unicodigo se puede escribir o llenar desde el buscador JS.
        self.fields["s01_dg01"].widget.attrs.update(
            {
                "placeholder": "Escriba o seleccione un unicodigo real",
                "autocomplete": "off",
                "data-establecimiento-campo": "unicodigo",
            }
        )
        self.fields["nivel_atencion"].widget.attrs.update(
            {
                "data-establecimiento-campo": "nivel_atencion",
            }
        )
        # Estos campos provienen de la fuente institucional y no se editan manualmente.
        for campo in [
            "s01_dg02",
            "s01_dg03",
            "s01_dg04",
            "s01_dg05",
            "s01_dg06",
            "s01_dg07",
            "s01_dg08",
            "s01_dg09",
            "s01_dg10",
        ]:
            # Se marcan como no requeridos en el formulario porque se autocompletan.
            self.fields[campo].required = False
            # readonly evita que el usuario modifique datos maestros institucionales.
            self.fields[campo].widget.attrs["readonly"] = "readonly"
            # El atributo data permite identificarlos desde CSS/JS si se requiere.
            self.fields[campo].widget.attrs["data-establecimiento-institucional"] = "true"
        # Se aplican clases visuales al final para cubrir todos los campos.
        self.aplicar_estilos()

    def clean_s01_dg01(self):
        """Valida que el unicodigo exista en la fuente institucional."""
        # Se limpia el valor escrito por el usuario.
        unicodigo = self.cleaned_data["s01_dg01"].strip()
        # Se lee el nivel ya validado por ChoiceField para cruzarlo con el unicodigo.
        nivel_atencion = self.cleaned_data.get("nivel_atencion")
        # Si no existe en PostgreSQL, el formulario no puede avanzar.
        if not EstablecimientoIngresado.objects.filter(
            uni_codigo=unicodigo,
            nivel_atencion=nivel_atencion,
        ).exists():
            raise forms.ValidationError(
                "Seleccione un unicodigo existente para el nivel de atencion seleccionado."
            )
        return unicodigo

    def clean(self):
        """Autocompleta datos institucionales faltantes despues de validar unicodigo."""
        cleaned_data = super().clean()
        # Se recupera el unicodigo ya validado por clean_s01_dg01.
        unicodigo = cleaned_data.get("s01_dg01")
        if not unicodigo:
            return cleaned_data

        # Se consulta el establecimiento real para completar campos institucionales.
        establecimiento = EstablecimientoIngresado.objects.filter(
            uni_codigo=unicodigo,
            nivel_atencion=cleaned_data.get("nivel_atencion"),
        ).first()
        if not establecimiento:
            return cleaned_data

        # Se transforma el establecimiento a campos S01.
        datos_institucionales = datos_s01_desde_establecimiento(establecimiento)
        for campo, valor in datos_institucionales.items():
            # Solo se reemplaza si el campo esta vacio, evitando pisar valores ya presentes.
            if campo in cleaned_data and not cleaned_data.get(campo):
                cleaned_data[campo] = valor
        return cleaned_data


class S02AccesoMovilizacionForm(BaseSigesForm):
    """Formulario de la seccion S02: Acceso y Movilizacion."""

    # Catalogo dicotomico de frontera; se guarda como etiqueta visible.
    s02_am01 = forms.ChoiceField(
        label="Frontera",
        choices=[],
        help_text="Indique si el establecimiento se ubica en una zona fronteriza.",
        widget=forms.RadioSelect,
    )
    # Catalogo de medios de movilizacion.
    s02_am02 = forms.ModelChoiceField(
        label="Medio de movilizacion",
        queryset=FormularioOpcion.objects.none(),
        empty_label="Seleccione...",
        help_text="Seleccione el medio principal utilizado para llegar al establecimiento.",
    )
    # Catalogo de frecuencia de transporte publico.
    s02_am03 = forms.ModelChoiceField(
        label="Frecuencia del transporte publico",
        queryset=FormularioOpcion.objects.none(),
        empty_label="Seleccione...",
        help_text="Registre con que frecuencia existe transporte publico hacia el establecimiento.",
    )
    # Campo numerico de tiempo; la regla funcional exige valores positivos.
    s02_am04 = forms.DecimalField(
        label="Tiempo hasta el Establecimiento de Salud",
        min_value=Decimal("1.00"),
        max_digits=6,
        decimal_places=2,
        help_text="Ingrese un valor positivo con maximo dos decimales segun la unidad seleccionada.",
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "1"}),
    )
    # Unidad del tiempo para diferenciar horas y minutos en la validacion.
    s02_am04_unidad = forms.ChoiceField(
        label="Unidad del tiempo de traslado",
        choices=[],
        help_text="Seleccione primero si el tiempo se expresara en horas o minutos.",
        widget=forms.RadioSelect,
    )
    # Catalogo territorial de accesibilidad; se guarda como etiqueta visible.
    s02_am05 = forms.ChoiceField(
        label="Categoria de accesibilidad",
        choices=[],
        help_text="Clasifique el entorno territorial del establecimiento como urbano o rural.",
        widget=forms.RadioSelect,
    )
    # Catalogo de tipos de via.
    s02_am06 = forms.ModelChoiceField(
        label="Tipo de via",
        queryset=FormularioOpcion.objects.none(),
        empty_label="Seleccione...",
        help_text="Seleccione el tipo de via principal de acceso al establecimiento.",
    )
    def __init__(self, *args, **kwargs):
        """Carga catalogos activos para los campos desplegables S02."""
        super().__init__(*args, **kwargs)

        for campo in ["s02_am01", "s02_am04_unidad", "s02_am05"]:
            # Estos campos se almacenan como texto, pero sus opciones visibles
            # se controlan desde formulario_opcion para evitar texto libre.
            opciones = (
                FormularioOpcion.objects
                .filter(variable__codigo=campo, variable__activo=True, activo=True)
                .select_related("variable")
                .order_by("orden")
            )
            self.fields[campo].choices = [(opcion.descripcion, opcion.descripcion) for opcion in opciones]

        for campo in ["s02_am02", "s02_am03", "s02_am06"]:
            # Cada campo consulta solo opciones activas de su variable correspondiente.
            self.fields[campo].queryset = (
                FormularioOpcion.objects
                .filter(variable__codigo=campo, variable__activo=True, activo=True)
                # select_related evita consultas adicionales al acceder a la variable.
                .select_related("variable")
                .order_by("orden")
            )

        # El valor del tiempo se habilita en navegador despues de elegir unidad.
        self.fields["s02_am04"].widget.attrs.update(
            {
                "data-tiempo-traslado": "valor",
                "placeholder": "Ejemplo: 1.65 horas o 45.5 minutos",
            }
        )
        # La unidad controla el estado visual del campo numerico de tiempo.
        self.fields["s02_am04_unidad"].widget.attrs.update({"data-tiempo-traslado": "unidad"})

        # Se aplican clases visuales al final.
        self.aplicar_estilos()

    def clean(self):
        """Valida la regla cruzada entre tiempo de traslado y unidad capturada."""
        cleaned_data = super().clean()
        # Se lee el valor numerico ya convertido por DecimalField.
        tiempo = cleaned_data.get("s02_am04")
        # Se lee la unidad controlada desde catalogo.
        unidad = cleaned_data.get("s02_am04_unidad")
        if tiempo is not None and unidad == "Horas" and tiempo < Decimal("1.00"):
            # Horas debe ser positivo y no admite cero.
            self.add_error("s02_am04", "Cuando la unidad es horas, ingrese un valor mayor o igual a 1.")
        if tiempo is not None and unidad == "Minutos" and not (Decimal("1.00") <= tiempo <= Decimal("59.00")):
            # Minutos debe quedar entre 1 y 59 para no duplicar una hora completa.
            self.add_error("s02_am04", "Cuando la unidad es minutos, ingrese un valor entre 1 y 59.")
        return cleaned_data
