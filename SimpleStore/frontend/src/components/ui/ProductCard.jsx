import { Box, Image, Heading, Text, IconButton, HStack, VStack, Input } from '@chakra-ui/react'
import { useColorMode } from './color-mode'
import { MdEdit, MdDelete } from "react-icons/md"
import { Button, CloseButton, Dialog, Portal } from "@chakra-ui/react"
import { useProductStore } from '../../store/productStore'
import { toaster } from './toaster' // Adjust the import path as necessary
import React, { useState } from 'react'

const ProductCard = ({ product }) => {
	const { colorMode } = useColorMode()
	const { deleteProduct, updateProduct } = useProductStore();

    const [ updatedProduct, setUpdatedProduct] = useState(product);

	const handleDelete = async (id) => {
		const { success, message } = await deleteProduct(id)
		if (!success) {
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
				type: "success",
				closable: true
			})
		}
	}

    const handleUpdate = async (id, product) => {
        const { success, message } = await updateProduct(id, product)
        console.log(id, product)
        if (!success) {
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
                type: "success",
                closable: true
            })
        }
    }

	const bg = colorMode === "light" ? "white" : "gray.800"
	const borderColor = colorMode === "light" ? "gray.200" : "gray.700"
	const hoverBg = colorMode === "light" ? "gray.100" : "gray.700"

	return (
        <Dialog.Root>
		<Box
			shadow="lg"
			rounded="lg"
			overflow="hidden"
			transition="all 0.3s"
			_hover={{ transform: "translateY(-5px)", shadow: "xl" }}
			bg={bg}>

			<Image src={product.image} alt={product.name} h={48} w="full" objectFit="cover" />

			<Box p={4}>
				<Heading as="h3" size="md" mb={2}>
					{product.name}
				</Heading>

				<Text fontWeight="bold" fontSize="xl" mb={4}>
					${product.price}
				</Text>

				<HStack spacing={2}>
                    <Dialog.Trigger asChild>
					    <IconButton
						    aria-label="Edit"
						    bg={bg}
						    border="2px solid"
						    borderColor={borderColor}
						    borderRadius="md"
						    _hover={{ bg: hoverBg }}
					    >
						    <MdEdit color="#0BC5EA" />
					    </IconButton>
                    </Dialog.Trigger>

					<IconButton
						aria-label="Delete"
						bg={bg}
						border="2px solid"
						borderColor={borderColor}
						borderRadius="md"
						_hover={{ bg: hoverBg }}
						key={product.id}
						onClick={() => handleDelete(product._id)}
					>
						<MdDelete color="red" />
					</IconButton>
				</HStack>
			</Box>
                <Portal>
                    <Dialog.Backdrop />
                    <Dialog.Positioner>
                        <Dialog.Content>
                            <Dialog.Header>
                                <Dialog.Title>Update Product</Dialog.Title>
                            </Dialog.Header>
                            <Dialog.Body>
                                <VStack spacing={4}>
                                    <Input placeholder='Product Name' name="name" value={updatedProduct.name} 
                                    onChange={(e) => setUpdatedProduct({...updatedProduct, name: e.target.value})}
                                    />
                                   
                                    <Input placeholder='Price' name='price' type='number' value={updatedProduct.price}
                                    onChange={(e) => setUpdatedProduct({...updatedProduct, price: e.target.value})}
                                    />
                                    
                                    <Input placeholder='Image Url' name="image" value={updatedProduct.image} 
                                    onChange={(e) => setUpdatedProduct({...updateProduct, image: e.target.value})}
                                    />
                                </VStack>
                            </Dialog.Body>
                            <Dialog.Footer>
                                <Button bg="#0BC5EA" onClick={() => handleUpdate(product._id, updatedProduct)}>Update</Button>
                                
                                <Dialog.ActionTrigger asChild>
                                    <Button variant="outline">Cancel</Button>
                                </Dialog.ActionTrigger>
                            </Dialog.Footer>
                            <Dialog.CloseTrigger asChild>
                                <CloseButton size="sm" />
                            </Dialog.CloseTrigger>
                        </Dialog.Content>
                    </Dialog.Positioner>
                </Portal>
		</Box>
        </Dialog.Root>
	)
}

export default ProductCard
