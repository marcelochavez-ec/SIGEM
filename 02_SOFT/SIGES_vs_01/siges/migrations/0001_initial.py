import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


SQL_BOOTSTRAP_SIGES = """
CREATE TABLE IF NOT EXISTS formulario_seccion (
    id_seccion bigserial PRIMARY KEY,
    codigo varchar(10) NOT NULL,
    nombre varchar(150) NOT NULL,
    descripcion text,
    orden smallint NOT NULL,
    activo boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS formulario_variable (
    id_variable bigserial PRIMARY KEY,
    id_seccion bigint NOT NULL REFERENCES formulario_seccion(id_seccion) ON DELETE CASCADE,
    codigo varchar(30) NOT NULL,
    etiqueta varchar(255) NOT NULL,
    tipo_control varchar(20) NOT NULL,
    tipo_dato varchar(20) NOT NULL,
    unidad_medida varchar(30),
    obligatorio boolean NOT NULL DEFAULT true,
    orden smallint NOT NULL,
    activo boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS formulario_opcion (
    id_opcion bigserial PRIMARY KEY,
    id_variable bigint NOT NULL REFERENCES formulario_variable(id_variable) ON DELETE CASCADE,
    codigo smallint NOT NULL,
    descripcion varchar(150) NOT NULL,
    nivel_accesibilidad varchar(30) NOT NULL DEFAULT '',
    orden smallint NOT NULL,
    activo boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS siges_formulario (
    id_formulario serial PRIMARY KEY,
    id_usuario bigint REFERENCES auth_user(id) ON DELETE SET NULL,
    fecha_registro timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    version integer NOT NULL DEFAULT 1,
    estado varchar(20) NOT NULL DEFAULT 'BORRADOR',
    unicodigo varchar(20) NOT NULL,
    nivel_atencion varchar(80) NOT NULL DEFAULT 'I NIVEL DE ATENCION'
);

CREATE TABLE IF NOT EXISTS formulario_validacion (
    id_validacion bigserial PRIMARY KEY,
    id_variable bigint NOT NULL REFERENCES formulario_variable(id_variable) ON DELETE CASCADE,
    regla varchar(80) NOT NULL,
    detalle text NOT NULL,
    parametros_json jsonb,
    activo boolean NOT NULL DEFAULT true
);

CREATE TABLE IF NOT EXISTS respuesta_s01 (
    id_respuesta_s01 bigserial PRIMARY KEY,
    id_formulario integer NOT NULL UNIQUE REFERENCES siges_formulario(id_formulario) ON DELETE CASCADE,
    s01_dg01 varchar(20) NOT NULL,
    s01_dg02 varchar(255) NOT NULL,
    s01_dg03 varchar(150) NOT NULL,
    s01_dg04 varchar(150) NOT NULL,
    s01_dg05 varchar(150) NOT NULL,
    s01_dg06 varchar(150) NOT NULL,
    s01_dg07 varchar(150) NOT NULL,
    s01_dg08 varchar(255) NOT NULL,
    s01_dg09 varchar(150) NOT NULL,
    s01_dg10 varchar(150) NOT NULL,
    s01_dg11 varchar(255) NOT NULL,
    s01_dg12 varchar(30) NOT NULL,
    s01_dg13 varchar(20) NOT NULL,
    creado_en timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS respuesta_s02 (
    id_respuesta_s02 bigserial PRIMARY KEY,
    id_formulario integer NOT NULL UNIQUE REFERENCES siges_formulario(id_formulario) ON DELETE CASCADE,
    s02_am01 varchar(150) NOT NULL,
    s02_am02 bigint NOT NULL REFERENCES formulario_opcion(id_opcion) ON DELETE RESTRICT,
    s02_am03 bigint NOT NULL REFERENCES formulario_opcion(id_opcion) ON DELETE RESTRICT,
    s02_am04 numeric(6, 2) NOT NULL,
    s02_am04_unidad varchar(10) NOT NULL DEFAULT 'Horas',
    s02_am05 varchar(150) NOT NULL,
    s02_am06 bigint NOT NULL REFERENCES formulario_opcion(id_opcion) ON DELETE RESTRICT,
    creado_en timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS siges_formulario_unicodigo_idx ON siges_formulario (unicodigo);
CREATE INDEX IF NOT EXISTS siges_formulario_nivel_atencion_idx ON siges_formulario (nivel_atencion);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_variable_seccion_codigo') THEN
        ALTER TABLE formulario_variable ADD CONSTRAINT uq_variable_seccion_codigo UNIQUE (id_seccion, codigo);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_variable_seccion_orden') THEN
        ALTER TABLE formulario_variable ADD CONSTRAINT uq_variable_seccion_orden UNIQUE (id_seccion, orden);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_opcion_variable_codigo') THEN
        ALTER TABLE formulario_opcion ADD CONSTRAINT uq_opcion_variable_codigo UNIQUE (id_variable, codigo);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_opcion_variable_orden') THEN
        ALTER TABLE formulario_opcion ADD CONSTRAINT uq_opcion_variable_orden UNIQUE (id_variable, orden);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'uq_validacion_variable_regla') THEN
        ALTER TABLE formulario_validacion ADD CONSTRAINT uq_validacion_variable_regla UNIQUE (id_variable, regla);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_siges_formulario_estado') THEN
        ALTER TABLE siges_formulario ADD CONSTRAINT ck_siges_formulario_estado
        CHECK (estado IN ('BORRADOR', 'ENVIADO', 'VALIDADO', 'ANULADO'));
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_respuesta_s02_am04_unidad') THEN
        ALTER TABLE respuesta_s02 ADD CONSTRAINT ck_respuesta_s02_am04_unidad CHECK (s02_am04_unidad IN ('Horas', 'Minutos'));
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_respuesta_s02_am04_rango_unidad') THEN
        ALTER TABLE respuesta_s02 ADD CONSTRAINT ck_respuesta_s02_am04_rango_unidad
        CHECK (
            (s02_am04_unidad = 'Horas' AND s02_am04 >= 1)
            OR (s02_am04_unidad = 'Minutos' AND s02_am04 >= 1 AND s02_am04 <= 59)
        );
    END IF;
END
$$;
"""


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(SQL_BOOTSTRAP_SIGES, reverse_sql=migrations.RunSQL.noop),
            ],
            state_operations=[
        migrations.CreateModel(
            name="FormularioSeccion",
            fields=[
                ("id_seccion", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo", models.CharField(max_length=10, unique=True)),
                ("nombre", models.CharField(max_length=150)),
                ("descripcion", models.TextField(blank=True)),
                ("orden", models.SmallIntegerField()),
                ("activo", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Seccion del formulario",
                "verbose_name_plural": "Secciones del formulario",
                "db_table": "formulario_seccion",
                "ordering": ["orden"],
            },
        ),
        migrations.CreateModel(
            name="SigesFormulario",
            fields=[
                ("id_formulario", models.AutoField(primary_key=True, serialize=False)),
                ("fecha_registro", models.DateTimeField(auto_now_add=True)),
                ("fecha_actualizacion", models.DateTimeField(auto_now=True)),
                ("version", models.PositiveIntegerField(default=1)),
                ("estado", models.CharField(choices=[("BORRADOR", "Borrador"), ("ENVIADO", "Enviado"), ("VALIDADO", "Validado"), ("ANULADO", "Anulado")], default="BORRADOR", max_length=20)),
                ("unicodigo", models.CharField(db_index=True, max_length=20)),
                ("nivel_atencion", models.CharField(db_index=True, default="I NIVEL DE ATENCION", max_length=80)),
                ("usuario", models.ForeignKey(blank=True, db_column="id_usuario", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="formularios_siges", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Formulario SIGES",
                "verbose_name_plural": "Formularios SIGES",
                "db_table": "siges_formulario",
                "ordering": ["-fecha_registro"],
            },
        ),
        migrations.CreateModel(
            name="FormularioVariable",
            fields=[
                ("id_variable", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo", models.CharField(max_length=30)),
                ("etiqueta", models.CharField(max_length=255)),
                ("tipo_control", models.CharField(choices=[("select", "Lista desplegable"), ("radio", "Opcion unica"), ("number", "Numerico"), ("text", "Texto"), ("date", "Fecha"), ("textarea", "Texto largo")], max_length=20)),
                ("tipo_dato", models.CharField(choices=[("catalogo", "Catalogo"), ("decimal", "Decimal"), ("entero", "Entero"), ("texto", "Texto"), ("fecha", "Fecha")], max_length=20)),
                ("unidad_medida", models.CharField(blank=True, max_length=30, null=True)),
                ("obligatorio", models.BooleanField(default=True)),
                ("orden", models.SmallIntegerField()),
                ("activo", models.BooleanField(default=True)),
                ("seccion", models.ForeignKey(db_column="id_seccion", on_delete=django.db.models.deletion.CASCADE, related_name="variables", to="siges.formularioseccion")),
            ],
            options={
                "verbose_name": "Variable",
                "verbose_name_plural": "Variables",
                "db_table": "formulario_variable",
                "ordering": ["seccion__orden", "orden"],
            },
        ),
        migrations.CreateModel(
            name="FormularioOpcion",
            fields=[
                ("id_opcion", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo", models.SmallIntegerField()),
                ("descripcion", models.CharField(max_length=150)),
                ("nivel_accesibilidad", models.CharField(blank=True, max_length=30)),
                ("orden", models.SmallIntegerField()),
                ("activo", models.BooleanField(default=True)),
                ("variable", models.ForeignKey(db_column="id_variable", on_delete=django.db.models.deletion.CASCADE, related_name="opciones", to="siges.formulariovariable")),
            ],
            options={
                "verbose_name": "Opcion",
                "verbose_name_plural": "Opciones",
                "db_table": "formulario_opcion",
                "ordering": ["variable__orden", "orden"],
            },
        ),
        migrations.CreateModel(
            name="FormularioValidacion",
            fields=[
                ("id_validacion", models.BigAutoField(primary_key=True, serialize=False)),
                ("regla", models.CharField(max_length=80)),
                ("detalle", models.TextField()),
                ("parametros_json", models.JSONField(blank=True, null=True)),
                ("activo", models.BooleanField(default=True)),
                ("variable", models.ForeignKey(db_column="id_variable", on_delete=django.db.models.deletion.CASCADE, related_name="validaciones", to="siges.formulariovariable")),
            ],
            options={
                "verbose_name": "Validacion",
                "verbose_name_plural": "Validaciones",
                "db_table": "formulario_validacion",
            },
        ),
        migrations.CreateModel(
            name="RespuestaS01",
            fields=[
                ("id_respuesta_s01", models.BigAutoField(primary_key=True, serialize=False)),
                ("s01_dg01", models.CharField(max_length=20, verbose_name="Unicodigo")),
                ("s01_dg02", models.CharField(max_length=255, verbose_name="Establecimiento de Salud")),
                ("s01_dg03", models.CharField(max_length=150, verbose_name="Tipologia")),
                ("s01_dg04", models.CharField(max_length=150, verbose_name="Institucion")),
                ("s01_dg05", models.CharField(max_length=150, verbose_name="Direccion Provincial")),
                ("s01_dg06", models.CharField(max_length=150, verbose_name="Canton")),
                ("s01_dg07", models.CharField(max_length=150, verbose_name="Parroquia")),
                ("s01_dg08", models.CharField(max_length=255, verbose_name="Direccion del Establecimiento")),
                ("s01_dg09", models.CharField(max_length=150, verbose_name="Permiso de funcionamiento")),
                ("s01_dg10", models.CharField(max_length=150, verbose_name="Estado del predio")),
                ("s01_dg11", models.CharField(max_length=255, verbose_name="Nombres completos del Responsable")),
                ("s01_dg12", models.CharField(max_length=30, verbose_name="Movil del Responsable")),
                ("s01_dg13", models.CharField(max_length=20, verbose_name="Cedula de identidad del Responsable")),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("formulario", models.OneToOneField(db_column="id_formulario", on_delete=django.db.models.deletion.CASCADE, related_name="respuesta_s01", to="siges.sigesformulario")),
            ],
            options={
                "verbose_name": "Respuesta S01",
                "verbose_name_plural": "Respuestas S01",
                "db_table": "respuesta_s01",
            },
        ),
        migrations.CreateModel(
            name="RespuestaS02",
            fields=[
                ("id_respuesta_s02", models.BigAutoField(primary_key=True, serialize=False)),
                ("s02_am01", models.CharField(choices=[("Si", "Si"), ("No", "No")], max_length=150, verbose_name="Frontera")),
                ("s02_am04", models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Tiempo hasta el Establecimiento de Salud")),
                ("s02_am04_unidad", models.CharField(choices=[("Horas", "Horas"), ("Minutos", "Minutos")], default="Horas", max_length=10, verbose_name="Unidad del tiempo de traslado")),
                ("s02_am05", models.CharField(choices=[("Urbano", "Urbano"), ("Rural", "Rural")], max_length=150, verbose_name="Categoria de accesibilidad")),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("formulario", models.OneToOneField(db_column="id_formulario", on_delete=django.db.models.deletion.CASCADE, related_name="respuesta_s02", to="siges.sigesformulario")),
                ("s02_am02", models.ForeignKey(db_column="s02_am02", on_delete=django.db.models.deletion.PROTECT, related_name="+", to="siges.formularioopcion", verbose_name="Medio de movilizacion")),
                ("s02_am03", models.ForeignKey(db_column="s02_am03", on_delete=django.db.models.deletion.PROTECT, related_name="+", to="siges.formularioopcion", verbose_name="Frecuencia del transporte publico")),
                ("s02_am06", models.ForeignKey(db_column="s02_am06", on_delete=django.db.models.deletion.PROTECT, related_name="+", to="siges.formularioopcion", verbose_name="Tipo de via")),
            ],
            options={
                "verbose_name": "Respuesta S02",
                "verbose_name_plural": "Respuestas S02",
                "db_table": "respuesta_s02",
            },
        ),
        migrations.AddConstraint(
            model_name="formulariovariable",
            constraint=models.UniqueConstraint(fields=("seccion", "codigo"), name="uq_variable_seccion_codigo"),
        ),
        migrations.AddConstraint(
            model_name="formulariovariable",
            constraint=models.UniqueConstraint(fields=("seccion", "orden"), name="uq_variable_seccion_orden"),
        ),
        migrations.AddConstraint(
            model_name="formularioopcion",
            constraint=models.UniqueConstraint(fields=("variable", "codigo"), name="uq_opcion_variable_codigo"),
        ),
        migrations.AddConstraint(
            model_name="formularioopcion",
            constraint=models.UniqueConstraint(fields=("variable", "orden"), name="uq_opcion_variable_orden"),
        ),
        migrations.AddConstraint(
            model_name="formulariovalidacion",
            constraint=models.UniqueConstraint(fields=("variable", "regla"), name="uq_validacion_variable_regla"),
        ),
        migrations.AddConstraint(
            model_name="sigesformulario",
            constraint=models.CheckConstraint(condition=models.Q(("estado__in", ["BORRADOR", "ENVIADO", "VALIDADO", "ANULADO"])), name="ck_siges_formulario_estado"),
        ),
        migrations.AddConstraint(
            model_name="respuestas02",
            constraint=models.CheckConstraint(condition=models.Q(("s02_am04_unidad__in", ["Horas", "Minutos"])), name="ck_respuesta_s02_am04_unidad"),
        ),
        migrations.AddConstraint(
            model_name="respuestas02",
            constraint=models.CheckConstraint(condition=(models.Q(s02_am04_unidad="Horas", s02_am04__gte=1) | models.Q(s02_am04_unidad="Minutos", s02_am04__gte=1, s02_am04__lte=59)), name="ck_respuesta_s02_am04_rango_unidad"),
        ),
            ],
        ),
    ]


