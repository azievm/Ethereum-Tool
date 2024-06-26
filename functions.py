import requests
import json
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

API_TOKEN = config["Alchemy"]["api_token"]
WEI_IN_ETH = 1000000000000000000


def get_balance_address(address):

    url = f"https://eth-mainnet.g.alchemy.com/v2/{API_TOKEN}"

    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "params": [address, "latest"],
        "method": "eth_getBalance"
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    result = int(json.loads(response.text)["result"], 16) / WEI_IN_ETH

    return result
