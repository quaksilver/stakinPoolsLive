import requests

BASE_URL = "https://api.koios.rest/api/v1"

def get_all_pool_ids():
    response = requests.get(f"{BASE_URL}/pool_list")
    response.raise_for_status()
    data = response.json()
    return [entry['pool_id_bech32'] for entry in data]

def get_stake_address(pool_id):
    response = requests.get(f"{BASE_URL}/pool_info", params={"pool_bech32": pool_id})
    response.raise_for_status()
    data = response.json()
    if data and "meta_json" in data[0] and "ticker" in data[0]["meta_json"]:
        name = data[0]["meta_json"]["ticker"]
    else:
        name = pool_id[:10] + "..."
    # Get first owner as stake address
    stake_address = data[0]["pool_owners"][0] if data[0]["pool_owners"] else None
    return stake_address, name

def get_rewards(stake_address):
    response = requests.get(f"{BASE_URL}/account_rewards", params={"_stake_addr": stake_address})
    response.raise_for_status()
    data = response.json()
    if not data:
        return 0
    rewards = sum(int(epoch["reward"]) for epoch in data[0]["rewards"])
    return rewards / 1_000_000  # Convert lovelace to ADA

def get_pool_rankings():
    rankings = []
    pool_ids = get_all_pool_ids()

    for pool_id in pool_ids[:50]:  # Limit to top 50 for speed
        try:
            stake_address, name = get_stake_address(pool_id)
            if not stake_address:
                continue
            rewards = get_rewards(stake_address)
            rankings.append({"name": name, "rewards": round(rewards, 2)})
        except Exception as e:
            print(f"Error processing {pool_id}: {e}")

    rankings.sort(key=lambda x: x["rewards"], reverse=True)
    return rankings
