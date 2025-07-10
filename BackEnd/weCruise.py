from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)
BASE_URL = "http://130.60.24.200:3000"
PAGE_SIZE = 100
REWARD_UNIT = 1_000_000
CACHE_EXPIRY = 60  # seconds

pool_cache = {"timestamp": 0, "data": []}

def get_all_pool_ids():
    pool_ids = []
    page = 1
    while True:
        url = f"{BASE_URL}/pools?page={page}&count={PAGE_SIZE}&order=asc"
        try:
            res = requests.get(url)
            if res.status_code == 404 or not res.json():
                break
            res.raise_for_status()
            pool_ids.extend(res.json())
            page += 1
        except:
            break
    return pool_ids

def get_pool_info(pool_id):
    try:
        res = requests.get(f"{BASE_URL}/pools/{pool_id}")
        res.raise_for_status()
        return res.json()
    except:
        return {}

def get_pool_metadata(pool_id):
    try:
        res = requests.get(f"{BASE_URL}/pools/{pool_id}/metadata")
        res.raise_for_status()
        data = res.json()
        return data.get("name") or data.get("ticker") or pool_id
    except:
        return pool_id

def get_rewards(stake_address):
    try:
        res = requests.get(f"{BASE_URL}/accounts/{stake_address}/rewards")
        res.raise_for_status()
        return res.json()
    except:
        return []

def sum_rewards_for_pool(rewards, pool_id):
    return sum(
        int(entry["amount"])
        for entry in rewards
        if entry.get("pool_id") == pool_id
    )

def fetch_pool_rankings():
    pool_ids = get_all_pool_ids()
    rankings = []
    for pool_id in pool_ids:
        info = get_pool_info(pool_id)
        stake_address = info.get("reward_account")
        if not stake_address:
            continue
        rewards = get_rewards(stake_address)
        total = sum_rewards_for_pool(rewards, pool_id)
        name = get_pool_metadata(pool_id)
        rankings.append({"name": name, "rewards": total / REWARD_UNIT})
        time.sleep(0.05)
    return sorted(rankings, key=lambda x: x["rewards"], reverse=True)

@app.route("/rankings")
def api_rankings():
    now = time.time()
    if now - pool_cache["timestamp"] > CACHE_EXPIRY:
        print("🔄 Refreshing rankings cache...")
        pool_cache["data"] = fetch_pool_rankings()
        pool_cache["timestamp"] = now
    return jsonify(pool_cache["data"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
