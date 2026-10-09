
import { listarSanidad, registrarSanidad, Sanidad } from "./api.js";

const tableBody = document.getElementById("sanidad-table-body") as HTMLTableSectionElement;
const form = document.getElementById("sanidad-form") as HTMLFormElement;

function renderSanidad(registros: Sanidad[]): void {
    tableBody.innerHTML = "";
    for (const reg of registros) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="font-bold text-slate-400 text-xs">${reg.fecha_aplicacion ?? "—"}</td>
            <td class="font-black text-gavac-primary tracking-tight">AN-${reg.animal_id}</td>
            <td>
                <div class="flex flex-col">
                    <span class="font-bold text-slate-700">${reg.producto}</span>
                    <span class="text-[10px] font-black text-slate-300 uppercase tracking-tighter">${reg.tipo}</span>
                </div>
            </td>
            <td class="font-medium text-slate-500">${reg.dosis ?? "—"}</td>
            <td class="text-xs font-bold ${reg.proxima_fecha ? 'text-amber-600' : 'text-slate-300'}">
                ${reg.proxima_fecha ?? "No programada"}
            </td>
            <td>
                <span class="badge-gavac ${reg.estado === 'Completada' ? 'badge-gavac-success' : 'badge-gavac-warning'}">
                    ${reg.estado}
                </span>
            </td>
            <td class="text-right">
                <button class="w-8 h-8 bg-slate-50 rounded-lg flex items-center justify-center text-slate-300 hover:text-gavac-primary transition-all">
                    <i data-lucide="more-horizontal" class="w-4 h-4"></i>
                </button>
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
    localStorage.clear();
    window.location.href = "/";
});

cargarSanidad();
