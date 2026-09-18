# Plan de Rediseño "GAVAC Elite Suite v2.0"

Este plan transforma el sistema GAVAC en una aplicación empresarial robusta, cumpliendo con los requerimientos de usabilidad (RN-007) y escalabilidad (RN-008) definidos en el documento de ADSO.

## User Review Required

> [!IMPORTANT]
> **Cambio de Flujo**: Se implementará un sistema de protección de rutas. Si el usuario intenta acceder al Dashboard sin loguearse, será redirigido al Login. Si ya está logueado, no verá la Landing comercial.

> [!NOTE]
> **Diseño Adaptativo**: Se utilizará una estructura de "Layout Maestro" con Sidebar para que la aplicación no se distorsione en diferentes resoluciones, cumpliendo con el requerimiento RNF-009 (Portabilidad).

## Proposed Changes

### Identidad Visual (Elite Theme)
- **Primario**: Verde Esmeralda Profesional (`#1B5E20`).
- **Navegación**: Azul Pizarra Profundo (`#0F172A`).
- **Fondo**: Gris de Trabajo Suave (`#F3F4F6`).

### Pantallas

#### [MODIFY] [dashboard.html](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/dashboard.html)
- Rediseño como "Centro de Comando" con Sidebar lateral.
- Tarjetas de estado para Inventario y Producción (RF-018, RF-016).

#### [MODIFY] [src/modules/ganado/index.html](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/src/modules/ganado/index.html)
- Integración del Sidebar unificado.
- Formulario de registro con validación visual (HU-006).

#### [MODIFY] [src/modules/auth/main.ts](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/src/modules/auth/main.ts)
- Sincronización de la redirección definitiva a `/dashboard`.

## Verification Plan

### Manual Verification
1. Loguearse y confirmar que el diseño del Dashboard sea limpio y los menús no se superpongan.
2. Navegar entre Ganado y Reportes sin que la barra lateral desaparezca o se mueva.
3. Redimensionar la ventana del navegador para verificar que el diseño se mantenga ordenado (Responsive Check).
