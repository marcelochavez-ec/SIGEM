"""Ejecucion del ETL unico para estructuras SIGES nivel 1.

El archivo orquesta la creacion de tablas, catalogos y validaciones del
primer nivel. Cada funcion se mantiene pequena para que el flujo pueda ser
leido, probado y ajustado por partes.
"""

from __future__ import annotations

import json

from sqlalchemy import text

try:
    from .paso_01_configuracion import crear_engine, obtener_configuracion
    from .paso_02_catalogos_nivel_1 import SECCIONES, VALIDACIONES, VARIABLES
    from .paso_04_ddl_nivel_1 import ddl_nivel_1
except ImportError:
    from paso_01_configuracion import crear_engine, obtener_configuracion
    from paso_02_catalogos_nivel_1 import SECCIONES, VALIDACIONES, VARIABLES
    from paso_04_ddl_nivel_1 import ddl_nivel_1


TABLAS_ESPERADAS = {
    "formulario_seccion",
    "formulario_variable",
    "formulario_opcion",
    "formulario_validacion",
    "siges_formulario",
    "respuesta_s01",
    "respuesta_s02",
}


COLUMNAS_ESPERADAS = {
    "formulario_seccion": {"id_seccion", "codigo", "nombre", "descripcion", "orden", "activo"},
    "formulario_variable": {
        "id_variable",
        "id_seccion",
        "codigo",
        "etiqueta",
        "tipo_control",
        "tipo_dato",
        "unidad_medida",
        "obligatorio",
        "orden",
        "validacion_json",
        "activo",
    },
    "formulario_opcion": {
        "id_opcion",
        "id_variable",
        "codigo",
        "descripcion",
        "nivel_accesibilidad",
        "orden",
        "activo",
    },
    "formulario_validacion": {
        "id_validacion",
        "id_variable",
        "regla",
        "detalle",
        "parametros_json",
        "activo",
    },
    "siges_formulario": {
        "id_formulario",
        "id_usuario",
        "fecha_registro",
        "fecha_actualizacion",
        "version",
        "estado",
        "unicodigo",
        "nivel_atencion",
    },
    "respuesta_s01": {
        "id_respuesta_s01",
        "id_formulario",
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
        "creado_en",
        "actualizado_en",
    },
    "respuesta_s02": {
        "id_respuesta_s02",
        "id_formulario",
        "s02_am01",
        "s02_am02",
        "s02_am03",
        "s02_am04",
        "s02_am04_unidad",
        "s02_am05",
        "s02_am06",
        "creado_en",
        "actualizado_en",
    },
}


TIPOS_ESPERADOS = {
    ("siges_formulario", "id_formulario"): "integer",
    ("respuesta_s01", "id_formulario"): "integer",
    ("respuesta_s02", "id_formulario"): "integer",
}

VISTAS_ESPERADAS = {"vw_catalogo_formulario_nivel_1"}

FUNCIONES_ESPERADAS = {
    "fn_actualizar_fecha_actualizacion",
    "fn_actualizar_actualizado_en",
    "fn_validar_respuesta_s02_opciones",
}

TRIGGERS_ESPERADOS = {
    "trg_siges_formulario_actualizacion",
    "trg_respuesta_s01_actualizado_en",
    "trg_respuesta_s02_actualizado_en",
    "trg_validar_respuesta_s02_opciones",
}

INDICES_ESPERADOS = {
    "ix_formulario_variable_id_seccion",
    "ix_formulario_opcion_id_variable",
    "ix_siges_formulario_unicodigo",
    "ix_siges_formulario_nivel_atencion",
    "ix_siges_formulario_estado",
    "ix_respuesta_s01_id_formulario",
    "ix_respuesta_s02_id_formulario",
}


def preparar_cabecera_formulario_limpia(conn, esquema: str) -> None:
    """Recrea tablas vacias si la cabecera conserva columnas o tipos heredados."""
    tipo_actual = conn.execute(
        text(
            """
            SELECT data_type
            FROM information_schema.columns
            WHERE table_schema = :esquema
              AND table_name = 'siges_formulario'
              AND column_name = 'id_formulario';
            """
        ),
        {"esquema": esquema},
    ).scalar()
    columnas_actuales = {
        fila[0]
        for fila in conn.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = :esquema
                  AND table_name = 'siges_formulario';
                """
            ),
            {"esquema": esquema},
        )
    }
    columnas_heredadas = {"observaciones", "establecimiento_id"} & columnas_actuales

    if tipo_actual in (None, "integer") and not columnas_heredadas:
        return

    conteos = conn.execute(
        text(
            f"""
            SELECT
                (SELECT COUNT(*) FROM {esquema}.siges_formulario) AS formularios,
                (SELECT COUNT(*) FROM {esquema}.respuesta_s01) AS respuesta_s01,
                (SELECT COUNT(*) FROM {esquema}.respuesta_s02) AS respuesta_s02;
            """
        )
    ).mappings().one()

    if any(valor > 0 for valor in conteos.values()):
        raise RuntimeError(
            "siges_formulario conserva una estructura heredada y existen registros. "
            "Se requiere una migracion controlada antes de ajustar columnas o tipos."
        )

    conn.execute(
        text(
            f"""
            DROP TABLE IF EXISTS {esquema}.respuesta_s02;
            DROP TABLE IF EXISTS {esquema}.respuesta_s01;
            DROP TABLE IF EXISTS {esquema}.siges_formulario;
            """
        )
    )


def ejecutar_ddl(conn, esquema: str) -> None:
    """Ejecuta la definicion estructural del nivel 1."""
    conn.execute(text(ddl_nivel_1(esquema)))


def cargar_secciones(conn, esquema: str) -> dict[str, int]:
    """Inserta o actualiza las secciones funcionales S01 y S02."""
    sql = text(
        f"""
        INSERT INTO {esquema}.formulario_seccion (codigo, nombre, descripcion, orden, activo)
        VALUES (:codigo, :nombre, :descripcion, :orden, TRUE)
        ON CONFLICT (codigo)
        DO UPDATE SET
            nombre = EXCLUDED.nombre,
            descripcion = EXCLUDED.descripcion,
            orden = EXCLUDED.orden,
            activo = TRUE
        RETURNING id_seccion;
        """
    )
    ids: dict[str, int] = {}
    for seccion in SECCIONES:
        ids[seccion["codigo"]] = conn.execute(sql, seccion).scalar_one()
    return ids


def cargar_variables(conn, esquema: str, ids_seccion: dict[str, int]) -> dict[str, int]:
    """Inserta o actualiza variables y conserva sus identificadores."""
    # Se libera temporalmente el orden de variables existentes para poder insertar nuevas
    # variables intermedias sin chocar contra la restriccion unica de seccion y orden.
    codigos_por_seccion: dict[str, list[str]] = {}
    # Se agrupan codigos por seccion para actualizar solamente las variables del nivel 1.
    for variable in VARIABLES:
        codigos_por_seccion.setdefault(variable["seccion_codigo"], []).append(variable["codigo"])
    # Cada grupo sube su orden a una franja temporal dentro de la misma transaccion.
    for codigo_seccion, codigos_variable in codigos_por_seccion.items():
        conn.execute(
            text(
                f"""
                UPDATE {esquema}.formulario_variable
                SET orden = orden + 1000
                WHERE id_seccion = :id_seccion
                  AND codigo = ANY(:codigos_variable);
                """
            ),
            {
                "id_seccion": ids_seccion[codigo_seccion],
                "codigos_variable": codigos_variable,
            },
        )

    sql = text(
        f"""
        INSERT INTO {esquema}.formulario_variable (
            id_seccion,
            codigo,
            etiqueta,
            tipo_control,
            tipo_dato,
            unidad_medida,
            obligatorio,
            orden,
            validacion_json,
            activo
        )
        VALUES (
            :id_seccion,
            :codigo,
            :etiqueta,
            :tipo_control,
            :tipo_dato,
            :unidad_medida,
            :obligatorio,
            :orden,
            CAST(:validacion_json AS JSONB),
            TRUE
        )
        ON CONFLICT (codigo)
        DO UPDATE SET
            id_seccion = EXCLUDED.id_seccion,
            etiqueta = EXCLUDED.etiqueta,
            tipo_control = EXCLUDED.tipo_control,
            tipo_dato = EXCLUDED.tipo_dato,
            unidad_medida = EXCLUDED.unidad_medida,
            obligatorio = EXCLUDED.obligatorio,
            orden = EXCLUDED.orden,
            validacion_json = EXCLUDED.validacion_json,
            activo = TRUE
        RETURNING id_variable;
        """
    )
    ids: dict[str, int] = {}
    for variable in VARIABLES:
        parametros = dict(variable)
        parametros["id_seccion"] = ids_seccion[variable["seccion_codigo"]]
        parametros["validacion_json"] = json.dumps(variable["validacion_json"], ensure_ascii=True)
        parametros.pop("seccion_codigo")
        parametros.pop("opciones")
        ids[variable["codigo"]] = conn.execute(sql, parametros).scalar_one()
    return ids


def cargar_opciones(conn, esquema: str, ids_variable: dict[str, int]) -> int:
    """Inserta o actualiza opciones solo en variables de catalogo."""
    sql = text(
        f"""
        INSERT INTO {esquema}.formulario_opcion (
            id_variable,
            codigo,
            descripcion,
            nivel_accesibilidad,
            orden,
            activo
        )
        VALUES (
            :id_variable,
            :codigo,
            :descripcion,
            :nivel_accesibilidad,
            :orden,
            TRUE
        )
        ON CONFLICT (id_variable, codigo)
        DO UPDATE SET
            descripcion = EXCLUDED.descripcion,
            nivel_accesibilidad = EXCLUDED.nivel_accesibilidad,
            orden = EXCLUDED.orden,
            activo = TRUE
        RETURNING id_opcion;
        """
    )
    total = 0
    for variable in VARIABLES:
        for codigo, descripcion, nivel in variable["opciones"]:
            conn.execute(
                sql,
                {
                    "id_variable": ids_variable[variable["codigo"]],
                    "codigo": codigo,
                    "descripcion": descripcion,
                    "nivel_accesibilidad": nivel,
                    "orden": codigo,
                },
            )
            total += 1
    return total


def cargar_validaciones(conn, esquema: str, ids_variable: dict[str, int]) -> int:
    """Registra validaciones documentales asociadas a variables clave."""
    sql = text(
        f"""
        INSERT INTO {esquema}.formulario_validacion (
            id_variable,
            regla,
            detalle,
            parametros_json,
            activo
        )
        VALUES (
            :id_variable,
            :regla,
            :detalle,
            CAST(:parametros_json AS JSONB),
            TRUE
        )
        ON CONFLICT (id_variable, regla)
        DO UPDATE SET
            detalle = EXCLUDED.detalle,
            parametros_json = EXCLUDED.parametros_json,
            activo = TRUE;
        """
    )
    total = 0
    for codigo_variable, regla, detalle in VALIDACIONES:
        conn.execute(
            sql,
            {
                "id_variable": ids_variable[codigo_variable],
                "regla": regla,
                "detalle": detalle,
                "parametros_json": json.dumps({}, ensure_ascii=True),
            },
        )
        total += 1
    return total


def verificar_estructura(conn, esquema: str) -> dict[str, object]:
    """Compara lo creado en PostgreSQL contra la definicion esperada."""
    tablas = {
        fila[0]
        for fila in conn.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = :esquema
                  AND table_type = 'BASE TABLE';
                """
            ),
            {"esquema": esquema},
        )
    }
    columnas = conn.execute(
        text(
            """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = :esquema
              AND table_name = ANY(:tablas)
            ORDER BY table_name, ordinal_position;
            """
        ),
        {"esquema": esquema, "tablas": sorted(TABLAS_ESPERADAS)},
    ).fetchall()

    columnas_por_tabla: dict[str, set[str]] = {tabla: set() for tabla in TABLAS_ESPERADAS}
    tipos_por_columna: dict[tuple[str, str], str] = {}
    for tabla, columna, tipo in columnas:
        columnas_por_tabla.setdefault(tabla, set()).add(columna)
        tipos_por_columna[(tabla, columna)] = tipo

    faltantes = {
        tabla: sorted(esperadas - columnas_por_tabla.get(tabla, set()))
        for tabla, esperadas in COLUMNAS_ESPERADAS.items()
        if esperadas - columnas_por_tabla.get(tabla, set())
    }
    sobrantes = {
        tabla: sorted(columnas_por_tabla.get(tabla, set()) - esperadas)
        for tabla, esperadas in COLUMNAS_ESPERADAS.items()
        if columnas_por_tabla.get(tabla, set()) - esperadas
    }
    conteos = conn.execute(
        text(
            f"""
            SELECT
                (SELECT COUNT(*) FROM {esquema}.formulario_seccion) AS secciones,
                (SELECT COUNT(*) FROM {esquema}.formulario_variable) AS variables,
                (SELECT COUNT(*) FROM {esquema}.formulario_opcion) AS opciones,
                (SELECT COUNT(*) FROM {esquema}.formulario_validacion) AS validaciones;
            """
        )
    ).mappings().one()
    vistas = {
        fila[0]
        for fila in conn.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.views
                WHERE table_schema = :esquema;
                """
            ),
            {"esquema": esquema},
        )
    }
    funciones = {
        fila[0]
        for fila in conn.execute(
            text(
                """
                SELECT routine_name
                FROM information_schema.routines
                WHERE routine_schema = :esquema;
                """
            ),
            {"esquema": esquema},
        )
    }
    triggers = {
        fila[0]
        for fila in conn.execute(
            text(
                """
                SELECT trigger_name
                FROM information_schema.triggers
                WHERE trigger_schema = :esquema;
                """
            ),
            {"esquema": esquema},
        )
    }
    indices = {
        fila[0]
        for fila in conn.execute(
            text(
                """
                SELECT indexname
                FROM pg_indexes
                WHERE schemaname = :esquema;
                """
            ),
            {"esquema": esquema},
        )
    }
    tipos_incorrectos = {
        f"{tabla}.{columna}": {"esperado": esperado, "actual": tipos_por_columna.get((tabla, columna))}
        for (tabla, columna), esperado in TIPOS_ESPERADOS.items()
        if tipos_por_columna.get((tabla, columna)) != esperado
    }

    return {
        "tablas_faltantes": sorted(TABLAS_ESPERADAS - tablas),
        "columnas_faltantes": faltantes,
        "columnas_sobrantes": sobrantes,
        "tipos_incorrectos": tipos_incorrectos,
        "vistas_faltantes": sorted(VISTAS_ESPERADAS - vistas),
        "funciones_faltantes": sorted(FUNCIONES_ESPERADAS - funciones),
        "triggers_faltantes": sorted(TRIGGERS_ESPERADOS - triggers),
        "indices_faltantes": sorted(INDICES_ESPERADOS - indices),
        "conteos": dict(conteos),
    }


def crear_estructura_nivel_1() -> dict[str, object]:
    """Orquesta todo el proceso de creacion y verificacion del nivel 1."""
    configuracion = obtener_configuracion()
    engine = crear_engine(configuracion)

    print("=" * 72)
    print("SIGES - ESTRUCTURAS BASE DE DATOS NIVEL 1")
    print("=" * 72)
    print(f"Host   : {configuracion.host}")
    print(f"Base   : {configuracion.base}")
    print(f"Schema : {configuracion.esquema}")
    print()

    with engine.begin() as conn:
        preparar_cabecera_formulario_limpia(conn, configuracion.esquema)
        ejecutar_ddl(conn, configuracion.esquema)
        ids_seccion = cargar_secciones(conn, configuracion.esquema)
        ids_variable = cargar_variables(conn, configuracion.esquema, ids_seccion)
        total_opciones = cargar_opciones(conn, configuracion.esquema, ids_variable)
        total_validaciones = cargar_validaciones(conn, configuracion.esquema, ids_variable)
        verificacion = verificar_estructura(conn, configuracion.esquema)

    print("Proceso ejecutado correctamente.")
    print(f"Secciones cargadas   : {len(ids_seccion)}")
    print(f"Variables cargadas   : {len(ids_variable)}")
    print(f"Opciones cargadas    : {total_opciones}")
    print(f"Validaciones cargadas: {total_validaciones}")
    print(f"Vista disponible     : {configuracion.esquema}.vw_catalogo_formulario_nivel_1")
    print()
    print("Verificacion:")
    print(f"  Tablas faltantes    : {verificacion['tablas_faltantes']}")
    print(f"  Columnas faltantes  : {verificacion['columnas_faltantes']}")
    print(f"  Columnas adicionales: {verificacion['columnas_sobrantes']}")
    print(f"  Tipos incorrectos   : {verificacion['tipos_incorrectos']}")
    print(f"  Vistas faltantes    : {verificacion['vistas_faltantes']}")
    print(f"  Funciones faltantes : {verificacion['funciones_faltantes']}")
    print(f"  Triggers faltantes  : {verificacion['triggers_faltantes']}")
    print(f"  Indices faltantes   : {verificacion['indices_faltantes']}")
    print(f"  Conteos             : {verificacion['conteos']}")
    print("=" * 72)

    return verificacion
