# agents/itinerary.py
from datetime import timedelta, datetime

class ItineraryAgent:
    """
    Simple itinerary generator.
    Distributes places across the requested number of days,
    produces time slots, approximate durations and travel-time estimates.
    """

    def __init__(self):
        # heuristic durations (in minutes) by simple category assumptions
        self.default_duration_min = 90  # default 1.5 hours
        self.museum_duration_min = 120
        self.sight_duration_min = 90
        self.park_duration_min = 60
        self.travel_between_min = 20  # assumed average travel time between spots

    def _estimate_duration(self, place_name):
        """Heuristic: choose duration based on keywords in the name."""
        name = place_name.lower()
        if "museum" in name or "gallery" in name:
            return self.museum_duration_min
        if "park" in name or "garden" in name:
            return self.park_duration_min
        if "tower" in name or "bridge" in name or "monument" in name or "temple" in name:
            return self.sight_duration_min
        return self.default_duration_min

    def generate_itinerary(self, city, places, hotels, days=3):
        """
        Generates a simple day-by-day itinerary.

        Args:
            city (str)
            places (list of dict) each dict: {"name": ..., "image": ...}
            hotels (list of dict) each dict: {"name": ..., "image": ...}
            days (int)

        Returns:
            dict: { "days": [ { "day": 1, "items": [ {name, start, end, duration_min, notes} ] }, ... ] }
        """
        days = max(1, int(days or 3))
        # Flatten place names
        place_names = [p["name"] for p in places][: max(1, len(places))]
        if not place_names:
            return {"days": [{"day": 1, "items": [{"name": "No places available", "start": "", "end": "", "duration_min": 0, "notes": ""}]}]}

        # Distribute places across days fairly
        schedule = []
        per_day = max(1, len(place_names) // days)
        remainder = len(place_names) % days

        idx = 0
        for d in range(1, days + 1):
            items = []
            # Morning start time 09:00 local (naive)
            current_time = datetime.strptime("09:00", "%H:%M")
            slots_today = per_day + (1 if remainder > 0 else 0)
            if remainder > 0:
                remainder -= 1

            for s in range(slots_today):
                if idx >= len(place_names):
                    break
                pname = place_names[idx]
                duration = self._estimate_duration(pname)
                start = current_time.strftime("%H:%M")
                end_time = current_time + timedelta(minutes=duration)
                end = end_time.strftime("%H:%M")

                notes = f"Suggested visit to {pname}. Spend ~{duration//60}h {duration%60}m. Travel ~{self.travel_between_min} minutes to next."
                items.append({
                    "name": pname,
                    "start": start,
                    "end": end,
                    "duration_min": duration,
                    "notes": notes
                })

                # increment time: travel + buffer
                current_time = end_time + timedelta(minutes=self.travel_between_min)
                idx += 1

            # Add an evening recommendation: dinner or hotel check-in
            hotel_name = hotels[0]["name"] if hotels and len(hotels) > 0 else "Recommended hotel"
            items.append({
                "name": f"Evening / Dinner near {hotel_name}",
                "start": current_time.strftime("%H:%M"),
                "end": (current_time + timedelta(minutes=90)).strftime("%H:%M"),
                "duration_min": 90,
                "notes": f"Relax at {hotel_name} or explore nearby dining options."
            })

            schedule.append({"day": d, "items": items})

        return {"days": schedule}
