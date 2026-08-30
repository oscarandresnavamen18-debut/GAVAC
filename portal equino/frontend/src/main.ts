import './style.css'

const app = document.querySelector<HTMLDivElement>('#app')!

// Estado Global de la App
const state = {
  isLoggedIn: false,
  token: '',
  usuario: { correo: '', rol: '' }
}

// --- VISTAS (RENDERIZADO) ---

const renderLogin = () => {
  app.innerHTML = `
    <div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-2xl shadow-2xl border border-gray-100">
        <div>
          <div class="flex justify-center">
            <span class="text-5xl">🐎</span>
          </div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 tracking-tight">
            Portal Equino
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Base Sólida: Inicie sesión para gestionar el ganado
          </p>
        </div>

        <form id="login-form" class="mt-8 space-y-6">
          <div class="rounded-md shadow-sm -space-y-px">
            <div class="mb-4">
              <label for="email-address" class="block text-xs font-bold text-gray-500 uppercase mb-1">Correo Electrónico</label>
              <input id="email-address" name="email" type="email" required
                class="appearance-none rounded-lg relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
                placeholder="usuario@equino.com">
            </div>
            <div>
              <label for="password" class="block text-xs font-bold text-gray-500 uppercase mb-1">Contraseña</label>
              <input id="password" name="password" type="password" required
                class="appearance-none rounded-lg relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
                placeholder="••••••••">
            </div>
          </div>

          <div id="login-error" class="text-red-500 text-xs text-center hidden font-medium"></div>

          <div>
            <button type="submit" id="btn-login"
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-lg text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all active:scale-[0.98] shadow-lg">
              <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                <svg class="h-5 w-5 text-green-500 group-hover:text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                </svg>
              </span>
              ENTRAR AL SISTEMA
            </button>
          </div>
        </form>

        <div class="text-center">
          <p class="text-xs text-gray-400">Auditoría Habilitada ● Conexión Segura Supabase</p>
        </div>
      </div>
    </div>
  `
  setupLoginListeners()
}

const renderDashboard = () => {
  app.innerHTML = `
    <div class="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div class="max-w-5xl mx-auto">
        <div class="bg-white shadow-xl rounded-2xl overflow-hidden border border-gray-200">
          <div class="bg-green-800 px-6 py-4 flex justify-between items-center shadow-md">
            <div class="flex items-center gap-3">
              <span class="text-2xl">🐎</span>
              <div>
                <h1 class="text-xl font-bold text-white tracking-tight">Portal Equino</h1>
                <p class="text-green-200 text-[10px] uppercase font-bold tracking-widest">Dashboard de Control Profesional</p>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <div class="text-right">
                <p class="text-white text-xs font-bold">${state.usuario.correo}</p>
                <p class="text-green-300 text-[9px] uppercase font-black">${state.usuario.rol}</p>
              </div>
              <button id="btn-logout" class="bg-red-500/20 hover:bg-red-500 text-red-200 hover:text-white p-2 rounded-lg transition-all border border-red-500/30">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </div>

          <div class="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Sidebar / Stats -->
            <div class="space-y-6">
              <div class="bg-green-50 p-4 rounded-xl border border-green-100">
                <h3 class="text-xs font-bold text-green-800 uppercase mb-3">Servidor</h3>
                <div class="flex items-center justify-between">
                  <button id="btn-test" class="bg-green-600 text-white text-[10px] px-3 py-1.5 rounded-full font-bold shadow-sm hover:bg-green-700 transition">Verificar</button>
                  <div id="status" class="text-[10px] font-bold text-green-600"></div>
                </div>
              </div>

              <div class="bg-blue-50 p-4 rounded-xl border border-blue-100">
                <h3 class="text-xs font-bold text-blue-800 uppercase mb-3">Seguridad JWT</h3>
                <p class="text-[10px] text-blue-600 break-all font-mono leading-tight bg-white p-2 rounded border border-blue-200 shadow-inner">
                  ${state.token.substring(0, 50)}...
                </p>
              </div>
            </div>

            <!-- Main Content: Módulo Oscar -->
            <div class="md:col-span-2 bg-gray-50 p-6 rounded-2xl border border-gray-200 shadow-inner">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                  🐄 Gestión de Ganado (Oscar)
                </h2>
                <span class="bg-green-600 text-white text-[9px] px-2 py-0.5 rounded-full font-black animate-pulse">LIVE</span>
              </div>

              <div class="space-y-6">
                <!-- Formulario -->
                <div class="grid grid-cols-2 gap-4">
                  <div class="col-span-1">
                    <label class="block text-[10px] font-bold text-gray-400 mb-1">NOMBRE ANIMAL</label>
                    <input type="text" id="nombre" class="w-full border-2 border-gray-200 rounded-lg px-3 py-2 text-sm focus:border-green-500 outline-none transition" />
                  </div>
                  <div class="col-span-1">
                    <label class="block text-[10px] font-bold text-gray-400 mb-1">TIPO / RAZA</label>
                    <select id="tipo" class="w-full border-2 border-gray-200 rounded-lg px-3 py-2 text-sm focus:border-green-500 outline-none transition bg-white cursor-pointer">
                      <option value="" disabled selected>Seleccione...</option>
                      <option value="Equino">🐎 Equino</option>
                      <option value="Vacuno">🐄 Vacuno</option>
                      <option value="Ovino">🐑 Ovino</option>
                      <option value="Porcino">🐖 Porcino</option>
                      <option value="Caprino">🐐 Caprino</option>
                    </select>
                  </div>
                  <button id="btn-registrar" class="col-span-2 bg-green-700 text-white py-3 rounded-xl font-bold text-sm shadow-md hover:bg-green-800 transition-all active:scale-[0.98]">
                    REGISTRAR ANIMAL EN NUBE
                  </button>
                </div>

                <!-- Consola -->
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Base de Datos - Salida</label>
                    <button id="btn-listar" class="text-green-600 font-bold text-[10px] hover:underline">RECARGAR LISTA</button>
                  </div>
                  <div id="ganado-list" class="bg-gray-900 text-green-400 p-4 rounded-xl text-[10px] font-mono h-48 overflow-auto shadow-2xl border border-gray-700 custom-scrollbar">
                    // Sistema listo. Esperando consulta...
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-gray-100 px-6 py-2 text-center">
             <p class="text-[9px] text-gray-400 uppercase font-black tracking-tighter">Jorge Security | Oscar Ganado | Juan Auth | Elian Frontend</p>
          </div>
        </div>
      </div>
    </div>
  `
  setupDashboardListeners()
}

// --- LÓGICA DE EVENTOS ---

const logger = (msg: string, type: 'info' | 'error' | 'success' = 'info') => {
  const el = document.querySelector('#ganado-list')!
  const colors = { info: 'text-blue-400', error: 'text-red-400', success: 'text-green-400' }
  const timestamp = new Date().toLocaleTimeString()
  el.innerHTML = `<div class="${colors[type]} mb-1 font-bold">[${timestamp}] ${msg}</div>` + el.innerHTML
}

const setupLoginListeners = () => {
  const form = document.querySelector('#login-form') as HTMLFormElement
  const errorEl = document.querySelector('#login-error')!

  form.addEventListener('submit', async (e) => {
    e.preventDefault()
    const correo = (document.querySelector('#email-address') as HTMLInputElement).value
    const clave = (document.querySelector('#password') as HTMLInputElement).value
    const btn = document.querySelector('#btn-login') as HTMLButtonElement

    btn.disabled = true
    btn.innerHTML = 'VALIDANDO CREDENCIALES...'
    errorEl.classList.add('hidden')

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo, clave })
      })

      const data = await res.json()

      if (res.ok) {
        state.isLoggedIn = true
        state.token = data.token
        // Decodificar payload básico del token para la UI (simulado aquí)
        state.usuario = { correo, rol: correo.includes('admin') ? 'ADMIN' : 'USUARIO' }
        renderDashboard()
      } else {
        errorEl.innerText = data.error || 'Credenciales incorrectas'
        errorEl.classList.remove('hidden')
        btn.disabled = false
        btn.innerHTML = 'ENTRAR AL SISTEMA'
      }
    } catch (err) {
      errorEl.innerText = 'Error: El servidor no responde'
      errorEl.classList.remove('hidden')
      btn.disabled = false
      btn.innerHTML = 'ENTRAR AL SISTEMA'
    }
  })
}

const setupDashboardListeners = () => {
  document.querySelector('#btn-logout')?.addEventListener('click', () => {
    state.isLoggedIn = false
    state.token = ''
    renderLogin()
  })

  document.querySelector('#btn-test')?.addEventListener('click', async () => {
    const status = document.querySelector('#status')!
    status.innerHTML = '...'
    try {
      const res = await fetch('/api');
      const text = await res.text();
      status.innerHTML = `ONLINE`;
    } catch (err) {
      status.innerHTML = 'OFFLINE';
    }
  })

  document.querySelector('#btn-listar')?.addEventListener('click', async () => {
    logger("Consultando Supabase (RBAC Activo)...", "info")
    try {
      const res = await fetch('/api/ganado', {
        headers: { 'Authorization': `Bearer ${state.token}` }
      });
      const data = await res.json();
      if (res.ok) logger("ÉXITO: Datos recuperados.\n" + JSON.stringify(data, null, 2), "success")
      else logger("ERROR: " + (data.error || 'Fallo de acceso'), "error")
    } catch (err) { logger("ERROR DE RED", "error") }
  })

  document.querySelector('#btn-registrar')?.addEventListener('click', async () => {
    const nombre = (document.querySelector('#nombre') as HTMLInputElement).value
    const tipo = (document.querySelector('#tipo') as HTMLInputElement).value
    if (!nombre || !tipo) return alert("Campos vacíos")

    logger(`Registrando "${nombre}"...`, "info")
    try {
      const res = await fetch('/api/ganado/registrar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.token}`
        },
        body: JSON.stringify({ nombre, tipo, peso: 0 })
      });
      const data = await res.json();
      if (res.ok) logger("REGISTRADO Y AUDITADO", "success")
      else logger("ERROR: " + data.error, "error")
    } catch (err) { logger("ERROR CRÍTICO", "error") }
  })
}

// Inicio
renderLogin()
