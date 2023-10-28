import aiohttp
import asyncio
import json

jwt = "{YOUR_JWT_TOKEN}"
url = "https://api.testnet.myriad.social/"
headers = {"Authorization": f"Bearer {jwt}"}

async def sleep(ms):
    await asyncio.sleep(ms / 1000)  # convert ms to seconds

async def login(token):
    async with aiohttp.ClientSession() as session:
        endpoint = f"{url}authentication/login/pat"
        payload = {"token": token}
        async with session.post(endpoint, json=payload) as resp:
            return await resp.json()

async def generate():
    async with aiohttp.ClientSession() as session:
        endpoint = f"{url}user/personal-admin-access-tokens"
        async with session.get(endpoint, headers=headers) as resp:
            return await resp.json()

async def revoke(token):
    async with aiohttp.ClientSession() as session:
        endpoint = f"{url}user/personal-access-tokens/{token}"
        async with session.delete(endpoint, headers=headers) as resp:
            return await resp.json()

async def main():
    try:
        resp = await generate()
        token = resp.get("id", None)
        print(f"Token is {token}")

        print("Logging in with token")
        resp = await login(str(token))
        print(resp)
        print("Login successful")

        resp = await revoke(token)
        print("Revoking successful")

        await sleep(3000)

        resp = await login(str(token))
        print(resp)
    except Exception as e:
        print("An error occurred")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
