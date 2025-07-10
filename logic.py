import requests
import time

BASE_URL = "http://130.60.24.200:3000"
PAGE_SIZE = 100
REWARD_UNIT = 1_000_000

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
            data = res.json()
            pool_ids.extend(data)
            page += 1
        except Exception as e:
            print(f"Error fetching pools on page {page}: {e}")
            break

    return pool_ids

def get_pool_info(pool_id):
    url = f"{BASE_URL}/pools/{pool_id}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except:
        return {}

def get_pool_metadata(pool_id):
    url = f"{BASE_URL}/pools/{pool_id}/metadata"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return data.get("name") or data.get("ticker") or pool_id
    except:
        return pool_id

def get_rewards(stake_address):
    url = f"{BASE_URL}/accounts/{stake_address}/rewards"
    try:
        res = requests.get(url)
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

def get_pool_rankings():
    pool_ids = get_all_pool_ids()
    pool_rewards = {}

    for pool_id in pool_ids:
        pool_info = get_pool_info(pool_id)
        stake_address = pool_info.get("reward_account")
        if not stake_address:
            continue

        rewards = get_rewards(stake_address)
        total = sum_rewards_for_pool(rewards, pool_id)
        pool_name = get_pool_metadata(pool_id)
        pool_rewards[pool_name] = total

    # Sort descending by rewards
    sorted_rewards = sorted(pool_rewards.items(), key=lambda x: x[1], reverse=True)
    # Return as list of dicts
    return [{"pool_name": name, "total_rewards": total} for name, total in sorted_rewards]
