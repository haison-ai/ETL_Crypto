#Import libraries.
import json
from dotenv import load_dotenv
from pathlib import Path
import requests
import os
import datetime
import boto3
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
    def __init__(self, api_url, path=None, bucket_name=None, aws_region=None):
        self.bucket_name = bucket_name or os.getenv("BUCKET_NAME")
        self.aws_region = aws_region or os.getenv("AWS_REGION")
        self.path = path
        self.api_url = api_url

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
        try:
            logger.debug(f"Attempting to connect to: {self.api_url}")
            r = requests.get(self.api_url)
            data = r.json()
            r.raise_for_status()
            logger.info(f"Successfully received {len(r.content)} bytes")

          
            # try to save the file into data_raw folder
            try:
                file_path = self.path / "data.json"
                with file_path.open("w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)

            except OSError as e:
                logger.error(f"Error creating folder")
                raise
               
                
                
                  # First 200 characters
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
        pass
    


if __name__ == '__main__':
    extra = Extract("https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&date=2017-11-15&apikey=api_key", "data_raw")
    extra.save_to_local()


