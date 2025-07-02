import { Container, Flex, Text, HStack, Button} from '@chakra-ui/react'
import { Link } from 'react-router-dom'
import React from 'react'
import { FiPlus } from "react-icons/fi";
import { IoMoon, IoSunny } from 'react-icons/io5';
import { useColorMode } from './color-mode';

const Navbar = () => {
    const {colorMode, toggleColorMode} = useColorMode();
    return (
    <Container maxW={"7xl"} px={4}>
        <Flex h={16} alignItems={"center"} justifyContent={"space-between"} flexDir={{base: "column", sm: "row"}}>
            <Text
                as={Link}
                to="/"
                textStyle=
                "2xl"
                fontWeight="bold"
                textTransform="uppercase"
                textAlign="center"
                bgGradient="to-r" gradientFrom="cyan.400" gradientTo="blue.500"
                bgClip="text"
                >
                Product Store 🛒
            </Text>


            <HStack spacing={2} alignItems={"center"}>
                <Link to={"/create"}>
                    <Button variant={'ghost'} border={"1px solid"} borderColor={colorMode === "light" ? "gray.300" : "gray.600"}>
                        <FiPlus />
                    </Button>
                </Link>
                <Link>
                    <Button variant={"ghost"} border={"1px solid"} borderColor= {colorMode === "light" ? "gray.300" : "gray.600"} onClick={toggleColorMode}>
                        {colorMode === "light" ? <IoMoon/> : <IoSunny/>}
                    </Button>
                </Link>
            </HStack>
        </Flex>
    </Container>
  )
}

export default Navbar