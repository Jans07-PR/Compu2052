from flask import Flask, request, jsonify

app = Flask(__name__)

datos = {'NOMBRE': 'SERVIDOR DE JACOB', 'DIA CREADO': '17-4-2025', 'CREADOR': 'Jacob Desuza Martinez'}

@app.route("/", methods=["GET"])
def home():
    return "Bienvenido al Servidor"


@app.route('/info', methods=['GET'])
def info():
    return jsonify(datos)


@app.route('/mensaje', methods=['POST'])
def mensaje():
    data = request.get_json()
    mensaje_usuario = data['mensaje']
    respuesta = f"Recibido tu mensaje: '{mensaje_usuario}'. ¡Gracias por enviarlo!"

    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    app.run(debug=True)


