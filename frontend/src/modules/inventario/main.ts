
import { listarInventario, registrarInventario, InventarioInsumo } from "./api.js";

const tableBody = document.getElementById("inventario-table-body") as HTMLTableSectionElement;
const form = document.getElementById("inventario-form") as HTMLFormElement;

function renderInventario(registros: InventarioInsumo[]): void {
    tableBody.innerHTML = "";
    for (const reg of registros) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><span class="font-bold text-gavac-primary">${reg.nombre}</span></td>
            <td><span class="text-slate-500">${reg.categoria}</span></td>
            <td><span class="font-bold text-slate-700">${reg.cantidad}</span></td>
            <td><span class="text-slate-500 font-medium">${reg.unidad}</span></td>
            <td>
                <span class="badge ${reg.cantidad > 10 ? 'badge-available' : 'badge-low'}">
                    ${reg.cantidad > 10 ? 'Disponible' : 'Bajo Stock'}
                </span>
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
    localStorage.removeItem("gavac_token");
    localStorage.removeItem("gavac_usuario");
    window.location.href = "/login.html";
});

cargarInventario();
