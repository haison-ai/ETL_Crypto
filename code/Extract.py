#Import libraries.
import json
from dotenv import load_dotenv
import requests
import os
import datetime
import boto3

BASE_FOLDER = "data_raw"

class extract():
    """
    Class to extract data from financial API.
    """
    def __init__(self):
        pass

    # Method to save data in local folder
    def save_to_local(str: path_local) -> None:
        pass

    # Method to upload data in S3 bucket
    def save_to_s3(str: path_S3) -> None: 
        pass
    




