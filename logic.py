import requests

BASE_URL = "http://130.60.24.200:3000"

def get_all_pool_ids():
    page = 1
    pool_ids = []

    while True:
        response = requests.get(f"{BASE_URL}/pools?page={page}")
        if response.status_code != 200:
            break
        data = response.json()  # ✅ FIXED: use .json()
        if not data:
            break
        pool_ids.extend([pool["pool_id"] for pool in data])
        page += 1

    return pool_ids

def get_stake_address(pool_id):
    response = requests.get(f"{BASE_URL}/pools/{pool_id}")
    if response.status_code != 200:
        return None
    data = response.json()
    return data.get("stake_address")

def get_pool_name(pool_id):
    response = requests.get(f"{BASE_URL}/pools/{pool_id}")
    if response.status_code != 200:
        return pool_id  # fallback
    data = response.json()
    return data.get("meta", {}).get("name", pool_id)

def get_total_rewards(stake_address):
    page = 1
    total = 0

    while True:
        response = requests.get(f"{BASE_URL}/accounts/{stake_address}/rewards?page={page}")
        if response.status_code != 200:
            break
        rewards = response.json()
        if not rewards:
            break
        for entry in rewards:
            total += int(entry.get("amount", 0))
        page += 1

    return total / 1_000_000  # Convert from lovelace to ADA

def get_pool_rankings():
    pool_ids = get_all_pool_ids()
    rankings = []

    for pool_id in pool_ids:
        stake_address = get_stake_address(pool_id)
        if not stake_address:
            continue
        total_rewards = get_total_rewards(stake_address)
        name = get_pool_name(pool_id)
        rankings.append({
            "name": name,
            "pool_id": pool_id,
            "total_rewards_ada": f"{total_rewards:.6f} ₳"
        })

    rankings.sort(key=lambda x: -float(x["total_rewards_ada"].split()[0]))
    return rankings
