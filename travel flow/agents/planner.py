# agents/planner.py
import os
from dotenv import load_dotenv

# Force-load the .env from the project root (works inside nested folders / streamlit)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)

from api.weather import get_weather
from api.places import get_places
from api.hotels import get_hotels
from api.images import get_place_image, get_hotel_image
from agents.itinerary import ItineraryAgent

class TravelPlannerAgent:
    """
    Travel planner that fetches weather, places, hotels and builds an itinerary.
    Accepts a `days` argument so UI can request a multi-day plan.
    """

    def plan_trip(self, city, days=3):
        # Defensive: normalize inputs
        if not city:
            city = "Unknown"

        # Fetch raw data
        weather = get_weather(city) or {}
        places_raw = get_places(city) or {"places": []}
        hotels_raw = get_hotels(city) or {"hotels": []}

        # Normalize places to list of dicts {name, image}
        places_list = []
        for p in places_raw.get("places", []):
            if isinstance(p, dict) and "name" in p:
                name = p["name"]
            else:
                name = p
            places_list.append({
                "name": name,
                "image": get_place_image(name)
            })

        # Normalize hotels to list of dicts {name, image}
        hotels_list = []
        for h in hotels_raw.get("hotels", []):
            if isinstance(h, dict) and "name" in h:
                hname = h["name"]
            else:
                hname = h
            hotels_list.append({
                "name": hname,
                "image": get_hotel_image(hname)
            })

        # Generate itinerary using the ItineraryAgent
        itinerary_agent = ItineraryAgent()
        itinerary = itinerary_agent.generate_itinerary(city, places_list, hotels_list, days=days)

        # Final combined result
        return {
            "city": city,
            "weather": weather,
            "places": places_list,
            "hotels": hotels_list,
            "itinerary": itinerary
        }