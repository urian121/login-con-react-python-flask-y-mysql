from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS
import mysql.connector
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "supersecretkey"  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


# Lista negra para tokens revocados
blacklist = set()


# 🔹 Función para crear conexión con MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="login_react_python_flask_mysql"
    )


# ✅ LOGIN
@app.route("/login", methods=["POST"])
def login():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.check_password_hash(user["password"], password):
            token = create_access_token(identity=str(user["id"]))
            return jsonify(access_token=token)
        
        return jsonify({"error": "Credenciales incorrectas"}), 401
    finally:
        cursor.close()
        db.close()

# ✅ PERFIL (Protegido con JWT)
@app.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        user_id = int(get_jwt_identity())
        cursor.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
            
        return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# ✅ REGISTRO DE USUARIO
@app.route("/register", methods=["POST"])
def register():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        email = data.get("email")
        password = data.get("password")

        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "El email ya está registrado"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, hashed_password)
        )
        db.commit()
        
        return jsonify({"message": "Usuario registrado correctamente"}), 201
    finally:
        cursor.close()
        db.close()

# ✅ LOGOUT (Revocar Token)
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Obtener identificador único del token
    blacklist.add(jti)  # Agregar token a la lista negra
    return jsonify({"message": "Sesión cerrada correctamente"}), 200

# ✅ Verificar si un token está en la lista negra
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blacklist

if __name__ == "__main__":
    app.run(debug=True, port=5000)