
import { listarSanidad, registrarSanidad, Sanidad } from "./api.js";

const tableBody = document.getElementById("sanidad-table-body") as HTMLTableSectionElement;
const form = document.getElementById("sanidad-form") as HTMLFormElement;

function renderSanidad(registros: Sanidad[]): void {
    tableBody.innerHTML = "";
    for (const reg of registros) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><span class="text-slate-500 font-medium">${reg.fecha_aplicacion ?? "—"}</span></td>
            <td><span class="font-bold text-gavac-primary">AN-${reg.animal_id}</span></td>
            <td>
                <div class="flex flex-col">
                    <span class="font-bold text-slate-700">${reg.producto}</span>
                    <span class="text-xs text-slate-400">${reg.tipo}</span>
                </div>
            </td>
            <td><span class="text-slate-500 font-medium">${reg.dosis ?? "—"}</span></td>
            <td><span class="text-slate-500 font-medium">${reg.proxima_fecha ?? "—"}</span></td>
            <td>
                <span class="badge ${reg.estado === 'Completada' ? 'badge-done' : 'badge-pending'}">
                    ${reg.estado}
                </span>
            </td>
        `;
        tableBody.appendChild(tr);
    }
    // @ts-ignore
    if (window.lucide) { window.lucide.createIcons(); }
}

async function cargarSanidad(): Promise<void> {
    try {
        const data = await listarSanidad();
        renderSanidad(data);
        document.getElementById("empty-state")?.classList.toggle("hidden", data.length > 0);
    } catch (err) {
        console.error(err);
        alert(`Error al conectar con la API: ${(err as Error).message}`);
    }
}

form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = {
        animal_tag: String(formData.get("animal_tag")),
        tipo: String(formData.get("tipo")),
        producto: String(formData.get("producto")),
        fecha_aplicacion: String(formData.get("fecha_aplicacion")) || undefined,
        proxima_fecha: String(formData.get("proxima_fecha")) || undefined,
    };

    try {
        await registrarSanidad(data);
        form.reset();
        document.getElementById('sanidad-modal')?.classList.add('hidden');
        await cargarSanidad();
    } catch (err) {
        alert((err as Error).message);
    }
});

document.getElementById('logoutBtn')?.addEventListener('click', () => {
    localStorage.removeItem("gavac_token");
    localStorage.removeItem("gavac_usuario");
    window.location.href = "/login.html";
});

cargarSanidad();
