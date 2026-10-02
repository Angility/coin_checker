import requests

def fetch_prices(coin_ids: list[str]) -> dict:

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "vs_currencies": "usd",
        "ids": ",".join(coin_ids)
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[!] an Exception occurred while connecting the server: {e}")
        return {}

    res = {item: price["usd"] for item,price in response.json().items()}

    return res

'''
if __name__ == "__main__":

    print(f"{fetch_prices(['bitcoin','solana'])}")
'''