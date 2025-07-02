import mongoose from "mongoose";
import { Product } from "../models/product.model.js"

export const createProduct = async (req, res, next) => {
    try {
        const product = req.body
        if (!product.name || !product.image || !product.price) {
            return res.status(404).json({ success: true, message: "Please fill out all fields."})}

        const newProduct = new Product(product);
        await newProduct.save()
        
        res.status(201).json({success: true, data: newProduct})
    } catch (error) {
        console.log("Error in createProduct", error)
        next()
    }
}

export const deleteProduct = async (req, res, next) => {
    try {
        const {id} = req.params;
        if (!mongoose.Types.ObjectId.isValid(id)){
            res.status(404).json({success: false, message: "Invalid Product ID"})
        }
        
        await Product.findByIdAndDelete(id);
        res.status(200).json({success: true, message: "Product deleted successfully"})
    } catch (error) {
        console.log("Error in deleteProduct", error)
        next()
    }
}

export const getAllProducts = async (req, res, next) => {
    try {
        const products = await Product.find({})
        res.status(201).json({success: true, data: products})
    } catch (error) {
        console.log("Error in getAllProducts", error)
        next()
    }
}

export const updateProduct = async (req, res, next) => {
    try {
        const {id} = req.params
        if (!mongoose.Types.ObjectId.isValid(id)){
            res.status(404).json({success: false, message: "Invalid Product ID"})
        }

        const updatedProduct = req.body;
        const data = await Product.findByIdAndUpdate(id, updatedProduct, {new: true})
        res.status(200).json({success: true, data: data, message: "Product updated successfully."}) // Return the updated product data
    } catch (error) {
        console.log("Error in updateProduct", error)
        next()
    }
}