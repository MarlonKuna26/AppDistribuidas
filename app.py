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