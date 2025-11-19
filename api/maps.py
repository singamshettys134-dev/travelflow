# api/maps.py
from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.getenv("GEOAPIFY_API_KEY")

def geocode_city(city: str):
    """
    Return (lat, lon) for a city using Geoapify geocoding API.
    Returns (None, None) if not found or on error.
    """
    if not API_KEY:
        raise RuntimeError("GEOAPIFY_API_KEY not set in .env")

    url = f"https://api.geoapify.com/v1/geocode/search?text={city}&limit=1&apiKey={API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None, None

    features = data.get("features", [])
    if not features:
        return None, None

    props = features[0].get("properties", {})
    # Geoapify returns lat and lon in properties
    return props.get("lat"), props.get("lon")