import requests
import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)

def get_places(city):
    api_key = os.getenv("FOURSQUARE_API_KEY")

    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }

    params = {
        "query": "tourist attraction",
        "near": city,
        "limit": 10
    }

    data = requests.get(url, headers=headers, params=params).json()

    places = []
    for item in data.get("results", []):
        name = item.get("name")
        if name:
            places.append(name)

    if not places:
        places = ["No tourist places found"]

    return {"city": city, "places": places[:5]}
