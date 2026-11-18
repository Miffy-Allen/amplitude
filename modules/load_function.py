# Libraries and Packages
import os
import json
import logging
import boto3
from dotenv import load_dotenv
from datetime import datetime

#appends log with filename
logger = logging.getLogger(__name__)

def load_function(data_dir: str, file_location: str, AWS_ACCESS_KEY: str, AWS_SECRET_ACCESS_KEY: str, AWS_BUCKET_NAME: str):
    """_summary_

    Args:
        data_dir (str): data directory
        file_location (str): file location
        AWS_ACCESS_KEY (str): Key Value - get value from your .env file
        AWS_SECRET_ACCESS_KEY (str): Secret Key - get value from your .env file
        AWS_BUCKET_NAME (str): Bucket Name
    """    
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
