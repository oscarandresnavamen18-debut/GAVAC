
const currentHost = window.location.hostname;
const isDev = window.location.port === '5434';
const BASE_URL = isDev ? `http://${currentHost}:8000` : '';
const API_BASE = `${BASE_URL}/api/reproduccion/`; // BARRA FINAL

export interface Reproduccion {
    id: number;
    animal_id: number;
    tipo: string;
    fecha_evento: string;
    estado: string;
    observaciones: string | null;
    created_at: string;
}

export interface ReproduccionInput {
    animal_tag: string;
    tipo: string;
    fecha_evento: string;
    estado?: string;
    observaciones?: string;
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

export async function listarReproduccion(animalId?: number): Promise<Reproduccion[]> {
    const url = animalId ? `${API_BASE}?animal_id=${animalId}` : API_BASE;
    const res = await fetch(url, { headers: authHeaders() });
    if (!res.ok) throw new Error("Error al obtener registros de reproducción");
    return await res.json();
}

export async function registrarReproduccion(data: ReproduccionInput): Promise<Reproduccion> {
    const res = await fetch(API_BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Error al registrar evento reproductivo");
    return await res.json();
}
