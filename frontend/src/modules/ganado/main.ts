// Lógica de interfaz: maneja el formulario, la tabla y los filtros,
// llamando a las funciones de api.ts.

import express from "express";
import cors from "cors";
import helmet from "helmet";
import dotenv from "dotenv";
import { listarAnimales, registrarAnimal, eliminarAnimal, Animal, Filtros, checkApiHealth } from "./api.js";

const form = document.getElementById("animal-form") as HTMLFormElement;
const formError = document.getElementById("form-error") as HTMLParagraphElement;
const tableBody = document.getElementById("animal-table-body") as HTMLTableSectionElement;
const emptyState = document.getElementById("empty-state") as HTMLDivElement;

const filterTagInput = document.getElementById("filter-tag") as HTMLInputElement;
const filterBreedInput = document.getElementById("filter-breed") as HTMLInputElement;
const filterBtn = document.getElementById("filter-btn") as HTMLButtonElement;
const clearFilterBtn = document.getElementById("clear-filter-btn") as HTMLButtonElement;

const statusDot = document.getElementById("api-status-dot") as HTMLSpanElement;
const statusText = document.getElementById("api-status-text") as HTMLSpanElement;

async function actualizarEstadoApi(): Promise<void> {
  try {
    const health = await checkApiHealth();
    statusDot.className = "w-2 h-2 rounded-full bg-emerald-500";
    statusText.textContent = `API: Conectada (${health.database})`;
    statusText.classList.replace("text-slate-500", "text-emerald-700");
  } catch (err) {
    statusDot.className = "w-2 h-2 rounded-full bg-red-500";
    statusText.textContent = "API: Desconectada";
    statusText.classList.replace("text-slate-500", "text-red-700");
  }
}

function renderAnimales(animales: Animal[]): void {
  tableBody.innerHTML = "";
  emptyState.classList.toggle("hidden", animales.length > 0);

  for (const animal of animales) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="px-4 py-3 font-medium text-slate-800">${animal.tag}</td>
      <td class="px-4 py-3 text-slate-600">${animal.breed ?? "—"}</td>
      <td class="px-4 py-3 text-slate-600">${animal.sex ?? "—"}</td>
      <td class="px-4 py-3 text-slate-600">${animal.birth_date ?? "—"}</td>
      <td class="px-4 py-3">
        <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-100 font-medium">${animal.status}</span>
      </td>
      <td class="px-4 py-3">
        <button data-id="${animal.id}" class="delete-btn text-red-600 hover:text-red-700 hover:underline text-xs font-medium">Eliminar</button>
      </td>
    `;
    tableBody.appendChild(tr);
  }

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
  console.log("Cargando animales con filtros:", filtros);
  try {
    const animales = await listarAnimales(filtros);
    console.log("Animales recibidos:", animales);
    renderAnimales(animales);
  } catch (err) {
    console.error("Error al cargar animales:", err);
    formError.textContent = "Error al conectar con la API. Verifica que el backend esté corriendo.";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formError.textContent = "";
  console.log("Intentando registrar animal...");

  const formData = new FormData(form);
  const tag = String(formData.get("tag") ?? "").trim();
  const breed = String(formData.get("breed") ?? "").trim();
  const sex = String(formData.get("sex") ?? "").trim();
  const birthDate = String(formData.get("birth_date") ?? "").trim();

  const animalData = {
    tag,
    breed: breed || undefined,
    sex: (sex || undefined) as any,
    birth_date: birthDate || undefined,
  };

  console.log("Enviando datos:", animalData);

  try {
    const nuevoAnimal = await registrarAnimal(animalData);
    console.log("Registro exitoso:", nuevoAnimal);
    alert("¡Animal registrado con éxito!");
    form.reset();
    await cargarAnimales();
  } catch (err) {
    console.error("Error en registro:", err);
    formError.textContent = (err as Error).message;
  }
});

filterBtn.addEventListener("click", () => {
  cargarAnimales({
    tag: filterTagInput.value.trim() || undefined,
    breed: filterBreedInput.value.trim() || undefined,
  });
});

clearFilterBtn.addEventListener("click", () => {
  filterTagInput.value = "";
  filterBreedInput.value = "";
  cargarAnimales();
});

// Carga inicial
actualizarEstadoApi();
cargarAnimales();
