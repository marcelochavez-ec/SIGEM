"""Prepara un plan de despliegue QA 194; no conecta ni modifica por defecto."""
from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="commit o etiqueta ya publicada; por defecto HEAD")
    parser.add_argument("--host", help="host SSH del QA; no se guarda")
    parser.add_argument("--user", help="usuario SSH del QA; no se guarda")
    parser.add_argument("--remote-dir", help="directorio remoto verificado")
    parser.add_argument("--ssh-key", help="ruta de clave SSH; no se imprime")
    parser.add_argument("--check-remote", action="store_true", help="ejecuta comprobaciones SSH de solo lectura")
    parser.add_argument("--execute", action="store_true", help="reservado; no habilitado en esta fase")
    args = parser.parse_args()
    if args.execute:
        print("ERROR: el despliegue real no está habilitado en esta fase.", file=sys.stderr)
        return 3
    if args.check_remote:
        missing = [name for name, value in (("--host", args.host), ("--user", args.user), ("--remote-dir", args.remote_dir), ("--ssh-key", args.ssh_key)) if not value]
        if missing:
            print(f"ERROR: --check-remote requiere: {', '.join(missing)}", file=sys.stderr)
            return 2
        remote = args.remote_dir.replace("'", "'\\''")
        command = (
            f"set -e; test -d '{remote}'; hostname; whoami; git -C '{remote}' rev-parse --show-toplevel; "
            f"git -C '{remote}' branch --show-current; git -C '{remote}' rev-parse HEAD; "
            f"test -f '{remote}/README_DEPLOY.md'; test -d '{remote}/deploy'; echo QA_LAYOUT_OK"
        )
        result = subprocess.run(
            ["ssh", "-i", args.ssh_key, "-o", "BatchMode=yes", "-o", "ConnectTimeout=12", f"{args.user}@{args.host}", command],
            text=True,
            capture_output=True,
        )
        if result.returncode:
            print(result.stderr.strip() or "SSH devolvió un error.", file=sys.stderr)
            return result.returncode
        print("COMPROBACIÓN SSH QA 194: OK")
        print(result.stdout.strip())
        return 0
    print("PLAN DE DESPLIEGUE QA 194")
    print(f"Referencia publicada: {args.ref}")
    print(f"Host: {args.host or '(pendiente en configuración externa)'}")
    print(f"Usuario: {args.user or '(pendiente de verificación)'}")
    print(f"Directorio remoto: {args.remote_dir or '(pendiente de verificación)'}")
    print("No se ejecutaron SSH, respaldos, migraciones, reinicios ni cambios remotos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
