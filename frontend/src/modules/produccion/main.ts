
import { listarProduccion, registrarProduccion, Produccion } from "./api.js";

const tableBody = document.getElementById("produccion-table-body") as HTMLTableSectionElement;
const form = document.getElementById("produccion-form") as HTMLFormElement;

function renderProduccion(registros: Produccion[]): void {
    tableBody.innerHTML = "";
    for (const reg of registros) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><span class="text-slate-500 font-medium">${reg.fecha}</span></td>
            <td><span class="font-bold text-gavac-primary">AN-${reg.animal_id}</span></td>
            <td><span class="font-bold text-slate-700">${reg.litros} Lts</span></td>
            <td>
                <span class="badge ${reg.jornada === 'Mañana' ? 'badge-active' : 'badge-alert'}">
                    ${reg.jornada}
                </span>
            </td>
            <td class="text-right text-xs text-slate-400 font-medium">${reg.created_at}</td>
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
    localStorage.removeItem("gavac_token");
    localStorage.removeItem("gavac_usuario");
    window.location.href = "../../../index.html";
});

cargarProduccion();
