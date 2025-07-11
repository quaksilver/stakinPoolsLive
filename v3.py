import requests
import time

# List of pool IDs to exclude from the leaderboard
EXCLUDED_POOL_IDS = {
    "pool13gsek6vd8dhqxsu346zvae30r4mtd77yth07fcc7p49kqc3fd09",
    "pool1457aldacllsdcq9p28hjqlmj7z3muphpu2vk7k22rp08sjg5ypg",
    "pool17ztt7y3ea4p7xurdpnfnapvrlwnkflnx4u8fuj7xrvyzyemtkjk",
    "pool13lyrs800h5x6ep6tp9j8ngqwfcssj73fdsuv6whfksynvmetm39",
    "pool123v85t3jhe5yxd4zkf09mgh9t8aepcf24s35unu8yxx3qsgxuvr",
    "pool1zztnenfcz3m6k6k5lu5z5wh680clacctrxnnzh6mwlv72anduth",
    "pool19287c4vpk6rr4t0jmcx93d7s9jtdue35gz92nqhgp09x56pkxd7",
    "pool1zqwls5suej6s7qk46hunne2kcznufr5wwgjaj0ahgdjhqr6m589",
    "pool15jza0xl7fvg3zjxx0f0gk9849exksa4u2atfsdjl5qr5kppf7h3",
    "pool1z52ft7c7k7vuu2ex2q627cz73cwwa9sa9pu83s60ulqykxcnyay"
}

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
    print("Collecting rewards...")
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
    url = f"{BASE_URL}/accounts/{stake_address}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return int(data.get("rewards_sum", 0))
    except:
        return 0

def print_rewards_summary(pool_rewards):
    print("NOTE: don't let total rewards be your only consideration. Check the margin cost to check for greedy SPO's")
    print("\n📊 Total Rewards by Pool:")
    sorted_rewards = sorted(pool_rewards.items(), key=lambda x: x[1], reverse=True)
    for name, lovelace in sorted_rewards:
        ada = lovelace / REWARD_UNIT
        print(f"  {name}: ₳{ada:.3f}")

def main():
    pool_ids = get_all_pool_ids()
    pool_rewards = {}

    for pool_id in pool_ids:
        if pool_id in EXCLUDED_POOL_IDS:
            #print(f"🚫 Skipping excluded pool: {pool_id}")
            continue

        pool_info = get_pool_info(pool_id)
        stake_address = pool_info.get("reward_account")
        if not stake_address:
            print(f"⚠️ No reward account for {pool_id}")
            continue

        total = get_rewards(stake_address)
        pool_name = get_pool_metadata(pool_id)
        pool_rewards[pool_name] = total

        time.sleep(0.05)  # polite delay

    print_rewards_summary(pool_rewards)

if __name__ == "__main__":
    main()
