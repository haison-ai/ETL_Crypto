#Import libraries.
import json
from dotenv import load_dotenv
from pathlib import Path
import requests
import os
import datetime
import boto3
from botocore.exceptions import ClientError
import logging


load_dotenv() # take env variables

# Detailed logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # Most detailed level (DEBUG shows everything)
    format='%(asctime)s [%(levelname)s] %(message)s - %(name)s:%(lineno)d',
    datefmt='%Y-%m-%d %H:%M:%S'  # Custom timestamp format
)

logger = logging.getLogger(__name__) # handle logs in my code

class Extract():
    """
    Class responsible for extracting and processing financial data from APIs.
    Handles data retrieval, local storage, and S3 upload operations.
    """
    def __init__(self, file_name, api_url, path=None, bucket_name=None, aws_region=None):
        self.bucket_name = bucket_name or os.getenv("BUCKET_NAME")
        self.aws_region = aws_region or os.getenv("AWS_REGION")
        self.path = path
        self.api_url = api_url
        self.file_name = file_name

        project_root = Path(__file__).resolve().parent.parent #root directory

        data_folder = project_root / "data"

        self.path = data_folder / self.path
        self.path.mkdir(parents=True, exist_ok=True)
            
        
        if not self.bucket_name:
            raise ValueError("No bucket name")
        
        if not self.aws_region:
            raise ValueError("No aws_region")
        

    
    # Method to save data in local folder
    def save_to_local(self) -> str:

        # Connect with the API.
        try:
            logger.debug(f"Attempting to connect to: {self.api_url}")
            r = requests.get(self.api_url)
            data = r.json()
            r.raise_for_status()
            logger.info(f"Successfully received {len(r.content)} bytes")

          
            # try to save the file into data_raw folder
            try:
                file_path = self.path / self.file_name
                with file_path.open("w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)

            except OSError as e:
                logger.error(f"Error creating folder")
                raise

        except requests.ConnectionError as e:
            logger.error(f"API connection error: {str(e)}")
            raise
        except requests.HTTPError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error occurred: {str(e)}")
            raise

        
    # Method to upload data in S3 bucket
    def save_to_s3(self) -> str:
        s3_client = boto3.client('s3')

        # Connect with the API
        try:
            logger.debug(f"Attempting to connect to: {self.api_url}")
            r = requests.get(self.api_url)
            data = r.json()
            r.raise_for_status()
            logger.info(f"Successfully received {len(r.content)} bytes")

            #try to upload the file into s#
            try:
                s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=self.file_name,
                    Body=json.dumps(data, indent=4) # Convert file to JSON format.
                )
                logger.info(f"File '{self.file_name}' uploaded to bucket '{self.bucket_name}'.")
                return True
            
            except ClientError as e:
                logger.error(e)
                return False
            return True

        
        except Exception as e:
            logger.error(f"Error inesperado {e}")
            raise
    

        
    


if __name__ == '__main__':
    extra = Extract("data.json", f"https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&date=2017-11-15&apikey={os.getenv("API_KEY")}", "data_raw")
    extra.save_to_local()


