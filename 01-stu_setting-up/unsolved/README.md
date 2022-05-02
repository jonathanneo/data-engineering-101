# Introduction

Today, we are going to learn how to build a fully automated ETL solution hosted on AWS. The goal for this lesson is to teach participants the principles of ETL and hosting the ETL solution on the cloud. 

![solution_architecture.drawio.png](../../images/solution_architecture.drawio.png)

### Extracting data 

We are going to pull data that is available on: 
- OpenWeatherAPI 
- An S3 Bucket with a CSV file which we will upload

### Transforming data 

We are going to transform the data using Pandas. The transformation logic will then be hosted on AWS Lambda, and triggered by a time-based (cron) trigger. 

### Loading data

We are going to load data into a PostgreSQL database hosted on AWS. 

# Task 

When you are ready, attempt the steps below in sequence. 

### Step 1: Deploying PostgreSQL on AWS RDS 

1. In the AWS Console, search for "RDS". 
2. Choose the region closest to you on the top-right e.g. Sydney (ap-southeast-2)
3. Select "Create database" 
4. Configure database. Note: Unless specified, leave the settings to default. 
    1. Select "PostgreSQL" 
    2. Select Version "12.9-R1" (for the free tier, you will need to use a version below 13). 
    3. Select templates: "Free tier"
    4. Provide a DB instance identifier. Note: this is the name that appears on AWS and not the actual name of the database or server. 
    5. Set master username: "postgres"
    6. Set master password: `<specify your password>`
    7. Set confirm password: `<specify your password>`
    8. In connectivity, set public access: "Yes" 
    9. In additional configuration, deselect "Enable automated backups" 
    10. Select "Create database" 
5. After the database has been deployed, select the database and go to "Security group rules" and select the Security Group(s) with Type: "CIDR/IP - Inbound". 
    1. In the Security Group, select "Inbound rules" 
    2. Select "Edit inbound rules" 
    3. Select "Add rule" and add a new rule for: 
        - Type: "All traffic" 
        - Protocol: "All" 
        - Port Range: "All" 
        - Source: "Anywhere-IPv4"
    4. Select "Save rules" 
6. Try connecting to your database now from PgAdmin4. You should be successful. 

### Step 2: Deploying an S3 Bucket 

1. In the AWS Console, search for "S3". 
2. Select "Create bucket" 
3. Configure bucket. Note: Unless specified, leave the settings to default. 
    1. Provide bucket name
    2. AWS Region: Choose the region closest to you e.g. Sydney (ap-southeast-2)
    3. Deselect "Block all public access" 
    4. Select "Create bucket" 
4. After the bucket is deployed, go to the bucket and into the "Permissions" tab and into the bucket policy. Set the bucket policy to: 

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicRead",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectVersion"
                ],
                "Resource": "arn:aws:s3:::your-bucket-arn-here/*"
            }
        ]
    }
    ```

    Save changes. 

5. Upload [australian_capital_cities.csv](../../data/australian_capital_cities.csv) to the bucket. 
6. Keep in mind the URL for newly uploaded CSV file. 

### Step 3: Getting a OpenWeather API Key 

1. Go to https://home.openweathermap.org/users/sign_up
2. Provide your sign up details 
3. Go to https://home.openweathermap.org/api_keys and retrieve your API Key 
4. Refer to the API docs for the API you are using today: https://openweathermap.org/current 
