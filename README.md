# GAVAC — Sistema de Registro de Ganado

Proyecto final ADSO — SENA CTMA (ficha 3223874).

## 🚀 Stack del Proyecto

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
└── guia_instalacion.md       # 🏁 Guía rápida de comandos
```

## ⚙️ Cómo ejecutar el proyecto

Para una guía detallada con comandos de copiado rápido, consulta la **[Guía de Instalación](guia_instalacion.md)**.

### Backend (FastAPI)
```powershell
cd backend
.\venv\Scripts\Activate+.ps1
$env:PYTHONPATH="."
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
python -m uvicorn app.main:app --reload --port 8000
```
> **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend (TypeScript)
```powershell
cd frontend
npm install
npx tsc  # Compilar TypeScript a JS
```
Abre `index.html` con **Live Server** o directamente en el navegador.

## 📜 Reglas de Trabajo

1. **Encapsulamiento:** Trabaja solo dentro de la carpeta de tu módulo.
2. **Base de Datos:** Elian gestiona el modelo en Supabase. No alteres las tablas sin coordinación previa.
3. **Flujo Git:** Usa ramas `feature/<módulo>` y sube cambios mediante Pull Requests.
4. **Auditoría:** Todas las acciones de escritura y lectura deben pasar por el servicio de auditoría modular.
5. **Configuración:** Nunca subas el archivo `.env` real al repositorio; usa siempre `.env.example`.
