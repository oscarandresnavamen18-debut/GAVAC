import os
import json

def crear_proyecto():
    print("=== ASISTENTE DE CREACIÓN DE PROYECTOS GAVAC ===")
    nombre_proyecto = input("Ingresa el nombre del nuevo proyecto: ").strip()
    
    if not nombre_proyecto:
        print("[X] El nombre del proyecto no puede estar vacío.")
        return

    # Ruta base del proyecto dentro de la carpeta actual
    ruta_base = os.path.join(os.getcwd(), nombre_proyecto)

    if os.path.exists(ruta_base):
        print(f"[!] La carpeta '{nombre_proyecto}' ya existe.")
        return

    print(f"Creando estructura para: {nombre_proyecto}...")
    
    # 1. Crear directorios clave (Mejores prácticas de arquitectura)
    carpetas = ["src", "src/modules", "config", "docs", "prisma"]
    for carpeta in carpetas:
        os.makedirs(os.path.join(ruta_base, carpeta), exist_ok=True)

    # 2. Crear package.json básico
    package_data = {
        "name": nombre_proyecto,
        "version": "1.0.0",
        "type": "module",
        "main": "src/index.js",
        "scripts": {
            "dev": "nodemon src/index.js"
        },
        "dependencies": {
            "cors": "^2.8.5",
            "dotenv": "^16.4.5",
            "express": "^4.19.2",
            "helmet": "^7.1.0"
        }
    }
    
    with open(os.path.join(ruta_base, "package.json"), "w", encoding="utf-8") as f:
        json.dump(package_data, f, indent=2)

    # 3. Crear archivo index.js base (Backend seguro con Express)
    index_content = '''import express from "express";
import cors from "cors";
import helmet from "helmet";
import dotenv from "dotenv";

dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;

app.use(helmet());
app.use(cors());
app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ ok: true, message: "Backend de " + process.env.npm_package_name + " funcionando correctamente" });
});

app.listen(PORT, () => {
  console.log(`Servidor activo en http://localhost:${PORT}`);
});
'''
    with open(os.path.join(ruta_base, "src", "index.js"), "w", encoding="utf-8") as f:
        f.write(index_content)

    # 4. Crear .gitignore estándar
    gitignore_content = """node_modules/
.env
dist/
build/
*.db
*.log
"""
    with open(os.path.join(ruta_base, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore_content)

    print(f"\n[OK] ¡Proyecto '{nombre_proyecto}' creado exitosamente en {ruta_base}!")

if __name__ == "__main__":
    crear_proyecto()