######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
########
########
########    Author:           Henry Steele, Library Technology Services, Tufts University
########    Name of Program:  Parse Funds
########	Files:			  parseFunds.py, functions.py
########    Date created:     2018-12
########
########    Purpose:
########      - using parsed MARC exports from Alma and Analytics, create a bibliography
########        of titles purchased with a set of gift funds so libraries can send thank you
########        letters to donors
########
########    Method:
########      - input a table containing all titles in the set of funds needing letters
########      - parse these titles lists per fund to convert them to BibTex (LaTeX for bibliography)".bib" format
########      - use Pybtex and a local system installation of Texworks latex processo
########        create a latex file and output to PDF
########      - Note this script is set to work with Python 2.7.x
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
from Tkinter import Tk
from tkFileDialog import askopenfilename
from django.utils.encoding import smart_str, smart_unicode
import subprocess
import ntpath
#for dataframes
import pandas as pd
import numpy as np
import shutil as shu


import time

sys.path.append('scripts/')
from functions import *


######################################################################################################
######################################################################################################
#######     input text file into dataframe

print("\n\n")
print("##########################################################################")
print("##########################################################################")
print("##########################################################################")
print("##########################################################################")
print("########     ")
print("########     This program takes two input files--one of ")
print("########     parsed bib export records from Analytics -->")
print("########     Managed Sets-->Export bibs, run through ")
print("########     the XSLT in this directory giftFunds.xsl")
print("########     , and one of gift funds taken directly from")
print("########     Analytics")

print("########     ")
print("########     It outputs bibliographies for each fund in the ")
print("########     \"Output\" folder, based on LaTeX and associated")
print("########     files in the \"Processing\" folder")
print("########     ")
print("########     If you run through the list and find that the process")
print("########     hangs on certain funds, you can either run LaTeX commands")
print("########     directly in each folder in the processing folder (see")
print("########     directions when script completes if there are errors)")
print("########     or, enter them in the exclusion list below after emptying")
print("########     out the processing folder before triggering the script")
print("########     ")
print("########     ")
print("\n\n\n\n")

exclusionFundsInput = raw_input("Enter the names of funds\nyou'd like to be excluded, separated by semicolons.\nOr press \"Enter\" to continue: ")

exclusionList = exclusionFundsInput.split(";")

marcFilename = askopenfilename(title = "Select TEXT .txt file containing parsed MARC records")
giftFilename = askopenfilename(title = "Select CSV .csv file containing titles with gift funds data")

oDir = "./Output"
if not os.path.isdir(oDir) or not os.path.exists(oDir):
       os.makedirs(oDir)

pDir = ".\\Processing"
if not os.path.isdir(pDir) or not os.path.exists(pDir):
       os.makedirs(pDir)

# outfile = open(oDir + "/output_file.bib", "w+")
marcDF = pd.read_csv(marcFilename, sep="~", encoding='utf-8')
fundDF = pd.read_csv(giftFilename, encoding='utf-8')

for col in marcDF.columns:
    marcDF[col] = marcDF[col].apply(lambda x: smart_str(x))

for col in fundDF.columns:
    fundDF[col] = fundDF[col].apply(lambda x: smart_str(x))

gf = pd.merge(marcDF, fundDF, on='MMS Id')



for col in gf.columns:
    gf[col] = gf[col].apply(lambda x: x.replace("&", "\&"))

gf= gf.replace('nan', '', regex=True)
# gfString = gf.select_dtypes(include='str')
# gfNonString = gf.select_dtype(exclude='str')


gf = gf.drop(gf[gf['Title'].str.isupper()].index)


gf = gf.drop_duplicates(subset=['Title', 'Author'], keep='first')



######################################################################################################
######################################################################################################
#######     sort by fund, get list of funds,
#######     for each fund in funds list,
#######     segment master dataframe
#gf = gf.sort_values(['Fund', 'Title'])



#print("\n\n")

# gf = gf.replace('nan', 'Empty', regex=True)


gf = gf.rename(columns={'Fund Ledger Code':'Fund'})
fundArray = gf.Fund.unique()
#print(gf)

fundList = fundArray.tolist()

#outfile.write(smart_str(gf.to_string()))
#outfile.write("\n")
print(fundList)

#print("\n\n")



######################################################################################################
#######################################################################################################
#######     loop through titles.
#######     for each title, create a bib-formatted
#######     entry in the bib file
#######     receive creator (authors from various)
#######     MARC fields) and relator strings
#######
#######     The string may be a semicolon delimited list, so iterate through
#######     this with a regex match loop and store in an array.  Do the same
#######     for the relators--turn them into an array (list)
#######
#######     Then you can create BibTex statements in the .bib file
#######     for author, translator, and editor


######################################################################################################
######################################################################################################
#######     for each segment, create a .bib file
#######     to store in "/Processing/"
#######

for fund in fundList:
    pFundDir = pDir + "/" + fund
    if not os.path.isdir(pFundDir) or not os.path.exists(pFundDir):
           os.makedirs(pFundDir)

    texOutputFilename = pFundDir + "/output_file.tex"
    texFundFilename = pFundDir + "/" + fund + ".tex"
    shu.copyfile("./output_file.tex", pFundDir + "/output_file.tex")

    # raw_input("Press Enter to continue[copied tex]...")
    texfile = open(texOutputFilename, mode='r')



    texFileString = texfile.read()



    #print("\n\n" + texFileString + "\n\n")
    fundDotBib = fund + ".bib"
    texFileString = texFileString.replace('output_file.bib', fundDotBib)
    if fund == "gmanb":
        print("Fund" + fund + "\n")
        print(fundDotBib + "\n")
        print(texFileString + "\n")
    # raw_input("\n\nPress Enter to continue...")
    #print("\n\n" + texFileString + "\n\n")
    texfile.close()

    time.sleep(1)
    texfileWrite = open(texFundFilename, "w+")

    texfileWrite.write(smart_str(texFileString))

    texfileWrite.close()

    # raw_input("\n\nPress Enter to continue...")
    bibFilename = pFundDir + "/" + fund + ".bib"
    outfile = open(bibFilename, "w+")
    # raw_input("Press Enter to continue[wrote empty bib]...")

    gfSegment = gf.loc[gf['Fund'] == fund]

    gfSegment = gfSegment.reset_index(drop=True)
    print(gfSegment)
    count = len(gfSegment.index)

    #print("Count: " + str(count) + "\n")

    x = 0
    while x < count:
        title = gfSegment.iloc[x]['Title']
        if title == "":
            continue
            if gfSegment.iloc[x]['Title'].isupper():
                continue
        creator = ""
        if gfSegment.iloc[x]['Author Name'] != "":
            author = gfSegment.iloc[x]['Author Name']

            authorRelator = gfSegment.iloc[x]['Author Relator']
            creator = parseCreator(author, authorRelator)
            #creator = parseCreator(author~ authorRelator)
            creator2 = author + "~ " + authorRelator + "\n"
        if gfSegment.iloc[x]['Second Author Name'] != "Empty":
            secondAuthor = gfSegment.iloc[x]['Second Author Name']
            secondAuthorRelator = gfSegment.iloc[x]['Second Author Relator']
            creator += parseCreator(secondAuthor, secondAuthorRelator)
            creator2 = secondAuthor + "~ " + secondAuthorRelator + "\n"
        if gfSegment.iloc[x]['Corporate Author Name'] != "Empty":
            corporateAuthor = gfSegment.iloc[x]['Corporate Author Name']
            corporateAuthorRelator = gfSegment.iloc[x]['Corporate Author Relator']
            creator += parseCreator(corporateAuthor, corporateAuthorRelator)
            creator2 = corporateAuthor + "~ " + corporateAuthorRelator + "\n"
        if gfSegment.iloc[x]['Second Corporate Author Name'] != "Empty":
            secondCorporateAuthor = gfSegment.iloc[x]['Second Corporate Author Name']
            secondCorporateAuthorRelator = gfSegment.iloc[x]['Second Corporate Author Relator']
            creator += parseCreator(secondCorporateAuthor, secondCorporateAuthorRelator)
            creator2 = secondCorporateAuthor + "~ " + secondCorporateAuthorRelator + "\n"


        if re.search(r'(author.+?)(\r\n|\r|\n)\t+(author.+?)(\r\n|\r|\n)', creator):
            oneAuthor = re.sub(r'(\tauthor.+?)(\r\n|\r|\n)(\t+author.+?)(\r\n|\r|\n)', r'\1\2', creator)
            creator = oneAuthor
        firstPlacePublished = gfSegment.iloc[x]['First Place of Publication']
        firstPublisher = gfSegment.iloc[x]['First Publisher']
        firstPublishedYear = gfSegment.iloc[x]['First Published Year']
        secondPlacePublished = gfSegment.iloc[x]['Second Place of Publication']
        secondPublisher = gfSegment.iloc[x]['Second Publisher']
        secondPublishedYear = gfSegment.iloc[x]['Second Published Year']

        publicationInfo = parsePublication(firstPlacePublished, firstPublisher, firstPublishedYear, secondPlacePublished, secondPublisher, secondPublishedYear)

        # author = gfSegment.iloc[x]['Author Name']
        # authorRelator = gfSegment.iloc[x]['Author Relator']
        # print("Title number " + str(x))
        #

        outfile.write("@BOOK{" + gfSegment.iloc[x]['MMS Id'] + ",\n")
        outfile.write(smart_str(creator))
        title = gfSegment.iloc[x]['Title']
        if title[-2:] == " /":
            title = title[:-2]
        outfile.write("\ttitle = {" + title + "},\n")
        outfile.write(smart_str(publicationInfo))
        #outfile.write(smart_str(creator2))
        outfile.write("}\n\n")

        x += 1

rootdir =pDir

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print os.path.join(subdir, file)

dir = pDir
faults = 0
faultsList = []
for root, dirs, files in os.walk(pDir):
    print("Root: " + str(root) + "; Directory List: " + str(dirs) + "; Files: " + str(files) + "\n")
    for subdir in dirs:
        print("\n\n" + subdir + "\n\n")
        files = os.walk(pDir + "/" + subdir).next()[2]
        if (len(files) > 0):
            for file in files:
                if ".tex" in file and "output" not in file:
                    os.chdir(pDir + "/" + subdir)
                    justFileName = ntpath.basename(file)
                    if len(exclusionList) > 0:
                        for f in exclusionList:
                            if justFileName == f + ".tex":
                                continue
                    justDatabaseName = justFileName.replace(".tex", "")
                    #raw_input("\n\nPress Enter to continue...[before first xelatex]")
                    commandLine = subprocess.Popen(['xelatex', justFileName])
                    commandLine.communicate()
                    #raw_input("\n\nPress Enter to continue...[ran first xelatex]")
                    # raw_input("\n\nPress Enter to continue...[ran first pdflatex]")
                    commandLine = subprocess.Popen(['biber', justDatabaseName])

                    commandLine.communicate()
                    #raw_input("\n\nPress Enter to continue...[ran biber]")
                    #raw_input("\n\nPress Enter to continue...[ran biber]")
                    commandLine = subprocess.Popen(['xelatex', justFileName])
                    commandLine.communicate()
                    # raw_input("\n\nPress Enter to continue...[ran second pdflatex]")
                    try:
                        shu.copyfile(justDatabaseName + ".pdf", "../../Output/" + justDatabaseName + ".pdf")
                    except:
                        faults += 1
                        faultsList.append(justDatabaseName)
                        print("Process hung on " + justDatabaseName + " \n")
                        print("Enter this into exclusion list when you rerun\n\n")
        os.chdir("../..")
if faults > 0:
    print("##################################################################")
    print("##################################################################")
    print("##################################################################")
    print("##################################################################")
    print("#########    You will need to rerun elatex--> biber --> xelatex ")
    print("#########    on the following funds in their folders")
    print("#########    in the Processing folder")
    print("#########    ")
    print("#########    ")
    a = 0
    for f1 in faultsList:
        if a == 0:
            print("#########    " + f1)
        else:
            print("#########    , "+ f1)
        a += 1
    print("#########    ")
    print("#########    ")
    print("#########    go in to these folders and run the following")
    print("#########    commands:")
    print("#########        - xelatex <fund>.tex")
    print("#########        - biber <fund>")
    print("#########        - xelatex <fund>.tex")
    print("#########    ")
    print("#########    ")
    exit(1)
######################################################################################################
######################################################################################################
#######
#######         I will need to pay special attention
#######         to the authors, editors, and trans-
#######         lators.
#######
#######         Ideally, I'd like authors to be in the
#######         authors field if they have an authors
#######         role, or if the editor
#######         or translator is the only creator
#######         entity.
#######
#######         Experiment using the author and editor
#######         bib tags in the bib file.  Otherwise,
#######         I will need to parse them here.
#######


######################################################################################################
######################################################################################################
#######     once the bib file is created,
#######     loop through each bib file in
#######     "/Processing/" in its own folder
#######
#######     copy the requisite .aux file into this
#######     folder.
#######     Include reference to the bst
#######     and the tex file (These aren't modified
#######     by Pybtex)


######################################################################################################
#######################################################################################################
#######     run the pybtex function (script)
#######     the bib, tex, and aux files
#######     this creates a bbl, modified aux, and
#######     pdf
#######
#######     move the PDF to the top level Output folder
