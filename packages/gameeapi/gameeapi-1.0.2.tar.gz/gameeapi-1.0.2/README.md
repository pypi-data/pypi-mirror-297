# gameeapi

An unofficial API wrapper for gamee.com written in Python.

# Installation

Installing through pip:
```bash
pip install gameeapi
```

Installing through source:
```bash
git clone https://github.com/zrekryu/gameeapi.git
cd gameeapi
pip install .
```

# Gamee API

## Initializing API Client

To initialize the API Client:
```py
from gameeapi import GameeAPIClient

client: GameeAPIClient = GameeAPIClient()
```

## Version Information

To print the version of the `gameeapi` library:
```py
from gameeapi import __version__

print(__version__)
```

## Authorizing user

To authorize the user:
```py
from typing import Any

game_url: str = "<game-url>"
auth_data: dict[str, Any] = await client.auth_user(game_url)

Print the authentication token and save it for later use.
print("Authentication Token:", auth_data["result"]["tokens"]["authenticate"])
```

## Get Web Gameplay Details

To retrieve web gameplay details:
```py
game_url: str = "<game-url>"
gameplay_details: dict[str, Any] = await client.get_web_gameplay_details(game_url)
print(gameplay_details)
```

## Get Geographical Block Status

To retrieve geographical block status:
```py
auth_token: str = "<auth-token>"
geo_block_status: dict[str, Any] = await client.get_geo_block_status(auth_token)
print(geo_block_status)
```

## Get Web Surrounding by Game

To get web surrounding by the game:
```py
game_url: str = "<game-url>"
auth_token: str = "<auth-token>"
game_surrounding: dict[str, Any] = await client.get_web_surrounding_by_game(auth_token, game_url)
print(game_surrounding)
```

## Save Web Gameplay

To save web gameplay score:
```py
auth_token: str = "<auth-token>"
game_url: str = "<game-url>"
score: int = 100
play_time: int = 120

gameplay_data: dict[str, Any] = await client.save_web_gameplay(auth_token, game_url, score, play_time)
print(gameplay_data)
```

# License

© 2024 Zrekryu. Licensed under MIT License. See the LICENSE file for details.