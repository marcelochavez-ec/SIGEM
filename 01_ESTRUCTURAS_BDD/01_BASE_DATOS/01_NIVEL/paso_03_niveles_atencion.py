"""Catalogo controlado de niveles de atencion para SIGEM nivel 1."""

from __future__ import annotations

import pandas as pd


NIVELES_ATENCION = [
    {
        "codigo": 1,
        "nivel_atencion": "I NIVEL DE ATENCION",
        "etiqueta": "I Nivel de atencion",
        "activo": True,
    },
    {
        "codigo": 2,
        "nivel_atencion": "II NIVEL DE ATENCION",
        "etiqueta": "II Nivel de atencion",
        "activo": True,
    },
    {
        "codigo": 3,
        "nivel_atencion": "III NIVEL DE ATENCION",
        "etiqueta": "III Nivel de atencion",
        "activo": True,
    },
]


def construir_dataframe_niveles_atencion() -> pd.DataFrame:
    """Devuelve el DataFrame maestro con los niveles permitidos por SIGEM."""
    return pd.DataFrame(NIVELES_ATENCION)
