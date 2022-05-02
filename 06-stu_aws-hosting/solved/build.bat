pip install --target ./.package -r ./requirements.lambda.txt
cd .package
7z a -tzip ../lambda_package.zip .
cd ..
7z a -tzip lambda_package.zip etl_lambda.py transform_functions.py