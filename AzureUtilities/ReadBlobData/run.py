#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : David Hurley
# Contact: davhurley@suncor.com
# Created Date: September 28, 2021
# ---------------------------------------------------------------------------
""" Script to run demo of load_azure_data.py """
# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
from load_azure_data import load_csv_data_azure
# ---------------------------------------------------------------------------
# CODE
# ---------------------------------------------------------------------------
# Set container name and blob name
container_name = 'XXXXX'
blob_name = 'XXXX/XXXX.csv'

# Read csv data into dataframe direct from Azure blob - can also use excel or parquet formats
data = load_csv_data_azure(container_name, blob_name)

# Print first few rows of data
print(data.head())