# Amplitude
### The 'amplitude_api' script extracts data from the Amplitude Export API, returning a saved timestamped zip file of yesterdays data. Logging is used to ensure progress/errors are recorded during the extraction. 
### The 'unzip' script locates the saved zipfile from the previous script and decompresses the file. It then saves the files in a json format in a separate directory, deleting the temporary directory containing the zipfile.

## Dependencies
### Required to run this project:
#### > Python 3.12
#### > An Amplitude account that can access the Export API
#### > Amplitude API key and secret key
#### > Execute pip install -r requirements.txt to see what packages are required
#### > .env variables required

