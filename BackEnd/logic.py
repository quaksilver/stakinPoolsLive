import requests

BASE_URL = "http://130.60.24.200:3000"
ADA_SYMBOL = "₳"

def get_all_pool_ids():
    pool_ids = []
    page = 1

    while True:
        response = requests.get(f"{BASE_URL}/pools?page={page}")
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        pool_ids.extend([pool["pool_id"] for pool in data])
        page += 1

    return pool_ids

def get_stake_address_from_pool(pool_id):
    response = requests.get(f"{BASE_URL}/pools/{pool_id}")
    if response.status_code == 200:
        return response.json().get("vrf_key")
    return None

def get_total_rewards_for_stake_address(stake_address):
    total = 0
    page = 1

    while True:
        response = requests.get(f"{BASE_URL}/accounts/{stake_address}/rewards?page={page}")
        if response.status_code != 200:
            break
        rewards = response.json()
        if not rewards:
            break
        total += sum(int(entry.get("amount", 0)) for entry in rewards)
        page += 1

    return total

def get_pool_name(pool_id):
    response = requests.get(f"{BASE_URL}/pools/{pool_id}")
    if response.status_code == 200:
        return response.json().get("pool_id")  # Placeholder if name not available
    return pool_id

def get_pool_rankings():
    pool_ids = get_all_pool_ids()
    rankings = []

    for pool_id in pool_ids:
        stake_address = get_stake_address_from_pool(pool_id)
        if not stake_address:
            continue
        total_rewards = get_total_rewards_for_stake_address(stake_address)
        pool_name = get_pool_name(pool_id)
        rankings.append({
            "pool_name": pool_name,
            "total_rewards": f"{int(total_rewards) / 1_000_000:.2f}{ADA_SYMBOL}"
        })

    rankings.sort(key=lambda x: float(x["total_rewards"].replace(ADA_SYMBOL, "")), reverse=True)
    return rankings

