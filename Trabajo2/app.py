from flask import Flask, request, jsonify

app = Flask(__name__)

usuarios = []

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "aplicacion": "Tabla Ejemplo",
        "version": "1.0",
        "creador": "Jacob J Desuza",
        "descripcion": "Una API para registrar y listar usuarios."
    }), 200

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibió ningún dato JSON"}), 400

    nombre = data.get("nombre")
    correo = data.get("correo")

    if not nombre or not correo:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje": "Se requieren los campos 'nombre' y 'correo'."
        }), 400

    usuario = {
        "id": len(usuarios) + 1,
        "nombre": nombre,
        "correo": correo
    }
    usuarios.append(usuario)

    return jsonify({
        "mensaje": "Usuario creado correctamente.",
        "usuario": usuario
    }), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify({
        "total": len(usuarios),
        "usuarios": usuarios
    }), 200

if __name__ == '__main__':
    app.run(debug=True)