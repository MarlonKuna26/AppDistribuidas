import os
import pymssql  # <--- CAMBIA ESTO (Antes decía mssql_python)
from flask import Flask, jsonify

app = Flask(__name__)

def get_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    
    # pymssql usa parámetros directos, no un connection_string largo
    return pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database,
        autocommit=True
    )

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "API funciona", "message": "Conectado a Azure SQL Server"}), 200

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "data": productos}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)