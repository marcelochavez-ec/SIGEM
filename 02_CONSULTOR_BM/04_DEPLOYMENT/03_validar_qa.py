"""Validación local reproducible, no destructiva, previa a QA 194."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "01_MSP" / "02_SOFT",
        help="raíz de la aplicación Django; por defecto 01_MSP/02_SOFT",
    )
    parser.add_argument("--report", type=Path, help="ruta de informe Markdown")
    parser.add_argument("--skip-tests", action="store_true", help="solo valida estructura y manage.py check")
    args = parser.parse_args()
    project = args.project.resolve()
    repo = project.parent.parent
    checks = [
        ("manage.py", (project / "manage.py").is_file(), str(project / "manage.py")),
        ("settings.py", (project / "config_sigem" / "settings.py").is_file(), "configuración Django"),
        ("requirements.txt", (project / "requirements.txt").is_file(), "dependencias declaradas"),
    ]
    if checks[0][1]:
        result = subprocess.run(
            [sys.executable, str(project / "manage.py"), "check"],
            cwd=project,
            text=True,
            capture_output=True,
        )
        checks.append(("manage.py check", result.returncode == 0, (result.stdout + result.stderr).strip() or "sin salida"))
        if not args.skip_tests and result.returncode == 0:
            result = subprocess.run(
                [sys.executable, str(project / "manage.py"), "test", "sigem.tests", "--verbosity", "1"],
                cwd=project,
                text=True,
                capture_output=True,
            )
            checks.append(("pruebas sigem.tests", result.returncode == 0, (result.stdout + result.stderr).strip() or "sin salida"))
    result = subprocess.run(["git", "diff", "--check"], cwd=repo, text=True, capture_output=True)
    checks.append(("git diff --check", result.returncode == 0, result.stdout + result.stderr or "sin errores"))
    status = "APTO" if all(ok for _, ok, _ in checks) else "NO APTO"
    lines = [f"# Validación QA 194\n\nResultado: **{status}**\n", "| Verificación | Estado | Evidencia |", "|---|---|---|"]
    lines.extend(f"| {name} | {'OK' if ok else 'FALLO'} | {evidence.replace('|', '/').strip()} |" for name, ok, evidence in checks)
    report = "\n".join(lines) + "\n"
    print(report)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    return 0 if status == "APTO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
