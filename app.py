import os
import threading
import pymssql
import resend
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE VARIABLES DESDE RENDER ---
# Estas llaves coinciden exactamente con tus capturas
resend.api_key = os.environ.get("RESEND_API_KEY")
FROM_EMAIL = os.environ.get("MAIL_RESEND", "onboarding@resend.dev")

# Variables de la base de datos Azure
DB_SERVER = os.environ.get("DB_SERVER")
DB_USER = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DATABASE = os.environ.get("DB_DATABASE")

# --- FUNCIÓN PARA SQL SERVER ---
def get_db_connection():
    try:
        conn = pymssql.connect(
            server=DB_SERVER,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        return conn
    except Exception as e:
        print(f"Error conectando a SQL Server: {e}")
        return None

# --- FUNCIÓN DE ENVÍO ASÍNCRONO ---
def ejecutar_envio_correo(destino, asunto, mensaje):
    try:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [destino],
            "subject": asunto,
            "html": f"<div>{mensaje}</div>"
        })
        print(f"Éxito: Correo enviado a {destino}")
    except Exception as e:
        print(f"Error en segundo plano: {e}")

# --- RUTAS ---

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "api": "Mars Sport API",
        "database_status": "Configured",
        "db_name": DB_DATABASE
    }), 200

@app.route("/enviar-alerta-resend", methods=["POST"])
def enviar_alerta_resend():
    data = request.get_json()
    
    # Extraemos datos (ajustado a tu script de WordPress)
    correo = data.get("to") or data.get("email")
    asunto = data.get("subject", "Alerta Mars Sport")
    mensaje = data.get("message", "Mensaje automático")

    if not correo:
        return jsonify({"status": "error", "msg": "Falta el destinatario"}), 400

    try:
        # Usamos threading para que la API responda "OK" de inmediato 
        # y no se quede esperando a que Resend termine.
        thread = threading.Thread(
            target=ejecutar_envio_correo, 
            args=(correo, asunto, mensaje)
        )
        thread.start()

        return jsonify({
            "status": "ok", 
            "msg": "Petición recibida, enviando correo..."
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == '__main__':
    # Render asigna el puerto automáticamente
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)