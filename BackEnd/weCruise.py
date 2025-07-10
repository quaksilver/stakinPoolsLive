from flask import Flask, jsonify
from staking_logic import get_pool_rankings

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
