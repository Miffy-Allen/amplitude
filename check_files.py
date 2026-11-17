import re
import os
from collections import defaultdict
from datetime import datetime
from dotenv import load_dotenv
import boto3

# Authenticate

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Find the earliest date in the bucket and the last (should be yesterday)
start_date = None 
include_today = False  

# Connect to AWS and list the files in the s3 bucket
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
s3 = session.resource("s3")
my_bucket = s3.Bucket(AWS_BUCKET_NAME)
files = [obj.key for obj in my_bucket.objects.all()]
print(f'Found {len(files)} objects in the bucket') # How many objects in bucket

# Read the date of each file in the list
file_dates = [] # create an empty list for these dates to go into
for file in files: # For loop to go through each json file in the bucket
    match = re.search(r'(\d{4}-\d{2}-\d{2})_(\d+)', file) #Searches for the 'date shape' of the file
    if match: # if finds a date then:
        date_str = match.groups()[0] # take the date part
        file_date = datetime.strptime(date_str, '%Y-%m-%d').date() # convert the string date into real date
        file_dates.append(file_date) #put the files into the empty list

