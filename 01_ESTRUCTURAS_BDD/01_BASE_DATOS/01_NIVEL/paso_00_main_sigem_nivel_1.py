"""Punto de entrada principal para crear estructuras SIGEM nivel 1.

Este script solo delega la ejecucion al orquestador del nivel 1. Se conserva
separado para que el usuario tenga un punto claro de arranque.
"""

from __future__ import annotations

try:
    from .paso_05_ejecutar_nivel_1 import crear_estructura_nivel_1
except ImportError:
    from paso_05_ejecutar_nivel_1 import crear_estructura_nivel_1


def main() -> None:
    """Ejecuta el proceso unico de construccion de estructuras nivel 1."""
    crear_estructura_nivel_1()


if __name__ == "__main__":
    main()
