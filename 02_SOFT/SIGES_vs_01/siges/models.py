# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


"""Modelos de datos del aplicativo SIGES.

Este archivo representa la capa Modelo dentro de Django. Su funcion es
describir las tablas, relaciones, restricciones y fuentes institucionales
que utiliza el aplicativo. No contiene HTML, CSS, JavaScript ni reglas de
presentacion.
"""


class EstablecimientoIngresado(models.Model):
    """Representa la vista institucional de establecimientos ingresados.

    Esta fuente se consulta para buscar unicodigos reales y autocompletar
    la seccion S01. Se define como `managed = False` porque ya existe en
    PostgreSQL y Django no debe crearla, eliminarla ni modificarla.
    """

    # Identificador tecnico de la vista; se usa como llave primaria en Django
    # para que el ORM pueda consultar registros individuales.
    uni_serial = models.TextField(primary_key=True)
    # Codigo institucional usado por el formulario SIGES como unicodigo.
    uni_codigo = models.TextField()
    # Nombre y atributos institucionales del establecimiento.
    uni_nombre = models.TextField(blank=True, null=True)
    uni_direccion = models.TextField(blank=True, null=True)
    prv_descripcion = models.TextField(blank=True, null=True)
    can_descripcion = models.TextField(blank=True, null=True)
    par_descripcion = models.TextField(blank=True, null=True)
    dis_descripcion = models.TextField(blank=True, null=True)
    tipologia = models.TextField(blank=True, null=True)
    igu_descripcion = models.TextField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    dificilacceso = models.TextField(blank=True, null=True)
    establecimiento = models.TextField(blank=True, null=True)
    nombre_comercial = models.TextField(blank=True, null=True)
    represen_legal = models.TextField(blank=True, null=True)
    tlf_movil = models.TextField(blank=True, null=True)
    ced_ident_rep_legal = models.TextField(blank=True, null=True)
    dp_descripcion = models.TextField(blank=True, null=True)
    nivel_atencion = models.TextField(blank=True, null=True)

    class Meta:
        # La fuente es una vista/tabla institucional existente; Django no la administra.
        managed = False
        # Gracias al search_path configurado, el nombre se resuelve en el schema siges.
        db_table = "vm_establecimientos_ingresados"
        verbose_name = "Establecimiento ingresado"
        verbose_name_plural = "Establecimientos ingresados"

    def __str__(self):
        """Devuelve una etiqueta legible para admin, depuracion y selects."""
        return f"{self.uni_codigo} - {self.uni_nombre or self.establecimiento or ''}"


class FormularioSeccion(models.Model):
    """Define una seccion funcional de la matriz SIGES."""

    # Llave primaria propia de la tabla de secciones.
    id_seccion = models.BigAutoField(primary_key=True)
    # Codigo institucional de seccion: por ejemplo S01 o S02.
    codigo = models.CharField(max_length=10, unique=True)
    # Nombre visible de la seccion.
    nombre = models.CharField(max_length=150)
    # Descripcion opcional para documentar el alcance funcional.
    descripcion = models.TextField(blank=True)
    # Orden de presentacion en el flujo secuencial.
    orden = models.SmallIntegerField()
    # Permite desactivar secciones sin borrar definiciones.
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "formulario_seccion"
        # Las secciones siempre se presentan segun el orden definido.
        ordering = ["orden"]
        verbose_name = "Seccion del formulario"
        verbose_name_plural = "Secciones del formulario"

    def __str__(self):
        """Muestra codigo y nombre para lectura humana."""
        return f"{self.codigo} - {self.nombre}"


class FormularioVariable(models.Model):
    """Define una variable o campo perteneciente a una seccion."""

    # Tipos de control disponibles para representar una variable en UI.
    TIPOS_CONTROL = [
        ("select", "Lista desplegable"),
        ("radio", "Opcion unica"),
        ("number", "Numerico"),
        ("text", "Texto"),
        ("date", "Fecha"),
        ("textarea", "Texto largo"),
    ]

    # Tipos de dato que ayudan a documentar la naturaleza de la variable.
    TIPOS_DATO = [
        ("catalogo", "Catalogo"),
        ("decimal", "Decimal"),
        ("entero", "Entero"),
        ("texto", "Texto"),
        ("fecha", "Fecha"),
    ]

    # Llave primaria de la variable.
    id_variable = models.BigAutoField(primary_key=True)
    # Relaciona cada variable con su seccion funcional.
    seccion = models.ForeignKey(
        FormularioSeccion,
        db_column="id_seccion",
        on_delete=models.CASCADE,
        related_name="variables",
    )
    # Codigo institucional de la variable: por ejemplo s02_am02.
    codigo = models.CharField(max_length=30)
    # Etiqueta visible para usuario y administracion.
    etiqueta = models.CharField(max_length=255)
    # Control HTML esperado para capturar el dato.
    tipo_control = models.CharField(max_length=20, choices=TIPOS_CONTROL)
    # Tipo logico del dato.
    tipo_dato = models.CharField(max_length=20, choices=TIPOS_DATO)
    # Unidad opcional, por ejemplo horas.
    unidad_medida = models.CharField(max_length=30, null=True, blank=True)
    # Indica si el dato es obligatorio.
    obligatorio = models.BooleanField(default=True)
    # Orden de presentacion dentro de la seccion.
    orden = models.SmallIntegerField()
    # Estado logico para ocultar sin borrar.
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "formulario_variable"
        ordering = ["seccion__orden", "orden"]
        constraints = [
            # Evita duplicar codigos dentro de la misma seccion.
            models.UniqueConstraint(fields=["seccion", "codigo"], name="uq_variable_seccion_codigo"),
            # Evita dos variables con el mismo orden dentro de una seccion.
            models.UniqueConstraint(fields=["seccion", "orden"], name="uq_variable_seccion_orden"),
        ]
        verbose_name = "Variable"
        verbose_name_plural = "Variables"

    def __str__(self):
        """Devuelve codigo y etiqueta para trazabilidad."""
        return f"{self.codigo} - {self.etiqueta}"


class FormularioOpcion(models.Model):
    """Define opciones de catalogo para variables tipo lista."""

    # Llave primaria de la opcion.
    id_opcion = models.BigAutoField(primary_key=True)
    # Variable a la que pertenece la opcion.
    variable = models.ForeignKey(
        FormularioVariable,
        db_column="id_variable",
        on_delete=models.CASCADE,
        related_name="opciones",
    )
    # Codigo numerico de la opcion dentro del catalogo.
    codigo = models.SmallIntegerField()
    # Texto visible de la opcion.
    descripcion = models.CharField(max_length=150)
    # Clasificacion opcional para reglas de accesibilidad.
    nivel_accesibilidad = models.CharField(max_length=30, blank=True)
    # Orden de visualizacion.
    orden = models.SmallIntegerField()
    # Permite retirar una opcion sin borrarla.
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "formulario_opcion"
        ordering = ["variable__orden", "orden"]
        constraints = [
            # Evita codigos repetidos en una misma variable.
            models.UniqueConstraint(fields=["variable", "codigo"], name="uq_opcion_variable_codigo"),
            # Evita ambiguedad de orden dentro de una variable.
            models.UniqueConstraint(fields=["variable", "orden"], name="uq_opcion_variable_orden"),
        ]
        verbose_name = "Opcion"
        verbose_name_plural = "Opciones"

    def __str__(self):
        """Devuelve la etiqueta visible que debe leer el usuario final."""
        return self.descripcion


class FormularioValidacion(models.Model):
    """Documenta reglas de validacion asociadas a una variable."""

    # Llave primaria de la regla.
    id_validacion = models.BigAutoField(primary_key=True)
    # Variable sobre la que aplica la regla.
    variable = models.ForeignKey(
        FormularioVariable,
        db_column="id_variable",
        on_delete=models.CASCADE,
        related_name="validaciones",
    )
    # Nombre corto de la regla, por ejemplo requerido o rango.
    regla = models.CharField(max_length=80)
    # Explicacion funcional de la regla.
    detalle = models.TextField()
    # Parametros flexibles para reglas futuras sin alterar columnas.
    parametros_json = models.JSONField(null=True, blank=True)
    # Estado logico de la regla.
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "formulario_validacion"
        constraints = [
            # Una variable no debe tener dos reglas con el mismo nombre.
            models.UniqueConstraint(fields=["variable", "regla"], name="uq_validacion_variable_regla")
        ]
        verbose_name = "Validacion"
        verbose_name_plural = "Validaciones"

    def __str__(self):
        """Identifica la regla por variable y nombre."""
        return f"{self.variable.codigo} - {self.regla}"


class SigesFormulario(models.Model):
    """Cabecera de una matriz SIGES registrada.

    El nombre tecnico de la clase queda alineado con SIGES para que la capa
    modelo, el admin, las vistas y la documentacion compartan la misma identidad.
    """

    # Estados permitidos para el ciclo basico del formulario.
    ESTADOS = [
        ("BORRADOR", "Borrador"),
        ("ENVIADO", "Enviado"),
        ("VALIDADO", "Validado"),
        ("ANULADO", "Anulado"),
    ]

    # Secuencial institucional del formulario, generado por PostgreSQL de 1 a N.
    id_formulario = models.AutoField(primary_key=True)
    # Usuario Django opcional; se deja nullable porque la autenticacion funcional aun no se implementa.
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="id_usuario",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="formularios_siges",
    )
    # Auditoria de creacion y modificacion.
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    # Version permite evolucionar la matriz sin perder trazabilidad.
    version = models.PositiveIntegerField(default=1)
    # Estado funcional de la matriz.
    estado = models.CharField(max_length=20, choices=ESTADOS, default="BORRADOR")
    # Unicodigo principal de la matriz; se indexa porque se usa en busquedas.
    unicodigo = models.CharField(max_length=20, db_index=True)
    # Nivel de atencion seleccionado para filtrar unicodigos y enrutar formularios futuros.
    nivel_atencion = models.CharField(max_length=80, default="I NIVEL DE ATENCION", db_index=True)
    class Meta:
        db_table = "siges_formulario"
        ordering = ["-fecha_registro"]
        constraints = [
            # Refuerza en base que solo se guarden estados conocidos.
            models.CheckConstraint(
                condition=Q(estado__in=["BORRADOR", "ENVIADO", "VALIDADO", "ANULADO"]),
                name="ck_siges_formulario_estado",
            )
        ]
        verbose_name = "Formulario SIGES"
        verbose_name_plural = "Formularios SIGES"

    def __str__(self):
        """Resume formulario, unicodigo y estado."""
        return f"{self.id_formulario} | {self.unicodigo} | {self.estado}"


class RespuestaS01(models.Model):
    """Almacena la seccion S01: datos generales del establecimiento."""

    # Llave primaria de la respuesta S01.
    id_respuesta_s01 = models.BigAutoField(primary_key=True)
    # Cada formulario tiene exactamente una respuesta S01.
    formulario = models.OneToOneField(
        SigesFormulario,
        db_column="id_formulario",
        on_delete=models.CASCADE,
        related_name="respuesta_s01",
    )
    # Campos institucionales y del responsable asociados a S01.
    s01_dg01 = models.CharField("Unicodigo", max_length=20)
    s01_dg02 = models.CharField("Establecimiento de Salud", max_length=255)
    s01_dg03 = models.CharField("Tipologia", max_length=150)
    s01_dg04 = models.CharField("Institucion", max_length=150)
    s01_dg05 = models.CharField("Direccion Provincial", max_length=150)
    s01_dg06 = models.CharField("Canton", max_length=150)
    s01_dg07 = models.CharField("Parroquia", max_length=150)
    s01_dg08 = models.CharField("Direccion del Establecimiento", max_length=255)
    s01_dg09 = models.CharField("Permiso de funcionamiento", max_length=150)
    s01_dg10 = models.CharField("Estado del predio", max_length=150)
    s01_dg11 = models.CharField("Nombres completos del Responsable", max_length=255)
    s01_dg12 = models.CharField("Movil del Responsable", max_length=30)
    s01_dg13 = models.CharField("Cedula de identidad del Responsable", max_length=20)
    # Auditoria propia de la respuesta.
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "respuesta_s01"
        verbose_name = "Respuesta S01"
        verbose_name_plural = "Respuestas S01"

    def __str__(self):
        """Identifica la respuesta por formulario padre."""
        return f"S01 - {self.formulario_id}"


class RespuestaS02(models.Model):
    """Almacena la seccion S02: acceso y movilizacion."""

    # Opciones controladas para variables que se guardan como etiqueta.
    OPCIONES_FRONTERA = [("Si", "Si"), ("No", "No")]
    # Unidades permitidas para interpretar el tiempo de traslado.
    OPCIONES_UNIDAD_TIEMPO = [("Horas", "Horas"), ("Minutos", "Minutos")]
    # Opciones territoriales permitidas para accesibilidad.
    OPCIONES_CATEGORIA_ACCESIBILIDAD = [("Urbano", "Urbano"), ("Rural", "Rural")]

    # Llave primaria de la respuesta S02.
    id_respuesta_s02 = models.BigAutoField(primary_key=True)
    # Cada formulario tiene exactamente una respuesta S02.
    formulario = models.OneToOneField(
        SigesFormulario,
        db_column="id_formulario",
        on_delete=models.CASCADE,
        related_name="respuesta_s02",
    )
    # Frontera se captura desde catalogo dicotomico y se guarda como etiqueta.
    s02_am01 = models.CharField("Frontera", max_length=150, choices=OPCIONES_FRONTERA)
    # Medio de movilizacion se toma del catalogo de opciones.
    s02_am02 = models.ForeignKey(
        FormularioOpcion,
        db_column="s02_am02",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="Medio de movilizacion",
    )
    # Frecuencia de transporte publico se toma del catalogo de opciones.
    s02_am03 = models.ForeignKey(
        FormularioOpcion,
        db_column="s02_am03",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="Frecuencia del transporte publico",
    )
    # Tiempo numerico hasta el establecimiento; su unidad se guarda en s02_am04_unidad.
    s02_am04 = models.DecimalField("Tiempo hasta el Establecimiento de Salud", max_digits=6, decimal_places=2)
    # Unidad seleccionada para interpretar el tiempo de traslado.
    s02_am04_unidad = models.CharField(
        "Unidad del tiempo de traslado",
        max_length=10,
        choices=OPCIONES_UNIDAD_TIEMPO,
        default="Horas",
    )
    # Horas completas normalizadas para reportes y consultas.
    s02_am04_horas = models.PositiveIntegerField("Horas de traslado", default=0)
    # Minutos normalizados, sin decimales y siempre menores a una hora.
    s02_am04_minutos = models.PositiveIntegerField("Minutos de traslado", default=0)
    # Categoria de accesibilidad se captura desde catalogo urbano/rural.
    s02_am05 = models.CharField(
        "Categoria de accesibilidad",
        max_length=150,
        choices=OPCIONES_CATEGORIA_ACCESIBILIDAD,
    )
    # Tipo de via se toma del catalogo de opciones.
    s02_am06 = models.ForeignKey(
        FormularioOpcion,
        db_column="s02_am06",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="Tipo de via",
    )
    # Auditoria propia de la respuesta.
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "respuesta_s02"
        constraints = [
            # La base de datos limita las unidades funcionales disponibles.
            models.CheckConstraint(
                condition=Q(s02_am04_unidad__in=["Horas", "Minutos"]),
                name="ck_respuesta_s02_am04_unidad",
            ),
            # El tiempo debe ser positivo y respetar el rango definido por unidad.
            models.CheckConstraint(
                condition=(
                    Q(s02_am04_unidad="Horas", s02_am04__gte=1)
                    | Q(s02_am04_unidad="Minutos", s02_am04__gte=1, s02_am04__lte=59)
                ),
                name="ck_respuesta_s02_am04_rango_unidad",
            ),
            # El resultado normalizado debe conservar minutos enteros entre 0 y 59.
            models.CheckConstraint(
                condition=Q(s02_am04_horas__gte=0, s02_am04_minutos__gte=0, s02_am04_minutos__lte=59),
                name="ck_respuesta_s02_am04_horas_minutos",
            ),
        ]
        verbose_name = "Respuesta S02"
        verbose_name_plural = "Respuestas S02"

    def clean(self):
        """Verifica que cada opcion seleccionada pertenezca a su variable esperada."""
        super().clean()
        # Mapa entre campo del modelo y codigo de variable permitido.
        esperadas = {
            "s02_am02": "s02_am02",
            "s02_am03": "s02_am03",
            "s02_am06": "s02_am06",
        }
        # Diccionario de errores que Django mostrara por campo.
        errores = {}

        for campo, codigo_variable in esperadas.items():
            # Se recupera la opcion seleccionada en el campo actual.
            opcion = getattr(self, campo, None)
            # Si la opcion existe pero pertenece a otra variable, se marca error.
            if opcion and opcion.variable.codigo != codigo_variable:
                errores[campo] = (
                    f"La opcion seleccionada pertenece a {opcion.variable.codigo} "
                    f"y no a {codigo_variable}."
                )

        if self.s02_am04_unidad == "Horas" and self.s02_am04 is not None and self.s02_am04 < Decimal("1.00"):
            # Horas no admite cero ni valores menores a una hora.
            errores["s02_am04"] = "Cuando la unidad es horas, ingrese un valor mayor o igual a 1."

        if (
            self.s02_am04_unidad == "Minutos"
            and self.s02_am04 is not None
            and not (Decimal("1.00") <= self.s02_am04 <= Decimal("59.00"))
        ):
            # Minutos queda limitado a 1..59 para mantener consistencia temporal.
            errores["s02_am04"] = "Cuando la unidad es minutos, ingrese un valor entre 1 y 59."

        if self.s02_am04_unidad == "Minutos" and self.s02_am04 is not None:
            if self.s02_am04 != self.s02_am04.to_integral_value():
                # Minutos capturados no admiten decimales.
                errores["s02_am04"] = "Cuando la unidad es minutos, ingrese solo valores enteros."

        if self.s02_am04_minutos is not None and self.s02_am04_minutos > 59:
            # Minutos normalizados nunca pueden completar otra hora.
            errores["s02_am04_minutos"] = "Los minutos normalizados deben estar entre 0 y 59."

        if errores:
            # ValidationError permite asociar errores al campo correspondiente.
            raise ValidationError(errores)

    def __str__(self):
        """Identifica la respuesta por formulario padre."""
        return f"S02 - {self.formulario_id}"


