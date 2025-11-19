from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("GEOAPIFY_API_KEY")

import requests
from api.maps import geocode_city


def get_places(city):
    """
    Fetch popular places around the given city using Geoapify.
    Returns {"city": city, "places": [...]}
    Geoapify does NOT provide images, so image=None.
    """

    lat, lon = geocode_city(city)

    # Correct categories (OR syntax, not commas)
    url = (
        "https://api.geoapify.com/v2/places?"
        "categories=tourism.attraction|entertainment|leisure.park|heritage|natural"
        f"&filter=circle:{lon},{lat},6000"
        f"&bias=proximity:{lon},{lat}"
        "&limit=12"
        f"&apiKey={API_KEY}"
    )

    response = requests.get(url).json()

    places = []
    for item in response.get("features", []):
        props = item.get("properties", {})
        name = props.get("name", "Unknown Place")

        # Geoapify does not provide images → always fallback to default in UI
        places.append({
            "name": name,
            "image": None
        })

    return {
        "city": city,
        "places": places
    }
