// ============================================
// API GAVAC - REPORTES Y CONSULTAS
// ============================================

const currentHost = window.location.hostname;
const isDev = window.location.port === '5434';
const BASE_URL = isDev ? `http://${currentHost}:8000` : '';

export interface ResumenItem { sexo: string | null; estado: string; cantidad: number; }
export interface ResumenReporte { fecha_generacion: string; resumen: ResumenItem[]; }
export interface AnimalReciente { id: number; tag: string; breed: string | null; sex: string | null; birth_date: string | null; status: string; created_at: string; updated_at: string; }
export interface AuditoriaLog { id: number; usuario_id: number | null; email: string | null; accion: string; detalles: string | null; ip_address: string | null; created_at: string; }

export class ApiError extends Error {
  constructor(message: string, public readonly status: number) {
    super(message);
    this.name = "ApiError";
  }
}

function getHeaders(token: string): Record<string, string> {
  const fincaData = JSON.parse(localStorage.getItem("gavac_active_finca") || '{}');
  const headers: Record<string, string> = { Accept: "application/json", Authorization: `Bearer ${token}` };
  if (fincaData.id) {
    headers["X-Finca-ID"] = String(fincaData.id);
  }
  return headers;
}

async function parseErrorMessage(res: Response): Promise<string> {
  try {
    const body = await res.json();
    return String(body.detail || body.message || `Error HTTP ${res.status}`);
  } catch {
    return `Error HTTP ${res.status}: ${res.statusText}`;
  }
}

export async function getResumenInventario(token: string): Promise<ResumenReporte> {
  const response = await fetch(`${BASE_URL}/api/reportes/resumen/`, {
    method: "GET",
    headers: getHeaders(token),
  });
  if (!response.ok) throw new ApiError(await parseErrorMessage(response), response.status);
  return (await response.json()) as ResumenReporte;
}

export async function getAnimalesRecientes(token: string): Promise<AnimalReciente[]> {
  const response = await fetch(`${BASE_URL}/api/reportes/recientes/`, {
    method: "GET",
    headers: getHeaders(token),
  });
  if (!response.ok) throw new ApiError(await parseErrorMessage(response), response.status);
  return (await response.json()) as AnimalReciente[];
}

export async function getLogsAuditoria(token: string): Promise<AuditoriaLog[]> {
  const response = await fetch(`${BASE_URL}/api/auth/auditoria/`, {
    method: "GET",
    headers: getHeaders(token),
  });
  if (!response.ok) throw new ApiError(await parseErrorMessage(response), response.status);
  return (await response.json()) as AuditoriaLog[];
}
