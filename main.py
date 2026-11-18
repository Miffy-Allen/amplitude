#Importing packages
import os
from datetime import datetime, timedelta
import time
import requests
import tempfile
import logging
from dotenv import load_dotenv
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
#add the URL
url = 'https://analytics.eu.amplitude.com/api/2/export'
zip_dir = 'zip'

# Format the start and end time strings (YYYYMMDDTHH)
date = datetime.now() - timedelta(days=1)
start_time = date.strftime('%Y%m%dT00') 
end_time = date.strftime('%Y%m%dT23')
max_attempt = 3
delay = 10

extract_result = extract_to_zip(url, zip_dir, max_attempt, delay, start_time, end_time, AMP_API_KEY,  AMP_SECRET_KEY)
# print(extract_result)


#unzip funct needs
# Create a temporary directory for extraction
temp_dir = tempfile.mkdtemp()
# Create local output directory
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
zipfilename = extract_result

# #load funct needs
# # Getting the file we want 
file_location = os.listdir(data_dir)

if extract_result:
    unzip_function(temp_dir, data_dir, zipfilename)
    logger.info('Extract saved successfully and unzipped') 
else:
    logger.info('Extract saved no data')

if unzip_function:
    load_function(data_dir, file_location, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME)
    logger.info('Json successfully uploaded')
else:
    logger.info('Unzip unsuccessful and json not uploaded to S3')