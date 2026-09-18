// API DE AUTENTICACIÓN - GAVAC
const currentHost = window.location.hostname;
const isDev = window.location.port === '5434';
// Usar 127.0.0.1 explícitamente para evitar conflictos de localhost
const BASE_URL = isDev ? `http://127.0.0.1:8000` : '';
const API_BASE = `${BASE_URL}/api/auth`;

export interface UsuarioCreate { email: string; password: string; nombre_organizacion?: string; }
export interface UsuarioLogin { email: string; password: string; }
export interface UsuarioOut { id: number; email: string; rol: string; created_at: string; }
export interface Token { access_token: string; token_type: string; usuario: UsuarioOut; }

async function obtenerMensajeError(response: Response, fallback: string): Promise<string> {
  try {
    const error = await response.json();
    console.log("DETALLE ERROR API:", error);

    if (error.detail && Array.isArray(error.detail)) {
        return "Error de validación: " + error.detail.map((e: any) => `${e.loc[1]}: ${e.msg}`).join(", ");
    }
    return String(error.mensaje || error.detail || fallback);
  } catch {
    return `${fallback} (HTTP ${response.status})`;
  }
}

export async function registrar(datos: UsuarioCreate): Promise<UsuarioOut> {
  const response = await fetch(`${API_BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });

  if (!response.ok) {
    throw new Error(await obtenerMensajeError(response, "Error en el registro"));
  }
  return await response.json();
}

export async function login(datos: UsuarioLogin): Promise<Token> {
  const response = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });

  if (!response.ok) {
    throw new Error(await obtenerMensajeError(response, "Error en login"));
  }

  return await response.json();
}
