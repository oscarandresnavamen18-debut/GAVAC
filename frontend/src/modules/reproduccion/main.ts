
import { listarReproduccion, registrarReproduccion, Reproduccion } from "./api.js";

const tableBody = document.getElementById("reproduccion-table-body") as HTMLTableSectionElement;
const form = document.getElementById("reproduccion-form") as HTMLFormElement;

function renderReproduccion(registros: Reproduccion[]): void {
    tableBody.innerHTML = "";
    for (const reg of registros) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="font-bold text-slate-400 text-xs">${reg.fecha_evento}</td>
            <td class="font-black text-gavac-primary tracking-tight">AN-${reg.animal_id}</td>
            <td class="font-bold text-slate-700">${reg.tipo}</td>
            <td>
                <span class="badge-gavac ${reg.estado === 'Completada' || reg.estado === 'Confirmada' ? 'badge-gavac-success' : 'badge-gavac-warning'}">
                    ${reg.estado}
                </span>
            </td>
            <td class="text-slate-400 font-medium text-xs">Vet. Responsable</td>
            <td class="text-right">
                <button class="w-8 h-8 bg-slate-50 rounded-lg flex items-center justify-center text-slate-300 hover:text-gavac-primary transition-all">
                    <i data-lucide="eye" class="w-4 h-4"></i>
                </button>
            </td>
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
    localStorage.clear();
    window.location.href = "/";
});

cargarReproduccion();
