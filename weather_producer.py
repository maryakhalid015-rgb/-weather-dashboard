import json
import time
import requests
import os
from kafka import KafkaProducer

API_KEY = "ea8fc90790cd4dfaa51204945261003"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

url = "https://api.weatherapi.com/v1/current.json"

while True:
    # ✅ READ SELECTED CITY FROM FILE
    if os.path.exists("selected_city.txt"):
        with open("selected_city.txt", "r") as f:
            CITY = f.read().strip()
    else:
        CITY = "Ajman"  # default

    print("Current city:", CITY)

    response = requests.get(url, params={
        "key": API_KEY,
        "q": CITY
    })

    data = response.json()

    weather_message = {
        "city": data["location"]["name"],
        "temperature": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"],
        "feelslike_c": data["current"]["feelslike_c"],
        "humidity": data["current"]["humidity"],
        "wind_kph": data["current"]["wind_kph"],
        "pressure_mb": data["current"]["pressure_mb"],
        "cloud": data["current"]["cloud"],
        "uv": data["current"]["uv"]
    }

    producer.send("weather-topic", weather_message)
    print("sent:", weather_message)

    time.sleep(5)

producer.flush()