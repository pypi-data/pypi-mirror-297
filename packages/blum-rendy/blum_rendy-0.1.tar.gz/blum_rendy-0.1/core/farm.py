import requests
from core.headers import headers
from core.logging_config import log

def start_farming(token, proxies=None):
    url = "https://game-domain.blum.codes/api/v1/farming/start"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except Exception as e:
        log(f"Error starting farming: {e}")
        return None

def claim_farming(token, proxies=None):
    url = "https://game-domain.blum.codes/api/v1/farming/claim"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except Exception as e:
        log(f"Error claiming farming: {e}")
        return None

def process_farming(token, proxies=None):
    process_claim = claim_farming(token=token, proxies=proxies)
    try:
        balance = float(process_claim["availableBalance"])
        log(f"Auto Farm: Claim Success | New balance: {balance:,} points")
    except Exception as e:
        message = process_claim.get("message", "Unknown error")
        log(f"Auto Farm: Claim Error | {message}")

    process_start = start_farming(token=token, proxies=proxies)
    try:
        farmed = float(process_start["balance"])
        if farmed > 0:
            log(f"Auto Farm: Farming | Farmed point: {farmed:,} points")
        else:
            log("Auto Farm: Start Farming Success")
    except Exception as e:
        log(f"Error processing farming: {e}")
