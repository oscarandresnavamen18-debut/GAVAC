// ============================================
// API GAVAC - REPORTES Y CONSULTAS
// Módulo: reportes (Responsable: Jorge Botero)
// ============================================

export interface ResumenItem {
  sexo: string | null;
  estado: string;
  cantidad: number;
}

export interface ResumenReporte {
  fecha_generacion: string;
  resumen: ResumenItem[];
}

export interface AnimalReciente {
  id: number;
  tag: string;
  breed: string | null;
  sex: string | null;
  birth_date: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface AuditoriaLog {
  id: number;
  usuario_id: number | null;
  email: string | null;
  accion: string;
  detalles: string | null;
  ip_address: string | null;
  created_at: string;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

// ============================================
// HELPER: CABECERAS DE AUTENTICACIÓN
// ============================================
function getHeaders(token: string): Record<string, string> {
  return {
    Accept: "application/json",
    Authorization: `Bearer ${token}`,
  };
}

// ============================================
// HELPER: PROCESAR MENSAJES DE ERROR
// ============================================
async function parseErrorMessage(res: Response): Promise<string> {
  try {
    const body = await res.json();
    if (body.detail) {
      if (Array.isArray(body.detail)) {
        return body.detail.map((err: any) => err.msg || "Error de validación").join(", ");
      }
      return String(body.detail);
    }
    return `Error HTTP ${res.status}`;
  } catch {
    return `Error HTTP ${res.status}: ${res.statusText}`;
  }
}

// ============================================
// ENPOINTS DE REPORTES
// ============================================

/** Obtiene el resumen de inventario por sexo y estado. */
export async function getResumenInventario(token: string): Promise<ResumenReporte> {
  if (!token) {
    throw new ApiError("No hay una sesión activa.", 401);
  }

  const response = await fetch("/api/reportes/resumen", {
    method: "GET",
    headers: getHeaders(token),
  });

  if (!response.ok) {
    const message = await parseErrorMessage(response);
    throw new ApiError(message, response.status);
  }

  return (await response.json()) as ResumenReporte;
}

/** Obtiene la lista de animales agregados recientemente. */
export async function getAnimalesRecientes(token: string): Promise<AnimalReciente[]> {
  if (!token) {
    throw new ApiError("No hay una sesión activa.", 401);
  }

  const response = await fetch("/api/reportes/recientes", {
    method: "GET",
    headers: getHeaders(token),
  });

  if (!response.ok) {
    const message = await parseErrorMessage(response);
    throw new ApiError(message, response.status);
  }

  return (await response.json()) as AnimalReciente[];
}

/** Obtiene la lista de logs de auditoría (Solo para rol Admin). */
export async function getLogsAuditoria(token: string): Promise<AuditoriaLog[]> {
  if (!token) {
    throw new ApiError("No hay una sesión activa.", 401);
  }

  const response = await fetch("/api/auth/auditoria", {
    method: "GET",
    headers: getHeaders(token),
  });

  if (!response.ok) {
    const message = await parseErrorMessage(response);
    throw new ApiError(message, response.status);
  }

  return (await response.json()) as AuditoriaLog[];
}
