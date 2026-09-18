-- =====================================================================
-- GAVAC - Esquema de base de datos (PostgreSQL / Supabase)
-- Arquitectura SaaS Multi-tenant
-- =====================================================================

-- 1. Módulo SaaS: Organizaciones (Clientes)
CREATE TABLE IF NOT EXISTS organizaciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    nit VARCHAR(50) UNIQUE NULL,
    plan_contratado VARCHAR(50) DEFAULT 'basic',
    estado VARCHAR(20) DEFAULT 'activa', -- activa, suspendida, cancelada
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Usuarios vinculados a una Organización
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol_organizacion VARCHAR(20) DEFAULT 'operario',
    organizacion_id INT REFERENCES organizaciones(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Fincas vinculadas a una Organización
CREATE TABLE IF NOT EXISTS fincas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ubicacion VARCHAR(255) NULL,
    area_hectareas DECIMAL(10,2) NULL,
    estado VARCHAR(20) DEFAULT 'Activa',
    organizacion_id INT REFERENCES organizaciones(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Roles dinámicos por Finca (Contextuales)
CREATE TABLE IF NOT EXISTS usuario_finca_roles (
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    finca_id INT REFERENCES fincas(id) ON DELETE CASCADE,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('admin', 'ganadero', 'mayordomo', 'veterinario', 'operario')),
    PRIMARY KEY (usuario_id, finca_id)
);

-- 5. Lotes / Potreros dentro de una Finca
CREATE TABLE IF NOT EXISTS lotes (
    id SERIAL PRIMARY KEY,
    finca_id INT REFERENCES fincas(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    area_hectareas DECIMAL(10,2) NULL,
    descripcion TEXT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Módulo: cattle / ganado
CREATE TABLE IF NOT EXISTS animales (
    id SERIAL PRIMARY KEY,
    tag VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NULL,
    especie VARCHAR(50) DEFAULT 'Bovino',
    raza VARCHAR(50) NULL,
    sexo VARCHAR(10) CHECK (sexo IN ('macho', 'hembra')),
    peso_actual DECIMAL(10,2) NULL,
    edad_meses INT NULL,
    finca_id INT REFERENCES fincas(id) ON DELETE SET NULL,
    lote_id INT REFERENCES lotes(id) ON DELETE SET NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Trazabilidad: Historial de movimientos
CREATE TABLE IF NOT EXISTS traslados_animales (
    id SERIAL PRIMARY KEY,
    animal_id INT REFERENCES animales(id) ON DELETE CASCADE,
    origen_finca_id INT REFERENCES fincas(id),
    destino_finca_id INT REFERENCES fincas(id),
    origen_lote_id INT REFERENCES lotes(id),
    destino_lote_id INT REFERENCES lotes(id),
    motivo TEXT,
    usuario_responsable_id INT REFERENCES usuarios(id),
    fecha_traslado TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Módulo: sanidad
CREATE TABLE IF NOT EXISTS sanidad (
    id SERIAL PRIMARY KEY,
    animal_id INT REFERENCES animales(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    producto VARCHAR(100) NOT NULL,
    dosis VARCHAR(50) NULL,
    fecha_aplicacion DATE DEFAULT CURRENT_DATE,
    proxima_fecha DATE NULL,
    estado VARCHAR(20) DEFAULT 'Completada',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. Módulo: reproduccion
CREATE TABLE IF NOT EXISTS reproduccion (
    id SERIAL PRIMARY KEY,
    animal_id INT REFERENCES animales(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    fecha_evento DATE NOT NULL,
    estado VARCHAR(50) DEFAULT 'En proceso',
    observaciones TEXT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Módulo: inventario_insumos
CREATE TABLE IF NOT EXISTS inventario_insumos (
    id SERIAL PRIMARY KEY,
    finca_id INT REFERENCES fincas(id) ON DELETE CASCADE,
    nombre VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL DEFAULT 0,
    unidad VARCHAR(20) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Disponible',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. Auditoría Centralizada
CREATE TABLE IF NOT EXISTS logs_auditoria (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE SET NULL,
    organizacion_id INT REFERENCES organizaciones(id) ON DELETE SET NULL,
    email VARCHAR(255) NULL,
    accion VARCHAR(100) NOT NULL,
    detalles TEXT NULL,
    ip_address VARCHAR(50) NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
