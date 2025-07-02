import { Container, Heading, Box, VStack, Button, Input} from '@chakra-ui/react'
import React, { useState } from 'react'
import { useColorMode } from '../components/ui/color-mode';
import { useProductStore } from '../store/productStore';
import { toaster } from '../components/ui/toaster'; // Adjust path if needed

const CreatePage = () => {33
    const {colorMode} = useColorMode();
    const [newProduct, setNewProduct] = useState({
        name: "",
        price: "",
        image: "",
    })
    const {createProduct} = useProductStore();

    const handleAddProduct = async () => {
        const {success, message} = await createProduct(newProduct)
        if (!success){
            toaster.create({
                title: "Error",
                description: message,
                type: "error",
                closable: true
            })
        } else {
            toaster.create({
                title: "Success",
                description: message,
                type: "Success",
                closable: true,
            })
        }
        setNewProduct({
            name: "",
            price: "",
            image: "",
        })
        // Optionally, you can redirect or clear the form after successful submission
    }
return (
    <Container maxW={"container.sm"}>
        <VStack spacing={8}>
            <Heading as="h1" size="2xl" textAlign="center" mb={8}>
                Create New Product
            </Heading>

            <Box w={"full"} p={6} rounded={"lg"} shadow={"md"} bg={colorMode === "light" ? "white" : "gray.800"}>
                <VStack spacing={4}>
                    <Input 
                        border={`1px solid ${colorMode === "light" ? "gray.300" : "gray.500"}`}
                        placeholder="Product Name"
                        value={newProduct.name}
                        onChange={(e) => setNewProduct({...newProduct, name: e.target.value})}
                    />

                    <Input 
                        border={`1px solid ${colorMode === "light" ? "gray.300" : "gray.500"}`}
                        placeholder="Product Price"
                        type="number"
                        value={newProduct.price}
                        onChange={(e) => setNewProduct({...newProduct, price:e.target.value})}
                    />
                    
                    <Input 
                        border={`1px solid ${colorMode === "light" ? "gray.300" : "gray.500"}`}
                        placeholder="Product Image URL"
                        value={newProduct.image}
                        onChange={(e) => setNewProduct({...newProduct, image: e.target.value})}
                    />
                    <Button
                        colorScheme="blue"
                        onClick={handleAddProduct}
                        disabled={!newProduct.name || !newProduct.price || !newProduct.image}>
                        Add Product
                    </Button>
                </VStack>
            </Box>
        </VStack>
    </Container>
)
}

export default CreatePage