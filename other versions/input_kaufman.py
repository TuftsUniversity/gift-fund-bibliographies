#!/usr/bin/env python3
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
########
########
########    Author:           Henry Steele, Library Technology Services, Tufts University
########    Name of Program:  Input
########	Files:			  input.py, functions.py
########    Date created:     2020-09
########
########    Purpose:
########      - input for the initial part of the gift funds bibliography process, automating the Alma
########        and Analtyics part of the process
########
########    Method:
########      - retrieve Analytics reports of MMS IDs and funds for gift funds for given library and year
########      - run Alma SRU query for each MMS ID
########      - parse into output files for rest of processo
########      - input a table containing all titles in the set of funds needing letters
########      - parse these titles lists per fund to convert them to BibTex (LaTeX for bibliography)".bib" format
########      - use Pybtex and a local system installation of Texworks latex processo
########        create a latex file and output to PDF
########      - Note this script is set to work with Python 3.x
########
########    Input:
########      - a tilde delimited text file containing a list of titles and funds with the following fields, from
########        an exported MARC file from Alma.  This tabular file is created with the XSLT file in this directoty
########        "giftFunds.xsl" that takes a MARC XML export from Alma's Export Bibliographic Records job
########        that was created from a managed set created by the "Titles Purchased with Gift Funds - for Export"
########        at https://analytics-na01.alma.exlibrisgroup.com/analytics/saw.dll?Answers&path=%2Fshared%2FTufts%20University%2FReports%2FCollections%2FGift%20Funds%2FTitles%20Purchased%20with%20Gift%20Funds%20-%20for%20Export
########
########        Since fund data isn't reliably in bib records, this script also takes a Analtics fund report directly, from
########        "Titles Purchased with Gift Funds - MMS and Fund" at https://analytics-na01.alma.exlibrisgroup.com/analytics/saw.dll?Answers&path=%2Fshared%2FTufts%20University%2FReports%2FCollections%2FGift%20Funds%2FTitles%20Purchased%20with%20Gift%20Funds%20-%20MMS%20and%20Fund
########
########        These are the fields needed for each
########
########        "Titles Purchased with Gift Funds - for Export":
########          + MMS Id
########          + Main entry Author (MARC 100|a)
########          + Main entry Author relator (MARC 100|e)
########          + Second author (MARC 110|a)
########          + Second author relator (MARC 110|e)
########          + Corporate author (MARC 700|a)
########          + Corporate author relator (MARC 700|e)
########          + Second corporate author (MARC 710|a)
########          + Second corporate author relator (MARC 710|e)
########          + Title (MARC 245|a)
########          + Subtitle (MARC 245|b)
########          + Place of publication (MARC 260|a)
########          + Name of publisher (MARC 260|b)
########          + Date of publication (MARC 260|c)
########          + Place of second publication (MARC 264|a)
########          + Name of second publisher (MARC 264|b)
########          + Date of second publication (MARC 264|c)
########          + Fund (MARC 981|a)
########
########        - "Titles Purchased with Gift Funds - MMS and Fund"
########          + MMS ID (changed field name to "MMS ID" from "MMS Id".  This is needed to match bib export)
########          + Fund Ledger Name
########          + Fund Ledger Code
########
########        - exclusion files
########          + if you run this script and find that it hangs on certain funds,
########            enter these fund names in the prompted exclusion list, and
########            then run the LaTeX processes separately on these funds manually
########            afterward
########    Outputs:
########      - A BibTex .bib file containing titles purchased with each fund in the input table
########      - a PDF of this data in human readable format suitable for attaching to a donor letter
########
########    Dependences:
########        You need to have a working LaTeX processor on your computer
########        I used this process with both MikTex and TexLive.
########
########        Installation instructions for MikTex and TexLive are below.  Note that because configuration of
########        these various LaTeX utilities requires use of GUI Tools, I am not currently installing
########        this on a server to which I only have command line accesss.
########
########        Installation links:
########          + https://miktex.org/howto/install-miktex
########          +https://www.tug.org/texlive/quickinstall.html
########
########        Note that if you want Tex Live to take precedence, you have to list it first in
########        the environment path variable.   You can see which program is used to process LaTeX
########        by just typing "latex --version" in the command line
########
########        You also need to add the "biblatex" and "biblatex-biber" packages through the MikTex admin console.
########        Biber allows you more flexibilty with citations such as having both
########        an author and translator or editors in the reference.
########        These directions are for MikTex but you could also manage this process using Tex Live.
########        Tufts Libraries want their citations in Chicago style, so you will also need to enable the
########        "biblatex-chicago" pacakage.
########
########        These directions are for Windows.
########          - open the MikTex admin console as an Administrator
########          - go to Packages and choose "biblatex"
########          - click the "+" sign to install (or update)
########          - in packages, find miktex-biber-bin-x64.  Press "+" to install and/or update
########          - in packages, find biblatex-chicago.  Press "+" to install and/or update
########          - you must now update the changes in MikTex's database.
########          - In the Tasks menu, click "Refresh filename databases"
########          - Wait for this to finish.  It may take a minute or so.  A message with the status appears
########            at the bottom of packages list.
########          - In the Tasks menu, click Update package database
########          - Wait for this to finish.  It may take a minute or so.  A message with the status appears
########            at the bottom of packages list.
########
########        Installation instructions for MikTex and TexLive are below.  Note that because configuration of
########        these various LaTeX utilities requires use of GUI Tools, I am not currently installing
########        this on a server to which I only have command line accesss.
########
########        Note that if you want Tex Live to take precedence, you have to list it first in
########        the environment path variable.   You can see which program is used to process LaTeX
########        by just typing "latex --version" in the command line
########
########      - need to install a few modules:
########        + pip install
########
########     Notes:
########       - DOS vs. Linux
########          such as described at
########          https://stackoverflow.com/questions/3949161/no-such-file-or-directory-but-it-exists
########          you can try converting the file to Unix format on linux by installing dos2unix
########
########          see https://unix.stackexchange.com/questions/277217/how-to-install-dos2unix-on-linux-without-root-access
########
########      - character encoding of command prompt window
########          Note that some input files will contain Unicode that can't be parsed with
########          command prompt's default ascii processor.  To get around this, follow the directions at
########          https://stackoverflow.com/questions/14109024/how-to-make-unicode-charset-in-cmd-exe-by-default
########          or simply Win + R --> cmd /K chcp 1250 every time you run this script
########
########      -
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

import sys
import requests
import json
import os
import csv
import re
import datetime
import codecs
from django.utils.encoding import python_2_unicode_compatible, smart_text
from tkinter.filedialog import askopenfilename
import pandas as pd
import numpy as np
import xml.etree.ElementTree as et


##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
########    Retrieve Analytics reports for initial input:
########    - list of MMS IDs from set list of gift funds purchased in the current fiscal year.
########      The list of funds will be be static and part of the Analytics report.
########      The date range will have to be passed as a SAW XML filter to the generic report, for Tisch.
########      The user will set the date range by entering fiscal year as "FY\d\d\d\d" in
########      the first prompt, and choose library by choosing either Tisch or Ginn in the second.
########      The library chosen will affect which report it goes to.
########    - The new version of this report will also contain fund, so that I don't need to retrieve both reports,
########      but for the intiial query it will just use MMS ID


# library = input("\n\nWhat library do you want to retreive MMS IDs for? \n\n      1) Tisch\n      2) Ginn\n\nChoose an option: ")
#
# fiscal_year = input("\n\nWhat fiscal year do you want to retreive MMS IDs for? E.g. '2020': ")
#
# parsed_library = ""
#
# if library == "Tisch Library" or library == "Tisch" or library == "TISCH" or library == "tisch" or library == 1:
#     parsed_library = "Tisch Library"
#
# elif library == "Ginn Library" or library == "Ginn" or library == "GINN" or library == "ginn" or library == 2:
#     parsed_library = "Ginn Library"
#
#
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
#
# ######################################################################################################
# ######################################################################################################
# #######     composing URL to retrieve Analtyics report, with filter
# url = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports?apikey=l7xxe0d3b0c4773a406083dd061775404faa"
# limit = "&limit=1000"
# format = "&format=xml"
# path = "&path=%2Fshared%2FTufts%20University%2FReports%2FCollections%2FGift%20Funds%2FTitles%20Purchased%20with%20Gift%20Funds%20-%20Tisch%20-%20Generic%20for%20Script"
# filter = "&filter=%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3Alogical%22+op%3D%22and%22+xmlns%3Asaw%3D%22com.siebel.analytics.web%2Freport%2Fv1.1%22+xmlns%3Asawx%3D%22com.siebel.analytics.web%2Fexpression%2Fv1.1%22+xmlns%3Axsi%3D%22http%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema-instance%22+xmlns%3Axsd%3D%22http%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%22%3E%0D%0A%09%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3Acomparison%22+op%3D%22greaterOrEqual%22%3E%0D%0A%09%09%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3AsqlExpression%22%3E%22Transaction+Date%22.%22Transaction+Date%22%3C%2Fsawx%3Aexpr%3E%0D%0A%09%09%3Csawx%3Aexpr+xsi%3Atype%3D%22xsd%3Adate%22%3E" + start_date_string + "%3C%2Fsawx%3Aexpr%3E%0D%0A%09%3C%2Fsawx%3Aexpr%3E%0D%0A%09%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3Acomparison%22+op%3D%22lessOrEqual%22%3E%0D%0A%09%09%3Csawx%3Aexpr+xsi%3Atype%3D%22sawx%3AsqlExpression%22%3E%22Transaction+Date%22.%22Transaction+Date%22%3C%2Fsawx%3Aexpr%3E%0D%0A%09%09%3Csawx%3Aexpr+xsi%3Atype%3D%22xsd%3Adate%22%3E" + end_date_string + "%3C%2Fsawx%3Aexpr%3E%0D%0A%09%3C%2Fsawx%3Aexpr%3E%0D%0A%3C%2Fsawx%3Aexpr%3E"
#
#
#
#
# report = requests.get(url + format + path + limit + filter)
#
#
#
# report_string = report.content
# # #
# print(report_string)
# tree = et.ElementTree(et.fromstring(report.content))
#
# root = tree.getroot()
#
# isFinished = root[0][1].text
# resumptionToken = root[0][0].text
# isFinishedContinue = isFinished
# result_set = root[0][2][0]
# ######################################################################################################
# ######################################################################################################
# #######     since, output is limited to 1,000 records, iterate through whole report
# while isFinishedContinue == "false":
#     full_path = url + "&token=" + resumptionToken
#     reportContinue = requests.get(url + "&token=" + resumptionToken)
#     # print ("\n\n\n\n" + str(reportContinue.content) + "\n\n\n\n")
#     report_string += reportContinue.content
#
#     treeContinue = et.ElementTree(et.fromstring(reportContinue.content))
#     rootContinue = treeContinue.getroot()
#     result_set_continue = rootContinue[0][1][0]
#     result_set.append(result_set_continue)
#
#
#     isFinishedContinue = rootContinue[0][0].text
#

mms_id_and_fund_df = pd.read_csv('input/Kaufman/Analytics input list - MMS Id and Fund.txt', dtype={'MMS Id': 'str'})
mms_id_df = pd.read_csv('input/Kaufman/Analytics input list - just MMS Id.txt', dtype={'MMS Id': 'str'})
mms_id_and_fund_dict = []
mms_id_list = []

x = 0

while x < len(mms_id_and_fund_df):
    mms_id = mms_id_and_fund_df.iloc[x]['MMS Id']
    mms_id_list.append(mms_id)

    fund_code = mms_id_and_fund_df.iloc[x]['Fund']
    mms_id_and_fund_dict.append({'MMS Id': mms_id, 'Fund Ledger Code': fund_code})
    x += 1
# for element in result_set.iter():
#
#
#     if re.match(r'.*Row', element.tag):
#         mms_id = ""
#         fund_code = ""
#
#         for subElement in element.iter():
#
#             if re.match(r'.*Column1', subElement.tag):
#
#                 mms_id = subElement.text
#                 mms_id_list.append(mms_id)
#
#             elif re.match(r'.*Column2', subElement.tag):
#                 fund_code = subElement.text
#
#         mms_id_and_fund_dict.append({'MMS Id': mms_id, 'Fund Ledger Code': fund_code})
#
#     x += 1
pDir = "./Processing"
if not os.path.isdir(pDir) or not os.path.exists(pDir):
       os.makedirs(pDir)
mms_id_and_fund_df = pd.DataFrame(columns=['MMS Id', 'Fund Ledger Code'], data=mms_id_and_fund_dict)
mms_id_and_fund_df.to_csv(pDir + "/MMS ID and Fund.csv", index=False)

print(json.dumps(mms_id_and_fund_dict))

y = 0
sru_url = "https://tufts.alma.exlibrisgroup.com/view/sru/01TUN_INST?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=alma.mms_id="



outfile = open(pDir + "/gifts_funds.txt", "w+", encoding='utf-8')

outfile.write("MMS Id~Author~Author Name~Author Relator~Second Author Name~Second Author Relator~Corporate Author Name~Corporate Author Relator~Second Corporate Author Name~Second Corporate Author Relator~Title~First Place of Publication~First Publisher~First Published Year~Second Place of Publication~Second Publisher~Second Published Year\n")
######################################################################################################
######################################################################################################
#######     iterate through MMS Id list and retrieve bib record by SRU
for id in mms_id_list:
    id = str(id)

    result = requests.get(sru_url + id)




    outfile.write(id + "~")
    print(id)
    tree_bib_record = et.ElementTree(et.fromstring(result.content.decode('utf-8')))
    root_bib_record = tree_bib_record.getroot()

    namespaces = namespaces = {'ns1': 'http://www.loc.gov/MARC21/slim'}

    ######################################################################################################
    ######################################################################################################
    #######     in the returned XML bib record, parse out relevant fields and write to
    #######     tilde-delimited text file
    one_hundred = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='100']/ns1:subfield[@code='a']", namespaces):
        one_hundred.append(record.text)

    outfile.write(";".join(one_hundred))
    outfile.write("~")


    one_hundred_2 = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='100']/ns1:subfield[@code='a']", namespaces):
        one_hundred_2.append(record.text)

    outfile.write(";".join(one_hundred_2))
    outfile.write("~")



    one_hundred_e = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='100']/ns1:subfield[@code='e']", namespaces):
        one_hundred_e.append(record.text)

    outfile.write(";".join(one_hundred_e))
    outfile.write("~")

    one_ten = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='110']/ns1:subfield[@code='a']", namespaces):
        one_ten.append(record.text)

    outfile.write(";".join(one_ten))
    outfile.write("~")



    one_ten_e = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='110']/ns1:subfield[@code='e']", namespaces):
        one_ten_e.append(record.text)

    outfile.write(";".join(one_ten_e))
    outfile.write("~")


    seven_hundred = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='700']/ns1:subfield[@code='a']", namespaces):
        seven_hundred.append(record.text.encode('utf-8', 'ignore').decode('utf-8', 'ignore'))


    # for element in seven_hundred:
    #     print(id + " - " + str(element.encode('utf-8', 'ignore').decode('utf-8', 'ignore')))
    outfile.write(";".join(seven_hundred).encode('utf-8', 'ignore').decode('utf-8', 'ignore'))
    outfile.write("~")



    seven_hundred_e = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='700']/ns1:subfield[@code='e']", namespaces):
        seven_hundred_e.append(record.text)

    outfile.write(";".join(seven_hundred_e))
    outfile.write("~")

    seven_ten = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='710']/ns1:subfield[@code='a']", namespaces):
        seven_ten.append(record.text)

    outfile.write(";".join(seven_ten))
    outfile.write("~")



    seven_ten_e = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='710']/ns1:subfield[@code='e']", namespaces):
        seven_ten_e.append(record.text)

    outfile.write(";".join(seven_ten_e))
    outfile.write("~")


    two_forty_five_a = root_bib_record.find(".//ns1:datafield[@tag='245']/ns1:subfield[@code='a']", namespaces)
    if two_forty_five_a is not None:
        # two_forty_fve_a = re.sub(r'().+?)\s$', r'\1', two_forty_five_a)
        outfile.write(two_forty_five_a.text)


    two_forty_five_b  = root_bib_record.find(".//ns1:datafield[@tag='245']/ns1:subfield[@code='b']", namespaces)
    if two_forty_five_b is not None:
        outfile.write(" ")
        outfile.write(two_forty_five_b.text)

    outfile.write("~")

    two_sixty_a = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='260']/ns1:subfield[@code='a']", namespaces):
        two_sixty_a.append(record.text)

    outfile.write(";".join(two_sixty_a))
    outfile.write("~")

    two_sixty_b = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='260']/ns1:subfield[@code='b']", namespaces):
        two_sixty_b.append(record.text)

    outfile.write(";".join(two_sixty_b))
    outfile.write("~")

    two_sixty_c = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='260']/ns1:subfield[@code='c']", namespaces):
        two_sixty_c.append(record.text)

    outfile.write(";".join(two_sixty_c))
    outfile.write("~")

    two_sixty_four_a = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='264']/ns1:subfield[@code='a']", namespaces):
        two_sixty_four_a.append(record.text)

    outfile.write(";".join(two_sixty_four_a))
    outfile.write("~")

    two_sixty_four_b = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='264']/ns1:subfield[@code='b']", namespaces):
        two_sixty_four_b.append(record.text)

    outfile.write(";".join(two_sixty_four_b))
    outfile.write("~")


    two_sixty_four_c = []
    for record in root_bib_record.findall(".//ns1:datafield[@tag='264']/ns1:subfield[@code='c']", namespaces):
        two_sixty_four_c.append(record.text)

    outfile.write(";".join(two_sixty_four_c))
    outfile.write("~")






    outfile.write("\n")

    y += 1

outfile.close()
