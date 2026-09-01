// API DE AUTENTICACIÓN - GAVAC (PRODUCCIÓN)
// Usamos rutas relativas para evitar conflictos de CORS/CSP

const API_BASE = "/api/auth";

export interface UsuarioCreate { email: string; password: string; rol?: string; }
export interface UsuarioLogin { email: string; password: string; }
export interface UsuarioOut { id: number; email: string; rol: string; created_at: string; }
export interface Token { access_token: string; token_type: string; usuario: UsuarioOut; }

async function obtenerMensajeError(response: Response, fallback: string): Promise<string> {
  try {
    const error = await response.json();
    if (Array.isArray(error.detail)) {
      return error.detail.map((item: { msg?: string }) => item.msg || fallback).join(", ");
    }
    return String(error.detail || error.message || fallback);
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
