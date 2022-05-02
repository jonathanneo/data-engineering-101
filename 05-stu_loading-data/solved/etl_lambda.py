import requests
import pandas as pd 
import os 
import transform_functions as tf 

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
# weather_df.to_csv("out.csv", index=False)

# ## Convert unix timestamp to datetime timestamp string 
date_fixed_weather_df = tf.convert_unix_timestamp(input_df = weather_df, date_columns=["dt"])
date_fixed_weather_df.head()


# ## Replace column names
clean_weather_df = tf.replace_column_character(date_fixed_weather_df, {".": "_"})
clean_weather_df.head()


# ## Rename fields
clean_weather_df = clean_weather_df.rename(columns={
    "id":"city_id", 
    "dt": "datetime"
})
clean_weather_df.head()


# ## Create City DataFrame
city_df = clean_weather_df[["city_id", "name", "coord_lon", "coord_lat"]].drop_duplicates() 
# city_df.head()
# city_df.to_csv("city_df.csv", index=False)


# ## Create Temperature DataFrame
temperature_df = clean_weather_df[["city_id", "datetime", "main_temp", "main_feels_like", "main_temp_min", "main_temp_max"]]
# temperature_df.head()
# temperature_df.to_csv("temp_df.csv", index=False)


# # ## Create Atmosphere DataFrame
atmosphere_df = clean_weather_df[["city_id", "datetime", 'main_pressure', 'main_humidity']]
# atmosphere_df.head()
# atmosphere_df.to_csv("atmos.csv", index=False)


# ## Create SQL Connection
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.dialects import postgresql

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_SERVER_NAME = os.environ.get("DB_SERVER_NAME")
DB_DATABASE_NAME = os.environ.get("DB_DATABASE_NAME")
connection_url = URL.create(
    drivername = "postgresql+pg8000", 
    username = DB_USER,
    password = DB_PASSWORD,
    host = DB_SERVER_NAME, 
    port = 5432,
    database = DB_DATABASE_NAME, 
)

engine = create_engine(connection_url)


# ## Reflect ORM
from sqlalchemy import MetaData
metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)
city = metadata_obj.tables["city"]
temperature = metadata_obj.tables["temperature"]
atmosphere = metadata_obj.tables["atmosphere"]


# ## Upsert: City
insert_statement = postgresql.insert(city).values(city_df.to_dict(orient='records'))
upsert_statement = insert_statement.on_conflict_do_update(
    index_elements=['city_id'],
    set_={c.key: c for c in insert_statement.excluded if c.key not in ['city_id']})
engine.execute(upsert_statement)


# ## Upsert: Temperature
insert_statement = postgresql.insert(temperature).values(temperature_df.to_dict(orient='records'))
upsert_statement = insert_statement.on_conflict_do_update(
    index_elements=['city_id', 'datetime'],
    set_={c.key: c for c in insert_statement.excluded if c.key not in ['city_id', 'datetime']})
engine.execute(upsert_statement)


# ## Upsert Atmosphere
insert_statement = postgresql.insert(atmosphere).values(atmosphere_df.to_dict(orient='records'))
upsert_statement = insert_statement.on_conflict_do_update(
    index_elements=['city_id', 'datetime'],
    set_={c.key: c for c in insert_statement.excluded if c.key not in ['city_id', 'datetime']})
engine.execute(upsert_statement)
