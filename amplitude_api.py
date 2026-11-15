#Importing packages
import os
from datetime import datetime, timedelta
import time
import requests
import logging
from dotenv import load_dotenv

#Authentication
load_dotenv() 
api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")

# Get yesterday's date 
yesterday = datetime.now() - timedelta(days=1)

# Format the start and end time strings (YYYYMMDDTHH)
start_time = yesterday.strftime('%Y%m%dT00')
end_time = yesterday.strftime('%Y%m%dT23')

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

# Making a folder to save it in
data_dir = 'data'
os.makedirs(data_dir, exist_ok = True)
filename = f'{data_dir}/{timestamp}.json'

url = 'https://analytics.eu.amplitude.com/api/2/export'

params = {
    'start': start_time,
    'end': end_time
}

zip_dir = 'zip'
os.makedirs(zip_dir, exist_ok = True)
zipfilename = f'{zip_dir}/{start_time}-T23.zip'



attempt = 0
max_attempt = 5

while attempt <= max_attempt:
      response = requests.get(url, params= params, auth = (api_key, secret_key),) ##check this
      status_code = response.status_code

      if 200 <= status_code < 300:
            try:
                  with open(zipfilename, 'wb') as file:
                        file.write(response.content)
                        print(f'Zipfile {zipfilename} saved successfully!')
                        logger.info(f'Zipfile {zipfilename} saved successfully!')
            except Exception as e:
                  print(f'An error occurred when saving the zipfile - oops: {e}')
            break
      
      elif 300 <= status_code < 505:
        print(f'API call failed, status code {status_code}')
        logger.error(f'API call failed, status code {status_code}')
        break
      
      else:
            if attempt == max_attempt:
                  print(f'Max number of attempts reached. Status code {status_code}. Investigate further 👀')
                  logger.warning(f'Max number of attempts reached. Status code {status_code}. Investigate further 👀')
            else:
                  print(f'Attempt {attempt} failed, status code {status_code}. Try again')
                  logger.error(f'Attempt {attempt} failed, status code {status_code}. Try again')

            attempt +=1
            
            time.sleep(30)