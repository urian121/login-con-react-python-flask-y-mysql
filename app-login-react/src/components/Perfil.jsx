import { useEffect, useState } from "react";
import axios from "axios";

function Perfil() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("No hay token, inicia sesión.");
        return;
      }

      try {
     const { data } = await axios.get("http://127.0.0.1:5000/perfil", {
       headers: {
         Authorization: `Bearer ${token}`,
         "Content-Type": "application/json",
       },
     });
      setUser(data);
      } catch (error) {
        console.error("No autorizado", error.response?.data || error.message);
        setError("Acceso no autorizado. Inicia sesión nuevamente.");
      }
    };

    fetchProfile();
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!user) return <p>Cargando perfil...</p>;

  return (
    <div>
      <h2>Perfil</h2>
      <p>
        <strong>ID:</strong> {user.id}
      </p>
      <p>
        <strong>Email:</strong> {user.email}
      </p>
    </div>
  );
}

export default Perfil;
