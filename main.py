#Importing packages
import os
from datetime import datetime, timedelta
import time
import requests
import logging
from dotenv import load_dotenv
from modules.extract_function import extract_to_zip

#Authentication
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

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
yesterday = datetime.now() - timedelta(days=1)
start_time = yesterday.strftime('%Y%m%dT00') 
end_time = yesterday.strftime('%Y%m%dT23') 

extract_result = extract_to_zip(url, zip_dir, max_attempt = 3, delay = 10, start_time = start_time , end_time = end_time, AWS_ACCESS_KEY = 'AWS_ACCESS_KEY',  AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY', AWS_BUCKET_NAME = 'AWS_BUCKET_NAME')

##if extract_result :
    ## unzip_function
    ## logger.info - extract saved and 
## else:
    ## logger.info - extract saved no data , nothing to attempt