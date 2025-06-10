import requests, time
from datetime import datetime, timedelta
from config import *

def get_new_tokens():
    url = "https://api.dexscreener.io/latest/dex/pairs"
    res = requests.get(url)
    data = res.json()["pairs"]

    promising = []
    for token in data:
        created_at = token.get("pairCreatedAt")
        if not created_at:
            continue

        age = datetime.utcnow() - datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        if age > timedelta(minutes=MAX_AGE_MINUTES):
            continue

        if token["liquidity"]["usd"] < MIN_LIQUIDITY:
            continue
        if token["fdv"] is None or token["fdv"] > MAX_MARKET_CAP:
            continue
        if token["volume"]["h24"] < MIN_VOLUME:
            continue

        promising.append({
            "name": token["baseToken"]["name"],
            "symbol": token["baseToken"]["symbol"],
            "url": token["url"],
            "liquidity": token["liquidity"]["usd"],
            "volume": token["volume"]["h24"],
            "fdv": token["fdv"],
        })

    return promising
