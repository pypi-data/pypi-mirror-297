from datetime import datetime, timezone
from hashlib import md5
from json import dumps
from random import randint
from uuid import uuid4
from urllib.parse import urlparse
from typing import Any, Self

import httpx

class GameeAPIClient:
    # Source: https://prizes.gamee.com/_next/static/chunks/8499-ca20992cf722abda.js.
    """
    Gamee API Client.
    """
    
    BASE_URL: str = "https://api.gamee.com/"
    TIMEOUT: int = 30
    
    SEED: str = "crmjbjm3lczhlgnek9uaxz2l9svlfjw14npauhen"
    
    USER_AGENT: str = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    
    def __init__(self: Self, base_url: str = BASE_URL, timeout: int = TIMEOUT) -> None:
        """
        Initialize API client.
        
        Parameters:
            base_url (str, optional): The base URL of the Gamee API. Defaults to `BASE_URL`.
            timeout (int, optional): Timeout for HTTP requests to the Gamee API. Defaults to `TIMEOUT`.
        """
        self.base_url = base_url
        self.timeout = timeout
        
        self._http_client: httpx.AsyncClient = httpx.AsyncClient(timeout=self.timeout)
        
        self._uuid: str = str(uuid4())
    
    def _generate_checksum(self: Self, score: int, play_time: int, game_url_path: str) -> str:
        """
        Generates a MD5 checksum.
        
        Parameters:
            score (str): The score of the game.
            play_time (str): The gameplay time in seconds.
            game_url_path (str): The path part from the game URL.
        
        Returns:
            str: MD5 checksum.
        """
        return md5(f"{score}:{play_time}:{game_url_path}::{self._uuid}:{self.SEED}".encode("utf-8")).hexdigest()
    
    async def auth_user(self: Self, game_url: str) -> dict[str, Any]:
        """
        Authorize user through bot login.
        
        Parameters:
            game_url (str): The URL of the game.
        
        Returns:
            dict[str, Any]: Authentication data.
        
        Raises:
            httpx.HTTPError: If an HTTP error occurs.
        """
        headers: dict[str, Any] = {
            "User-Agent": self.USER_AGENT,
            "X-Install-Uuid": self._uuid
        }
        data: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": "user.authentication.botLogin",
            "method": "user.authentication.botLogin",
            "params": {
                "botGameUrl": urlparse(game_url).path,
                "botName": "telegram",
                "botUserIdentifier": None
            }
        }
        
        response: httpx.Response = await self._http_client.post(self.base_url, data=dumps(data), headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def get_web_gameplay_details(self: Self, game_url: str) -> dict[str, Any]:
        """
        Get web gameplay details.
        
        Parameters:
            game_url (str): The URL of the game.
        
        Returns:
            dict[str, Any]: Web gameplay data.
        
        Raises:
            httpx.HTTPError: If an HTTP error occurs.
        """
        headers: dict[str, Any] = {
            "User-Agent": self.USER_AGENT,
            "X-Install-Uuid": self._uuid
        }
        data: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": "game.getWebGameplayDetails",
            "method": "game.getWebGameplayDetails",
            "params": {
                "gameUrl": urlparse(game_url).path
            }
        }
        
        response: httpx.Response = await self._http_client.post(self.base_url, data=dumps(data), headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def get_geo_block_status(self: Self, auth_token: str) -> dict[str, Any]:
        """
        Get geographical block status.
        
        Parameters:
            auth_token (str): The authentication token of user.
        
        Returns:
            dict[str, Any]: Geographical block status data.
        
        Raises:
            httpx.HTTPError: If an HTTP error occurs.
        """
        headers: dict[str, Any] = {
            "User-Agent": self.USER_AGENT,
            "Authorization": f"Bearer {auth_token}",
            "X-Install-Uuid": self._uuid
        }
        data: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": "user.getGeoBlockStatus",
            "method": "user.getGeoBlockStatus",
            "params": {}
        }
        
        response: httpx.Response = await self._http_client.post(self.base_url, data=dumps(data), headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def get_web_surrounding_by_game(self: Self, auth_token: str, game_url: str) -> dict[str, Any]:
        """
        Get web surrounding by the game.
        
        Parameters:
            auth_token (str): The authentication token of user.
            game_url (str): The URL of the game.
        
        Returns:
            dict[str, Any]: Web surrounding by the game.
        
        Raises:
            httpx.HTTPError: If an HTTP error occurs.
        """
        headers: dict[str, Any] = {
            "User-Agent": self.USER_AGENT,
            "Authorization": f"Bearer {auth_token}",
            "X-Install-Uuid": self._uuid
        }
        data: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": "leaderboards.getWebSurroundingByGame",
            "method": "leaderboards.getWebSurroundingByGame",
            "params": {
                "gameUrl": game_url
            }
        }
        
        response: httpx.Response = await self._http_client.post(self.base_url, data=dumps(data), headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    async def save_web_gameplay(
        self: Self,
        auth_token: str,
        game_url: str,
        score: int,
        play_time: int
        ) -> dict[str, Any]:
        """
        Save web gameplay state.
        
        Parameters:
            auth_token (str): authentication token of user.
            game_url (str): The URL of the game.
            score (int): The score to save.
            play_time (int): The gameplay time in seconds.
        
        Returns:
            dict[str, Any] - Gameplay data.
        
        Raises:
            httpx.HTTPError: If an HTTP error occurs.
        """
        gameplay_details: dict[str, Any] = await self.get_web_gameplay_details(game_url)
        
        headers: dict[str, Any] = {
            "User-Agent": self.USER_AGENT,
            "Authorization": f"Bearer {auth_token}",
            "X-Install-Uuid": self._uuid
        }
        
        data: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": "game.saveWebGameplay",
            "method": "game.saveWebGameplay",
            "params": {
                "gameplayData": {
                    "gameId": gameplay_details["result"]["game"]["id"],
                    "score": score,
                    "playTime": play_time,
                    "gameUrl": urlparse(game_url).path,
                    "releaseNumber": gameplay_details["result"]["game"]["release"]["number"],
                    "createdTime": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z'),
                    "metadata": {
                        "gameplayId": randint(1, 500)
                    },
                    "isSaveState": False,
                    "gameStateData": None,
                    "gameplayOrigin": "game",
                    "replayData": None,
                    "replayVariant": None,
                    "replayDataChecksum": None,
                    "uuid": self._uuid,
                    "checksum": self._generate_checksum(score, play_time, urlparse(game_url).path)
                }
            }
        }
        
        response: httpx.Response = await self._http_client.post(self.base_url, data=dumps(data), headers=headers)
        response.raise_for_status()
        
        return response.json()