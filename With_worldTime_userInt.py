import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# City to Timezone mapping
city_to_timezone = {
    "minneapolis, mn": "America/Chicago",
    "houston, tx": "America/Chicago",
    "arlington, tx": "America/Chicago",
    "abidjan, ivory coast": "Africa/Abidjan",
    "paris, france": "Europe/Paris"
}

# WorldTimeAPI - Get time zone data for a specific location
def fetch_world_time_api(timezone: str):
    try:
        url = f'http://worldtimeapi.org/api/timezone/{timezone}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Extracting datetime and formatting
            utc_time = data['datetime']
            local_time = datetime.strptime(utc_time[:19], '%Y-%m-%dT%H:%M:%S')
            formatted_time = local_time.strftime('%I:%M %p')  # 12-hour format with AM/PM
            formatted_date = local_time.strftime('%m/%d/%Y')  # MM/DD/YYYY format
            return f"{formatted_date} {formatted_time}", data['timezone']
        else:
            return None, None
    except Exception as e:
        return None, None

# TimeZoneDB API - Get current time for a specific time zone
def fetch_timezone_db_api(api_key: str, zone: str):
    try:
        url = f'http://api.timezonedb.com/v2.1/get-time-zone?key={api_key}&format=json&by=zone&zone={zone}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                # Extracting time and formatting
                formatted_time = datetime.strptime(data['formatted'], '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
                formatted_date = datetime.strptime(data['formatted'], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
                return f"{formatted_date} {formatted_time}", data['zoneName']
            else:
                return None, None
        else:
            return None, None
    except Exception as e:
        return None, None

# Function to match partial user input to known cities
def match_city(input_city: str):
    input_city = input_city.lower().strip()
    for city in city_to_timezone.keys():
        if input_city in city:  # Partial match
            return city
    return None

# Function to fetch the time when the button is clicked
def get_time():
    location = city_entry.get().lower().strip()  # Get the user's input from the entry field

    # Attempt to match the user input to a city
    matched_city = match_city(location)
    if matched_city:
        timezone = city_to_timezone[matched_city]

        # Try fetching from WorldTimeAPI first
        time, zone = fetch_world_time_api(timezone)

        # If WorldTimeAPI fails, use TimeZoneDB API as a fallback
        if time:
            result_label.config(text=f"Time in {matched_city.capitalize()}:\n{time} ({zone})", fg="green")
        else:
            time, zone = fetch_timezone_db_api('your_timezone_db_api_key', timezone)  # Replace with your API key
            if time:
                result_label.config(text=f"Time in {matched_city.capitalize()}:\n{time} ({zone})", fg="green")
            else:
                result_label.config(text="Could not fetch the time.", fg="red")
    else:
        result_label.config(text="City not recognized. Please try again.", fg="red")

# Create the main application window
root = tk.Tk()
root.title("World Clock")

# Set window size
root.geometry("400x300")

# Label and entry for user to input city
city_label = tk.Label(root, text="Enter city:")
city_label.pack(pady=10)

city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=10)

# Button to fetch time
get_time_button = tk.Button(root, text="Get Time", command=get_time)
get_time_button.pack(pady=10)

# Label to display results
result_label = tk.Label(root, text="", font=('Helvetica', 14))
result_label.pack(pady=20)

# Start the GUI application
root.mainloop()
