"""Configuracion de conexion para la capa de base de datos SIGES nivel 1."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, URL


@dataclass(frozen=True)
class ConfiguracionBaseDatos:
    """Representa los parametros minimos para conectar con PostgreSQL."""

    usuario: str
    clave: str
    host: str
    puerto: int
    base: str
    esquema: str


def raiz_proyecto() -> Path:
    """Devuelve la carpeta raiz del repositorio SIGES."""
    return Path(__file__).resolve().parents[3]


def ruta_configuracion() -> Path:
    """Ubica el archivo YAML institucional de configuracion."""
    return raiz_proyecto() / "01_ESTRUCTURAS_BDD" / "03_CONFIGURACIONES" / "config.yml"


def leer_yaml_seguro(ruta: Path) -> dict[str, Any]:
    """Lee un YAML local y devuelve un diccionario sin imprimir credenciales."""
    if not ruta.exists():
        return {}
    contenido = ruta.read_text(encoding="utf-8")
    return yaml.safe_load(contenido) or {}


def obtener_configuracion() -> ConfiguracionBaseDatos:
    """Combina variables de ambiente y YAML para conectar a productos_bm.siges."""
    datos = leer_yaml_seguro(ruta_configuracion())
    bloque_default = datos.get("default", {})
    bloque_postgres = bloque_default.get("postgresql_dneaisns", {})

    usuario = os.getenv("SIGES_DB_USER") or str(bloque_postgres.get("user", ""))
    clave = os.getenv("SIGES_DB_PASSWORD") or str(bloque_postgres.get("password", ""))
    host = os.getenv("SIGES_DB_HOST") or str(bloque_postgres.get("host", "127.0.0.1"))
    puerto = int(os.getenv("SIGES_DB_PORT") or bloque_postgres.get("port", 5432))
    base = os.getenv("SIGES_DB_NAME") or str(bloque_postgres.get("database", "productos_bm"))
    esquema = (os.getenv("SIGES_DB_SCHEMA") or str(bloque_postgres.get("schema", "siges"))).lower()

    if not usuario:
        raise RuntimeError("No se encontro usuario PostgreSQL para SIGES.")
    if not clave:
        raise RuntimeError("No se encontro clave PostgreSQL para SIGES.")

    return ConfiguracionBaseDatos(
        usuario=usuario,
        clave=clave,
        host=host,
        puerto=puerto,
        base=base,
        esquema=esquema,
    )


def crear_engine(configuracion: ConfiguracionBaseDatos) -> Engine:
    """Crea el motor SQLAlchemy usando psycopg y validacion de conexion."""
    url = URL.create(
        drivername="postgresql+psycopg",
        username=configuracion.usuario,
        password=configuracion.clave,
        host=configuracion.host,
        port=configuracion.puerto,
        database=configuracion.base,
    )
    return create_engine(url, pool_pre_ping=True, future=True)

