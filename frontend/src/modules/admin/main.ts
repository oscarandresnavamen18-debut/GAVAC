import { listarFincas, crearFinca, listarUsuarios, asignarRolFinca, crearUsuarioAdmin, actualizarUsuarioAdmin, eliminarUsuarioAdmin } from "./api.js";

const fincasTable = document.getElementById("fincas-table-body");
const usuariosTable = document.getElementById("usuarios-table-body");
const fincaForm = document.getElementById("finca-form") as HTMLFormElement;
const userForm = document.getElementById("user-form") as HTMLFormElement;
const assignForm = document.getElementById("assign-form") as HTMLFormElement;
const userSelect = document.getElementById("assign-user-select") as HTMLSelectElement;
const fincaSelect = document.getElementById("assign-finca-select") as HTMLSelectElement;

async function cargarDatos() {
    try {
        const fincas = await listarFincas();
        const usuarios = await listarUsuarios();

        // Render Fincas
        if (fincasTable) {
            fincasTable.innerHTML = fincas.map((f: any) => `
                <tr class="border-b border-slate-50">
                    <td class="px-6 py-4 font-bold">${f.nombre}</td>
                    <td class="px-6 py-4 text-slate-500">${f.ubicacion ?? "—"}</td>
                    <td class="px-6 py-4 text-right">
                        <button class="text-gavac-primary font-bold text-xs uppercase hover:underline">Gestionar</button>
                    </td>
                </tr>
            `).join("");
        }

        // Render Usuarios
        if (usuariosTable) {
            usuariosTable.innerHTML = usuarios.map((u: any) => {
                const roles = u.finca_roles || [];

                return `
                <tr class="border-b border-slate-50">
                    <td class="px-6 py-4">
                        <p class="font-bold">${u.email}</p>
                        <span class="text-[10px] font-black uppercase text-slate-400">Rol Base: ${u.rol_organizacion}</span>
                    </td>
                    <td class="px-6 py-4">
                        <div class="flex flex-wrap gap-2">
                            ${roles.length > 0 ? roles.map((r: any) => `
                                <span class="px-3 py-1 rounded-full text-[10px] font-bold bg-slate-50 text-slate-600 border border-slate-100">
                                    ${r.finca_nombre}: ${r.rol.toUpperCase()}
                                </span>
                            `).join("") : '<span class="text-xs text-slate-400 italic">Sin fincas asignadas</span>'}
                        </div>
                    </td>
                    <td class="px-6 py-4 text-right">
                        <div class="flex justify-end gap-3">
                            <button onclick="window.prepareEditUser(${u.id}, '${u.email}', '${u.rol_organizacion}')" class="text-slate-400 hover:text-gavac-primary">
                                <i data-lucide="edit-3" class="w-4 h-4"></i>
                            </button>
                            <button onclick="window.deleteUser(${u.id})" class="text-slate-400 hover:text-red-500">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `}).join("");
        }

        // Populate Selects
        if (userSelect) {
            userSelect.innerHTML = usuarios.map((u: any) => `<option value="${u.id}">${u.email}</option>`).join("");
        }
        if (fincaSelect) {
            fincaSelect.innerHTML = fincas.map((f: any) => `<option value="${f.id}">${f.nombre}</option>`).join("");
        }

        // @ts-ignore
        if (window.lucide) { window.lucide.createIcons(); }

    } catch (e) {
        console.error(e);
    }
}

fincaForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(fincaForm);
    await crearFinca({
        nombre: formData.get("nombre"),
        ubicacion: formData.get("ubicacion")
    });
    fincaForm.reset();
    document.getElementById('finca-modal')?.classList.add('hidden');
    cargarDatos();
});

assignForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(assignForm);
    try {
        await asignarRolFinca({
            usuario_id: Number(formData.get("usuario_id")),
            finca_id: Number(formData.get("finca_id")),
            rol: String(formData.get("rol"))
        });
        assignForm.reset();
        document.getElementById('assign-modal')?.classList.add('hidden');
        cargarDatos();
    } catch (e: any) {
        alert("Error al asignar rol");
    }
});

userForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(userForm);
    const userId = formData.get("id");
    const email = formData.get("email") as string;
    const rol = formData.get("rol") as string;
    const password = formData.get("password") as string;

    try {
        if (userId) {
            await actualizarUsuarioAdmin(Number(userId), { email, rol });
        } else {
            await crearUsuarioAdmin({ email, password, rol });
        }
        userForm.reset();
        document.getElementById('user-modal')?.classList.add('hidden');
        cargarDatos();
    } catch (e: any) {
        alert(e.message || "Error al procesar usuario");
    }
});

// @ts-ignore
window.prepareEditUser = (id: number, email: string, rol: string) => {
    const modalTitle = document.getElementById('user-modal-title');
    const editIdInput = document.getElementById('edit-user-id') as HTMLInputElement;
    const emailInput = document.getElementById('user-email') as HTMLInputElement;
    const rolSelect = document.getElementById('user-rol') as HTMLSelectElement;
    const passField = document.getElementById('password-field');

    if (modalTitle) modalTitle.textContent = "Editar Usuario";
    if (editIdInput) editIdInput.value = String(id);
    if (emailInput) emailInput.value = email;
    if (rolSelect) rolSelect.value = rol;
    if (passField) passField.classList.add('hidden');

    document.getElementById('user-modal')?.classList.remove('hidden');
};

// @ts-ignore
window.deleteUser = async (id: number) => {
    if (confirm("¿Estás seguro de eliminar este usuario? Perderá todo acceso a la organización.")) {
        try {
            await eliminarUsuarioAdmin(id);
            cargarDatos();
        } catch (e: any) {
            alert(e.message || "Error al eliminar");
        }
    }
};

cargarDatos();
