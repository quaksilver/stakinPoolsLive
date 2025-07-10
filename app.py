from flask import Flask, jsonify, render_template
from logic import get_pool_rankings

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("frontEnd.html")  # or 'index.html' if you rename

@app.route("/rankings")
def rankings():
    data = get_pool_rankings()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
