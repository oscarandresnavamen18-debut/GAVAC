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
                <tr>
                    <td class="font-black text-gavac-primary tracking-tight">${f.nombre}</td>
                    <td class="text-slate-500 font-medium">${f.ubicacion ?? "—"}</td>
                    <td class="text-right">
                        <button class="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-slate-400 hover:bg-gavac-primary hover:text-white transition-all shadow-sm">
                            <i data-lucide="edit-3" class="w-4 h-4"></i>
                        </button>
                    </td>
                </tr>
            `).join("");
        }

        // Render Usuarios
        if (usuariosTable) {
            usuariosTable.innerHTML = usuarios.map((u: any) => {
                const roles = u.finca_roles || [];

                return `
                <tr>
                    <td>
                        <p class="font-black text-gavac-primary tracking-tighter text-sm">${u.email}</p>
                        <span class="text-[9px] font-black uppercase text-emerald-600 tracking-widest">${u.rol_organizacion}</span>
                    </td>
                    <td>
                        <div class="flex flex-wrap gap-2">
                            ${roles.length > 0 ? roles.map((r: any) => `
                                <span class="badge-gavac badge-gavac-info !text-[8px]">
                                    ${r.finca_nombre}: ${r.rol}
                                </span>
                            `).join("") : '<span class="text-[10px] text-slate-300 font-bold uppercase tracking-tighter">Sin accesos</span>'}
                        </div>
                    </td>
                    <td class="text-right">
                        <div class="flex justify-end gap-2">
                            <button onclick="window.prepareEditUser(${u.id}, '${u.email}', '${u.rol_organizacion}')" class="w-9 h-9 bg-slate-50 rounded-lg flex items-center justify-center text-slate-400 hover:bg-gavac-primary hover:text-white transition-all shadow-sm">
                                <i data-lucide="user-cog" class="w-4 h-4"></i>
                            </button>
                            <button onclick="window.deleteUser(${u.id})" class="w-9 h-9 bg-red-50 rounded-lg flex items-center justify-center text-red-400 hover:bg-red-500 hover:text-white transition-all shadow-sm">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `}).join("");
        }

        // Populate Selects
        if (userSelect) {
            if (usuarios.length === 0) {
                userSelect.innerHTML = `<option value="" disabled selected>No hay usuarios registrados</option>`;
            } else {
                userSelect.innerHTML = `<option value="" disabled selected>Seleccione un usuario...</option>` +
                    usuarios.map((u: any) => `<option value="${u.id}">${u.email} (${u.rol_organizacion})</option>`).join("");
            }
        }
        if (fincaSelect) {
            if (fincas.length === 0) {
                fincaSelect.innerHTML = `<option value="" disabled selected>No hay fincas registradas</option>`;
            } else {
                fincaSelect.innerHTML = `<option value="" disabled selected>Seleccione una finca...</option>` +
                    fincas.map((f: any) => `<option value="${f.id}">${f.nombre}</option>`).join("");
            }
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

document.getElementById('logoutBtn')?.addEventListener('click', () => {
    localStorage.clear();
    window.location.href = "/";
});

cargarDatos();
