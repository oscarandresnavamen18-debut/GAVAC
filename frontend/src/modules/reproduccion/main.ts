
import { listarReproduccion, registrarReproduccion, Reproduccion } from "./api.js";

const tableBody = document.getElementById("reproduccion-table-body") as HTMLTableSectionElement;
const form = document.getElementById("reproduccion-form") as HTMLFormElement;

function renderReproduccion(registros: Reproduccion[]): void {
    tableBody.innerHTML = "";
    for (const reg of registros) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><span class="text-slate-500 font-medium">${reg.fecha_evento}</span></td>
            <td><span class="font-bold text-gavac-primary">AN-${reg.animal_id}</span></td>
            <td><span class="font-bold text-slate-700">${reg.tipo}</span></td>
            <td>
                <span class="badge ${reg.estado === 'Completada' || reg.estado === 'Confirmada' ? 'badge-done' : 'badge-process'}">
                    ${reg.estado}
                </span>
            </td>
            <td><span class="text-slate-500 italic text-sm">${reg.observaciones ?? "—"}</span></td>
        `;
        tableBody.appendChild(tr);
    }
    // @ts-ignore
    if (window.lucide) { window.lucide.createIcons(); }
}

async function cargarReproduccion(): Promise<void> {
    try {
        const data = await listarReproduccion();
        renderReproduccion(data);
        document.getElementById("empty-state")?.classList.toggle("hidden", data.length > 0);
    } catch (err) {
        console.error(err);
        alert(`Error: ${(err as Error).message}`);
    }
}

form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = {
        animal_tag: String(formData.get("animal_tag")),
        tipo: String(formData.get("tipo")),
        fecha_evento: String(formData.get("fecha_evento")),
        observaciones: String(formData.get("observaciones")) || undefined,
    };

    try {
        await registrarReproduccion(data);
        form.reset();
        document.getElementById('reproduccion-modal')?.classList.add('hidden');
        await cargarReproduccion();
    } catch (err) {
        alert((err as Error).message);
    }
});

document.getElementById('logoutBtn')?.addEventListener('click', () => {
    localStorage.removeItem("gavac_token");
    localStorage.removeItem("gavac_usuario");
    window.location.href = "/login.html";
});

cargarReproduccion();
