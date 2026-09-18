
const currentHost = window.location.hostname;
const isDev = window.location.port === '5434';
const BASE_URL = isDev ? `http://${currentHost}:8000` : '';
const API_BASE = `${BASE_URL}/api/inventario/`; // BARRA FINAL

export interface InventarioInsumo {
    id: number;
    nombre: string;
    categoria: string;
    cantidad: number;
    unidad: string;
    estado: string;
    created_at: string;
}

export interface InventarioInput {
    nombre: string;
    categoria: string;
    cantidad: number;
    unidad: string;
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

export async function listarInventario(categoria?: string): Promise<InventarioInsumo[]> {
    const url = categoria ? `${API_BASE}?categoria=${categoria}` : API_BASE;
    const res = await fetch(url, { headers: authHeaders() });
    if (!res.ok) throw new Error("Error al obtener registros de inventario");
    return await res.json();
}

export async function registrarInventario(data: InventarioInput): Promise<InventarioInsumo> {
    const res = await fetch(API_BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Error al registrar insumo");
    return await res.json();
}
