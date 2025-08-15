import requests
import os

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(lat, lon):
    if not WEATHER_API_KEY:
        return "⚠️ Weather API key is not set."

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return "🌧 Could not fetch weather data."

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        city = data["name"]

        return f"🌦 Weather in {city}: {weather}, {temp}°C"

    except Exception as e:
        print(f"[Weather Fetch Error] {e}")
        return "⚠️ Failed to get weather info."
