# GAVAC — Sistema de Registro de Ganado

Proyecto final ADSO — SENA CTMA (ficha 3223874).

## Stack del Proyecto

- **Front-end:** HTML5 + TypeScript + Tailwind CSS
- **Back-end:** Python 3.12+ (FastAPI)
- **Base de Datos:** PostgreSQL (Alojada en Supabase)
- **Servidor:** Uvicorn con soporte para recarga en caliente

## 👥 Equipo y Módulos

| Integrante | Módulo | Carpeta Backend | Carpeta Frontend |
|---|---|---|---|
| **Oscar (Líder)** | Registro de ganado + coordinación | `backend/app/modules/cattle` | `frontend/src/modules/ganado` |
| **Juan Herrera** | Usuarios y autenticación | `backend/app/modules/auth` | `frontend/src/modules/auth` |
| **Jorge Botero** | Consultas y reportes | `backend/app/modules/reportes` | `frontend/src/modules/reportes` |
| **Elian Martínez** | Base de datos y documentación | — (Administra Supabase) | — |

## 📂 Estructura del Repositorio

```text
gavac/
├── backend/                  # API en Python (FastAPI)
│   ├── requirements.txt      # Dependencias del sistema
│   ├── .env.example          # Plantilla para DATABASE_URL
│   └── app/
│       ├── main.py           # Punto de entrada unificado
│       ├── database.py       # Conexión centralizada a Supabase
│       └── modules/          # Módulos funcionales
├── frontend/                 # Interfaz de usuario
│   ├── index.html            # Punto de entrada (Login)
│   ├── tsconfig.json         # Configuración de TypeScript
│   └── src/
│       ├── shared/           # Tipos y utilidades comunes
│       └── modules/          # Módulos de la UI
├── docs/                     # Documentación técnica adicional
└── run_gavac.ps1             # Inicio automatizado del sistema
```

## ⚙️ Cómo ejecutar el proyecto

### Inicio rápido para el equipo

Desde la carpeta del proyecto, ejecuta:

```powershell
.\run_gavac.ps1
```

El script prepara el backend y frontend, valida las herramientas necesarias y muestra la URL de la landing pública y del login. La primera vez crea `backend\.env`; completa sus valores y ejecútalo nuevamente.

### Backend (FastAPI)
```powershell
cd backend
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH="."
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
python -m uvicorn app.main:app --reload --port 8000
```
> **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Crear el administrador inicial

El rol `admin` no se puede asignar desde el registro público. Para crear la primera cuenta administrativa:

```powershell
cd backend
$env:PYTHONPATH="."
.\venv\Scripts\python.exe scripts\crear_admin.py
```

El comando solicita el correo y la contraseña sin guardarlos en archivos. Después del primer acceso, Administración y Empleados estarán disponibles para esa cuenta.

### Frontend (TypeScript)
```powershell
cd frontend
npm install
npx tsc  # Compilar TypeScript a JS
```
El backend sirve la landing pública en `http://127.0.0.1:8000/` y el acceso en `http://127.0.0.1:8000/login`.

## 📜 Reglas de Trabajo

1. **Encapsulamiento:** Trabaja solo dentro de la carpeta de tu módulo.
2. **Base de Datos:** Elian gestiona el modelo en Supabase. No alteres las tablas sin coordinación previa.
3. **Flujo Git:** Usa ramas `feature/<módulo>` y sube cambios mediante Pull Requests.
4. **Auditoría:** Todas las acciones de escritura y lectura deben pasar por el servicio de auditoría modular.
5. **Configuración:** Nunca subas el archivo `.env` real al repositorio; usa siempre `.env.example`.
