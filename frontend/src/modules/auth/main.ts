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

const btnText = document.getElementById("btnText") as HTMLSpanElement;
const toggleText = document.getElementById("toggleText") as HTMLSpanElement;

let modoRegistro = false;

function mostrarMensaje(texto: string, tipo: "error" | "exito"): void {
    messageBox.textContent = texto;
    messageBox.className = `msg-${tipo === "error" ? "error" : "success"} mt-8`;
    messageBox.classList.remove("hidden");
}

toggleLink.addEventListener("click", (e) => {
    e.preventDefault();
    modoRegistro = !modoRegistro;

    if (formTitle) formTitle.textContent = modoRegistro ? "Crear Perfil" : "Bienvenido";
    if (formSubtitle) formSubtitle.textContent = modoRegistro ? "Únete a la gestión inteligente del agro." : "Ingresa al centro de mando ganadero.";
    if (btnText) btnText.textContent = modoRegistro ? "Finalizar Registro" : "Acceder al Sistema";
    if (toggleText) toggleText.textContent = modoRegistro ? "¿Ya tienes cuenta?" : "¿Nuevo en GAVAC?";
    if (toggleLink) toggleLink.textContent = modoRegistro ? "Inicia sesión" : "Regístrate aquí";

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

    if (!email || !password) {
        mostrarMensaje("Por favor, complete todos los campos.", "error");
        submitBtn.disabled = false;
        return;
    }

    try {
        if (modoRegistro) {
            const nombreOrg = (document.getElementById('org-name-input') as HTMLInputElement)?.value || "";
            await registrar({ email, password, nombre_organizacion: nombreOrg } as any);
            mostrarMensaje("✅ Registro exitoso. Iniciando sesión...", "exito");
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
