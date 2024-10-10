import requests


# Base URL for OpenWeatherMap API
API_ROOT = 'https://api.openweathermap.org/data/2.5/weather'
API_KEY = '16cf292eb35b138a4049f9a4358b7a89'  # Replace with your actual
# OpenWeatherMap API key


def fetch_weather(query):
    """Fetch weather for a given location from
    OpenWeatherMap."""
    params = {
        'q': query,            # City name
        'appid': API_KEY,      # API key
        'units': 'metric'      # Get temperature in Celsius
    }
    response = requests.get(API_ROOT, params=params)
    return response.json()


def display_weather(weather):
    """Display weather information."""
    if weather.get('cod') != 200:
        print(f"Error: {weather.get('message', 'Unknown error')}")
        return

    city = weather['name']
    country = weather['sys']['country']
    temp = weather['main']['temp']
    temp_min = weather['main']['temp_min']
    temp_max = weather['main']['temp_max']
    weather_state = weather['weather'][0]['description']

    print(f"Weather for {city}, {country}:")
    print(f"Condition: {weather_state.capitalize()}")
    print(f"Current Temperature: {temp:.1f}°C")
    print(f"High: {temp_max:.1f}°C\tLow: {temp_min:.1f}°C")


def weather_dialog():
    """Prompt user for location and display the weather."""
    try:
        where = ''
        while not where:
            where = input("Where in the world are you? ")
        weather = fetch_weather(where)
        display_weather(weather)
    except requests.exceptions.ConnectionError:
        print("Couldn't connect to the server! Is the network up?")


if __name__ == '__main__':
    while True:
        weather_dialog()
