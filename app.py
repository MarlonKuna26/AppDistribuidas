import os
import pymssql
from flask import Flask, jsonify

app = Flask(__name__)

def get_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    
    # pymssql no usa cadena de conexión larga, usa parámetros directos
    return pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database,
        autocommit=True
    )

@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "API Flask funcionando con pymssql (sin drivers ODBC)"
    })

@app.route("/test-db")
def test_db():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT GETDATE()")
        row = cursor.fetchone()
        return jsonify({
            "success": True,
            "message": "¡Conexión exitosa sin drivers ODBC!",
            "server_date": str(row[0])
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error de conexión",
            "error": str(e)
        }), 500
    finally:
        if conn:
            conn.close()

@app.route("/productos")
def listar_productos():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(as_dict=True) # Devuelve los datos como diccionario
        cursor.execute("SELECT TOP 20 Id, Nombre, Precio, Stock, version FROM productos ORDER BY Id DESC")
        rows = cursor.fetchall()

        return jsonify({
            "success": True,
            "data": rows
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Error al consultar productos",
            "error": str(e)
        }), 500
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)