#!/usr/bin/env python3
import sys
import requests
import json
import os
import csv
import re
import datetime

import tkinter as tk # this is the preferred import for tkinter
from tkinter.filedialog import askopenfilename

import pandas as pd
import numpy as np


oDir = "./Output"
if not os.path.isdir(oDir) or not os.path.exists(oDir):
    os.makedirs(oDir)


mmsIdFilename = askopenfilename(title = "Select BARCODES input file")

df = pd.read_excel(mmsIdFilename, engine='openpyxl', dtype={'MMS Id': 'str'})


df = df[['MMS Id', 'Title']]

df['Primo Link'] = ""

link_prefix = "https://tufts-primo.hosted.exlibrisgroup.com/primo-explore/search?query=any,contains,"
link_suffix = "&context=L&vid=01TUN&search_scope=EVERYTHING&tab=everything&lang=en_US"

df['Primo Link'] = df['MMS Id'].apply(lambda x: link_prefix + str(x) + link_suffix)

df.to_excel(oDir + "/Titles with Links to Primo from MMS ID.xlsx", index=False)
