import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_current_weather(city: str) -> str:
    """Fetch real-time weather details for a given city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") == 200:
            condition = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"Weather in {city}: {condition}, Temperature: {temp}°C."
        return f"Error: City '{city}' not found."
    except Exception as e:
        return f"API Connection Error: {str(e)}"

if __name__ == "__main__":
    # Local quick test
    print(get_current_weather("Auckland"))