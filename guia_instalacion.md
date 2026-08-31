# 🏁 Guía Unificada de Producción - GAVAC

Esta guía garantiza que el sistema funcione sin errores de compilación, utilizando Python 3.12 o superior.

---

## 1️⃣ Instalación Limpia (Solo la primera vez)

Si tuviste errores previos, ejecuta esto para limpiar y reinstalar correctamente:

```powershell
# 1. Borrar entorno anterior si existe (desde la raíz del proyecto)
Remove-Item -Recurse -Force backend/venv

# 2. Crear entorno con Python 3.12 (O versión instalada)
python -m venv backend/venv

# 3. Activar e instalar dependencias
.\backend\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r backend/requirements.txt
```

---

## 2️⃣ Compilación de Estilos y Código (Frontend)

Para que el diseño se vea correctamente y sin errores de Tailwind:

```powershell
cd frontend
npm install
npm run build
```

---

## 3️⃣ Configuración de Base de Datos

Asegúrate de tener el archivo `.env` en la carpeta `backend`:
1. Crea la copia: `cp backend/.env.example backend/.env`
2. Edita `backend/.env` con la URL de Supabase real.

---

## 4️⃣ Ejecución del Servidor (Modo Producción)

Cada vez que inicies el sistema, usa este bloque en tu terminal:

```powershell
# Moverse a la carpeta del servidor
cd backend

# Activar el entorno seguro
.\venv\Scripts\Activate.ps1

# Configurar el entorno de ejecución
$env:PYTHONPATH="."

# Lanzar el servidor unificado
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## ✅ Lista de Verificación Final (Audit)

*   **Ruta API:** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Ruta Web:** [http://localhost:8000/login](http://localhost:8000/login)
*   **Seguridad:** Cabeceras HSTS, CSP y X-Frame activadas automáticamente.

> [!IMPORTANT]
> **Auditoría Activa:** Todas las acciones del sistema quedan registradas en la tabla `logs_auditoria` de Supabase para trazabilidad total.
