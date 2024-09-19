import requests
import random
import time

from core.headers import headers
from core.info import get_info
from core.token import get_token

from core.logging_config import log

def play_game(token, proxies=None):
    url = "https://game-domain.blum.codes/api/v1/game/play"

    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        game_id = data["gameId"]
        return game_id
    except:
        return None


def claim_game(token, game_id, point, proxies=None):
    url = "https://game-domain.blum.codes/api/v1/game/claim"
    payload = {"gameId": game_id, "points": point}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.text
        return data
    except:
        return None


def process_play_game(data, proxies=None):
    while True:
        token = get_token(data=data, proxies=proxies)
        ticket = get_info(token=token, proxies=proxies)
        if ticket is None:
            log(f"Auto Play Game: Ticket data not found")
            break

        if ticket > 0:
            log(f"Available tickets: {ticket}")
            game_id = play_game(token=token, proxies=proxies)
            if game_id:
                log(f"Playing for 30 seconds...")
                time.sleep(30)
                point = random.randint(250, 300)
                claim = claim_game(
                    token=token, game_id=game_id, point=point, proxies=proxies
                )
                if "OK" in claim:
                    log(
                        f"Auto Play Game: Success | Added {point} points"
                    )
                else:
                    log(f"Auto Play Game: Claim Point Fail")
                    break
            else:
                log(f"Auto Play Game: Game ID not Found")
                break
        else:
            log(f"Auto Play Game: No ticket available")
            break