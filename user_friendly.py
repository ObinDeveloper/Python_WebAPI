import requests
from datetime import datetime
from colorama import Fore, init

# Initialize colorama for Windows support
init(autoreset=True)

# City to Timezone mapping
city_to_timezone = {
    "minneapolis, mn": "America/Chicago",
    "houston, tx": "America/Chicago",
    "arlington, tx": "America/Chicago",
    "abidjan, ivory coast": "Africa/Abidjan",
    "paris, france": "Europe/Paris"
}

# Unicode city symbols
city_symbols = {
    "minneapolis, mn": "🏙️",
    "houston, tx": "🌆",
    "arlington, tx": "🏠",
    "abidjan, ivory coast": "🌍",
    "paris, france": "🗼"
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
        print(f"{Fore.RED}Error fetching from WorldTimeAPI: {e}")
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
                print(f"{Fore.RED}Error: {data['message']}")  # Show any error message from the API response
                return None, None
        else:
            print(f"{Fore.RED}Failed to fetch from TimeZoneDB. HTTP Status: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"{Fore.RED}Error fetching from TimeZoneDB: {e}")
        return None, None

# Function to match partial user input to known cities
def match_city(input_city: str):
    input_city = input_city.lower().strip()
    for city in city_to_timezone.keys():
        if input_city in city:  # Partial match
            return city
    return None

# Function to allow user input for a location and fetch the time once
def get_time_for_location():
    while True:
        # Ask user to input a location or type quit/exit
        location = input("Enter a city (e.g., Minneapolis) or type 'quit'/'exit' to stop: ").lower().strip()

        if location in ['quit', 'exit']:
            print(f"{Fore.CYAN}Exiting the program. Goodbye!")
            break

        # Attempt to match the user input to a city
        matched_city = match_city(location)
        if matched_city:
            timezone = city_to_timezone[matched_city]
            symbol = city_symbols.get(matched_city, "📍")
            print(f"{Fore.CYAN}{symbol} Fetching time for {matched_city.capitalize()}...")

            # Try fetching from WorldTimeAPI first
            print(f"{Fore.YELLOW}\nFetching time from WorldTimeAPI...")
            time, zone = fetch_world_time_api(timezone)

            # If WorldTimeAPI fails, use TimeZoneDB API as a fallback
            if time:
                print(f"{Fore.GREEN}Time: {time} ({zone})")
            else:
                print(f"{Fore.RED}Could not fetch time from WorldTimeAPI. Trying TimeZoneDB API...")
                api_key_tzdb = 'your_timezone_db_api_key'  # Replace with your TimeZoneDB API key
                time, zone = fetch_timezone_db_api(api_key_tzdb, timezone)

                if time:
                    print(f"{Fore.GREEN}Time: {time} ({zone})")
                else:
                    print(f"{Fore.RED}Could not fetch time from TimeZoneDB API either.")

        else:
            print(f"{Fore.RED}Sorry, location '{location}' not recognized. Please try again.")

# Main function call
get_time_for_location()
