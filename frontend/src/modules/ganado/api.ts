// ============================================
// API GAVAC - GANADO
// ============================================

const currentHost = window.location.hostname;
const isDev = window.location.port === '5434';
const BASE_URL = isDev ? `http://${currentHost}:8000` : '';
const API_BASE = `${BASE_URL}/api/ganado/`; // BARRA FINAL OBLIGATORIA
const API_HEALTH = `${BASE_URL}/health/`;

export type Sexo = "macho" | "hembra";
export type Estado = "active" | "inactive" | "sold" | "deceased";

export interface Animal {
  id: number;
  tag: string;
  nombre: string | null;
  especie: string;
  raza: string | null;
  sexo: Sexo | null;
  peso_actual: number | null;
  edad_meses: number | null;
  lote: string | null;
  finca_id: number | null;
  status: Estado;
  created_at: string;
  updated_at: string;
}

export interface AnimalInput {
  tag: string;
  nombre?: string;
  especie?: string;
  raza?: string;
  sexo?: Sexo;
  peso_actual?: number;
  edad_meses?: number;
  lote?: string;
  finca_id?: number;
}

export interface Filtros {
  tag?: string;
  breed?: string;
}

function authHeaders(): Record<string, string> {
  const token = localStorage.getItem("gavac_token");
  const fincaData = JSON.parse(localStorage.getItem("gavac_active_finca") || '{}');
  const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {};
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

export async function listarAnimales(filtros: Filtros = {}): Promise<Animal[]> {
  const params = new URLSearchParams();
  if (filtros.tag) params.set("tag", filtros.tag);
  if (filtros.breed) params.set("breed", filtros.breed);

  const query = params.toString();
  const url = query ? `${API_BASE}?${query}` : API_BASE;

  const res = await fetch(url, { method: "GET", headers: authHeaders() });
  if (!res.ok) throw new Error(await parseErrorMessage(res));
  return await res.json();
}

export async function registrarAnimal(data: AnimalInput): Promise<Animal> {
  const res = await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await parseErrorMessage(res));
  return await res.json();
}

export async function eliminarAnimal(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}${id}/`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(await parseErrorMessage(res));
}
