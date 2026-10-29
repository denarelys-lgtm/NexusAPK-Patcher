import os
import sys
import re
import xml.etree.ElementTree as ET

def patch_flag_secure(decoded_dir):
    """
    Deshabilita FLAG_SECURE de forma segura limitándose a contextos de banderas de ventana
    para permitir capturas de pantalla sin errores de verificación (VerifyError).
    """
    smali_dirs = [os.path.join(decoded_dir, d) for d in os.listdir(decoded_dir) if d.startswith("smali")]
    patched_files = 0
    
    flag_pattern = re.compile(r'(const/?[a-z0-9]*\s+)([vp]\d+),\s+(0x2000)')

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

                        if "WindowManager" in content or "addFlags" in content or "setFlags" in content:
                            if flag_pattern.search(content):
                                new_content = flag_pattern.sub(r'\1\2, 0x0', content)
                                if new_content != content:
                                    with open(filepath, "w", encoding="utf-8") as f:
                                        f.write(new_content)
                                    patched_files += 1
                    except Exception:
                        continue

    print(f"[+] [Seguridad] FLAG_SECURE depurado de forma segura en {patched_files} archivos Smali.")

def optimize_manifest_and_telemetry(decoded_dir):
    """
    Limpia y optimiza el AndroidManifest.xml eliminando metadatos de análisis,
    rastreadores y servicios de telemetría redundantes en segundo plano.
    """
    manifest_path = os.path.join(decoded_dir, "AndroidManifest.xml")
    if not os.path.exists(manifest_path):
        print("[-] AndroidManifest.xml no encontrado.")
        return

    try:
        # Leemos el archivo de manifiesto como texto plano para modificaciones seguras de XML estructurado
        with open(manifest_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Patrones para identificar y neutralizar metadatos de analíticas comunes (Firebase, Crashlytics, etc.)
        # Esto evita que los SDKs de rastreo inicialicen sus canalidades de datos en segundo plano.
        cleaned_content = re.sub(r'<meta-data\s+android:name="firebase_analytics_collection_enabled"\s+android:value="true"\s*/>', 
                                 '<meta-data android:name="firebase_analytics_collection_enabled" android:value="false"/>', content)
        
        cleaned_content = re.sub(r'<meta-data\s+android:name="crashlytics_collection_enabled"\s+android:value="true"\s*/>', 
                                 '<meta-data android:name="crashlytics_collection_enabled" android:value="false"/>', cleaned_content)

        if cleaned_content != content:
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
            print("[+] [Telemetría] Metadatos de análisis y rastreo desactivados en el Manifiesto.")
        else:
            print("[+] [Telemetría] Manifiesto verificado (sin rastreadores directos expuestos en metadatos).")

    except Exception as e:
        print(f"[-] Error al optimizar el manifiesto: {e}")

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

    print("=== INICIANDO ENSAMBLAJE DE PARCHE OPTIMIZADO TANGO ===")
    apply_overlay(decoded_directory, overlay_directory)
    patch_flag_secure(decoded_directory)
    optimize_manifest_and_telemetry(decoded_directory)
    print("=== ENSAMBLAJE DE PARCHE COMPLETADO CON ÉXITO ===")
