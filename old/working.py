import requests
import time

BASE_URL = "http://130.60.24.200:3000"
PAGE_SIZE = 100
REWARD_UNIT = 1_000_000
REFRESH_INTERVAL = 60  # seconds between refreshes

def get_all_pool_ids():
    print("🔄 Fetching all stake pools...")
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
            print(f"  📦 Page {page}: {len(data)} pools")
            page += 1
        except Exception as e:
            print(f"❌ Error fetching pools on page {page}: {e}")
            break

    print(f"✅ Total pools fetched: {len(pool_ids)}\n")
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

def print_rewards_summary(pool_rewards):
    print("\n📊 Total Rewards by Pool:")
    sorted_rewards = sorted(pool_rewards.items(), key=lambda x: x[1], reverse=True)
    for name, lovelace in sorted_rewards:
        ada = lovelace / REWARD_UNIT
        print(f"  {name}: ₳{ada:.6f}")

def main():
    while True:
        pool_ids = get_all_pool_ids()
        pool_rewards = {}

        for pool_id in pool_ids:
            pool_info = get_pool_info(pool_id)
            stake_address = pool_info.get("reward_account")
            if not stake_address:
                print(f"⚠️ No reward account for {pool_id}")
                continue

            rewards = get_rewards(stake_address)
            total = sum_rewards_for_pool(rewards, pool_id)

            pool_name = get_pool_metadata(pool_id)
            pool_rewards[pool_name] = total

            print(f"✅ {pool_name}: ₳{total / REWARD_UNIT:.6f}")
            time.sleep(0.05)  # polite delay

        print_rewards_summary(pool_rewards)

        print(f"\n⏳ Waiting {REFRESH_INTERVAL} seconds before next update...\n")
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    main()
