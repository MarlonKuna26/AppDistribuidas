import os
from flask import Flask, jsonify, request  # Añadido 'request'

app = Flask(__name__)

# Ruta de salud existente
@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "API funciona"}), 200

# NUEVA RUTA: Debes agregar el decorador aquí
@app.route('/enviar-alerta', methods=['POST']) # Usamos POST porque recibes datos
def enviar_alerta():
    try:
        data = request.get_json()
        destino = data.get("to")
        asunto = data.get("subject")
        mensaje = data.get("message")

        if not destino or not asunto or not mensaje:
            return jsonify({
                "success": False,
                "message": "Faltan datos (to, subject, message)"
            }), 400

        # Nota: Asegúrate de que la función enviar_correo_alerta esté definida
        enviar_correo_alerta(asunto, mensaje, destino)
        
        return jsonify({
            "success": True,
            "message": "Correo enviado"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Esta parte SIEMPRE debe ir al final
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True) # debug=True ayuda a ver errores