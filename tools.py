import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_current_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    # Using metric units to get Celsius and m/s
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Extract ALL granular metrics that the elite agent needs
            structured_weather = {
                "weather_main": data["weather"][0]["main"],
                "weather_description": data["weather"][0]["description"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "wind_speed": data["wind"]["speed"],
                "clouds_all": data["clouds"]["all"]
            }
            # Return as a clean JSON string so the LLM can parse it perfectly
            return json.dumps(structured_weather)
        else:
            return f"Error: Cannot find city '{city}' or API issue."
    except Exception as e:
        return f"Error occurred: {str(e)}"