import os
from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

def get_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    
    # Intentamos Driver 18 (que es el que instalaremos en el build script)
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)

@app.route("/")
def home():
    return jsonify({"success": True, "message": "API funcionando"})

@app.route("/productos")
def listar_productos():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Agregamos url_imagen a la consulta SQL
        cursor.execute("""
            SELECT TOP 20 Id, Nombre, Precio, Stock, url_imagen, Versions
            FROM productos
            ORDER BY Id DESC
        """)
        rows = cursor.fetchall()

        data = []
        for row in rows:
            version_hex = row[5].hex() if row[5] else None
            data.append({
                "id": row[0],
                "nombre": row[1],
                "precio": float(row[2]) if row[2] is not None else 0.0,
                "stock": row[3],
                "imagen_url": row[4], # La nueva columna
                "row_version": f"0x{version_hex}" if version_hex else None
            })

        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)