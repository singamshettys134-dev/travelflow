import random

UNSPLASH_URL = "https://source.unsplash.com/1600x900/?"

def get_place_image(name):
    q = name.replace(" ", "+")
    return f"{UNSPLASH_URL}{q},travel"

def get_hotel_image(name):
    q = name.replace(" ", "+")
    return f"{UNSPLASH_URL}{q},hotel"
