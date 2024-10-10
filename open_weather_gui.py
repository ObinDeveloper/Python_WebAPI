import tkinter as tk
from tkinter import messagebox
import requests

# Base URL for OpenWeatherMap API
API_ROOT = 'https://api.openweathermap.org/data/2.5/weather'
API_KEY = '16cf292eb35b138a4049f9a4358b7a89'  # Replace with your actual OpenWeatherMap API key


def fetch_weather(query):
    """Fetch weather for a given location from OpenWeatherMap."""
    params = {
        'q': query,            # City name
        'appid': API_KEY,      # API key
        'units': 'metric'      # Get temperature in Celsius
    }
    response = requests.get(API_ROOT, params=params)
    return response.json()


def display_weather(weather):
    """Update the labels with weather information."""
    if weather.get('cod') != 200:
        messagebox.showerror("Error", f"Error: {weather.get('message', 'Unknown error')}")
        return

    city = weather['name']
    country = weather['sys']['country']
    temp = weather['main']['temp']
    temp_min = weather['main']['temp_min']
    temp_max = weather['main']['temp_max']
    weather_state = weather['weather'][0]['description']

    weather_info_label['text'] = f"Weather for {city}, {country}:\n"
    condition_label['text'] = f"Condition: {weather_state.capitalize()}"
    temperature_label['text'] = f"Current Temperature: {temp:.1f}°C"
    high_low_label['text'] = f"High: {temp_max:.1f}°C\tLow: {temp_min:.1f}°C"


def fetch_and_display_weather():
    """Fetch and display the weather for the entered location."""
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return

    try:
        weather = fetch_weather(city)
        display_weather(weather)
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Connection Error", "Couldn't connect to the server! Is the network up?")

# Create the main application window


app = tk.Tk()
app.title("Weather App")
app.geometry("400x300")
app.configure(bg='#f0f0f0')  # Light gray background

# Create and place the widgets in the window
tk.Label(app, text="Enter City:", font=("Arial", 12)).pack(pady=10)

city_entry = tk.Entry(app, font=("Arial", 14), width=30)
city_entry.pack(pady=5)

fetch_button = tk.Button(app, text="Fetch Weather", font=("Arial", 12), command=fetch_and_display_weather)
fetch_button.pack(pady=10)

# Labels to display the weather information
weather_info_label = tk.Label(app, text="", font=("Arial", 14), bg='#f0f0f0')
weather_info_label.pack(pady=10)

condition_label = tk.Label(app, text="", font=("Arial", 12), bg='#f0f0f0')
condition_label.pack(pady=5)

temperature_label = tk.Label(app, text="", font=("Arial", 12), bg='#f0f0f0')
temperature_label.pack(pady=5)

high_low_label = tk.Label(app, text="", font=("Arial", 12), bg='#f0f0f0')
high_low_label.pack(pady=5)

# Start the application's main loop
app.mainloop()
