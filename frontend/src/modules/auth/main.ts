import { registrar, login } from "./api.js";

const form = document.getElementById("loginForm") as HTMLFormElement;
const emailInput = document.getElementById("email") as HTMLInputElement;
const passwordInput = document.getElementById("password") as HTMLInputElement;
const submitBtn = document.getElementById("submitBtn") as HTMLButtonElement;
const toggleLink = document.getElementById("toggleMode") as HTMLAnchorElement;
const messageBox = document.getElementById("loginMessage") as HTMLDivElement;

let modoRegistro = false;

// ============================================
// MOSTRAR MENSAJES
// ============================================

function mostrarMensaje(
    texto: string,
    tipo: "error" | "exito"
): void {
    messageBox.textContent = texto;
    messageBox.className = "block mt-6 p-4 rounded-xl font-bold text-center";

    if (tipo === "error") {
        messageBox.classList.add("msg-error");
    } else {
        messageBox.classList.add("msg-success");
    }
}

// ============================================
// CAMBIAR LOGIN / REGISTRO
// ============================================

toggleLink.addEventListener("click", (e) => {
    e.preventDefault();

    modoRegistro = !modoRegistro;

    submitBtn.textContent = modoRegistro
        ? "Registrarme"
        : "Iniciar Sesión";

    toggleLink.textContent = modoRegistro
        ? "¿Ya tienes cuenta? Inicia sesión"
        : "¿No tienes cuenta? Regístrate";

    messageBox.classList.add("hidden");

    passwordInput.value = "";
});

// ============================================
// LOGIN / REGISTRO
// ============================================

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    messageBox.classList.add("hidden");
    submitBtn.disabled = true;

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!email || !password) {
        mostrarMensaje(
            "Debes ingresar email y contraseña.",
            "error"
        );

        submitBtn.disabled = false;
        return;
    }

    try {

        // ========================================
        // REGISTRO
        // ========================================

        if (modoRegistro) {

            console.log("Creando cuenta...");

            await registrar({
                email,
                password,
            });

            mostrarMensaje(
                "✅ Cuenta creada correctamente. Ahora inicia sesión.",
                "exito"
            );

            modoRegistro = false;

            submitBtn.textContent = "Iniciar Sesión";

            toggleLink.textContent =
                "¿No tienes cuenta? Regístrate";

            passwordInput.value = "";

        }

        // ========================================
        // LOGIN
        // ========================================

        else {

            console.log("Iniciando sesión...");

            const resultado = await login({
                email,
                password,
            });

            console.log("Login exitoso.");
            console.log("Usuario:", resultado.usuario);

            // ========================================
            // GUARDAR TOKEN
            // ========================================

            localStorage.setItem(
                "gavac_token",
                resultado.access_token
            );

            // ========================================
            // GUARDAR USUARIO
            // ========================================

            localStorage.setItem(
                "gavac_usuario",
                JSON.stringify(resultado.usuario)
            );

            console.log(
                "Token guardado:",
                localStorage.getItem("gavac_token")
            );

            mostrarMensaje(
                "✅ Sesión iniciada. Redirigiendo...",
                "exito"
            );

            // ========================================
            // REDIRECCIÓN CORRECTA
            // ========================================

            setTimeout(() => {
                // Redirigimos al Dashboard Central de Roles
                window.location.href = "/dashboard";
            }, 800);
        }

    } catch (err: unknown) {

        console.error("Error:", err);

        const mensaje =
            err instanceof Error
                ? err.message
                : "Ocurrió un error inesperado.";

        mostrarMensaje(
            `⚠️ ${mensaje}`,
            "error"
        );

    } finally {

        submitBtn.disabled = false;
    }
});
