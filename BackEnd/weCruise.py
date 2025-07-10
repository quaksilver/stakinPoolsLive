from flask import Flask, jsonify
from logic import get_pool_rankings

app = Flask(__name__)

@app.route("/")
def home():
    return "Staking Pools API is live!"

@app.route("/rankings")
def rankings():
    rankings = get_pool_rankings()
    return jsonify(rankings)

# Optional: Add a health check
@app.route("/health")
def health():
    return "OK", 200

from flask import Flask, jsonify
from BackEnd.logic import get_pool_rankings

app = Flask(__name__)

@app.route("/")
def home():
    return "Staking Pools API is live!"

@app.route("/rankings")
def rankings():
    rankings = get_pool_rankings()
    return jsonify(rankings)

@app.route("/health")
def health():
    return "OK", 200

# ✅ REQUIRED to run on Render (with python BackEnd/weCruise.py)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

