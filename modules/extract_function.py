#Importing packages
import os
from datetime import datetime, timedelta
import time
import requests
import logging
from dotenv import load_dotenv

#appends log with filename
logger = logging.getLogger(__name__)

# Creating a function for modularizing

def extract_to_zip(url: str, zip_dir: str, max_attempt: int, delay: int, start_time: str, end_time: str, AWS_ACCESS_KEY: str, AWS_SECRET_ACCESS_KEY: str, AWS_BUCKET_NAME: str):
    """_summary_

    Args:
        url (str): URL to pull data from
        zip_dir (str): filepath to save data to
        max_attempt (int): no of times to retry calls
        delay (int): how long to wait between calls
        start_time (str): date of file
        end_time (str): date of file
        AWS_ACCESS_KEY (str): Key Value - get value from your .env file
        AWS_SECRET_ACCESS_KEY (str): Secret Key - get value from your .env file
        AWS_BUCKET_NAME (str): filepath to save data to
    """    

    #Maked directory if not exist
    os.makedirs(zip_dir, exist_ok = True)

    zipfilename = f'{zip_dir}/{start_time}-T23.zip'

    params = {
    'start': start_time,
    'end': end_time
}

    attempt = 0

    while attempt <= max_attempt:
        response = requests.get(url, params= params, auth = (AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME),) ##check this
        status_code = response.status_code

        if 200 <= status_code < 300:
                try:
                    with open(zipfilename, 'wb') as file:
                            file.write(response.content)
                            print(f'Zipfile {zipfilename} saved successfully!')
                            logger.info(f'Zipfile {zipfilename} saved successfully!')
                            return True
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