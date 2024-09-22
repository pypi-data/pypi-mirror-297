import asyncio

from gameeapi import GameeAPIClient

async def main() -> None:
    gamee_api_client: GameeAPIClient = GameeAPIClient()
    
    game_url: str = "https://prizes.gamee.com/game-bot/OmRJ0j4lO-bcf6a352391131111e37abd89467fa835d10c090#tgShareScoreUrl=tgb%3A%2F%2Fshare_game_score%3Fhash%3DRSwinLWpQNUlQzxtmBFS"
    auth_token: str = await gamee_api_client.auth_user(game_url)
    print(auth_token)
    auth_token = auth_token['result']['tokens']["authenticate"]
    return
    #auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIxNzI2OTc3MDY4IiwidXNlcklkIjoxMDExNDUyMzAsImluc3RhbGxVdWlkIjoiNjRlYWI3OTgtMzI1Yy00NDEzLWJiOWQtOTI0OGY0MDYwYzdjIiwidHlwZSI6ImF1dGhlbnRpY2F0aW9uVG9rZW4iLCJhdXRob3JpemF0aW9uTGV2ZWwiOiJib3QiLCJwbGF0Zm9ybSI6ImJvdC10ZWxlZ3JhbSJ9.eSRz-yP3ROCADIOq0N8Ydm_0m2iXOG_fsUEHb4R7tk8"
    
    print(await gamee_api_client.save_web_gameplay(auth_token, game_url, 300, 300))

asyncio.run(main())