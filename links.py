#!/usr/bin/env python3
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
########
########
########    Author:           Henry Steele, Library Technology Services, Tufts University
########    Name of Program:  Links
########	Files:			  links.py
########    Date created:     2019-06
########
########    Purpose and method:
########      - Retrieves an Analytics report of MMS Ids and fund codes, by specifying a path to
########        each libray's separate report, and sending a date filter for fiscal year.
########        parses out MMS ID from report and uses to construct a Primo URL (search)
########        that can be used as a link in the bookplate site in Drupal
########

import sys
import requests
import json
import os
import csv
import re
import datetime
import xml.etree.ElementTree as et
# from tkinter.filedialog import askopenfilename
# from django.utils.encoding import smart_str, smart_unicode
# import shutil as shu
# import subprocess
# import ntpath
#for dataframes
import pandas as pd
import numpy as np

# iep_filename = askopenfilename(title = "Select CSV containing Gift Fund records with MMS Id and IEP")
# gift_filename = askopenfilename(title = "Select CSV .csv file containing titles with gift funds data")
#
# iep_df = pd.read_csv(iep_filename, encoding='utf-8', dtype={'MMS Id': 'str', 'Item Id': 'str', 'IEP': 'str'})
# fund_df = pd.read_csv(gift_filename, encoding='utf-8', dtype={'MMS Id': 'str', 'Item Id': 'str', 'IEP': 'str'})
#
# df = pd.merge(iep_df, fund_df, on='MMS Id')

oDir = "./Output"
if not os.path.isdir(oDir) or not os.path.exists(oDir):
       os.makedirs(oDir)

library = input("\n\nWhat library do you want to retreive MMS IDs for? \n\n      1) Tisch\n      2) Ginn\n\nChoose an option: ")

fiscal_year = input("\n\nWhat fiscal year do you want to retreive MMS IDs for? E.g. '2020': ")

parsed_library = ""

if library == "1" or library == "Tisch Library" or library == "Tisch" or library == "TISCH" or library == "tisch" or library == 1:
    parsed_library = "Tisch Library"

elif library == "2" or library == "Ginn Library" or library == "Ginn" or library == "GINN" or library == "ginn" or library == 2:
    parsed_library = "Ginn Library"


# if re.search("^\d{4}$", fiscal_year, re.IGNORECASE) == None:
#     print("Please enter a 4 digit year")
#     sys.exit(1)
# fiscal_year = int(fiscal_year)
# last_year = int(fiscal_year) - 1
# start_date = datetime.date(last_year, 7, 1)
# end_date = datetime.date(fiscal_year, 6, 30)
#
# start_date_string = start_date.strftime("%Y-%m-%d")
# end_date_string = end_date.strftime("%Y-%m-%d")

######################################################################################################
######################################################################################################
#######     composing URL to retrieve Analtyics report, with filter
url = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports?apikey=l7xxe0d3b0c4773a406083dd061775404faa"
limit = "&limit=1000"
format = "&format=xml"

if parsed_library == "Tisch Library":
    path = "&path=%2Fshared%2FTufts%20University%2FReports%2FCollections%2FGift%20Funds%2FTitles%20Purchased%20with%20Gift%20Funds%20-%20MMS%20and%20Fund%20-%20Tisch"
elif parsed_library == "Ginn Library":
    path = "&path=%2Fshared%2FTufts%20University%2FReports%2FCollections%2FGift%20Funds%2FTitles%20Purchased%20with%20Gift%20Funds%20-%20MMS%20and%20Fund%20-%20Ginn"


filter = "&filter=%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3Acomparison%22+op%3D%22and%22+xmlns%3Asaw%3D%22com.siebel.analytics.web%2Freport%2Fv1.1%22+%0D%0A++xmlns%3Asawx%3D%22com.siebel.analytics.web%2Fexpression%2Fv1.1%22+%0D%0A++xmlns%3Axsi%3D%22http%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema-instance%22+%0D%0A++xmlns%3Axsd%3D%22http%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%22%3E%0D%0A%09%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3Acomparison%22+op%3D%22notEqual%22%3E%0D%0A%09%09%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3AsqlExpression%22%3E%22Bibliographic+Details%22.%22MMS+Id%22%3C%2Fsawx%3Aexpr%3E%0D%0A%09%09%3Csawx%3Aexpr+xsi%3Atype%3D%22xsd%3Astring%22%3E-1%3C%2Fsawx%3Aexpr%3E%0D%0A%09%3C%2Fsawx%3Aexpr%3E%0D%0A%09%0D%0A%09%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3Acomparison%22+op%3D%22equal%22%3E%0D%0A+++++++++++++++%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3AsqlExpression%22%3E%22Transaction+Date%22.%22Transaction+Date+Fiscal+Year%22%3C%2Fsawx%3Aexpr%3E%3Csawx%3Aexpr+xsi%3Atype%3D%22xsd%3Adecimal%22%3E" + str(fiscal_year) + "%3C%2Fsawx%3Aexpr%3E%0D%0A%09%3C%2Fsawx%3Aexpr%3E%0D%0A%3C%2Fsawx%3Aexpr%3E"




report = requests.get(url + format + path + limit + filter)



report_string = report.content
# #
print(report_string)
tree = et.ElementTree(et.fromstring(report.content))

root = tree.getroot()

isFinished = root[0][1].text
resumptionToken = root[0][0].text
isFinishedContinue = isFinished
result_set = root[0][2][0]
######################################################################################################
######################################################################################################
#######     since, output is limited to 1,000 records, iterate through whole report
while isFinishedContinue == "false":
    full_path = url + "&token=" + resumptionToken
    reportContinue = requests.get(url + "&token=" + resumptionToken)
    # print ("\n\n\n\n" + str(reportContinue.content) + "\n\n\n\n")
    report_string += reportContinue.content

    treeContinue = et.ElementTree(et.fromstring(reportContinue.content))
    rootContinue = treeContinue.getroot()
    result_set_continue = rootContinue[0][1][0]
    result_set.append(result_set_continue)


    isFinishedContinue = rootContinue[0][0].text


mms_id_and_fund_dict = []
mms_id_list = []

x = 0

for element in result_set.iter():


    if re.match(r'.*Row', element.tag):
        mms_id = ""
        fund_code = ""

        for subElement in element.iter():

            if re.match(r'.*Column1', subElement.tag):

                mms_id = subElement.text
                mms_id_list.append(mms_id)

            elif re.match(r'.*Column2', subElement.tag):
                fund_code = subElement.text

            elif re.match(r'.*Column4', subElement.tag):
                fiscal_year = subElement.text



        mms_id_and_fund_dict.append({'MMS Id': mms_id, 'Fund Ledger Code': fund_code, 'Fiscal Year': fiscal_year})

    x += 1

mms_id_and_fund_df = pd.DataFrame(columns=['MMS Id', 'Fund Ledger Code', 'Fiscal Year'], data=mms_id_and_fund_dict)
mms_id_and_fund_df.to_csv(oDir + "/MMS ID and Fund.csv", index=False)


iep_df = pd.read_csv(oDir + "/MMS ID and Fund.csv", encoding='utf-8', dtype={'MMS Id': 'str', 'Fund Ledger Code': 'str'})

# oDir = "./Output"
# if not os.path.isdir(oDir) or not os.path.exists(oDir):
#        os.makedirs(oDir)

#output_file = open(oDir + "/Primo Links for Website.txt")

#link_prefix = "https://tufts-primo.hosted.exlibrisgroup.com/primo-explore/fulldisplay?docid=01TUN_ALMA"

link_prefix = "https://tufts-primo.hosted.exlibrisgroup.com/primo-explore/search?query=any,contains,"
link_suffix = "&context=L&vid=01TUN&search_scope=EVERYTHING&tab=everything&lang=en_US"
#link = "https://tufts-primo.hosted.exlibrisgroup.com/primo-explore/search?query=any,contains,991009865119703851&tab=everything&search_scope=EVERYTHING&vid=01TUN&lang=en_US&offset=0"
mms_id_and_fund_df['Link'] = mms_id_and_fund_df['MMS Id'].apply(lambda x: link_prefix + str(x) + link_suffix)

mms_id_and_fund_df.to_excel(oDir + "/Titles with Links to Primo.xlsx", index=False)
