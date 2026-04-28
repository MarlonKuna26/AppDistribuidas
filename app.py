import os
import pymssql
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "API funciona"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)