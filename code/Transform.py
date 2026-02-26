import json
import boto3
import logging
from pathlib import Path
import os
from botocore import regions
from botocore.retries.adaptive import bucket
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()  # load env variables

logging.basicConfig(
    level=logging.DEBUG,  # Most detailed level
    format="%(asctime)s [%(levelname)s] %(message)s - %(name)s:%(lineno)d",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)  # handle logs in my code


class TransformData:
    """Class to transform data from s3 bucket"""

    def __init__(
        self,
        path: str,
        bucket_name: str | None = None,
        aws_region: str | None = None,
    ):
        if not path:
            raise ValueError("path is required")

        self.bucket_name = bucket_name or os.getenv("BUCKET_NAME")
        self.aws_region = aws_region or os.getenv("AWS_REGION")
        self.path = Path(path)

        # initialized connection with s3 bucket to get the data
        try:
            self.s3_client = boto3.client("s3", region_name=self.aws_region)
            logger.info(f"S3 client initialized in the {self.aws_region}")
        except Exception as e:
            logger.error(f"Problem with initialied client {e}")
            raise

    # lists object inside s3 bucket
    def list_object_s3(self, prefix: str = "") -> list[str]:
        # try to list object  inside the bucket
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=prefix
            )
            logger.info(f"object list in {self.bucket_name}")
            content = response.get("Contents", [])
            keys = [obj["Key"] for obj in content if obj["Key"].endswith(".json")]
            logger.info(f"Found {len(keys)} JSON files in bucket {self.bucket_name}")
            return keys
        except ClientError as e:
            logger.error(f"ClientError {e}")
            return []

    # get object from s3
    def get_object_s3(self, key: str) -> dict | None:
        try:
            logger.info(f"Downloading object: {key}")
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            body = response["Body"]
            content = body.read()
            text = content.decode()
            data = json.loads(text)
            logger.info(f"Successfully downloaded and parsed: {key}")
            return data
        except ClientError as e:
            logger.error(f"ClientError downloading {key}: {e}")
            return None


if __name__ == "__main__":
    trans = TransformData("./temp")
    keys = trans.list_object_s3()
    data = trans.get_object_s3(keys[0])
    print(data)
