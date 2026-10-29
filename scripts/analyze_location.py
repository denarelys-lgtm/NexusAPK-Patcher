import os
import sys
import re

def search_location_patterns(source_dir):
    """
    Escanea recursivamente los archivos de código fuente en busca de rastros
    de geolocalización, coordenadas, distancias o funciones de cercanía.
    """
    if not os.path.exists(source_dir):
        print(f"[-] El directorio de fuentes '{source_dir}' no existe.")
        return

    # Palabras clave orientadas a ubicar lógica de ubicación y cercanía
    keywords = [
        "latitude", "longitude", "gps", "location", "distance", 
        "nearby", "geo", "coordinate", "radius", "cerca", "ubicacion"
    ]
    
    # Expresión regular para buscar las palabras clave ignorando mayúsculas/minúsculas
    pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
    
    matches_found = 0
    print(f"=== INICIANDO ESCANEO DE LOCALIZACIÓN EN: {source_dir} ===")

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith((".java", ".smali", ".kt")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    
                    file_matched = False
                    for idx, line in enumerate(lines, 1):
                        if pattern.search(line):
                            if not file_matched:
                                rel_path = os.path.relpath(filepath, source_dir)
                                print(f"\n[📁 Archivo] {rel_path}")
                                file_matched = True
                            
                            print(f"  Line {idx}: {line.strip()}")
                            matches_found += 1
                except Exception:
                    continue

    print(f"\n=== ESCANEO FINALIZADO. Se encontraron {matches_found} coincidencias potenciales. ===")

if __name__ == "__main__":
    # Directorio predeterminado donde JADX suele exportar el código fuente descompilado
    default_source = "work/jadx-out/sources"
    
    target_dir = sys.argv[1] if len(sys.argv) > 1 else default_source
    search_location_patterns(target_dir)
