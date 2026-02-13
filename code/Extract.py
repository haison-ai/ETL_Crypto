# Import libraries.
import json
import time
import logging
import os
from datetime import datetime
from pathlib import Path

import boto3
import requests
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()  # take env variable

# Detailed logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # Most detailed level (DEBUG shows everything)
    format="%(asctime)s [%(levelname)s] %(message)s - %(name)s:%(lineno)d",
    datefmt="%Y-%m-%d %H:%M:%S",  # Custom timestamp format
)

logger = logging.getLogger(__name__)  # handle logs in my code


class Extract:
    """
    Class responsible for extracting and processing financial data from APIs.
    Handles data retrieval, local storage, and S3 upload operations.
    """

    def __init__(
        self,
        extraction_date=None,
        api_url=None,
        path=None,
        bucket_name=None,
        aws_region=None,
        self_data=None,
        coin_name=None,
    ):
        self.bucket_name = bucket_name or os.getenv("BUCKET_NAME")
        self.aws_region = aws_region or os.getenv("AWS_REGION")
        self.path = path
        self.data = self_data
        self.api_url = api_url
        self.extraction_date = extraction_date
        self.coin_name = coin_name

        # Format the extraction date for partitioning
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        dt = datetime.strptime(self.extraction_date, "%Y-%m-%d")
        self.partition_path = f"year={dt.year}/month={dt.month}/day={dt.day:02d}/"
        self.file_name = (
            f"raw/{self.partition_path}/data_{current_time}_{self.coin_name}.json"
        )
        project_root = Path(__file__).resolve().parent.parent  # root directory
        data_folder = project_root / "data"
        self.path = data_folder / path / self.partition_path
        self.path.mkdir(parents=True, exist_ok=True)

        if not self.bucket_name:
            raise ValueError("No bucket name")

        if not self.aws_region:
            raise ValueError("No aws_region")

    # get_data_api
    def fetch_data_api(self):
        try:
            logger.debug(f"Attempting to connect to: {self.api_url}")
            # We define the headers as per the documentation
            headers = {
                "accept": "application/json",
                "x-cg-demo-api-key": os.getenv(
                    "API_KEY"
                ),  # Fetches YOUR_API_KEY from .env
            }

            r = requests.get(self.api_url)
            self.data = r.json()
            r.raise_for_status()
            logger.info(f"Successfully received {len(r.content)} bytes")
            return self.data
        except Exception as e:
            logger.error(f"Error fetching data from API: {e}")

    # Method to save data in local folder
    def save_to_local(self) -> str:
        if self.data is None:
            logger.error("No data to save")
            return False
        try:
            only_file_name = Path(self.file_name).name
            file_path = self.path / only_file_name
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            logger.info(f"File '{self.file_name}' saved to '{self.path}'.")
            return True
        except OSError as e:
            logger.error(f"Error creating folder {e}")
            raise

    # Method to upload data in S3 bucket
    def save_to_s3(self) -> str:
        s3_client = boto3.client("s3")

        # Connect with the API
        if self.data is None:
            logger.error("No data to upload")
            return False

        # try to upload the file into s#
        try:
            s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.file_name,
                Body=json.dumps(self.data, indent=4),  # Convert file to JSON format.
            )
            logger.info(
                f"File '{self.file_name}' uploaded to bucket '{self.bucket_name}'."
            )
            return True

        except ClientError as e:
            logger.error(f"client error: {e}")
            return False


if __name__ == "__main__":
    date = "2026-02-09"
    coins = ["bitcoin", "ethereum", "solana", "binancecoin", "cardano"]
    for coin in coins:
        api_url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=30&interval=daily"
        extra = Extract(date, api_url, "data_raw", coin_name=coin)
        if extra.fetch_data_api():
            extra.save_to_local()
            extra.save_to_s3()

        time.sleep(15)
