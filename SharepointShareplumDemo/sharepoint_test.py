#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : David Hurley
# Contact: davhurley@suncor.com
# Created Date: March 24, 2022
# ---------------------------------------------------------------------------
""" Demo of using SharePlum library to push and pull images from a SharePoint site """
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from shareplum import Site, Office365
from shareplum.site import Version
from dotenv import load_dotenv
from io import BytesIO, StringIO
import datetime
# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------
# Load environment variables - set in .env, override system env with .env
load_dotenv(override=True)

def GetSharePointObject():
    """ Function to authenticate to SharePoint and get site and folder object and files

    Args:

    Returns:
        JSON: files in specified folder
        OBJECT: object pointing to folder
    """
    # use SharePlum REST API to get authorization to SharePoint site
    authcookie = Office365(os.environ['SHAREPOINT_ROOTPATH'], username=os.environ['SHAREPOINT_USERNAME'], password=os.environ['SHAREPOINT_PASSWORD']).GetCookies()

    # get site object containing site contents - found that this works best with v2016
    site = Site(os.environ['SHAREPOINT_ROOTPATH'] + '/sites/' + os.environ['SHAREPOINT_SITENAME'] + '/', version=Version.v2016, authcookie=authcookie)

    # get folder object and json dump of all files in folder
    folder = site.Folder(os.environ['SHAREPOINT_FOLDERPATH'])
    all_files = json.dumps(folder.files, indent=2)

    return all_files, folder

# ---------------------------------------------------------------------------
# PUSH
# ---------------------------------------------------------------------------
# create figure to test upload - this is saved on disk - probably a method to upload direct without saving to disk
X = [0, 1, 2, 3, 4, 5]
y = [10, 20, 30, 40, 50, 60]
plt.figure(figsize=(14,7))
plt.plot(X, y)
plt.title('This image was uploaded {}'.format(datetime.datetime.now()))
plt.savefig('test_plot.jpg')

# convert image to binary
image_stream = 'test_plot.jpg'
with open(image_stream, mode='rb') as file:
    fileContent = file.read()

# upload to folder on SharePoint - (local file path, remote file name)
all_files, folder = GetSharePointObject()
folder.upload_file(fileContent, image_stream)

# ---------------------------------------------------------------------------
# PULL
# ---------------------------------------------------------------------------
# read specific file from SharePoint - uses folder object from above
df = pd.read_csv(BytesIO(folder.get_file('test.csv')))

# export to local csv
df.to_csv('test.csv')