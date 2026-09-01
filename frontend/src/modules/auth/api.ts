// API DE AUTENTICACIÓN - GAVAC (PRODUCCIÓN)
// Usamos rutas relativas para evitar conflictos de CORS/CSP

const API_BASE = "/api/auth";

export interface UsuarioCreate { email: string; password: string; rol?: string; }
export interface UsuarioLogin { email: string; password: string; }
export interface UsuarioOut { id: number; email: string; rol: string; created_at: string; }
export interface Token { access_token: string; token_type: string; usuario: UsuarioOut; }

export async function registrar(datos: UsuarioCreate): Promise<UsuarioOut> {
  const response = await fetch(`${API_BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Error en el registro");
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
    const error = await response.json();
    throw new Error(error.detail || "Error en login");
  }
  return await response.json();
}
