
const currentHost = window.location.hostname;
const isDev = window.location.port === '5434';
const BASE_URL = isDev ? `http://${currentHost}:8000` : '';
const API_BASE = `${BASE_URL}/api/sanidad/`; // BARRA FINAL

export interface Sanidad {
    id: number;
    animal_id: number;
    tipo: string;
    producto: string;
    dosis: string | null;
    fecha_aplicacion: string | null;
    proxima_fecha: string | null;
    estado: string;
    created_at: string;
}

export interface SanidadInput {
    animal_tag: string;
    tipo: string;
    producto: string;
    dosis?: string;
    fecha_aplicacion?: string;
    proxima_fecha?: string;
    estado?: string;
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

export async function listarSanidad(animalId?: number): Promise<Sanidad[]> {
    const url = animalId ? `${API_BASE}?animal_id=${animalId}` : API_BASE;
    const res = await fetch(url, { headers: authHeaders() });
    if (!res.ok) throw new Error("Error al obtener registros de sanidad");
    return await res.json();
}

export async function registrarSanidad(data: SanidadInput): Promise<Sanidad> {
    const res = await fetch(API_BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Error al registrar evento de sanidad");
    return await res.json();
}
