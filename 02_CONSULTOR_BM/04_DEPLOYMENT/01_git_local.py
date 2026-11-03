"""Inspección y commit local seguro de SIGEM."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SENSITIVE_PARTS = (".env", "password", "secret", "token", "credential")
EXCLUDED_PARTS = ("03_IA", "backups", "logs")


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Git devolvió un error.")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true", help="prepara y crea el commit")
    parser.add_argument("--message", help="mensaje del commit")
    parser.add_argument("--yes", action="store_true", help="confirma sin pregunta interactiva")
    args = parser.parse_args()
    try:
        root = Path(run_git(Path(__file__).resolve().parent, "rev-parse", "--show-toplevel"))
        output = run_git(root, "status", "--short", "--untracked-files=all")
        changes = output.splitlines() if output else []
        print(f"Repositorio: {root}\nRama: {run_git(root, 'branch', '--show-current')}")
        print("Cambios pendientes:\n" + ("\n".join(changes) if changes else "(ninguno)"))
        candidates = [line[3:].split(" -> ")[-1] for line in changes if len(line) >= 4]
        blocked = [path for path in candidates if any(part.lower() in path.replace('\\', '/').lower() for part in EXCLUDED_PARTS + SENSITIVE_PARTS)]
        if blocked:
            print("Archivos excluidos o potencialmente sensibles:\n" + "\n".join(blocked))
        if not args.commit:
            print("Modo inspección: no se modificó Git.")
            return 0
        selected = [path for path in candidates if path not in blocked]
        if not selected:
            print("No hay archivos autorizados para preparar.")
            return 0
        message = args.message or input("Mensaje del commit: ").strip()
        if not message:
            raise ValueError("El mensaje del commit no puede estar vacío.")
        run_git(root, "add", "--", *selected)
        if not args.yes and input("¿Crear el commit? [s/N] ").strip().lower() != "s":
            run_git(root, "reset", "--", *selected)
            print("Operación cancelada; no se creó commit.")
            return 0
        print(run_git(root, "commit", "-m", message))
        return 0
    except (RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
