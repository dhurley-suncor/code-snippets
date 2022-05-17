#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : David Hurley
# Contact: davhurley@suncor.com
# Created Date: September 28, 2021
# ---------------------------------------------------------------------------
""" Utility functions to help in connecting to Azure resources. These functions
    authenticate to Azure using the DefaultAzureCredential function which 
    attempts to authenticate in 6 ways (see README). Less sensitive information
    such as blob storage url paths can go in .env but better yet is to put in 
    key vault (not done here). """
# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
import os
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from io import StringIO, BytesIO
from dotenv import load_dotenv
# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------
# Load environment variables - set in .env, override system env with .env
load_dotenv(override=True)

def load_csv_data_azure(container_name, blob_name):
    """ Function to read csv data direct from Azure storage resource to pandas dataframe. 
     When developing locally reads Azure path variables from .env and when deployed
     as a web app reads from the App Services parameters. Or set up as key vault and 
     code will work across Azure resources

    Args:
        container_name: name of container to read data from
        blob_name: blob_name and path to blob within container, this is everything after container name in the url path

    Returns:
        DataFrame of file values
    """
    
    # Setup access credentials to Azure resource
    default_credential = DefaultAzureCredential(exclude_interactive_browser_credential=False) # allow interactive authentication
    blob_service_client_instance = BlobServiceClient(os.environ['STORAGE_ACCOUNT_URL'], credential=default_credential)
    blob_client_instance = blob_service_client_instance.get_blob_client(container_name, blob_name)

    # Read csv blob into memory
    blob_target = blob_client_instance.download_blob().content_as_text()
    data = pd.read_csv(StringIO(blob_target)) # StringIO creates a string buffer in memory which can be read like a file - nothing on disk

    return data

def load_excel_data_azure(container_name, blob_name):
    """ Function to read excel data direct from Azure storage resource to pandas dataframe
    When developing locally reads Azure path variables from .env and when deployed
    as a web app reads from the App Services parameters. Or set up as key vault and 
    code will work across Azure resources

    Args:
        container_name: name of container to read data from
        blob_name: blob_name and path to blob within container, this is everything after container name in the url path

    Returns:
        DataFrame of file values
    """
    # Set access to Azure resource
    default_credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    blob_service_client_instance = BlobServiceClient(os.environ['STORAGE_ACCOUNT_URL'], credential=default_credential)
    blob_client_instance = blob_service_client_instance.get_blob_client(container_name, blob_name)

    # Read excel blob into memory - must use openpyxl engine
    blob_target = blob_client_instance.download_blob().content_as_bytes()
    data = pd.read_excel(blob_target, engine='openpyxl')

    return data

def load_parquet_data_azure(container_name, blob_name):
    """ Function to read parquet data direct from Azure storage resource to pandas dataframe
    When developing locally reads Azure path variables from .env and when deployed
    as a web app reads from the App Services parameters. Or set up as key vault and 
    code will work across Azure resources

    Args:
        container_name: name of container to read data from
        blob_name: blob_name and path to blob within container, this is everything after container name in the url path

    Returns:
        DataFrame of file values
    """
    # Set access to Azure resource
    default_credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    blob_service_client_instance = BlobServiceClient(os.environ['STORAGE_ACCOUNT_URL'], credential=default_credential)
    blob_client_instance = blob_service_client_instance.get_blob_client(container_name, blob_name)

    # Read parquet blob into memory
    stream = BytesIO()
    blob_client_instance.download_blob().readinto(stream)
    data = pd.read_parquet(stream, engine='pyarrow')

    # For some reason parquet data read into pandas doesn't retain dtype so everything is an object type - conversion to numeric
    # is needed in order to plot, guess and check....
    for column in data:
        try:
            data[column] = pd.to_numeric(data[column])
        except:
            data[column] = data[column]

    return data