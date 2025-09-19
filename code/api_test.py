# import libraries necessary

import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("api_key")

def coin(api: str,url: str):

    querystring = {"vs_currency":"usd","from":"1755708009","to":"1758300009"}
    headers = { 'x-cg-demo-api-key': api }
    response = requests.get(url, headers= headers, params = querystring)

    if response.status_code == 200:
        data = response.json()
        print(f"historical data {data}")
    else:
        print("Failed to retrieve data")



coin(api_key, "https://api.coingecko.com/api/v3/coins//market_chart/range")

