# Walkthrough: Sistema Listo para Pruebas SaaS

Se ha configurado exitosamente el entorno de pruebas con la nueva arquitectura **Multi-tenant SaaS** y se ha resuelto el problema de conectividad con la base de datos.

## 📡 Conectividad Restaurada
- Se actualizó el archivo `.env` para utilizar el **Connection Pooler de Supabase** (Puerto 6543) con el hostname de IPv4. Esto soluciona los errores de "Name or service not known" causados por la red local.

## 👥 Usuarios de Prueba Creados
Se ejecutó un proceso de *seeding* que limpió las tablas y generó la siguiente estructura:

### **Organización: Ganadería GAVAC Demo**
| Usuario | Clave | Rol Principal | Acceso a Fincas |
| :--- | :--- | :--- | :--- |
| **admin@gavac.test** | `admin123` | Administrador | Hacienda El Paraíso, Finca La Esperanza |
| **vete@gavac.test** | `vete123` | Veterinario | Hacienda El Paraíso |
| **campo@gavac.test** | `campo123` | Operario | Finca La Esperanza |

## 🚀 Instrucciones para Iniciar
1.  **Backend**: Ejecuta el servidor desde la carpeta `backend`:
    ```powershell
    python -m uvicorn app.main:app --reload --port 8000
    ```
2.  **Frontend**: Ejecuta el servidor desde la carpeta `frontend`:
    ```powershell
    npm start
    ```
3.  **Acceso**: Abre tu navegador en [http://127.0.0.1:5434](http://127.0.0.1:5434).

## ✅ Pruebas Recomendadas
- **Prueba 1 (Admin)**: Entra con `admin@gavac.test`. Deberías poder ver y gestionar ambas fincas y todos los módulos.
- **Prueba 2 (Contexto)**: Entra con `vete@gavac.test`. Verifica que solo aparezca "Hacienda El Paraíso" en tu selector y que tengas acceso a los módulos de Sanidad.
- **Prueba 3 (Seguridad)**: Entra con `campo@gavac.test`. Verifica que solo veas "Finca La Esperanza" y que los módulos administrativos estén bloqueados.

> [!SUCCESS]
> El sistema es ahora 100% funcional bajo el modelo SaaS. Los datos están aislados y los roles se aplican dinámicamente según la finca seleccionada.
