import os
import sys

def escanear_disco():
    # Definir la unidad a escanear (por defecto la C: o la ruta principal del workspace)
    unidad_objetivo = "C:\\"
    limite_peso_mb = 100  # Archivos mayores a 100 MB para detectar sobrecargas rápidas
    
    print("==================================================")
    print(f" ESCANEANDO DISCO EN BUSCA DE ARCHIVOS PESADOS...")
    print(f" Unidad analizada: {unidad_objetivo}")
    print("==================================================\n")
    
    archivos_pesados = []
    
    # Recorrido seguro por el sistema de archivos
    for raiz, directorios, archivos in os.walk(unidad_objetivo):
        # Omitir carpetas del sistema que suelen denegar acceso o generar ruido innecesario
        if any(exc in raiz.lower() for exc in ["windows", "$recycle.bin", "appdata\\local\\temp"]):
            continue
            
        for archivo in archivos:
            ruta_completa = os.path.join(raiz, archivo)
            try:
                tamano_bytes = os.path.getsize(ruta_completa)
                tamano_mb = tamano_bytes / (1024 * 1024)
                
                if tamano_mb > limite_peso_mb:
                    archivos_pesados.append((ruta_completa, round(tamano_mb, 2)))
            except (PermissionError, FileNotFoundError):
                # Omitir archivos bloqueados por el sistema operativo
                continue

    # Ordenar de mayor a menor tamaño
    archivos_pesados.sort(key=lambda x: x[1], reverse=True)

    print("\n--- ARCHIVOS QUE MÁS ESPACIO OCUPAN (>100MB) ---")
    if not archivos_pesados:
        print("No se encontraron archivos grandes en las rutas analizadas.")
    else:
        for idx, (ruta, peso) in enumerate(archivos_pesados[:20], 1):
            print(f"{idx}. [{peso} MB] -> {ruta}")

    print("\n==================================================")
    print(" AUDITORÍA DE ESPACIO FINALIZADA.")
    print("==================================================")

if __name__ == "__main__":
    escanear_disco()