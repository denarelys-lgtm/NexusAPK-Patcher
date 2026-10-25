
#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print(
            "Uso: python3 scripts/apply_patch.py "
            "<directorio_descompilado> <directorio_overlay>"
        )
        return 2

    decoded = Path(sys.argv[1]).resolve()
    overlay = Path(sys.argv[2]).resolve()
    project_root = Path(__file__).resolve().parent.parent
    delete_file = project_root / "patches" / "delete.txt"

    if not decoded.is_dir():
        print(f"ERROR: no existe el APK descompilado: {decoded}")
        return 1

    if not overlay.is_dir():
        print(f"ERROR: no existe el directorio del parche: {overlay}")
        return 1

    files = [p for p in overlay.rglob("*") if p.is_file()]

    for source in files:
        relative = source.relative_to(overlay)
        destination = (decoded / relative).resolve()

        # Impide que un archivo del parche escape del proyecto.
        if not destination.is_relative_to(decoded):
            print(f"ERROR: ruta no permitida: {relative}")
            return 1

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        print(f"REEMPLAZADO: {relative}")

    if delete_file.exists():
        for line in delete_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            relative = Path(line)

            if relative.is_absolute() or ".." in relative.parts:
                print(f"ERROR: ruta de eliminación no permitida: {line}")
                return 1

            target = (decoded / relative).resolve()

            if not target.is_relative_to(decoded):
                print(f"ERROR: ruta de eliminación no permitida: {line}")
                return 1

            if target.is_file() or target.is_symlink():
                target.unlink()
                print(f"ELIMINADO: {relative}")
            elif target.is_dir():
                shutil.rmtree(target)
                print(f"DIRECTORIO ELIMINADO: {relative}")
            else:
                print(f"AVISO: no existe, se omite: {relative}")

    print(f"Parche aplicado. Archivos copiados: {len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
