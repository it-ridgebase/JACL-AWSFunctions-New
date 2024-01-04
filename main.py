"""
Main Script for LiveIQ Data Processing and Uploading

This script automates the process of downloading an Excel file from LiveIQ,
processing the data, and then uploading the processed data to Airtable and AWS S3.

The script uses AWS Secrets Manager to securely retrieve credentials for LiveIQ,
and environment variables for configuration settings for Airtable and AWS S3.

Requirements:
- AWS CLI configured with access to the required AWS Secrets Manager secret.
- Environment variables set for Airtable API key, base ID, table name, and S3 bucket name.
- Python packages: boto3, pandas, selenium, airtable-python-wrapper, python-dotenv.

Usage:
Run the script in a Python environment where all dependencies have been installed:
$ python main.py
"""

import logging # Import the logging module
import os # Import the os module
import tempfile
from crawler.crawler import download_excel # Import the download_excel function from the crawler module
from processor.processor import process_excel # Import the process_excel function from the processor module
from airtable_module.airtable import upload_to_airtable # Import the upload_to_airtable function from the airtable_module within the airtable package
from aws.s3 import upload_file_to_s3 # Import the upload_file_to_s3 function from the s3 module within the aws package
from jacal_secrets.secrets_manager import get_secret # Import the get_secret function from the secrets_manager module within the secrets package


def setup_logging():
    # Create a logger
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler that logs debug messages
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)

    # Create a console handler that also logs debug messages
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

def main(): # Define the main function that will be executed
    setup_logging()
    logger = logging.getLogger('my_app')

    logger.debug("Starting main function V2")
    try:
        logger.debug("Starting main function")

        region_name = os.getenv('AWS_REGION', 'ca-central-1') # Define the AWS region name for the Secrets Manager
        liveiq_secret_name = os.getenv('LIVEIQ_SECRET_NAME', 'liveiq')
        liveiq_secret = get_secret('liveiq', region_name) # Retrieve the LiveIQ secret (username and password) from AWS Secrets Manager
        logger.debug("Retrieved LiveIQ secret")
        
        download_path = tempfile.mkdtemp() # Define the path where the downloaded Excel file will be stored
        logger.debug(f"Downloading Excel file to {download_path}")
        excel_file = download_excel(download_path, liveiq_secret) # Call the download_excel function to download the Excel file using the LiveIQ credentials

        if excel_file is None:
            logger.error("Failed to download the Excel file or no file was downloaded.")
            return
        
        logger.debug("Processing Excel file")
        processed_data = process_excel(excel_file) # Process the downloaded Excel file and store the processed data
        processed_data = processed_data.fillna("")  # Replace NaN with empty strings

        # Define the API key, base ID, and table name for Airtable
        airtable_api_key = os.getenv('AIRTABLE_API_KEY')
        airtable_base_id = os.getenv('AIRTABLE_BASE_ID')
        airtable_table_name = os.getenv('AIRTABLE_TABLE_NAME')
        
        # Print statements to check the types and values
        print(f"base_id type: {type(airtable_base_id)}, value: {airtable_base_id}")
        print(f"table_name type: {type(airtable_table_name)}, value: {airtable_table_name}")
        print(f"api_key type: {type(airtable_api_key)}, value: {airtable_api_key}")

        logger.debug("Uploading data to Airtable")
        upload_to_airtable(airtable_api_key, airtable_base_id, airtable_table_name, processed_data) # Upload the processed data to Airtable

        s3_bucket = os.getenv('S3_BUCKET_NAME') # Define the S3 bucket name where the file will be uploaded
        print(f"s3_bucket type: {type(s3_bucket)}, value: {s3_bucket}")
        logger.debug(f"Uploading Excel file to S3 bucket: {s3_bucket}")
        upload_file_to_s3(excel_file, s3_bucket)  # Upload the Excel file to the specified S3 bucket
    
        logger.debug("Main function completed successfully")

    except Exception as e:
        logger.exception("An error occurred")

if __name__ == "__main__":
    main()