import express from "express";
import cors from "cors";
import helmet from "helmet";
import dotenv from "dotenv";
dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;
app.use(helmet());
app.use(cors());
app.use(express.json());
app.get("/health", (req, res) => {
 res.json({ ok: true, message: "Backend funcionando correctamente" });
});
app.listen(PORT, () => {
 console.log(`Servidor backend activo en http://localhost:${PORT}`);
});
