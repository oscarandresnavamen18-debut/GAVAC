
const currentHost = window.location.hostname;
const isDev = window.location.port === '5434';
const BASE_URL = isDev ? `http://${currentHost}:8000` : '';
const API_BASE = `${BASE_URL}/api/produccion/`;

export interface Produccion {
    id: number;
    animal_id: number;
    litros: number;
    fecha: string;
    jornada: string;
    created_at: string;
}

export interface ProduccionInput {
    animal_tag: string;
    litros: number;
    fecha?: string;
    jornada: string;
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

export async function listarProduccion(animalId?: number): Promise<Produccion[]> {
    const url = animalId ? `${API_BASE}?animal_id=${animalId}` : API_BASE;
    const res = await fetch(url, { headers: authHeaders() });
    if (!res.ok) throw new Error("Error al obtener registros de producción");
    return await res.json();
}

export async function registrarProduccion(data: ProduccionInput): Promise<Produccion> {
    const res = await fetch(API_BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(data)
    });
    if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Error al registrar producción");
    }
    return await res.json();
}
