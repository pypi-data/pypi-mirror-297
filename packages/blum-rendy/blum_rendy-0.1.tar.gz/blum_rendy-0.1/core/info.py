import requests
from core.headers import headers
from core.logging_config import log

def get_info(token, proxies=None):
    url = "https://game-domain.blum.codes/api/v1/user/balance"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        balance = float(data["availableBalance"])
        ticket = data["playPasses"]

        log(f"Balance: {balance:,}")
        return ticket
    except Exception as e:
        log(f"Error getting info: {e}")
        return None
