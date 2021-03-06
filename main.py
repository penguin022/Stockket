import pandas as pd
import googlemaps
import pprint
import time
import json
import re
from credentials import API_KEY

# Takes a long time to load the pandas df due to length of table.
groceries_db = pd.read_csv("db/Grocery_UPC_Database.csv", encoding="ISO-8859-1", index_col=0)
brands = groceries_db['brand'].tolist()
name = groceries_db['name'].tolist()

# user_loc = get_user_location()

gmaps = googlemaps.Client(key=API_KEY)


def search(query):
    """
    Use cases: search(query) will be constantly called as a query is being typed,
    resulting in autofilled results or related results through a trie data structure

    Runtime: O(n)

    Input: a search query
    Output: an output of list of related search terms
    """
    # TODO: Implement a trie data stucture to improve runtime a simple brute force method for now
    matching = [s for s in name if query in s]
    return matching


def get_user_location():
    """
    Returns the user current location (as a tuple of lat, long)
    """
    # TODO: find a way to grap user location through mobile app, device, or website
    return None


def distance(user_location, destination):
    distance_data = gmaps.distance_matrix(user_location, destination)

    distance = distance_data["rows"][0]['elements'][0]['distance']['text']

    distance = float(re.findall(r"[-+]?\d*\.\d+|\d+", distance)[0])

    return distance


def nearest_stores(user_location, radius=20000):
    """
    parameters:
    radius is 20000 meters which equates to 12.5 miles
    supported types here: https://developers.google.com/places/supported_types
    """
    # TODO: open_now set to False for debugging purposes!
    nearest_places = gmaps.places_nearby(location=user_location, radius=radius, open_now=False,
                                         type='grocery_or_supermarket')
    nearest_places_result = nearest_places["results"]

    return [(place["name"], place["vicinity"], distance(user_location, place["vicinity"])) for place in
            nearest_places_result]


test_location = (37.8712358, -122.2581406)  # TODO:Coordinates of UC Berkeley, for debugging purposes!

print(nearest_stores(test_location))
