
import { listarAnimales, registrarAnimal, eliminarAnimal, Animal, Filtros } from "./api.js";

const form = document.getElementById("animal-form") as HTMLFormElement;
const tableBody = document.getElementById("animal-table-body") as HTMLTableSectionElement;
const searchInput = document.getElementById("search-input") as HTMLInputElement;

function renderAnimales(animales: Animal[]): void {
  tableBody.innerHTML = "";

  for (const animal of animales) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="font-black text-gavac-primary tracking-tight">${animal.tag}</td>
      <td class="font-bold text-slate-600">${animal.nombre ?? "—"}</td>
      <td class="text-slate-500 font-medium">${animal.raza ?? "—"}</td>
      <td class="text-slate-500 capitalize font-medium">${animal.sexo ?? "—"}</td>
      <td>
        <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
            <span class="text-xs font-black text-slate-400 uppercase tracking-widest">${animal.lote ?? "Sin Lote"}</span>
        </div>
      </td>
      <td>
        <span class="badge-gavac ${animal.status === 'active' ? 'badge-gavac-success' : 'badge-gavac-warning'}">
          ${animal.status === 'active' ? 'Activo' : animal.status}
        </span>
      </td>
      <td class="text-right">
        <div class="flex justify-end gap-3">
            <button class="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-slate-400 hover:bg-gavac-primary hover:text-white transition-all shadow-sm">
                <i data-lucide="eye" class="w-4 h-4"></i>
            </button>
            <button data-id="${animal.id}" class="delete-btn w-10 h-10 bg-red-50 rounded-xl flex items-center justify-center text-red-400 hover:bg-red-500 hover:text-white transition-all shadow-sm">
                <i data-lucide="trash-2" class="w-4 h-4"></i>
            </button>
        </div>
      </td>
    `;
    tableBody.appendChild(tr);
  }

  // @ts-ignore
  if (window.lucide) { window.lucide.createIcons(); }

  document.querySelectorAll<HTMLButtonElement>(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = Number(btn.dataset.id);
      if (!confirm("¿Eliminar este animal?")) return;
      try {
        await eliminarAnimal(id);
        await cargarAnimales();
      } catch (err) {
        alert((err as Error).message);
      }
    });
  });
}

async function cargarAnimales(filtros: Filtros = {}): Promise<void> {
  try {
    const animales = await listarAnimales(filtros);
    renderAnimales(animales);
    document.getElementById("empty-state")?.classList.toggle("hidden", animales.length > 0);
  } catch (err) {
    console.error("Error al cargar animales:", err);
    alert(`Error: ${(err as Error).message || "No se pudo conectar con el servidor"}`);
  }
}

searchInput?.addEventListener("input", () => {
    cargarAnimales({ tag: searchInput.value.trim() });
});

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const animalData = {
    tag: String(formData.get("tag") ?? "").trim(),
    nombre: String(formData.get("nombre") ?? "").trim() || undefined,
    especie: String(formData.get("especie") ?? "Bovino"),
    raza: String(formData.get("raza") ?? "").trim() || undefined,
    sexo: (String(formData.get("sexo") ?? "").trim() || undefined) as any,
    peso_actual: formData.get("peso_actual") ? Number(formData.get("peso_actual")) : undefined,
    edad_meses: formData.get("edad_meses") ? Number(formData.get("edad_meses")) : undefined,
    lote: String(formData.get("lote") ?? "").trim() || undefined,
  };

  try {
    await registrarAnimal(animalData);
    alert("¡Animal registrado con éxito!");
    form.reset();
    document.getElementById('animal-modal')?.classList.add('hidden');
    await cargarAnimales();
  } catch (err) {
    console.error("Error en registro:", err);
    alert((err as Error).message);
  }
});

// Botón de salir
document.getElementById('logoutBtn')?.addEventListener('click', () => {
    localStorage.clear();
    window.location.href = "/";
});

// Carga inicial
cargarAnimales();
