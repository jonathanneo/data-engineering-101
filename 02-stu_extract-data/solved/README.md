# Task 

### Step 1: Extract from CSV file 

Read the list of cities from the CSV file into a Pandas dataframe. 

Reference docs for [pd.read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html). 

### Step 2: Loop through each city name and make a request to OpenWeatherAPI

For each city in the CSV file, make a request to OpenWeatherAPI. See [OpenWeatherAPI docs](https://openweathermap.org/current)

Retrieve results with units specified as metric. 

Append each result to an empty list. 

### Step 3: Normalize list of results into a Pandas dataframe 

Take the list from step 2, and normalize the result (aka "flatten"). 

Reference docs for [pd.json_normalize](https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html). 

### Step 4: Save normalized dataframe to csv and check your results 

Save the dataframe from step 3 into CSV to check your results. 

Reference docs for [df.to_csv()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html). 

You should see something similar to the following csv output:

```
weather,base,visibility,dt,timezone,id,name,cod,coord.lon,coord.lat,main.temp,main.feels_like,main.temp_min,main.temp_max,main.pressure,main.humidity,wind.speed,wind.deg,clouds.all,sys.type,sys.id,sys.country,sys.sunrise,sys.sunset,wind.gust
"[{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}]",stations,10000,1651502195,36000,2172517,Canberra,200,149.1281,-35.2835,6.05,6.05,5.81,7.93,1022,93,0.0,0,0,2,2004200,AU,1651524086,1651562356,
```

### Step 5: Remove secrets 

Remove the CSV endpoint path and API key from your code. 

You should instead set the CSV endpoint path and API key as environment variables. You may set environment variables by running the following in shell: 

```
export CSV_ENDPOINT_CAPITAL_CITIES="your_path_to_csv_endpoint"
```

In Python, use `os.environ.get()` to retrieve the environment variables. See example usage [here](https://stackoverflow.com/questions/4906977/how-do-i-access-environment-variables-in-python).

You may choose to write a shell script to hold the export commands and add the shell script to your gitignore so that it is not committed to the git repository. 