

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";
import Perfil from "./components/Perfil";
import Register from "./components/Register";
import Logout from "./components/logout";
import Navbar from "./components/Navbar";

function App() {
  return (
    <>
      <Navbar />
      <div className="container mt-5">
        <Router>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/perfil" element={<Perfil />} />
            <Route path="/register" element={<Register />} />
            <Route path="/salir" element={<Logout />} />
          </Routes>
        </Router>
      </div>
    </>
  );
}

export default App;
