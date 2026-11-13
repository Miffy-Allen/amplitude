import os
import json
from datetime import datetime
import time
import requests
import logging
from dotenv import load_dotenv

load_dotenv() 
api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")


timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

data_dir = 'data'
os.makedirs(data_dir, exist_ok = True)
filename = f'{data_dir}/{timestamp}.json'

url = 'https://analytics.eu.amplitude.com/api/2/export'

zip_dir = 'zip'
os.makedirs(zip_dir, exist_ok = True)
zipfilename = f'{zip_dir}/{timestamp}.zip'



attempt = 0
max_attempt = 5

while attempt <= max_attempt:
      response = requests.get(url, params= {"start": "20261101T00", "end": "20261101T23"}, auth = (api_key, secret_key),) ##check this
      status_code = response.status_code
      if 200 <= status_code < 300:
            try:
                  with open(zipfilename, 'wb') as file:
                        file.write(response.content)
                        print(f'Zipfile {zipfilename} saved successfully!')
            except Exception as e:
                  print(f'An error occurred when saving the zipfile - oops: {e}')
            break
      elif 300 <= status_code < 505:
        print(f'API call failed, status code {status_code}')
        break
      else:
            if attempt == max_attempt:
                  print(f'Max number of attempts reached. Status code {status_code}. Investigate further 👀')
            else:
                  print(f'Attempt {attempt} failed, ststus code {status_code}. Try again')
            
            attempt +=1
            
            time.sleep(30)