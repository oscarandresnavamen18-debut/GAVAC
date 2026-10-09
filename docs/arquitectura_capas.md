# Arquitectura por Capas Estricta Monolítica — GAVAC

Documento técnico presentado para la evaluación del proyecto formativo ADSO — SENA CTMA.

---

## 1. Introducción y Justificación Arquitectónica

GAVAC está construido bajo un patrón de **Monolito con Arquitectura por Capas Estricta (*Strict Layered Monolith*)**. Esta arquitectura organiza el código fuente del sistema en capas horizontales claramente definidas, donde cada capa tiene una única responsabilidad y solo se comunica con la capa inmediatamente inferior.

Este diseño garantiza:
* **Mantenibilidad:** Separación clara entre la interfaz de usuario, la lógica de negocio y el acceso a datos.
* **Escalabilidad:** Facilita la adición de nuevos módulos sin acoplar las consultas a la base de datos con las peticiones HTTP.
* **Soporte Multiplataforma (Web y Móvil):** El backend expone una API REST robusta documentada con OpenAPI (Swagger), diseñada para ser consumida tanto por la aplicación Web (HTML5/TypeScript) como por la aplicación Móvil desarrollada en **Flutter (Dart)**.

---

## 2. Estructura de Capas del Backend (FastAPI / Python)

```text
backend/
├── app/
│   ├── core/              # Configuración central (Base de datos, seguridad, middlewares)
│   ├── models/            # Capa de Dominio / Entidades ORM (SQLAlchemy)
│   ├── schemas/           # Capa de Transferencia de Datos — DTOs (Pydantic)
│   ├── repositories/      # Capa de Acceso a Datos (Consultas SQL / ORM)
│   ├── services/          # Capa de Lógica de Negocio (Reglas del dominio ganadero)
│   ├── api/               # Capa de Presentación (Routers / Controladores REST)
│   └── main.py            # Punto de entrada de la aplicación FastAPI
```

### Descripción de cada Capa:

1. **Capa de Presentación (`api/` o Routers):**
   * Recibe las peticiones HTTP (`GET`, `POST`, `PUT`, `DELETE`).
   * Valida los encabezados (ej. `X-Finca-ID`, Tokens JWT de autenticación).
   * Llama a los servicios correspondientes y retorna las respuestas HTTP y esquemas DTO.

2. **Capa de Lógica de Negocio (`services/`):**
   * Contiene los algoritmos, reglas de negocio ganaderas (cálculos de producción, controles sanitarios, reproducción).
   * Orquesta las transacciones entre repositorios y servicios de auditoría.

3. **Capa de Acceso a Datos (`repositories/`):**
   * Encapsula todas las consultas a la base de datos PostgreSQL alojada en Supabase.
   * Evita que los routers o servicios ejecuten código SQL o métodos ORM directos.

4. **Capa de Dominio y Esquemas (`models/` y `schemas/`):**
   * `models/`: Mapeo objeto-relacional (ORM) de las tablas de la base de datos.
   * `schemas/`: Validación de tipos de datos de entrada y salida mediante Pydantic.

---

## 3. Integración Multiplataforma: Web y Móvil (Flutter / Dart)

Para cumplir con el requerimiento de tener acceso tanto Web como Móvil, el proyecto incluye una estructura cliente para **Flutter (Dart)** ubicada en la carpeta `/mobile`.

### Cliente Móvil (Flutter / Dart)
* **Lenguaje:** **Dart**
* **Framework:** **Flutter**
* **Comunicación:** Consumo de la API REST de GAVAC mediante `http` o `dio` con manejo de tokens JWT y cabecera `X-Finca-ID`.

Estructura propuesta en `/mobile`:
```text
mobile/
├── pubspec.yaml           # Dependencias de Flutter
└── lib/
    ├── main.dart          # Punto de entrada de la app móvil
    ├── models/            # Modelos de datos en Dart (Animal, Finca, etc.)
    ├── services/          # Cliente API REST para conectar con FastAPI
    └── views/             # Pantallas móviles (Login, Dashboard, Inventario)
```
