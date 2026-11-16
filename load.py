# Libraries and Packages
import os
import json
import logging
import boto3
from dotenv import load_dotenv

#Authentication

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Getting the file we want 

data_dir = 'data'
file_location = os.listdir(data_dir)

# Connecting to AWS
s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)
