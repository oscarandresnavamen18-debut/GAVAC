import { Router } from 'express';
import pool from '../../lib/db';
import { validarJWT } from '../../middlewares/jwt.middleware';

const router = Router();

/**
 * @route   GET /api/ganado
 * @desc    Obtener lista completa de ganado
 * @access  Privado
 */
router.get('/', validarJWT, async (req, res) => {
    try {
        const result = await pool.query("SELECT * FROM ganado ORDER BY id DESC");
        res.json(result.rows);
    } catch (err: any) {
        res.status(500).json({ error: "Error al obtener ganado", detalle: err.message });
    }
});

/**
 * @route   POST /api/ganado/registrar
 * @desc    Registrar un nuevo animal
 * @access  Privado
 */
router.post('/registrar', validarJWT, async (req, res) => {
    const { nombre, tipo, peso } = req.body;

    if (!nombre || !tipo || peso === undefined) {
        return res.status(400).json({ error: "Todos los campos son obligatorios" });
    }

    const sql = 'INSERT INTO ganado (nombre, tipo, peso) VALUES ($1, $2, $3) RETURNING *';

    try {
        const result = await pool.query(sql, [nombre, tipo, peso]);
        res.status(201).json({
            mensaje: "Animal registrado exitosamente",
            datos: result.rows[0]
        });
    } catch (err: any) {
        res.status(500).json({ error: "Error al registrar animal", detalle: err.message });
    }
});

/**
 * @route   PUT /api/ganado/:id
 * @desc    Actualizar datos de un animal
 * @access  Privado (Admin/Usuario)
 */
router.put('/:id', validarJWT, async (req, res) => {
    const { id } = req.params;
    const { nombre, tipo, peso } = req.body;

    try {
        const sql = 'UPDATE ganado SET nombre = $1, tipo = $2, peso = $3 WHERE id = $4 RETURNING *';
        const result = await pool.query(sql, [nombre, tipo, peso, id]);

        if (result.rowCount === 0) {
            return res.status(404).json({ error: "Animal no encontrado" });
        }

        res.json({ mensaje: "Animal actualizado", datos: result.rows[0] });
    } catch (err: any) {
        res.status(500).json({ error: "Error al actualizar", detalle: err.message });
    }
});

/**
 * @route   DELETE /api/ganado/:id
 * @desc    Eliminar un animal (Solo ADMIN recomendado)
 * @access  Privado
 */
router.delete('/:id', validarJWT, async (req, res) => {
    const { id } = req.params;

    try {
        const result = await pool.query('DELETE FROM ganado WHERE id = $1 RETURNING *', [id]);

        if (result.rowCount === 0) {
            return res.status(404).json({ error: "Animal no encontrado" });
        }

        res.json({ mensaje: "Animal eliminado correctamente" });
    } catch (err: any) {
        res.status(500).json({ error: "Error al eliminar", detalle: err.message });
    }
});

export default router;
