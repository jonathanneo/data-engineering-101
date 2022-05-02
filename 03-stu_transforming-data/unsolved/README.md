# Task 

Extend the ETL script to transform data according to the steps below. 

### Step 1: Write a function to convert unix timestamp 

Complete the below function specification. You may wish to save the function in a separate `transformation_functions.py` python file.

```python
def convert_unix_timestamp(input_df:pd.DataFrame, date_columns:list=[])->pd.DataFrame:
    """
    Converts unix timestamp columns to datetime string. 

    input: 
    - input_df: your input dataframe 
    - date_columns: a list of column names which contains unix timestamps you wish to convert 

    returns: 
    - cleaned dataframe
    """
```

Hint: 
- Begin the function with a deep copy of the dataframe. Reference docs for [df.copy(deep=True)](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.copy.html)
- Loop through each date column and convert the column from unix timestamp to datetime string using [pd.to_datetime()](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)

### Step 2: Use function to convert unix timestamp 

Use the function specified in step 1 to convert `dt` column to datetime string. 


### Step 3: Write a function to replace characters in the column names 

Complete the below function specification. You may wish to save the function in a separate `transformation_functions.py` python file.

```python
def replace_column_character(input_df:pd.DataFrame, replace_dict:dict={})->pd.DataFrame:
    """
    Replaces characters that exist in your columns. 

    input: 
    - input_df: your input dataframe 
    - replace_dict: a dictionary with mappings of {"source": "target"}

    returns: 
    - cleaned dataframe
    """
```

Hint: 
- Begin the function with a deep copy of the dataframe. Reference docs for [df.copy(deep=True)](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.copy.html)
- Create a new dictionary of columns 
- Loop through each column and perform a python string replace for characters specified in the replace dict of source to target 
- Perform a [df.rename()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html) to rename columns using the new dictionary of columns 

### Step 4: Use function to replace characters in column names 

Use the function specified in step 3 to replace the full stop character (`.`) with an underscore character (`_`). 

### Step 5: Rename columns 

Rename columns using the following mapping: 

```json
{
    "id":"city_id", 
    "dt": "datetime"
}
```

### Step 6: Create the city dataframe 

Create a new dataframe called `city_df` with the following columns selected `"city_id", "name", "coord_lon", "coord_lat"`, and duplicates removed. 

Save city_df to a csv. You should see roughly the following output: 

```
city_id,name,coord_lon,coord_lat
2172517,Canberra,149.1281,-35.2835
2147714,Sydney,151.2073,-33.8679
2073124,Darwin,130.8418,-12.4611
2174003,Brisbane,153.0281,-27.4679
2078025,Adelaide,138.6,-34.9333
2163355,Hobart,147.3294,-42.8794
4163971,Melbourne,-80.6081,28.0836
2063523,Perth,115.8333,-31.9333
```

### Step 7: Create the temperature dataframe

Create a new dataframe called `temperature_df` with the following columns selected `"city_id", "datetime", "main_temp", "main_feels_like", "main_temp_min", "main_temp_max"`. 

Save temperature_df to a csv. You should see roughly the following output: 

```
city_id,datetime,main_temp,main_feels_like,main_temp_min,main_temp_max
2172517,2022-05-02 15:05:52,5.42,3.34,4.99,7.37
2147714,2022-05-02 15:06:36,14.82,14.58,12.69,16.33
2073124,2022-05-02 15:10:22,24.97,25.69,22.25,24.99
2174003,2022-05-02 15:11:46,15.53,15.36,13.6,17.55
2078025,2022-05-02 15:07:09,13.65,13.06,11.23,16.83
2163355,2022-05-02 15:10:50,14.83,14.27,13.48,16.26
4163971,2022-05-02 15:09:30,27.19,29.27,25.02,28.92
2063523,2022-05-02 15:09:29,16.6,16.64,15.1,17.59
```

### Step 8: Create the atmosphere dataframe 

Create a new dataframe called `atmosphere_df` with the following columns selected `"city_id", "datetime", 'main_pressure', 'main_humidity'`. 

Save atmosphere_df to a csv. You should see roughly the following output: 

```
city_id,datetime,main_pressure,main_humidity
2172517,2022-05-02 15:05:34,1022,95
2147714,2022-05-02 15:16:58,1020,84
2073124,2022-05-02 15:10:22,1009,83
2174003,2022-05-02 15:11:46,1020,85
2078025,2022-05-02 15:07:09,1016,76
2163355,2022-05-02 15:10:50,1008,73
4163971,2022-05-02 15:09:30,1019,71
2063523,2022-05-02 15:09:29,1021,89
```