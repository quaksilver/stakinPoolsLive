# 🏦 Cardano Staking Rewards Leaderboard

This project fetches staking rewards from a Koios API instance and generates a leaderboard of stake pools by total rewards.

## 📁 Project Structure

- `v3.py`: Main Python script for fetching rewards and generating the leaderboard.
- `requirements.txt`: Lists the required Python packages.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cardano-staking-leaderboard.git
cd cardano-staking-leaderboard
```

### 2. Create and Activate a Virtual Environment

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

> ✅ **Note:** If `python` or `python3` doesn’t work, make sure Python 3.9+ is installed and added to your system’s PATH.

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the Script

```bash
python v3.py
```

---

## 🔍 What the Script Does

- Fetches all stake pools using the Koios `/pools` endpoint.
- Collects staking rewards for each pool.
- Excludes specific pools (see the `EXCLUDED_POOL_IDS` set in `v3.py`).
- Sorts pools by total rewards.
- Prints a leaderboard of top performers.

---

## 🛠️ Troubleshooting

- **Timeouts or API errors?** Make sure the Koios server at `http://130.60.24.200:3000` is reachable.
- **Virtual environment not activating?** Ensure you're using a supported shell (e.g., bash, zsh, cmd, or PowerShell) and correct Python version.

---

## 📜 License

MIT License — feel free to use, modify, and distribute.
