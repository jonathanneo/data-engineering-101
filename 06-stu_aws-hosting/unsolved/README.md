# Task 

Deploy the python application to AWS Lambda. 

### Step 1: Convert script to function for AWS Lambda  

Place the following wrapper around your python script:

```python
import requests
import pandas as pd 
import os 
import transform_functions as tf 

import warnings
warnings.filterwarnings('ignore')

def lambda_function(request, context):
    # YOUR SCRIPT GOES HERE 
```

AWS Lambda calls a python function that accepts two arguments within your script. Therefore, we need to adhere to that convention. 

### Step 2: Build app

Before we can deploy the app, we need to first build the app. 

Building the app refers to packaging and compiling the app so that it is in a state that can be readily deployed onto the target platform (e.g. AWS, Heroku, Azure, GCP, etc). We can skip the compilation since Python is not a compiled language, however we still need to package the app. 

To package the app, we will run the following lines of code: 

<b>macOS</b>:
```
pip install --target ./.package -r ./requirements.lambda.txt
cd .package
zip -r ../lambda_package.zip .
cd ..
zip -g ../lambda_package.zip etl_lambda.py transform_functions.py
```

The code above does the following: 
1. Installs python library specified in requirements.lambda.txt 
2. Zips all python libraries into the zip file 
3. Zips all python scripts into the zip file 

<b>windows</b>:

Note for Windows-only - You will need to install 7z (7-zip) which is a command line tool used for zipping files. 

1. Go to https://www.7-zip.org/ and download the version for your windows PC (usually 64-bit x64)
2. Run the installer .exe file 
3. Add the path `C:\Program Files\7-Zip` to your environment variables `path` 


```
pip install --target ./.package -r ./requirements.lambda.txt
cd .package
7z a -tzip ../lambda_package.zip .
cd ..
7z a -tzip lambda_package.zip etl_lambda.py transform_functions.py
```


This will produce a `.zip` file which contains all the code and library packages required to run the app on AWS Lambda. Note that some libraries like Pandas and Numpy were not packaged in the process as those libraries need to be packaged using a linux machine, whereas we are using Mac or Windows machines. So instead, we will use Layers in AWS Lambda later. 

For re-use, we've stored the commands in [build.sh](build.sh) and [build.bat](build.bat) respectively. 

You can just build the app by running either 

<b>macOS</b>:
```
. ./build.sh
```

<b>windows</b>:
```
build.bat
```

### Step 3: Deploy app 

1. In the AWS Console, search for "Lambda". 
2. Choose the region closest to you on the top-right e.g. Sydney (ap-southeast-2)
3. Select "Create function" 
4. Configure the lambda function. Note: Unless specified, leave the settings to default. 
    1. Provide function name 
    2. Runtime: Python 3.9
    3. Select "Create function" 
5. After the lambda function is deployed, go to the "Code" section, and select "Upload from" > ".zip file" and provide the .zip file you have built. Click "save" and allow up to 2 mins for the file to be uploaded and processed. 
6. In the "Code" section go to "Runtime settings" and select "Edit". 
    1. We need to tell AWS Lambda which file and function to execute. 
    2. In "Handler", specify: "etl_lambda.lambda_function".
    3. Select "Save" 
7. In the "Code" section, scroll down to "Layers" and select "Add a layer". 
    1. Some libraries need to be installed using a linux machine as AWS Lambda is running on linux machines. However, we have Mac and Windows machines. So we will use a "Layer" which is a set of packaged libraries we can use. We will be using layers provided by https://github.com/keithrozario/Klayers. For a list of available packaged libraries in Sydney (ap-southeast-2), see: https://api.klayers.cloud//api/v2/p3.9/layers/latest/ap-southeast-2/json. The Layer we will be using is the pandas layer. 
    2. In the Layer config, select "Specify an ARN" and provide "arn:aws:lambda:ap-southeast-2:770693421928:layer:Klayers-p39-pandas:1" and select "Verify". 
    3. After the layer is verified, select "Add" 
8. In the "Configuration" section, go to "Environment variables" and select "Edit". You will now create environment variables that correspond to the environment variables you have used locally. 
    1. Select "Add environment variable" and proceed to populate the "Key" and "Value" pairs for each environment variable corresponding to your environment variables you have used locally. 
9. In the "Configuration" section, go to "General configuration" and change the timeout to 30 seconds. 
10. In the "Test" section, click on the "Test" button to trigger your lambda function. If successful, you should see more records appear in your database. 

### Step 4: Deploy Cron Trigger on AWS EventBridge 

Finally, we can look at automating the scheduling of the ETL job. 

1. In the AWS Console, search for "EventBridge". 
2. Choose the region closest to you on the top-right e.g. Sydney (ap-southeast-2)
3. Select "Create create" 
4. Configure EventBridge. Note: Unless specified, leave the settings to default. 
    1. Provide a rule name 
    2. Define pattern: "Schedule" 
    3. Fixed rate every: "1" "minutes" (you can set it to every 1 minute to try it out)
    4. Select targets: "Lambda function"
    5. Function: `select your function name`
    6. Select "Create" 
5. Wait until your trigger runs and check your database again. You should see more records appear. 

