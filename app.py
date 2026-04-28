import os
import pyodbc
from flask import Flask, jsonify

app = Flask(__name__)

def get_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    
    # Connection string para Azure SQL Server
    connection_string = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )
    
    return pyodbc.connect(connection_string)

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "API funciona", "message": "Conectado a Azure SQL Server"}), 200

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        # Validar variables de ambiente
        server = os.getenv("DB_SERVER")
        database = os.getenv("DB_DATABASE")
        username = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")
        
        if not all([server, database, username, password]):
            missing = [k for k, v in [
                ("DB_SERVER", server),
                ("DB_DATABASE", database),
                ("DB_USERNAME", username),
                ("DB_PASSWORD", password)
            ] if not v]
            return jsonify({
                "success": False,
                "error": f"Variables de ambiente faltantes: {', '.join(missing)}"
            }), 500
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convertir None a lista vacía
        datos = list(productos) if productos else []
        
        return jsonify({"success": True, "data": datos}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)