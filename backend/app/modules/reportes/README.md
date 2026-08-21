# Módulo de Consultas y Reportes (GAVAC)

**Responsable:** Jorge Botero

Este módulo se encarga de procesar la información del inventario ganadero y generar vistas consolidadas para la toma de decisiones. 

## Estructura Profesional del Módulo
- `router.py`: Define los puntos de entrada (API) protegidos por JWT.
- `service.py`: Contiene la lógica de negocio y el registro de auditoría de cada consulta.
- `repository.py`: Ejecuta las consultas SQL optimizadas sobre el modelo central de animales.
- `schemas.py`: Define las estructuras de datos para entrada y salida (Pydantic).

## Integración y Seguridad
El módulo utiliza la seguridad centralizada del proyecto. Cada vez que se genera un reporte, se registra automáticamente en la tabla de auditoría para garantizar la trazabilidad de la información sensible.

Para agregar nuevos reportes, se debe seguir la arquitectura de capas (Router -> Service -> Repository) respetando los modelos definidos por el equipo de base de datos.
