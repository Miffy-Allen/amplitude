import os
import json
from datetime import datetime
import time
import requests
import logging
from dotenv import load_dotenv

load_dotenv() 
api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv


timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

data_dir = 'data'
os.makedirs(data_dir, exist_ok = True)
filename = f'{data_dir}/{timestamp}.json'

url = 'https://analytics.eu.amplitude.com/api/2/export'

response = requests.get(url,
params = {"start": "20261101T00", "end": "20261101T23"},
auth=(api_key, secret_key),
)

zip_dir = 'zip'
os.makedirs(zip_dir, exist_ok = True)
zipfilename = f'{zip_dir}/{timestamp}.zip'

with open(zipfilename, 'wb') as file:
	file.write(response.content)
	
print(file)