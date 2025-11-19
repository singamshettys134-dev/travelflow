# ui/app.py

import sys
import os

# Allow Streamlit to import backend folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load .env correctly
from dotenv import load_dotenv
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)
API_KEY = os.getenv("GEOAPIFY_API_KEY")

import streamlit as st
from agents.planner import TravelPlannerAgent


# =========================================================
# DEFAULT IMAGES (shown when Geoapify returns no photos)
# =========================================================
DEFAULT_HOTEL_IMAGE = "https://cdn-icons-png.flaticon.com/512/2173/2173665.png"
DEFAULT_PLACE_IMAGE = "https://cdn-icons-png.flaticon.com/512/854/854878.png"
# Small clean vector icons


# ---- GLOBAL CSS THEME ----
st.set_page_config(page_title="TravelFlow", layout="centered")

st.markdown("""
<style>
body { background-color: #F7F9FA; }
.card {
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #e6e6e6;
    background: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}
.small { font-size: 0.9rem; color: #666; }
</style>
""", unsafe_allow_html=True)


# ---- HEADER ----
st.markdown("<h1 style='text-align:center;'>🌍 TravelFlow</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#666; margin-top:-12px;'>AI-powered day-by-day travel plans</h4>", unsafe_allow_html=True)
st.write("")


# ---- INPUTS ----
st.markdown("<h5 style='text-align:center;'>Enter a City to Begin Your Journey</h5>", unsafe_allow_html=True)

city = st.text_input("", placeholder="Example: Paris, Tokyo, Mumbai", key="city_input")

# number of days input
days = st.number_input("Trip length (days)", min_value=1, max_value=14, value=3, step=1)

# Center button
col1, col2, col3 = st.columns([1,2,1])
with col2:
    clicked = st.button("Plan Trip", use_container_width=True)


# ---- MAIN LOGIC ----
if clicked:
    with st.spinner("✈️ Planning your trip, please wait..."):
        agent = TravelPlannerAgent()
        result = agent.plan_trip(city, days=days)

    # Two columns for weather & places
    col_left, col_right = st.columns(2)

    # -----------------------------------------------------
    # WEATHER
    # -----------------------------------------------------
    with col_left:
        st.markdown("<div class='card'><h3>🌤️ Weather</h3></div>", unsafe_allow_html=True)
        weather = result.get("weather", {})
        st.write(f"**Temperature:** {weather.get('temperature', 'N/A')} °C")
        st.write(f"**Condition:** {weather.get('weather', 'N/A')}")
        st.write(f"**Humidity:** {weather.get('humidity', 'N/A')}%")

    # -----------------------------------------------------
    # POPULAR PLACES (with default fallback image)
    # -----------------------------------------------------
    with col_right:
        st.markdown("<div class='card'><h3>🏙️ Popular Places</h3></div>", unsafe_allow_html=True)

        for place in result.get("places", []):
            image_url = place.get("image")
            if not image_url:
                image_url = DEFAULT_PLACE_IMAGE

            st.markdown(f"""
                <div class='card'>
                    <img src="{image_url}" width="100%" style="border-radius:8px;">
                    <h4 style="margin-bottom:6px;">{place.get('name')}</h4>
                </div>
            """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # HOTELS (with default fallback image)
    # -----------------------------------------------------
    st.markdown("<div class='card' style='margin-top:12px;'><h3>🏨 Hotels</h3></div>", unsafe_allow_html=True)

    for hotel in result.get("hotels", []):
        image_url = hotel.get("image")
        if not image_url:
            image_url = DEFAULT_HOTEL_IMAGE

        st.markdown(f"""
            <div class='card' style='display:flex; gap:12px; align-items:center;'>
                <img src="{image_url}" width="120px" style="border-radius:8px;">
                <div>
                    <h4 style="margin-bottom:4px;">{hotel.get('name')}</h4>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # ITINERARY
    # -----------------------------------------------------
    st.markdown("<div class='card' style='margin-top:14px;'><h3>🗺️ Itinerary</h3></div>", unsafe_allow_html=True)
    itinerary = result.get("itinerary", {}).get("days", [])

    for day_block in itinerary:
        st.markdown(f"### Day {day_block.get('day')}")
        for item in day_block.get("items", []):
            start = item.get("start", "")
            end = item.get("end", "")
            duration = item.get("duration_min", 0)
            notes = item.get("notes", "")
            st.markdown(f"- **{start} - {end}** — **{item.get('name')}**  \n  _{duration} min_ • {notes}")
        st.write("")  # spacing
