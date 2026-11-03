"""Genera un inventario Quarto reproducible a partir de archivos del proyecto."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).parents[2])
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[1] / "inventario_proyecto.qmd")
    args = parser.parse_args()
    root = args.root.resolve()
    patterns = ("02_SOFT/**/*.py", "03_DEPLOYMENT/**/*.py", "04_DOCUMENTACION/**/*.qmd", "05_REPRODUCIBILIDAD/**/*")
    files = sorted({str(path.relative_to(root)).replace("\\", "/") for pattern in patterns for path in root.glob(pattern) if path.is_file()})
    today = date.today().isoformat()
    lines = ["---", "title: 'Inventario reproducible de SIGEM'", "format: html", f"date: {today}", "---", "", "# Fuente", "", f"La fecha de generación es `{today}`. El inventario se deriva de archivos existentes en `{root}` y no utiliza servicios de inteligencia artificial.", "", "# Archivos identificados", ""]
    lines.extend(f"- `{path}`" for path in files)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generado: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
