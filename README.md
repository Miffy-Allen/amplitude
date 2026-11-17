# Amplitude API and S3 Pipeline
This project extracts data from the **Amplitude Export API**, decompresses the files and uploads the JSON files to an AWS S3 bucket.

## Description
### amplitude_api.py script

This script extracts data from the Amplitude Export API, returning a saved timestamped zip file of yesterdays data. Logging is used to ensure progress/errors are recorded during the extraction. 

### unzip.py script
The 'unzip' script locates the saved zipfile from the previous script and decompresses the file. It then saves the files in a json format in a separate directory, deleting the temporary directory containing the zipfile.

### load.py script
The 'load' script connects to AWS using boto3, uploading the JSON files to an AWS s3 bucket. Once the file has been uploaded to the s3 bucket it is locally deleted. It also lists files that are currently in the s3 bucket.

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