
import { listarAnimales, registrarAnimal, eliminarAnimal, Animal, Filtros } from "./api.js";

const form = document.getElementById("animal-form") as HTMLFormElement;
const tableBody = document.getElementById("animal-table-body") as HTMLTableSectionElement;
const searchInput = document.getElementById("search-input") as HTMLInputElement;

function renderAnimales(animales: Animal[]): void {
  tableBody.innerHTML = "";

  for (const animal of animales) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><span class="font-bold text-gavac-primary">${animal.tag}</span></td>
      <td><span class="font-medium text-slate-600">${animal.nombre ?? "—"}</span></td>
      <td><span class="text-slate-500">${animal.raza ?? "—"}</span></td>
      <td><span class="text-slate-500 capitalize">${animal.sexo ?? "—"}</span></td>
      <td>
        <span class="badge ${animal.status === 'active' ? 'badge-active' : 'badge-alert'}">
          ${animal.status === 'active' ? 'Activo' : animal.status}
        </span>
      </td>
      <td><span class="text-slate-500 font-medium">${animal.lote ?? "—"}</span></td>
      <td>
        <div class="flex gap-2">
            <button class="p-2 hover:bg-slate-100 rounded-lg transition-colors">
                <i data-lucide="edit-2" class="w-4 h-4 text-slate-400"></i>
            </button>
            <button data-id="${animal.id}" class="delete-btn p-2 hover:bg-red-50 rounded-lg transition-colors">
                <i data-lucide="trash-2" class="w-4 h-4 text-red-400"></i>
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
    localStorage.removeItem("gavac_token");
    localStorage.removeItem("gavac_usuario");
    window.location.href = "/login.html";
});

// Carga inicial
cargarAnimales();
