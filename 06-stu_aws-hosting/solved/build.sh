#!/usr/bin/env bash

pip install --target ./.package -r ./requirements.lambda.txt
cd .package
zip -r ../lambda_package.zip .
cd .. 
zip -g lambda_package.zip etl_lambda.py transform_functions.py