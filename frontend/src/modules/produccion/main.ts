
import { listarProduccion, registrarProduccion, Produccion } from "./api.js";

const tableBody = document.getElementById("produccion-table-body") as HTMLTableSectionElement;
const form = document.getElementById("produccion-form") as HTMLFormElement;

function renderProduccion(registros: Produccion[]): void {
    tableBody.innerHTML = "";
    for (const reg of registros) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="font-bold text-slate-400 text-xs">${reg.fecha}</td>
            <td class="font-black text-gavac-primary tracking-tight">AN-${reg.animal_id}</td>
            <td class="font-black text-blue-600">${reg.litros} Lts</td>
            <td>
                <span class="badge-gavac ${reg.jornada === 'Mañana' ? 'badge-gavac-info' : 'badge-gavac-warning'}">
                    ${reg.jornada}
                </span>
            </td>
            <td class="text-right text-[10px] font-black text-slate-300 uppercase tracking-widest">${reg.created_at}</td>
        `;
        tableBody.appendChild(tr);
    }
    // @ts-ignore
    if (window.lucide) { window.lucide.createIcons(); }
}

async function cargarProduccion(): Promise<void> {
    try {
        const data = await listarProduccion();
        renderProduccion(data);
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
        litros: Number(formData.get("litros")),
        jornada: String(formData.get("jornada")),
        fecha: String(formData.get("fecha")) || undefined,
    };

    try {
        await registrarProduccion(data);
        form.reset();
        document.getElementById('produccion-modal')?.classList.add('hidden');
        await cargarProduccion();
    } catch (err) {
        alert((err as Error).message);
    }
});

document.getElementById('logoutBtn')?.addEventListener('click', () => {
    localStorage.clear();
    window.location.href = "/";
});

cargarProduccion();
