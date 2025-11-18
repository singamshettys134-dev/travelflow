import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city):
    """
    Returns current weather for a city using OpenWeatherMap API.
    """
    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        return {"error": "Missing OWM_API_KEY in .env file"}

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except KeyError:
        return {"error": "Unexpected response shape", "raw": data}
