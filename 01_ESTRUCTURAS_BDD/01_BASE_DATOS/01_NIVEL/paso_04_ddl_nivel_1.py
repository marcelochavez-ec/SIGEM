"""DDL PostgreSQL para crear la estructura SIGES del nivel 1.

El DDL se mantiene idempotente: puede ejecutarse mas de una vez sin borrar
datos existentes. Las reglas nuevas se expresan como restricciones para que
la base de datos proteja la calidad minima de las respuestas futuras.
"""

from __future__ import annotations


def ddl_nivel_1(esquema: str) -> str:
    """Construye el SQL idempotente para schema, tablas, indices, funciones y vistas."""
    return f"""
CREATE SCHEMA IF NOT EXISTS {esquema};

CREATE TABLE IF NOT EXISTS {esquema}.formulario_seccion (
    id_seccion BIGSERIAL PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    orden SMALLINT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_formulario_seccion_codigo UNIQUE (codigo),
    CONSTRAINT uq_formulario_seccion_orden UNIQUE (orden),
    CONSTRAINT ck_formulario_seccion_orden CHECK (orden > 0)
);

CREATE TABLE IF NOT EXISTS {esquema}.formulario_variable (
    id_variable BIGSERIAL PRIMARY KEY,
    id_seccion BIGINT NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    etiqueta VARCHAR(255) NOT NULL,
    tipo_control VARCHAR(20) NOT NULL,
    tipo_dato VARCHAR(20) NOT NULL,
    unidad_medida VARCHAR(30),
    obligatorio BOOLEAN NOT NULL DEFAULT TRUE,
    orden SMALLINT NOT NULL,
    validacion_json JSONB,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_formulario_variable_seccion
        FOREIGN KEY (id_seccion)
        REFERENCES {esquema}.formulario_seccion (id_seccion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT uq_formulario_variable_codigo UNIQUE (codigo),
    CONSTRAINT uq_formulario_variable_seccion_codigo UNIQUE (id_seccion, codigo),
    CONSTRAINT uq_formulario_variable_seccion_orden UNIQUE (id_seccion, orden),
    CONSTRAINT ck_formulario_variable_tipo_control
        CHECK (tipo_control IN ('select', 'number', 'text', 'textarea', 'date', 'radio', 'checkbox')),
    CONSTRAINT ck_formulario_variable_tipo_dato
        CHECK (tipo_dato IN ('catalogo', 'decimal', 'entero', 'texto', 'fecha', 'booleano')),
    CONSTRAINT ck_formulario_variable_orden CHECK (orden > 0)
);

CREATE TABLE IF NOT EXISTS {esquema}.formulario_opcion (
    id_opcion BIGSERIAL PRIMARY KEY,
    id_variable BIGINT NOT NULL,
    codigo SMALLINT NOT NULL,
    descripcion VARCHAR(150) NOT NULL,
    nivel_accesibilidad VARCHAR(30) NOT NULL DEFAULT '',
    orden SMALLINT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_formulario_opcion_variable
        FOREIGN KEY (id_variable)
        REFERENCES {esquema}.formulario_variable (id_variable)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT uq_formulario_opcion_variable_codigo UNIQUE (id_variable, codigo),
    CONSTRAINT uq_formulario_opcion_variable_orden UNIQUE (id_variable, orden),
    CONSTRAINT ck_formulario_opcion_codigo CHECK (codigo > 0),
    CONSTRAINT ck_formulario_opcion_orden CHECK (orden > 0)
);

CREATE TABLE IF NOT EXISTS {esquema}.formulario_validacion (
    id_validacion BIGSERIAL PRIMARY KEY,
    id_variable BIGINT NOT NULL,
    regla VARCHAR(80) NOT NULL,
    detalle TEXT NOT NULL,
    parametros_json JSONB,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_formulario_validacion_variable
        FOREIGN KEY (id_variable)
        REFERENCES {esquema}.formulario_variable (id_variable)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT uq_formulario_validacion_variable_regla UNIQUE (id_variable, regla)
);

CREATE TABLE IF NOT EXISTS {esquema}.siges_formulario (
    id_formulario SERIAL PRIMARY KEY,
    id_usuario BIGINT,
    fecha_registro TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    version INTEGER NOT NULL DEFAULT 1,
    estado VARCHAR(20) NOT NULL DEFAULT 'BORRADOR',
    unicodigo VARCHAR(20) NOT NULL,
    nivel_atencion VARCHAR(80) NOT NULL DEFAULT 'I NIVEL DE ATENCION',
    CONSTRAINT ck_siges_formulario_id_formulario CHECK (id_formulario > 0),
    CONSTRAINT ck_siges_formulario_version CHECK (version >= 1),
    CONSTRAINT ck_siges_formulario_estado CHECK (estado IN ('BORRADOR', 'ENVIADO', 'VALIDADO', 'ANULADO'))
);

CREATE TABLE IF NOT EXISTS {esquema}.respuesta_s01 (
    id_respuesta_s01 BIGSERIAL PRIMARY KEY,
    id_formulario INTEGER NOT NULL,
    s01_dg01 VARCHAR(20) NOT NULL,
    s01_dg02 VARCHAR(255) NOT NULL,
    s01_dg03 VARCHAR(150) NOT NULL,
    s01_dg04 VARCHAR(150) NOT NULL,
    s01_dg05 VARCHAR(150) NOT NULL,
    s01_dg06 VARCHAR(150) NOT NULL,
    s01_dg07 VARCHAR(150) NOT NULL,
    s01_dg08 VARCHAR(255) NOT NULL,
    s01_dg09 VARCHAR(150) NOT NULL,
    s01_dg10 VARCHAR(150) NOT NULL,
    s01_dg11 VARCHAR(255) NOT NULL,
    s01_dg12 VARCHAR(30) NOT NULL,
    s01_dg13 VARCHAR(20) NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_respuesta_s01_formulario
        FOREIGN KEY (id_formulario)
        REFERENCES {esquema}.siges_formulario (id_formulario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT uq_respuesta_s01_formulario UNIQUE (id_formulario)
);

CREATE TABLE IF NOT EXISTS {esquema}.respuesta_s02 (
    id_respuesta_s02 BIGSERIAL PRIMARY KEY,
    id_formulario INTEGER NOT NULL,
    s02_am01 VARCHAR(150) NOT NULL,
    s02_am02 BIGINT NOT NULL,
    s02_am03 BIGINT NOT NULL,
    s02_am04 NUMERIC(6,2) NOT NULL,
    s02_am04_unidad VARCHAR(10) NOT NULL DEFAULT 'Horas',
    s02_am05 VARCHAR(150) NOT NULL,
    s02_am06 BIGINT NOT NULL,
    creado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_respuesta_s02_formulario
        FOREIGN KEY (id_formulario)
        REFERENCES {esquema}.siges_formulario (id_formulario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT uq_respuesta_s02_formulario UNIQUE (id_formulario),
    CONSTRAINT fk_respuesta_s02_am02
        FOREIGN KEY (s02_am02)
        REFERENCES {esquema}.formulario_opcion (id_opcion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_respuesta_s02_am03
        FOREIGN KEY (s02_am03)
        REFERENCES {esquema}.formulario_opcion (id_opcion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_respuesta_s02_am06
        FOREIGN KEY (s02_am06)
        REFERENCES {esquema}.formulario_opcion (id_opcion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT ck_respuesta_s02_am01_frontera CHECK (UPPER(TRIM(s02_am01)) IN ('SI', 'SÍ', 'NO')),
    CONSTRAINT ck_respuesta_s02_am04_unidad CHECK (UPPER(TRIM(s02_am04_unidad)) IN ('HORAS', 'MINUTOS')),
    CONSTRAINT ck_respuesta_s02_am04_no_negativo CHECK (s02_am04 >= 0),
    CONSTRAINT ck_respuesta_s02_am04_minutos CHECK (
        UPPER(TRIM(s02_am04_unidad)) <> 'MINUTOS'
        OR s02_am04 <= 59
    ),
    CONSTRAINT ck_respuesta_s02_am05_categoria CHECK (UPPER(TRIM(s02_am05)) IN ('URBANO', 'RURAL'))
);

ALTER TABLE {esquema}.respuesta_s02
    ADD COLUMN IF NOT EXISTS s02_am04_unidad VARCHAR(10) NOT NULL DEFAULT 'Horas';

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_respuesta_s02_am01_frontera') THEN
        ALTER TABLE {esquema}.respuesta_s02
        ADD CONSTRAINT ck_respuesta_s02_am01_frontera
        CHECK (UPPER(TRIM(s02_am01)) IN ('SI', 'SÍ', 'NO')) NOT VALID;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_respuesta_s02_am04_unidad') THEN
        ALTER TABLE {esquema}.respuesta_s02
        ADD CONSTRAINT ck_respuesta_s02_am04_unidad
        CHECK (UPPER(TRIM(s02_am04_unidad)) IN ('HORAS', 'MINUTOS')) NOT VALID;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_respuesta_s02_am04_minutos') THEN
        ALTER TABLE {esquema}.respuesta_s02
        ADD CONSTRAINT ck_respuesta_s02_am04_minutos
        CHECK (
            UPPER(TRIM(s02_am04_unidad)) <> 'MINUTOS'
            OR s02_am04 <= 59
        ) NOT VALID;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'ck_respuesta_s02_am05_categoria') THEN
        ALTER TABLE {esquema}.respuesta_s02
        ADD CONSTRAINT ck_respuesta_s02_am05_categoria
        CHECK (UPPER(TRIM(s02_am05)) IN ('URBANO', 'RURAL')) NOT VALID;
    END IF;
END
$$;

CREATE INDEX IF NOT EXISTS ix_formulario_variable_id_seccion
    ON {esquema}.formulario_variable (id_seccion);

CREATE INDEX IF NOT EXISTS ix_formulario_opcion_id_variable
    ON {esquema}.formulario_opcion (id_variable);

CREATE INDEX IF NOT EXISTS ix_siges_formulario_unicodigo
    ON {esquema}.siges_formulario (unicodigo);

CREATE INDEX IF NOT EXISTS ix_siges_formulario_nivel_atencion
    ON {esquema}.siges_formulario (nivel_atencion);

CREATE INDEX IF NOT EXISTS ix_siges_formulario_estado
    ON {esquema}.siges_formulario (estado);

CREATE INDEX IF NOT EXISTS ix_respuesta_s01_id_formulario
    ON {esquema}.respuesta_s01 (id_formulario);

CREATE INDEX IF NOT EXISTS ix_respuesta_s02_id_formulario
    ON {esquema}.respuesta_s02 (id_formulario);

CREATE OR REPLACE FUNCTION {esquema}.fn_actualizar_fecha_actualizacion()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_siges_formulario_actualizacion ON {esquema}.siges_formulario;

CREATE TRIGGER trg_siges_formulario_actualizacion
BEFORE UPDATE ON {esquema}.siges_formulario
FOR EACH ROW
EXECUTE FUNCTION {esquema}.fn_actualizar_fecha_actualizacion();

CREATE OR REPLACE FUNCTION {esquema}.fn_actualizar_actualizado_en()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.actualizado_en = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_respuesta_s01_actualizado_en ON {esquema}.respuesta_s01;

CREATE TRIGGER trg_respuesta_s01_actualizado_en
BEFORE UPDATE ON {esquema}.respuesta_s01
FOR EACH ROW
EXECUTE FUNCTION {esquema}.fn_actualizar_actualizado_en();

DROP TRIGGER IF EXISTS trg_respuesta_s02_actualizado_en ON {esquema}.respuesta_s02;

CREATE TRIGGER trg_respuesta_s02_actualizado_en
BEFORE UPDATE ON {esquema}.respuesta_s02
FOR EACH ROW
EXECUTE FUNCTION {esquema}.fn_actualizar_actualizado_en();

CREATE OR REPLACE FUNCTION {esquema}.fn_validar_respuesta_s02_opciones()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM {esquema}.formulario_opcion o
        JOIN {esquema}.formulario_variable v ON v.id_variable = o.id_variable
        WHERE o.id_opcion = NEW.s02_am02 AND v.codigo = 's02_am02' AND o.activo = TRUE AND v.activo = TRUE
    ) THEN
        RAISE EXCEPTION 's02_am02 contiene una opcion que no pertenece a Medio de movilizacion';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM {esquema}.formulario_opcion o
        JOIN {esquema}.formulario_variable v ON v.id_variable = o.id_variable
        WHERE o.id_opcion = NEW.s02_am03 AND v.codigo = 's02_am03' AND o.activo = TRUE AND v.activo = TRUE
    ) THEN
        RAISE EXCEPTION 's02_am03 contiene una opcion que no pertenece a Frecuencia del transporte publico';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM {esquema}.formulario_opcion o
        JOIN {esquema}.formulario_variable v ON v.id_variable = o.id_variable
        WHERE o.id_opcion = NEW.s02_am06 AND v.codigo = 's02_am06' AND o.activo = TRUE AND v.activo = TRUE
    ) THEN
        RAISE EXCEPTION 's02_am06 contiene una opcion que no pertenece a Tipo de via';
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_validar_respuesta_s02_opciones ON {esquema}.respuesta_s02;

CREATE TRIGGER trg_validar_respuesta_s02_opciones
BEFORE INSERT OR UPDATE ON {esquema}.respuesta_s02
FOR EACH ROW
EXECUTE FUNCTION {esquema}.fn_validar_respuesta_s02_opciones();

CREATE OR REPLACE VIEW {esquema}.vw_catalogo_formulario_nivel_1 AS
SELECT
    s.id_seccion,
    s.codigo AS seccion_codigo,
    s.nombre AS seccion_nombre,
    s.descripcion AS seccion_descripcion,
    s.orden AS seccion_orden,
    v.id_variable,
    v.codigo AS variable_codigo,
    v.etiqueta AS variable_etiqueta,
    v.tipo_control,
    v.tipo_dato,
    v.unidad_medida,
    v.obligatorio,
    v.orden AS variable_orden,
    v.validacion_json,
    o.id_opcion,
    o.codigo AS opcion_codigo,
    o.descripcion AS opcion_descripcion,
    o.nivel_accesibilidad,
    o.orden AS opcion_orden
FROM {esquema}.formulario_seccion s
JOIN {esquema}.formulario_variable v
  ON v.id_seccion = s.id_seccion
LEFT JOIN {esquema}.formulario_opcion o
  ON o.id_variable = v.id_variable
 AND o.activo = TRUE
WHERE s.codigo IN ('s01', 's02')
  AND s.activo = TRUE
  AND v.activo = TRUE
ORDER BY s.orden, v.orden, o.orden NULLS FIRST;
"""
