from flask import Flask, jsonify, send_from_directory
from logic import get_pool_rankings

app = Flask(__name__, static_folder='static')

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "frontEnd.html")

@app.route("/rankings")
def rankings():
    return jsonify(get_pool_rankings())

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run()
