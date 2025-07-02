import { createProduct, deleteProduct, getAllProducts, updateProduct } from "../controllers/product.controller.js";
import { Router } from "express";
const router = Router();

router.get("/", getAllProducts);
router.post("/", createProduct);
router.delete("/:id", deleteProduct);
router.put("/:id", updateProduct);

export default router;
