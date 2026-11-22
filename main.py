#Importing packages
import os
from datetime import datetime, timedelta
import time
import requests
import tempfile
import logging
from dotenv import load_dotenv

# Add Modules
from modules.extract_function import extract_to_zip
from modules.unzip_function import unzip_function
from modules.load_function import load_function

#Authentication
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')

#-------------------------------------------------------------
# add logging in - this can be modularised later
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

#-----------------------------------------------------------
# API call
url = 'https://analytics.eu.amplitude.com/api/2/export'


# Format the start and end time strings (YYYYMMDDTHH)
## current_date = datetime/now()
yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.strftime('%Y%m%dT00') 
end_time = yesterday.strftime('%Y%m%dT23')

# Directories
zip_dir = 'zip' # Stores the raw zip file from API
temp_dir = tempfile.mkdtemp() # Temporary Folder for extraction - deletes after
data_dir = "data" # Stores final extracted json file for s3 upload

#Final output folder exists before unzipping 
os.makedirs(data_dir, exist_ok=True)

max_attempt = 3
delay = 10

extract_result = extract_to_zip(url, zip_dir, max_attempt, delay, start_time, end_time, AMP_API_KEY,  AMP_SECRET_KEY)
# print(extract_result)


#unzip funct needs




# #load funct needs
# # Getting the file we want 


if extract_result:
    zipfilename = extract_result
    unzip_result = unzip_function(temp_dir, data_dir, zipfilename)
    logger.info('Extract saved successfully and unzipped') 
    file_location = os.listdir(data_dir)
else:
    unzip_result = False
    logger.info('Extract saved no data')

if unzip_result:
    load_function(data_dir, file_location, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME)
    logger.info('Json successfully uploaded')
else:
    logger.info('Unzip unsuccessful and json not uploaded to S3')