import requests
from datetime import datetime, timedelta

# City to Timezone mapping (You can expand this for more cities)
city_to_timezone = {
    "london": "Europe/London",
    "new york": "America/New_York",
    "tokyo": "Asia/Tokyo",
    "sydney": "Australia/Sydney",
    "paris": "Europe/Paris"
}

# WorldTimeAPI - Get time zone data for a specific location
def fetch_world_time_api(timezone: str):
    try:
        url = f'http://worldtimeapi.org/api/timezone/{timezone}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['datetime'], data['timezone']
        else:
            print(f"Invalid location for WorldTimeAPI: {timezone}")
            return None, None
    except Exception as e:
        print(f"Error fetching from WorldTimeAPI: {e}")
        return None, None

# TimeZoneDB API - Get current time for a specific time zone
def fetch_timezone_db_api(api_key: str, zone: str):
    try:
        url = f'http://api.timezonedb.com/v2.1/get-time-zone?key={api_key}&format=json&by=zone&zone={zone}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['formatted'], data['zoneName']
        else:
            print(f"Invalid location for TimeZoneDB API: {zone}")
            return None, None
    except Exception as e:
        print(f"Error fetching from TimeZoneDB: {e}")
        return None, None

# OpenWeatherMap Time API (requires location coordinates)
def fetch_openweather_api(api_key: str, lat: float, lon: float):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            timezone_offset = data['timezone']  # Timezone offset in seconds
            current_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
            return current_time.strftime("%Y-%m-%d %H:%M:%S"), data['name']
        else:
            print(f"Invalid coordinates for OpenWeatherMap API: {lat}, {lon}")
            return None, None
    except Exception as e:
        print(f"Error fetching from OpenWeatherMap API: {e}")
        return None, None

# Function to allow user input for a location and fetch the time
def get_time_for_location():
    # Ask user to input a location
    location = input("Enter the location (city, timezone, or coordinates): ").lower().strip()

    # Check if the location is a known city
    if location in city_to_timezone:
        timezone = city_to_timezone[location]
        print(f"Recognized city: {location.capitalize()} mapped to timezone: {timezone}")
    else:
        timezone = location  # Assuming the user entered a valid timezone or coordinates directly

    # WorldTimeAPI Example
    print("\nFetching time from WorldTimeAPI...")
    time1, zone1 = fetch_world_time_api(timezone)
    if time1:
        print(f"WorldTimeAPI: {zone1} - {time1}")
    else:
        print(f"Could not fetch time for {location} from WorldTimeAPI.")

    # TimeZoneDB API Example
    print("\nFetching time from TimeZoneDB API...")
    api_key_tzdb = 'your_timezone_db_api_key'  # replace with your TimeZoneDB API key
    time2, zone2 = fetch_timezone_db_api(api_key_tzdb, timezone)
    if time2:
        print(f"TimeZoneDB API: {zone2} - {time2}")
    else:
        print(f"Could not fetch time for {location} from TimeZoneDB API.")

    # OpenWeatherMap API Example (if coordinates are given, e.g., lat, lon)
    try:
        lat, lon = map(float, location.split(','))
        print("\nFetching time from OpenWeatherMap API...")
        api_key_owm = 'your_openweather_api_key'  # replace with your OpenWeatherMap API key
        time3, city_name = fetch_openweather_api(api_key_owm, lat, lon)
        if time3:
            print(f"OpenWeatherMap: {city_name} - {time3}")
        else:
            print(f"Could not fetch time for coordinates {lat}, {lon} from OpenWeatherMap API.")
    except ValueError:
        print("\nInvalid coordinates format, skipping OpenWeatherMap fetch.")

# Main function call
get_time_for_location()
