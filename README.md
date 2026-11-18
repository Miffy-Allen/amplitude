# Amplitude API and S3 Pipeline
This project extracts event data from the **Amplitude Export API**, decompresses the files and uploads the JSON files to an AWS S3 bucket.

## Description
### main.py

This script extracts event data from the Amplitude Export API, returning a saved timestamped zip file of yesterdays data. The script then decompresses the file and saves it as a json in a seperate directory, deleting the temporary directory containing the zip file. The script connects to AWS using boto3 and uploads the json files to an AWS s3 bucket. Once the file has been uploaded to the s3 bucket it is locally deleted. Logging is used to ensure progress/errors are recorded throughout the script. 

## Dependencies
Required to run this project:
- Python 3.12
- An Amplitude account that can access the Export API
- Amplitude API key and secret key
- An AWS account
- An AWS bucket
- Execute pip install -r requirements.txt to see what packages are required
- .env variables required

## Execution Order
- amplitude_api.py
- unzip.py
- load.py