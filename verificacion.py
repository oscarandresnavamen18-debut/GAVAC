import os
import json
import urllib.request
import urllib.error

def auditar_proyecto():
    print("=== ASISTENTE DE AUDITORÍA Y VERIFICACIÓN GAVAC ===")
    nombre_proyecto = input("Ingresa el nombre de la carpeta del proyecto a auditar: ").strip()
    
    ruta_proyecto = os.path.join(os.getcwd(), nombre_proyecto)

    if not os.path.exists(ruta_proyecto):
        print(f"[X] La ruta del proyecto '{ruta_proyecto}' no existe.")
        return

    print(f"\nIniciando auditoría para: {nombre_proyecto}...\n")
    errores = 0

    # 1. Verificar archivos críticos obligatorios
    archivos_requeridos = ["package.json", ".gitignore", "src/index.js"]
    for archivo in archivos_requeridos:
        full_path = os.path.join(ruta_proyecto, archivo)
        if os.path.exists(full_path):
            print(f"  [OK] Archivo encontrado: {archivo}")
        else:
            print(f"  [X] Falta archivo crítico: {archivo}")
            errores += 1

    # 2. Verificar integridad del package.json
    pkg_path = os.path.join(ruta_proyecto, "package.json")
    if os.path.exists(pkg_path):
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                json.load(f)
            print("  [OK] package.json tiene un formato JSON válido.")
        except Exception as e:
            print(f"  [X] package.json está corrupto o mal formado: {e}")
            errores += 1

    # 3. Verificar variables de entorno (.env)
    env_path = os.path.join(ruta_proyecto, ".env")
    if os.path.exists(env_path):
        print("  [OK] Archivo .env detectado.")
    else:
        print("  [!] Advertencia: No se encontró el archivo .env (Riesgo de error 500 en producción).")

    # 4. Comprobación de conectividad local (/health)
    print("\nVerificando endpoint de salud (/health en puerto 3000)...")
    try:
        req = urllib.request.Request("http://localhost:3000/health")
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            if data.get("ok") == True:
                print("  [OK] El backend responde correctamente al endpoint /health.")
            else:
                print("  [X] El endpoint /health respondió pero con datos inválidos.")
                errores += 1
    except Exception:
        print("  [!] El servidor local no está corriendo en http://localhost:3000 (Inícialo para validar rutas).")

    # Resumen Final de Auditoría
    print("\n" + "="*45)
    if errores > 0:
        print(f" AUDITORÍA FALLIDA: Se detectaron {errores} errores críticos.")
        print(" Corrige los elementos marcados con [X] antes de desplegar.")
    else:
        print(" ¡AUDITORÍA EXITOSA! El proyecto cumple con la estructura base.")
    print("="*45)

if __name__ == "__main__":
    auditar_proyecto()