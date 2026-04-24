import os
from flask import Flask, jsonify
from mssql_python import connect

app = Flask(__name__)

def get_connection():
    # ... (tu código de conexión actual está perfecto aquí)
    # Solo asegúrate de tener las variables en Render -> Environment
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT", "1433")
    
    connection_string = (
        f"Server=tcp:{server},{port};"
        f"Database={database};"
        f"Uid={username};"
        f"Pwd={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Authentication=SqlPassword;"
    )
    return connect(connection_string)

# --- ESTO ES LO QUE TE FALTA ---

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "Servidor de AppDistribuidas funcionando"}), 200

@app.route('/test-db')
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        return jsonify({"db_version": row[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Importante para Render: usar el puerto que ellos asignan
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)