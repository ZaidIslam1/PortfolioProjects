import { Box } from "@chakra-ui/react"
import { Route, Routes } from "react-router-dom";
import Navbar from "./components/ui/Navbar";
import HomePage from "./pages/HomePage";
import CreatePage from "./pages/CreatePage";
import { useColorMode } from "./components/ui/color-mode"; 

  
function App() {
  const { colorMode } = useColorMode();
  return (
    <Box minH={"100vh"} bg={colorMode === "light" ? "gray.100" : "gray.800"}>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/create" element={<CreatePage/>}/>
      </Routes>
    </Box>
  )
}

export default App
