-- =====================================================================
-- GAVAC - Esquema de base de datos (PostgreSQL / Supabase)
-- Encargado: Elian Martinez
--
-- Este archivo documenta las tablas que existen actualmente en Supabase.
-- SQLAlchemy las crea automáticamente, pero este SQL sirve para referencia.
-- =====================================================================

-- Módulo: auth (Usuarios y Auditoría)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'operario' CHECK (rol IN ('admin', 'operario')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS logs_auditoria (
    id SERIAL PRIMARY KEY,
    usuario_id INT,
    email VARCHAR(255),
    accion VARCHAR(255) NOT NULL,
    detalles TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Módulo: cattle / ganado (Gestión de Animales)
CREATE TABLE IF NOT EXISTS animales (
    id SERIAL PRIMARY KEY,
    tag VARCHAR(50) NOT NULL UNIQUE,
    birth_date DATE NULL,
    sex VARCHAR(10) NULL,
    breed VARCHAR(50) NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Módulo: reportes
CREATE TABLE IF NOT EXISTS reportes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
