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

    formTitle.textContent = modoRegistro ? "Crear Perfil" : "Iniciar Sesión";
    formSubtitle.textContent = modoRegistro ? "Únase a la gestión inteligente del agro." : "Acceda a su ecosistema ganadero inteligente.";
    submitBtn.textContent = modoRegistro ? "Finalizar Registro" : "Entrar al Sistema";
    toggleLink.textContent = modoRegistro ? "Volver al Acceso" : "Registro de usuario";

    roleContainer.classList.toggle("hidden", !modoRegistro);
    messageBox.classList.add("hidden");
    passwordInput.value = "";
});

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageBox.classList.add("hidden");
    submitBtn.disabled = true;

    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const selectedRole = (document.querySelector('input[name="rol"]:checked') as HTMLInputElement)?.value || "operario";

    if (!email || !password) {
        mostrarMensaje("Por favor, complete todos los campos.", "error");
        submitBtn.disabled = false;
        return;
    }

    try {
        if (modoRegistro) {
            console.log("Registrando con rol:", selectedRole);
            await registrar({ email, password, rol: selectedRole as any });
            mostrarMensaje("✅ Cuenta creada con éxito. Iniciando sesión...", "exito");
        }

        const resultado = await login({ email, password });
        localStorage.setItem("gavac_token", resultado.access_token);
        localStorage.setItem("gavac_usuario", JSON.stringify(resultado.usuario));

        setTimeout(() => {
            window.location.href = "/dashboard";
        }, 1000);

    } catch (err: any) {
        console.error("Auth Error:", err);
        mostrarMensaje(err.message || "Error al procesar la solicitud.", "error");
    } finally {
        submitBtn.disabled = false;
    }
});
