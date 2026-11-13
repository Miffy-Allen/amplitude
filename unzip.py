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

# Unpacks the .zip folder to the temp directory, revealing several .gz files

with zipfile.ZipFile("zip/2026-11-13 09-50-36.zip", "r") as zip_ref:
    zip_ref.extractall(temp_dir)

# Locate target folder - find all folders with numeric names only and returns the file path as a variable to be tranversed

day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
day_path = os.path.join(temp_dir, day_folder)

# Directory Walking and File Processing

for root, _, files in os.walk(day_path):
    for file in files:
        if file.endswith('.gz'):
            # Process each .gz file
            print(file)

# to unpack .gz files to obtain the .json we need:
# filepath of the .gz file
# the filename of the .gz file, and what it will be as .json
# the location of where to store it (data_dir)

# we read the contents of the .gz file and write the content to a new json in our data_dir

gz_path = os.path.join(root, file)
json_filename = file[:-3]  
output_path = os.path.join(data_dir, json_filename)

with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
    shutil.copyfileobj(gz_file, out_file)

shutil.rmtree(temp_dir)