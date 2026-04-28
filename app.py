import os
from flask import Flask, jsonify, request
from flask_cors import CORS  # Recomendado para evitar errores de bloqueo en el navegador

app = Flask(__name__)
CORS(app)  # Esto permite que tu API reciba peticiones desde cualquier origen

# --- Función Auxiliar (Debes configurarla con tu lógica de envío) ---
def enviar_correo_alerta(asunto, mensaje, destino):
    """
    Aquí debe ir tu lógica para conectar con un servidor SMTP o API de correos.
    Por ahora, simularemos que el proceso es exitoso.
    """
    print(f"Enviando correo a: {destino} | Asunto: {asunto}")
    # Aquí iría el código de smtplib o similar
    return True

# --- RUTAS ---

@app.route('/', methods=['GET'])
def health():
    return jsonify({
        "status": "API funciona",
        "mensaje": "Servidor activo en Render"
    }), 200

@app.route('/enviar-alerta', methods=['POST'])
def enviar_alerta():
    try:
        # 1. Obtener los datos del JSON
        data = request.get_json()
        
        # Si no llega JSON, data será None
        if not data:
            return jsonify({"success": False, "message": "No se recibió un cuerpo JSON"}), 400

        destino = data.get("to")
        asunto = data.get("subject")
        mensaje = data.get("message")

        # 2. Validar que existan los campos
        if not destino or not asunto or not mensaje:
            return jsonify({
                "success": False,
                "message": "Faltan datos obligatorios: to, subject, message"
            }), 400

        # 3. Ejecutar la función de envío
        enviar_correo_alerta(asunto, mensaje, destino)
        
        return jsonify({
            "success": True,
            "message": "Correo enviado con éxito"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# --- INICIO DEL SERVIDOR ---

if __name__ == '__main__':
    # Render usa la variable de entorno PORT
    port = int(os.getenv("PORT", 5000))
    # debug=False en producción (Render)
    app.run(host='0.0.0.0', port=port, debug=False)