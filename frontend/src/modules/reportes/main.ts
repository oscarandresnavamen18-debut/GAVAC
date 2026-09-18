// ============================================================
// LÓGICA DE INTERFAZ: PANEL DE CONSULTAS Y REPORTE
// Módulo: reportes (Responsable: Jorge Botero)
// ============================================================

import { 
  getResumenInventario, 
  getAnimalesRecientes, 
  getLogsAuditoria, 
  ApiError,
  ResumenReporte,
  AnimalReciente,
  AuditoriaLog
} from "./api.js";

const TOKEN_STORAGE_KEY = "gavac_token";

// Elementos de la UI
const reportLoader = document.getElementById("reportLoader") as HTMLDivElement;
const reportResult = document.getElementById("reportResult") as HTMLDivElement;
const logoutBtn = document.getElementById("logoutBtn") as HTMLButtonElement;

// Tarjetas del Panel
const cardResumen = document.getElementById("card-resumen") as HTMLDivElement;
const cardProduccion = document.getElementById("card-produccion") as HTMLDivElement;
const cardAuditoria = document.getElementById("card-auditoria") as HTMLDivElement;

// Formateador de Fechas
const dateFormatter = new Intl.DateTimeFormat("es-CO", {
  dateStyle: "medium",
  timeStyle: "short",
});

// ============================================================
// AUXILIARES DE ESTADO Y VISIBILIDAD
// ============================================================
function mostrarLoader(visible: boolean): void {
  if (reportLoader) {
    reportLoader.classList.toggle("hidden", !visible);
  }
}

function mostrarError(mensaje: string): void {
  if (reportResult) {
    reportResult.innerHTML = `
      <div class="p-4 bg-red-50 text-red-700 border border-red-200 rounded-lg text-sm text-center">
        ${mensaje}
      </div>
    `;
  }
}

function obtenerToken(): string {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY) ?? "";
  if (!token) {
    // Redirigir a login si no hay sesión
    alert("Tu sesión no es válida o ha expirado. Por favor inicia sesión.");
    window.location.href = "/login";
  }
  return token;
}

// ============================================================
// RENDERIZADO DE TABLAS
// ============================================================

function renderResumenTable(data: ResumenReporte): void {
  if (!data.resumen || data.resumen.length === 0) {
    reportResult.innerHTML = `<p class="text-center text-slate-500 py-6">No hay datos de inventario disponibles.</p>`;
    return;
  }

  const fechaFormateada = dateFormatter.format(new Date(data.fecha_generacion));

  let filasHtml = "";
  for (const item of data.resumen) {
    filasHtml += `
      <tr class="hover:bg-slate-50 transition-colors">
        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900 capitalize">${item.sexo ?? "No definido"}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600 uppercase">${item.estado}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-800 text-right">${item.cantidad}</td>
      </tr>
    `;
  }

  reportResult.innerHTML = `
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h3 class="font-bold text-slate-800 text-base">Resumen de Inventario Ganadero</h3>
        <span class="text-xs text-slate-500">Generado el: ${fechaFormateada}</span>
      </div>
      <table class="min-w-full divide-y divide-slate-200">
        <thead class="bg-slate-100/70 text-slate-500 text-xs font-semibold uppercase tracking-wider">
          <tr>
            <th class="px-6 py-3 text-left">Sexo</th>
            <th class="px-6 py-3 text-left">Estado</th>
            <th class="px-6 py-3 text-right">Cantidad</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 bg-white">
          ${filasHtml}
        </tbody>
      </table>
    </div>
  `;
}

function renderRecientesTable(data: AnimalReciente[]): void {
  if (data.length === 0) {
    reportResult.innerHTML = `<p class="text-center text-slate-500 py-6">No hay animales registrados recientemente.</p>`;
    return;
  }

  let filasHtml = "";
  for (const animal of data) {
    const fNacimiento = animal.birth_date ? new Date(animal.birth_date).toLocaleDateString("es-CO") : "—";
    filasHtml += `
      <tr class="hover:bg-slate-50 transition-colors">
        <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-900">${animal.tag}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">${animal.breed ?? "—"}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600 capitalize">${animal.sex ?? "—"}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">${fNacimiento}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm">
          <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-green-50 text-green-700 border border-green-200/50 uppercase">${animal.status}</span>
        </td>
      </tr>
    `;
  }

  reportResult.innerHTML = `
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="p-5 border-b border-slate-100 bg-slate-50/50">
        <h3 class="font-bold text-slate-800 text-base">Animales Registrados Recientemente</h3>
        <p class="text-xs text-slate-500 mt-1">Últimos 5 animales incorporados al sistema.</p>
      </div>
      <table class="min-w-full divide-y divide-slate-200">
        <thead class="bg-slate-100/70 text-slate-500 text-xs font-semibold uppercase tracking-wider">
          <tr>
            <th class="px-6 py-3 text-left">N.° Chapeta</th>
            <th class="px-6 py-3 text-left">Raza</th>
            <th class="px-6 py-3 text-left">Sexo</th>
            <th class="px-6 py-3 text-left">F. Nacimiento</th>
            <th class="px-6 py-3 text-left">Estado</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 bg-white">
          ${filasHtml}
        </tbody>
      </table>
    </div>
  `;
}

function renderAuditoriaTable(data: AuditoriaLog[]): void {
  if (data.length === 0) {
    reportResult.innerHTML = `<p class="text-center text-slate-500 py-6">No hay registros de auditoría.</p>`;
    return;
  }

  let filasHtml = "";
  for (const log of data) {
    const fecha = dateFormatter.format(new Date(log.created_at));
    filasHtml += `
      <tr class="hover:bg-slate-50 transition-colors">
        <td class="px-4 py-3 whitespace-nowrap text-xs text-slate-500">${fecha}</td>
        <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-slate-800">${log.email ?? "Invitado"}</td>
        <td class="px-4 py-3 whitespace-nowrap text-sm text-slate-900 font-semibold">${log.accion}</td>
        <td class="px-4 py-3 text-sm text-slate-600 max-w-xs truncate" title="${log.detalles ?? ""}">${log.detalles ?? "—"}</td>
        <td class="px-4 py-3 whitespace-nowrap text-xs text-slate-500">${log.ip_address ?? "—"}</td>
      </tr>
    `;
  }

  reportResult.innerHTML = `
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="p-5 border-b border-slate-100 bg-slate-50/50">
        <h3 class="font-bold text-slate-800 text-base">Registro de Auditoría del Sistema</h3>
        <p class="text-xs text-slate-500 mt-1">Historial de accesos y modificaciones (Solo administradores).</p>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200">
          <thead class="bg-slate-100/70 text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <tr>
              <th class="px-4 py-3 text-left">Fecha y Hora</th>
              <th class="px-4 py-3 text-left">Usuario</th>
              <th class="px-4 py-3 text-left">Acción</th>
              <th class="px-4 py-3 text-left">Detalles</th>
              <th class="px-4 py-3 text-left">IP</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 bg-white">
            ${filasHtml}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// ============================================================
// ACCIONES DE CARGA DE REPORTES
// ============================================================

async function fetchResumen(): Promise<void> {
  const token = obtenerToken();
  if (!token) return;

  mostrarLoader(true);
  reportResult.innerHTML = "";

  try {
    const data = await getResumenInventario(token);
    renderResumenTable(data);
  } catch (error: unknown) {
    const msg = error instanceof ApiError ? error.message : "Error al conectar con la API.";
    mostrarError(msg);
  } finally {
    mostrarLoader(false);
  }
}

async function fetchRecientes(): Promise<void> {
  const token = obtenerToken();
  if (!token) return;

  mostrarLoader(true);
  reportResult.innerHTML = "";

  try {
    const data = await getAnimalesRecientes(token);
    renderRecientesTable(data);
  } catch (error: unknown) {
    const msg = error instanceof ApiError ? error.message : "Error al conectar con la API.";
    mostrarError(msg);
  } finally {
    mostrarLoader(false);
  }
}

async function fetchAuditoria(): Promise<void> {
  const token = obtenerToken();
  if (!token) return;

  mostrarLoader(true);
  reportResult.innerHTML = "";

  try {
    const data = await getLogsAuditoria(token);
    renderAuditoriaTable(data);
  } catch (error: unknown) {
    let msg = "Error al conectar con la API.";
    if (error instanceof ApiError) {
      msg = error.status === 403 
        ? "Acceso Denegado: No tienes permisos de Administrador para ver los logs." 
        : error.message;
    }
    mostrarError(msg);
  } finally {
    mostrarLoader(false);
  }
}

// ============================================================
// INICIALIZACIÓN
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
  // Asegurar que el token exista al cargar la página
  obtenerToken();

  // Mensaje por defecto en el panel de resultados
  if (reportResult) {
    reportResult.innerHTML = `
      <div class="text-center text-slate-400 py-12 border-2 border-dashed border-slate-200 rounded-xl bg-white">
        <span class="text-sm font-black tracking-widest mb-3 block">BI</span>
        <p class="font-medium text-slate-500">Selecciona un reporte de arriba para ver las consultas</p>
        <p class="text-xs text-slate-400 mt-1">Los datos se cargarán en tiempo real desde Supabase</p>
      </div>
    `;
  }

  // Enlazar eventos a las tarjetas
  if (cardResumen) {
    cardResumen.addEventListener("click", () => void fetchResumen());
  }

  if (cardProduccion) {
    // La tarjeta 2 es para Producción. De momento la vincularemos a listar los animales recientes 
    // y presentaremos un aviso de que el módulo completo de pesaje está en producción/construcción.
    cardProduccion.addEventListener("click", () => void fetchRecientes());
  }

  if (cardAuditoria) {
    cardAuditoria.addEventListener("click", () => void fetchAuditoria());
  }

  // Cerrar Sesión
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      localStorage.removeItem("gavac_usuario");
      window.location.href = "/login";
    });
  }
});
