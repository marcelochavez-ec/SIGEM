"""Compatibilidad para ejecutar la construccion CGS nivel 1 desde la ruta antigua."""

from __future__ import annotations

import sys
from pathlib import Path


RAIZ_REPOSITORIO = Path(__file__).resolve().parents[3]
RUTA_MODULO_NIVEL_1 = RAIZ_REPOSITORIO / "01_ESTRUCTURAS_BDD" / "01_BASE_DATOS" / "01_NIVEL"

if str(RUTA_MODULO_NIVEL_1) not in sys.path:
    sys.path.insert(0, str(RUTA_MODULO_NIVEL_1))

from main_cgs_nivel_1 import main


if __name__ == "__main__":
    main()

