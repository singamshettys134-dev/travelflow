import requests
import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)

def get_hotels(city):
    api_key = os.getenv("FOURSQUARE_API_KEY")

    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }

    params = {
        "query": "hotel",
        "near": city,
        "limit": 10
    }

    data = requests.get(url, headers=headers, params=params).json()

    hotels = []
    for item in data.get("results", []):
        name = item.get("name", "Unknown Hotel")
        hotels.append({"name": name})

    if not hotels:
        hotels = [{"name": "No hotels found"}]

    return {"city": city, "hotels": hotels[:5]}
