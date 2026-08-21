import { ApiError, getReports, type Report } from "./api.js";
import express from "express";
import cors from "cors";
import helmet from "helmet";
import dotenv from "dotenv";


const TOKEN_STORAGE_KEY = "access_token";

function setVisible(selector: string, visible: boolean): void {
  const element = document.querySelector<HTMLElement>(selector);
  if (element) {
    element.hidden = !visible;
  }
}

function showError(message: string): void {
  const errorElement = document.querySelector<HTMLElement>("[data-reportes-error]");
  if (errorElement) {
    errorElement.textContent = message;
  }
  setVisible("[data-reportes-error]", true);
}

function renderReports(reports: Report[]): void {
  const tableBody = document.querySelector<HTMLTableSectionElement>(
    "[data-reportes-table-body]",
  );
  if (!tableBody) {
    return;
  }

  tableBody.replaceChildren();
  const dateFormatter = new Intl.DateTimeFormat("es-CO", {
    dateStyle: "medium",
    timeStyle: "short",
  });

  for (const report of reports) {
    const row = document.createElement("tr");
    const id = document.createElement("td");
    const name = document.createElement("td");
    const createdAt = document.createElement("td");

    id.textContent = String(report.id);
    name.textContent = report.name;
    const date = new Date(report.created_at);
    createdAt.textContent = Number.isNaN(date.valueOf())
      ? report.created_at
      : dateFormatter.format(date);

    row.append(id, name, createdAt);
    tableBody.append(row);
  }
}

async function loadReports(): Promise<void> {
  setVisible("[data-reportes-loading]", true);
  setVisible("[data-reportes-error]", false);
  setVisible("[data-reportes-empty]", false);

  try {
    const reports = await getReports(localStorage.getItem(TOKEN_STORAGE_KEY) ?? "");
    renderReports(reports);
    setVisible("[data-reportes-empty]", reports.length === 0);
  } catch (error: unknown) {
    const message = error instanceof ApiError && error.status === 401
      ? "Tu sesión venció o no es válida. Inicia sesión nuevamente."
      : error instanceof Error
        ? error.message
        : "Ocurrió un error inesperado al cargar los reportes.";
    showError(message);
  } finally {
    setVisible("[data-reportes-loading]", false);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  void loadReports();
});
