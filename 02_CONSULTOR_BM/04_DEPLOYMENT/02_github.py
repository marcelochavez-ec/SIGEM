"""Verifica conectividad y publicación GitHub sin publicar por defecto."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Git devolvió un error.")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--push", action="store_true", help="publica después de confirmar")
    parser.add_argument("--yes", action="store_true", help="confirma sin pregunta interactiva")
    args = parser.parse_args()
    try:
        root = Path(git(Path(__file__).resolve().parent, "rev-parse", "--show-toplevel"))
        branch = git(root, "branch", "--show-current")
        remote = git(root, "remote", "get-url", "origin")
        print(f"Repositorio: {root}\nRama: {branch}\nRemoto: {remote}")
        remote_heads = git(root, "ls-remote", "--heads", "origin")
        if not remote_heads:
            raise RuntimeError("GitHub no devolvió ramas para el remoto origin.")
        print("Conectividad GitHub: OK")
        if not args.push:
            print("Modo diagnóstico: no se ejecutó fetch ni push; no se modificó el remoto.")
            return 0
        git(root, "fetch", "origin", branch)
        print("Divergencia remoto/local:", git(root, "rev-list", "--left-right", "--count", f"origin/{branch}...HEAD"))
        if not args.yes and input("¿Publicar con git push? [s/N] ").strip().lower() != "s":
            print("Publicación cancelada.")
            return 0
        print(git(root, "push", "origin", branch))
        return 0
    except RuntimeError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
