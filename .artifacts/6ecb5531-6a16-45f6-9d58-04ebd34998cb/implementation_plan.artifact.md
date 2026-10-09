# Plan de Rediseño UX/UI Profesional - GAVAC

Este plan detalla la evolución visual y de experiencia de usuario para transformar GAVAC en una plataforma SaaS de gestión ganadera de nivel profesional, manteniendo su identidad visual core.

## User Review Required

> [!IMPORTANT]
> **Consistencia Visual**: Se aplicará una rejilla y un sistema de componentes (botones, inputs, tablas) unificado en todos los módulos.
> **Flujo de Acceso**: El login será exclusivamente por credenciales, y la identificación de roles y fincas será automática y posterior al éxito de la autenticación.
> **Contexto de Finca**: Se implementará un selector de finca persistente y visible en la barra superior.

## Proposed Changes

### [Componentes Globales]

#### [NEW] [components.css](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/src/styles/components.css)
- Definición de clases Tailwind personalizadas para: `btn-gavac`, `input-gavac`, `card-gavac`, `table-gavac`, `badge-gavac`.

### [Acceso y Autenticación]

#### [MODIFY] [index.html](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/index.html)
- Rediseño del Login: Fondo profesional (campo/ganado con overlay), caja de login centrada o lateral con jerarquía clara. Eliminación de cualquier selección manual de rol.

#### [MODIFY] [fincas.html](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/fincas.html)
- Rediseño de selección de finca: Tarjetas informativas con conteo de animales, ubicación y rol asignado.

### [Estructura Principal (Layout)]

#### [MODIFY] [dashboard.html](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/dashboard.html)
- Actualización de Sidebar: Iconografía Lucide consistente, separación clara de módulos operativos vs administrativos.
- Inserción de Topbar: Perfil de usuario (dropdown), notificaciones, y nombre de finca activa con botón de cambio rápido.

### [Módulos Operativos]

#### [MODIFY] [Ganado](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/src/modules/ganado/index.html)
- Listado con filtros avanzados.
- **Ficha del Animal**: Vista de detalle con historial clínico, productivo y reproductivo.

#### [NEW] [Productividad](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/src/modules/produccion/index.html)
- Rediseño de la interfaz de registro de producción (leche/carne) e indicadores por lote.

#### [NEW] [Reproductividad](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/src/modules/reproduccion/index.html)
- Interfaz para eventos de celo, monta, palpación y partos con cronogramas.

### [Administración y Configuración]

#### [MODIFY] [Administración](file:///C:/proyecto_Final_Gavac/GAVAC/frontend/src/modules/admin/index.html)
- Separación estricta de gestión de usuarios, roles, fincas y catálogos.

## Verification Plan

### Manual Verification
1. **Flujo de Entrada**: Login -> Identificación automática -> Selección de Finca (si > 1) -> Dashboard.
2. **Cambio de Contexto**: Cambiar de finca desde la Topbar y verificar que los datos se actualicen (se usará el header `X-Finca-ID`).
3. **Cierre de Sesión**: Probar el botón desde el Sidebar y desde el menú de Perfil, confirmando el diálogo de seguridad.
4. **Diseño Responsive**: Probar en móvil la transformación del menú a modo hamburguesa.
