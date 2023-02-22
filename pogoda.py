import requests
from requests import get
import json

from geopy.geocoders import Nominatim


def oras(oras1):
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(oras1)
    return temperatura(f"{location.latitude}, {location.longitude}")


def get_geo_location_from_ip(ip):
    response = requests.get(
        f"http://api.ipstack.com/{ip}?access_key=" + get_api_key("ipstack")
    )
    data = response.json()
    latitude = data["latitude"]
    longitude = data["longitude"]
    return latitude, longitude


def temperatura(coordinates):
    url = (
        "http://api.weatherapi.com/v1/current.json?"
        + "&key="
        + get_api_key("weatherapi")
        + "&q="
        + coordinates
    )
    weather_data = requests.get(url).json()
    country = weather_data["location"]["country"]
    name = weather_data["location"]["name"]
    temp_c = weather_data["current"]["temp_c"]
    feelslike_c = weather_data["current"]["feelslike_c"]
    humidity = weather_data["current"]["humidity"]
    # print(
    #     f"In {country}, {name} avem {temp_c}({feelslike_c})grade, cu umiditatea de {humidity}%"
    # )
    return f"""In {country}, {name} avem {temp_c}({feelslike_c})grade,
                     cu umiditatea de {humidity}%"""


def get_api_key(name):
    with open("apikey.json", "r") as f:
        keydata = json.load(f)
        for api in keydata:
            if name in api:
                return api[name]["key"]


if __name__ == "__main__":
    # print(get_api_key('ipstack'))
    # print()
    # print("Caut adresa IP externa...", end=" ")
    # ip = get("https://api.ipify.org").content.decode("utf8")
    # print(ip)
    # print("Caut coordonate dupa adresa IP...", end=" ")
    # latitude, longitude = get_geo_location_from_ip(ip)
    # print("OK")
    # temperatura(f"{latitude},{longitude}")
    # print()
    print(oras("Chisinau"))
