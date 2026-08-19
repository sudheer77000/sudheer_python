import sys
import json
import requests
import ollama

# ==========================================
# CONFIGURATION
# ==========================================
# Get a free API key at https://www.weatherapi.com/
WEATHER_API_KEY = "YOUR_WEATHER_API_KEY"  
OLLAMA_MODEL = "qwen2.5:3b"

def fetch_live_weather(location: str, date_str: str = None) -> dict:
    """
    Fetches live weather or forecast data from WeatherAPI.com.
    - If date_str is provided (YYYY-MM-DD), fetches forecast/future data.
    - If date_str is None, fetches real-time current weather.
    """
    if date_str:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&dt={date_str}&days=1"
    else:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to fetch weather data: {e}")
        return None

def parse_weather_data(data: dict) -> str:
    """
    Parses the raw JSON payload and extracts key travel metrics.
    """
    loc = data.get("location", {})
    city = loc.get("name", "Unknown Location")
    region = loc.get("region", "")
    country = loc.get("country", "")
    local_time = loc.get("localtime", "Unknown Time")

    # Check if payload contains forecast data or current data
    forecast_list = data.get("forecast", {}).get("forecastday", [])
    
    if forecast_list:
        day_info = forecast_list[0].get("day", {})
        condition = day_info.get("condition", {}).get("text", "Unknown")
        temp_c = day_info.get("avgtemp_c")
        temp_f = day_info.get("avgtemp_f")
        humidity = day_info.get("avghumidity")
        rain_chance = day_info.get("daily_chance_of_rain", 0)
        max_wind_kph = day_info.get("maxwind_kph")
        
        summary = (
            f"Location: {city}, {region}, {country}\n"
            f"Date: {local_time}\n"
            f"Forecasted Weather: {condition}\n"
            f"Avg Temperature: {temp_c}°C ({temp_f}°F)\n"
            f"Avg Humidity: {humidity}%\n"
            f"Chance of Rain: {rain_chance}%\n"
            f"Max Wind Speed: {max_wind_kph} km/h"
        )
    else:
        current = data.get("current", {})
        condition = current.get("condition", {}).get("text", "Unknown")
        temp_c = current.get("temp_c")
        temp_f = current.get("temp_f")
        humidity = current.get("humidity")
        rain_chance = current.get("chance_of_rain", 0)
        wetbulb_f = current.get("wetbulb_f", "N/A")
        
        summary = (
            f"Location: {city}, {region}, {country}\n"
            f"Date/Time: {local_time}\n"
            f"Current Weather: {condition}\n"
            f"Temperature: {temp_c}°C ({temp_f}°F)\n"
            f"Humidity: {humidity}%\n"
            f"Chance of Rain: {rain_chance}%\n"
            f"Wet-Bulb Temp: {wetbulb_f}°F"
        )

    return summary

def analyze_with_ollama(summary_text: str, model_name: str = OLLAMA_MODEL) -> str:
    """
    Sends the weather summary to Ollama for evaluation and decision making.
    """
    system_prompt = """You are a professional, pragmatic travel adviser. I will provide Location, Date, and Weather Conditions for a planned trip/program. 
Your task is to analyze these factors and determine whether to proceed with the program/trip.

Consider how the weather impacts outdoor activities, packing logistics, safety, and general comfort during that specific time of year.

Respond strictly using the following format and nothing else:
RATING: [Score]/10
ANALYSIS: [2-3 short sentences explaining the pros and cons of traveling in these conditions]
VERDICT: [Choose one: Highly Recommended, Pack Strategically, or Reschedule]"""

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": summary_text}
            ],
            options={"temperature": 0.2}
        )
        return response["message"]["content"]
    except Exception as e:
        return f"[Error] Ollama processing failed: {e}\nEnsure Ollama is running and '{model_name}' is pulled."

def main():
    print("=== Live Weather Travel Decision Pipeline ===")
    
    # Take user inputs
    location_input = input("Enter City/Location (e.g., Abdullahpur, London): ").strip()
    date_input = input("Enter Date (YYYY-MM-DD) or press Enter for current live weather: ").strip()
    
    target_date = date_input if date_input else None

    # Step 1: Call Live Weather API
    print("\n[1/3] Calling Weather API for live data...")
    raw_weather = fetch_live_weather(location_input, target_date)
    
    if not raw_weather or "error" in raw_weather:
        print("[!] Execution stopped. Could not retrieve weather data.")
        return

    # Step 2: Extract key metrics
    print("[2/3] Extracting key metrics...")
    weather_summary = parse_weather_data(raw_weather)
    print("\n--- Weather Summary ---")
    print(weather_summary)
    print("------------------------\n")

    # Step 3: Run analysis with Ollama
    print(f"[3/3] Sending data to Ollama ({OLLAMA_MODEL})...")
    advisory = analyze_with_ollama(weather_summary)

    print("\n" + "=" * 40)
    print("         TRIP ADVISOR VERDICT        ")
    print("=" * 40)
    print(advisory)
    print("=" * 40)

if __name__ == "__main__":
    main()