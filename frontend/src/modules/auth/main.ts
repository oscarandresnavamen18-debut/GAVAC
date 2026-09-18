import { registrar, login } from "./api.js";

const form = document.getElementById("loginForm") as HTMLFormElement;
const emailInput = document.getElementById("email") as HTMLInputElement;
const passwordInput = document.getElementById("password") as HTMLInputElement;
const submitBtn = document.getElementById("submitBtn") as HTMLButtonElement;
const toggleLink = document.getElementById("toggleMode") as HTMLAnchorElement;
const messageBox = document.getElementById("loginMessage") as HTMLDivElement;
const roleContainer = document.getElementById("roleSelectorContainer") as HTMLDivElement;
const formTitle = document.getElementById("form-title") as HTMLHeadingElement;
const formSubtitle = document.getElementById("form-subtitle") as HTMLParagraphElement;

let modoRegistro = false;

function mostrarMensaje(texto: string, tipo: "error" | "exito"): void {
    messageBox.textContent = texto;
    messageBox.className = `block mt-8 p-5 rounded-2xl font-bold text-center text-sm shadow-sm transition-all ${tipo === "error" ? "msg-error" : "msg-success"}`;
    messageBox.classList.remove("hidden");
}

toggleLink.addEventListener("click", (e) => {
    e.preventDefault();
    modoRegistro = !modoRegistro;

    if (formTitle) formTitle.textContent = modoRegistro ? "Crear Perfil" : "Iniciar Sesión";
    if (formSubtitle) formSubtitle.textContent = modoRegistro ? "Únase a la gestión inteligente del agro." : "Introduce tus credenciales para acceder al centro de mando.";
    if (submitBtn) submitBtn.textContent = modoRegistro ? "Finalizar Registro" : "Ingresar al Sistema";
    if (toggleLink) toggleLink.textContent = modoRegistro ? "¿Ya tienes cuenta? Inicia sesión" : "¿No tienes cuenta? Regístrate aquí";

    roleContainer?.classList.toggle("hidden", !modoRegistro);
    messageBox?.classList.add("hidden");
    passwordInput.value = "";
});

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageBox.classList.add("hidden");
    submitBtn.disabled = true;

    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const selectedRole = (document.getElementById('selected-rol-input') as HTMLInputElement)?.value || "operario";

    if (!email || !password) {
        mostrarMensaje("Por favor, complete todos los campos.", "error");
        submitBtn.disabled = false;
        return;
    }

    try {
        if (modoRegistro) {
<<<<<<< HEAD
            const nombreOrg = (document.getElementById('org-name-input') as HTMLInputElement)?.value || "";
            await registrar({ email, password, nombre_organizacion: nombreOrg } as any);
            mostrarMensaje("✅ Registro exitoso. Iniciando sesión...", "exito");
=======
            console.log("Registrando con rol:", selectedRole);
            await registrar({ email, password, rol: selectedRole as any });
            mostrarMensaje("Cuenta creada con éxito. Iniciando sesión...", "exito");
>>>>>>> a583192508a8de8f5f8a80617669f41a01d080f0
        }

        const resultado = await login({ email, password });
        localStorage.setItem("gavac_token", resultado.access_token);
        localStorage.setItem("gavac_usuario", JSON.stringify(resultado.usuario));

        setTimeout(() => {
            window.location.href = "/fincas.html";
        }, 1000);

    } catch (err: any) {
        console.error("DEBUG AUTH ERROR:", {
            mensaje: err.message,
            stack: err.stack,
            error: err
        });
        mostrarMensaje(err.message || "Error al procesar la solicitud.", "error");
    } finally {
        submitBtn.disabled = false;
    }
});
