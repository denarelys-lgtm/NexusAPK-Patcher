import os
import sys
import re

def patch_flag_secure(decoded_dir):
    """
    Deshabilita de forma segura la bandera FLAG_SECURE (0x2000) en todos los archivos Smali
    para permitir capturas y grabaciones de pantalla sin restricciones ni errores de registro.
    """
    smali_dirs = [os.path.join(decoded_dir, d) for d in os.listdir(decoded_dir) if d.startswith("smali")]
    patched_files = 0
    
    # Patrón preciso para buscar la asignación de FLAG_SECURE
    flag_pattern = re.compile(r'const/?[a-z0-9]*\s+([vp]\d+),\s+0x2000')

    for smali_dir in smali_dirs:
        if not os.path.exists(smali_dir):
            continue
        for root, _, files in os.walk(smali_dir):
            for file in files:
                if file.endswith(".smali"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()

                        match = flag_pattern.search(content)
                        if match:
                            reg = match.group(1)
                            # Reemplaza la bandera por 0x0 utilizando el mismo registro original
                            new_content = flag_pattern.sub(f'const/16 {reg}, 0x0', content)
                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write(new_content)
                            patched_files += 1
                    except Exception:
                        continue

    print(f"[+] [Seguridad] FLAG_SECURE neutralizado de forma segura en {patched_files} archivos Smali.")

def apply_overlay(decoded_dir, overlay_dir):
    """
    Aplica archivos personalizados desde el repositorio si existen.
    """
    if not os.path.exists(overlay_dir):
        print("[-] No se encontró carpeta de overlay estático. Continuando...")
        return

    for root, _, files in os.walk(overlay_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, overlay_dir)
            dest_path = os.path.join(decoded_dir, rel_path)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(src_path, "rb") as sf, open(dest_path, "wb") as df:
                df.write(sf.read())
            print(f"[+] [Overlay] Archivo aplicado: {rel_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 apply_patch.py <decoded_dir> <overlay_dir>")
        sys.exit(1)

    decoded_directory = sys.argv[1]
    overlay_directory = sys.argv[2]

    print("=== INICIANDO ENSAMBLAJE DE PARCHE SEGURO TANGO ===")
    apply_overlay(decoded_directory, overlay_directory)
    patch_flag_secure(decoded_directory)
    print("=== ENSAMBLAJE DE PARCHE COMPLETADO CON ÉXITO ===")
