# libraries 
import logging
from datetime import datetime
import os          
import zipfile     
import gzip        
import shutil     
import tempfile    
from datetime import timedelta

#appends log with filename
logger = logging.getLogger(__name__)


def unzip_function(temp_dir: str, data_dir : str, zipfilename: str ):
    """_summary_

    Args:
        temp_dir (str): tempory directory to unzip to
        data_dir (str): data directory where json files are loaded to
        zip_dir (_type_): file to unzip
    """    
    # Unpacks the .zip folder to the temp directory, revealing several .gz files
    try:
        with zipfile.ZipFile(zipfilename, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
            logger.info(f"{zipfilename}] extracted to temp directory: {temp_dir} ")
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

    processed = 0
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
                        ## return True ##
                        processed += 1 ##added
                except Exception as e:
                    logger.error(f"Failed to process file {file}: {str(e)}")
                    raise #added
    try:
        # Delete the temporary directory
        shutil.rmtree(temp_dir)
        logger.info("Temp directory deleted")

    except Exception as e:
        logger.error(f"Failed to delete temp directory: {str(e)}")


    #remove the zipfile after
    try:
        os.remove(zipfilename)
        logger.info(f'{zipfilename} successfully deleted!')
    except Exception as e:
        logger.error(f"Failed to delete zipfile {zipfilename} : {str(e)}")

    print("All files extracted to the 'data' directory!")
    return True

