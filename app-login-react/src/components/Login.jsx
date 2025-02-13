import { useState } from "react";
import { useNavigate } from "react-router-dom";

import axios from "axios";
import { jwtDecode } from "jwt-decode";

function Login() {
  const navigate = useNavigate();
  
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(""); // Reinicia errores anteriores

    try {
      const { data } = await axios.post("http://127.0.0.1:5000/login", {
        email,
        password,
      });

      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        const decoded = jwtDecode(data.access_token);
        setUser(decoded);
        navigate("/perfil"); // Redirigir al perfil después del logi
      }
    } catch (err) {
      console.error("Login fallido:", err.response?.data || err.message);
      setError("Credenciales incorrectas o error en el servidor");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {user && <p>Bienvenido, Usuario ID: {user.sub} </p>}
    </div>
  );
}

export default Login;
