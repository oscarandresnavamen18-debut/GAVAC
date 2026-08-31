import os
import shutil

# Rutas del Workspace y Carpetas Reales
workspace_base = r"C:\Workspace_Dev"
carpeta_proyectos = r"C:\Workspace_Dev\1_Proyectos"
carpeta_documentacion = r"C:\Workspace_Dev\2_Documentacion"

def ejecutar_limpieza_y_orden():
    print("=== INICIANDO LIMPIEZA DE BASURA Y REUBICACIÓN ===")
    
    # 1. Limpieza de archivos basura conocidos
    archivos_basura = [
        r"C:\MiCarpetaBase\Descargas\Armoury_Crate_Full_Installation_Package.zip",
        r"C:\MiCarpetaBase\Descargas\Armoury_Crate_Full_Installation_Package"
    ]

    for item in archivos_basura:
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
                print(f"[BASURA ELIMINADA] {item}")
            except Exception as e:
                print(f"[ERROR] No se pudo borrar {item}: {e}")

    # 2. Reubicación de archivos sueltos en Workspace_Dev
    if os.path.exists(workspace_base):
        for item in os.listdir(workspace_base):
            ruta_item = os.path.join(workspace_base, item)
            if item in ["1_Proyectos", "2_Documentacion", ".git"]:
                continue
                
            if os.path.isfile(ruta_item):
                if item.lower().endswith(('.docx', '.pdf', '.txt', '.xlsx', '.md')):
                    destino = os.path.join(carpeta_documentacion, item)
                    if not os.path.exists(destino):
                        shutil.move(ruta_item, destino)
                        print(f"[DOC] Movido a Documentación: {item}")
                elif item.lower().endswith(('.zip', '.rar', '.py', '.js')):
                    destino = os.path.join(carpeta_proyectos, item)
                    if not os.path.exists(destino):
                        shutil.move(ruta_item, destino)
                        print(f"[PROYECTO] Movido a Proyectos: {item}")
            elif os.path.isdir(ruta_item):
                destino = os.path.join(carpeta_proyectos, item)
                if not os.path.exists(destino):
                    shutil.move(ruta_item, destino)
                    print(f"[CARPETA] Movida a Proyectos: {item}")

    print("=== LIMPIEZA Y REUBICACIÓN FINALIZADA CON ÉXITO ===")

if __name__ == "__main__":
    ejecutar_limpieza_y_orden()
