# Libraries and Packages
import os
import json
import logging
import boto3
from dotenv import load_dotenv
from datetime import datetime

#Authentication

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Creating Timestamp and Logging

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_filename = f'{log_dir}/{timestamp}.log'

logging.basicConfig(
    filename=log_filename,
    format= '%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO  
)

logger = logging.getLogger()
logger.info('Logger was successfully initialised')

# Getting the file we want 

data_dir = 'data'
file_location = os.listdir(data_dir)

# Connecting to AWS

s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

# Loop through json files and upload to s3

for file in file_location:
    to_upload = f'{data_dir}/{file}'
    try:
        s3_client.upload_file(
            to_upload,
            AWS_BUCKET_NAME,
            file
        )
        print(f'{file} successfully uploaded - yay')
        logger.info(f'{file} successfully uploaded - yay')
        os.remove(to_upload)
    except Exception as e:
        print(f'Oops something went wrong. Error: {e}')
        logger.error(f'Oops something went wrong. Error: {e}')

# Listing what's in the s3 bucket
session = boto3.Session( aws_access_key_id= AWS_ACCESS_KEY, aws_secret_access_key= AWS_SECRET_ACCESS_KEY) # Creating a 'session' with aws and authenticating - a session holds your authentication
s3 = session.resource('s3') # session = authenticated / resource means that aws will return the data as objects / s3 specifies what we are looking for
my_bucket = s3.Bucket(AWS_BUCKET_NAME) # Points to my bucket
for my_bucket_object in my_bucket.objects.all(): # Loops through all the objects in my bucket
    print(my_bucket_object.key) # Prints the objects