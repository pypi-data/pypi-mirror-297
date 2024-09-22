import os
import requests
from mridumanda_shvedt.weather_ascii import ascii_arts


def get_city_from_ip():
    try:
        ip_info_response = requests.get("https://ipinfo.io/json")
        
        if ip_info_response.status_code!= 200:
            raise Exception("Failed to get location from IP info \nEnter city name manually")
        
        return ip_info_response.json().get('city')
    
    except requests.exceptions.RequestException as e:
        print("Failed to get location from IP info \nEnter city name manually")
        return None


def get_weather():
    city = get_city_from_ip()
    
    if city == None:
        city = input("Enter city name: ")
    
    API_KEY = get_api_key()
    API_URL = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + API_KEY
    
    try:
        weather_map_response = requests.get(API_URL)
        
        if weather_map_response.status_code is not 200:
            print("Unable to fetch weather data")
            return None
    except requests.exceptions.RequestException as e:
        print("Failed to fetch weather data")
        return None

    weather_data = weather_map_response.json()

    temp = f"{weather_data['main'].get('temp') - 273.15:.2f} °C"
    temp_min = f"{weather_data['main'].get('temp_min') - 273.15:.2f} °C"
    temp_max = f"{weather_data['main'].get('temp_max') - 273.15:.2f} °C"
    hum = f"{weather_data['main'].get('humidity')}%"
    pressure = f"{weather_data['main'].get('pressure')} hPa"
    desc = weather_data['weather'][0].get('description').title()
    city_name = weather_data['name']
    country = weather_data['sys'].get('country')
    location = f"{city_name}, {country}"

    return [ " ", location, temp, temp_min, temp_max, hum, desc, pressure, " "]


def get_api_key():
    api_key_file = os.path.join(os.getenv('HOME'), '.config','mridumanda', 'api_key.txt')

    with open(api_key_file, 'r') as f:
        api_key = f.read().split('=')[1].strip()

    return api_key


# def display_weather_data_ascii(weather_data):
#     os.system('clear')

#     for i in range(len(weather_data)):
#         print(ascii_arts.clear_day[i] + f"{weather_data[i]}")


def display_weather_one_liner(weather_data):
    os.system('clear')

    print(f"Location: {weather_data[1]} | Temp: {weather_data[2]} | Humidity: {weather_data[5]} | Pressure: {weather_data[7]} | {weather_data[6]}")


def display_weather(weather_data):
    os.system('clear')

    print(f"Weather data for {weather_data[1]}")
    print(f" {'-' * (len(weather_data[-1]) - 2)} ")
    print(f"Temperature:          {weather_data[2]}")
    print(f"Humidity:             {weather_data[5]}")
    print(f"Min Temperature:      {weather_data[3]}")
    print(f"Max Temperature:      {weather_data[4]}")
    print(f"Condition:            {weather_data[6]}")
    print(f"Pressure:             {weather_data[7]}")