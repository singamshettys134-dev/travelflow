# api/hotels.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEOAPIFY_API_KEY")

from api.places import geocode_city


def get_hotels(city):
    """
    Get hotels near a city using Geoapify Places API.
    """
    lat, lon = geocode_city(city)

    if lat is None:
        return {"city": city, "hotels": []}

    url = (
        "https://api.geoapify.com/v2/places?"
        "categories=accommodation.hotel,accommodation.hostel,accommodation.motel&"
        f"filter=circle:{lon},{lat},8000&"
        f"bias=proximity:{lon},{lat}&"
        "limit=20&"
        f"apiKey={API_KEY}"
    )

    r = requests.get(url).json()

    hotels = []
    for item in r.get("features", []):
        props = item.get("properties", {})
        name = props.get("name", "Unknown Hotel")
        hotels.append({"name": name})

    return {"city": city, "hotels": hotels[:5]}  # top 5 hotels
