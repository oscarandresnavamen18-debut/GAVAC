# Plan de Ejecución con Usuarios de Prueba

Este plan detalla los pasos para poblar la base de datos con usuarios de prueba y poner en marcha el sistema para validación.

## User Review Required

> [!IMPORTANT]
> **Conexión a Base de Datos**: Actualmente el archivo `.env` utiliza una dirección IPv6 directa que parece ser inalcanzable. Se recomienda verificar si el proyecto en Supabase está activo y obtener la URL de conexión del "Connection Pooler" (Puerto 6543) con el hostname de IPv4 si es posible.
> **Limpieza de Datos**: El script de seeding borrará las tablas actuales y las creará de cero para asegurar que la estructura SaaS sea consistente.

## Proposed Changes

### [Backend - Datos de Prueba]

#### [MODIFY] [backend/app/seed.py](file:///C:/proyecto_Final_Gavac/GAVAC/backend/app/seed.py)
- Actualizar el script para crear:
  - **Organización**: "Ganadería GAVAC Demo"
  - **Finca**: "Hacienda El Paraíso"
  - **Finca**: "Finca La Esperanza"
  - **Usuario Admin**: `admin@gavac.test` / `admin123` (Acceso total)
  - **Usuario Veterinario**: `vete@gavac.test` / `vete123` (Acceso a Sanidad)
  - **Usuario Operario**: `campo@gavac.test` / `campo123` (Acceso a Producción)

### [Frontend - Configuración]

#### [VERIFY] [frontend/src/modules/auth/api.ts](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/src/modules/auth/api.ts)
- Asegurar que apunta a `127.0.0.1:8000` para las pruebas locales.

## Verification Plan

### Manual Verification
1. **Sincronización**: Ejecutar `python app/seed.py` y confirmar que no hay errores de conexión.
2. **Inicio del Servidor**: Ejecutar el backend con `uvicorn`.
3. **Prueba de Login**:
   - Entrar con `admin@gavac.test`.
   - Seleccionar una finca.
   - Verificar que el Dashboard carga correctamente.
4. **Prueba de Roles**:
   - Entrar con `campo@gavac.test`.
   - Verificar que el acceso está restringido según los permisos definidos.
