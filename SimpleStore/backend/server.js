import express from "express";
import dotenv from "dotenv";
import { connectDB } from "./config/connectDB.js";
import productRoutes from "./routes/product.route.js"
import path from "path";

dotenv.config();

const PORT = process.env.PORT;
const app = express();
const __dirname = path.resolve();

app.use(express.json()) // allows us to accept JSON data in the request body

app.use("/api/products", productRoutes);

app.use((err, req, res, next) => {
    res.status(500).json({ success: false, error: "Internal Server Error" });
});

if (process.env.NODE_ENV === "production") {
	app.use(express.static(path.join(__dirname, "/frontend/dist")));
	app.get("*", (req, res) => {
		res.sendFile(path.resolve(__dirname, "frontend", "dist", "index.html"));
	});
}

app.listen(PORT, () => {
    connectDB();
    console.log(`Server started on http://localhost:${PORT}`) // Port: 5002
})