
import { listarInventario, registrarInventario, InventarioInsumo } from "./api.js";

const tableBody = document.getElementById("inventario-table-body") as HTMLTableSectionElement;
const form = document.getElementById("inventario-form") as HTMLFormElement;

function renderInventario(registros: InventarioInsumo[]): void {
    tableBody.innerHTML = "";
    for (const reg of registros) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="font-bold text-gavac-primary tracking-tight">${reg.nombre}</td>
            <td class="text-xs font-black text-slate-400 uppercase tracking-widest">${reg.categoria}</td>
            <td class="font-black text-slate-800">${reg.cantidad}</td>
            <td class="text-slate-500 font-medium">${reg.unidad}</td>
            <td>
                <span class="badge-gavac ${reg.cantidad > 10 ? 'badge-gavac-success' : 'badge-gavac-warning'}">
                    ${reg.cantidad > 10 ? 'Disponible' : 'Bajo Stock'}
                </span>
            </td>
            <td class="text-right">
                <button class="w-8 h-8 bg-slate-50 rounded-lg flex items-center justify-center text-slate-300 hover:text-gavac-primary transition-all">
                    <i data-lucide="edit-2" class="w-4 h-4"></i>
                </button>
            </td>
        `;
        tableBody.appendChild(tr);
    }
    // @ts-ignore
    if (window.lucide) { window.lucide.createIcons(); }
}

async function cargarInventario(): Promise<void> {
    try {
        const data = await listarInventario();
        renderInventario(data);
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
        nombre: String(formData.get("nombre")),
        categoria: String(formData.get("categoria")),
        cantidad: Number(formData.get("cantidad")),
        unidad: String(formData.get("unidad")),
    };

    try {
        await registrarInventario(data);
        form.reset();
        document.getElementById('inventario-modal')?.classList.add('hidden');
        await cargarInventario();
    } catch (err) {
        alert((err as Error).message);
    }
});

document.getElementById('logoutBtn')?.addEventListener('click', () => {
    localStorage.clear();
    window.location.href = "/";
});

cargarInventario();
