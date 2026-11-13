import logging
from datetime import datetime

# Set Log filepath location
log_filename = f"logs/amplitude_load_unzip_folder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logs to retrieve INFO messages and higher
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

# load libraries
import os          
import zipfile     
import gzip        
import shutil     
import tempfile    


# Create a temporary directory for extraction
temp_dir = tempfile.mkdtemp()

# Create local output directory
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
logger.info("Environment Setup: beginning unzip process") 

# Unpacks the .zip folder to the temp directory, revealing several .gz files
try:
    with zipfile.ZipFile("zip/2026-11-13 09-50-36.zip", "r") as zip_ref:
        zip_ref.extractall(temp_dir)
        logger.info(f"zip/2026-11-13 09-50-36.zip extracted to temp directory: {temp_dir} ")
except Exception as e:
    logger.error(f"Error extracting zip file: {str(e)}")
    raise

# Locate target folder - find all folders with numeric names only and returns the file path as a variable to be tranversed
try:
    day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
    day_path = os.path.join(temp_dir, day_folder)
except Exception as e:
    logger.error(f"Error finding day folder: {str(e)}")
    raise

# Directory Walking and File Processing
# to unpack .gz files to obtain the .json we need:
# filepath of the .gz file
# the filename of the .gz file, and what it will be as .json
# the location of where to store it (data_dir)

# we read the contents of the .gz file and write the content to a new json in our data_dir


for root, _, files in os.walk(day_path):
    for file in files:
        if file.endswith('.gz'):
            # Process each .gz file
            try:
                gz_path = os.path.join(root, file)
                json_filename = file[:-3]  # remove .gz extension
                output_path = os.path.join(data_dir, json_filename)
                with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file)
                    
                    logger.info(f"Successfully processed: {file} -> {json_filename}")
            except Exception as e:
                logger.error(f"Failed to process file {file}: {str(e)}")
            
try:
    # Delete the temporary directory
    shutil.rmtree(temp_dir)
    logger.info("Temp directory deleted")

except Exception as e:
    logger.error(f"Failed to delete temp directory: {str(e)}")

print("All files extracted to the 'data' directory!")


