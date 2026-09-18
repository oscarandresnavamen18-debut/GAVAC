const currentHost = window.location.hostname;
const isDev = window.location.port === '5434';
const BASE_URL = isDev ? `http://${currentHost}:8000` : '';
const API_ADMIN = `${BASE_URL}/api/admin`;

function authHeaders(): Record<string, string> {
    const token = localStorage.getItem("gavac_token");
    const fincaData = JSON.parse(localStorage.getItem("gavac_active_finca") || '{}');
    const headers: Record<string, string> = token ? { "Authorization": `Bearer ${token}` } : {};
    if (fincaData.id) {
        headers["X-Finca-ID"] = String(fincaData.id);
    }
    return headers;
}

export async function listarFincas() {
    const res = await fetch(`${API_ADMIN}/fincas/`, { headers: authHeaders() });
    return await res.json();
}

export async function crearFinca(data: any) {
    const res = await fetch(`${API_ADMIN}/fincas/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(data)
    });
    return await res.json();
}

export async function listarUsuarios() {
    const res = await fetch(`${API_ADMIN}/usuarios/`, { headers: authHeaders() });
    return await res.json();
}

export async function asignarRolFinca(data: { usuario_id: number; finca_id: number; rol: string }) {
    const res = await fetch(`${API_ADMIN}/fincas/asignar-rol/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(data)
    });
    return await res.json();
}

export async function crearUsuarioAdmin(data: any) {
    const res = await fetch(`${API_ADMIN}/usuarios/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(await res.text());
    return await res.json();
}

export async function actualizarUsuarioAdmin(id: number, data: any) {
    const res = await fetch(`${API_ADMIN}/usuarios/${id}/`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(await res.text());
    return await res.json();
}

export async function eliminarUsuarioAdmin(id: number) {
    const res = await fetch(`${API_ADMIN}/usuarios/${id}/`, {
        method: "DELETE",
        headers: authHeaders()
    });
    if (!res.ok) throw new Error(await res.text());
    return true;
}
