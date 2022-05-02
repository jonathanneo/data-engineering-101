import requests
import pandas as pd 
import os 

CSV_ENDPOINT_CAPITAL_CITIES = os.environ.get("CSV_ENDPOINT_CAPITAL_CITIES")
capital_cities_df = pd.read_csv(CSV_ENDPOINT_CAPITAL_CITIES)

# ## Get Weather Data 
# Get weather data by requesting from openweathermap REST APIs for each capital city 
API_KEY_OPEN_WEATHER = os.environ.get("API_KEY_OPEN_WEATHER")
weather_data = []
for city_name in capital_cities_df["city_name"]:
    params = {
        "q": city_name,
        "units": "metric",
        "appid": API_KEY_OPEN_WEATHER
    }   
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather", params=params)
    if response.status_code == 200: 
        weather_data.append(requests.get(f"http://api.openweathermap.org/data/2.5/weather", params=params).json())
    else: 
        raise Exception("Extracting weather api data failed. Please check if API limits have been reached.")

# ## Read JSON data into Pandas DataFrame
weather_df = pd.json_normalize(weather_data)
weather_df.to_csv("out.csv", index=False)