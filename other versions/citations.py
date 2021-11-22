#!/usr/bin/env python3
# -*- coding: utf-8 -*-
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
########
########
########    Author:           Henry Steele, Library Technology Services, Tufts University
########    Name of Program:  Citations
########	Files:			  citations.py, Scripts/functions.py
########    Date created:     2018-12
########
########    Purpose:
########      - To create a series of word documents that contain bibliographies of all the Titles
########        purchased in a given fiscal year for a given library (Tisch or Ginn)
########
########    Method:
########      - provide library and fiscal year prompt
########      - program retrives the appropriate Analytics report:
########          - either/or
########              - /shared/Tufts University/Reports/Collections/Gift Funds/Titles Purchased with Gift Funds - Tisch - Generic for Script
########              - /shared/Tufts University/Reports/Collections/Gift Funds/Titles Purchased with Gift Funds - Ginn - Generic for Script
########          - outputs:
########              - MMS Id
########              - fund
########          - filters on
########              - "MMS Id is not equal to / is not in  -1"
########              - (Tisch) "AND Fund Ledger Code is equal to / is in  dalex; dalel; daron; dbarr; dcamp; dchri; dcros; dduke; dfitc; dgiff; dgonz; dgord; dhaly; dharo; dloeb; dmeas; dnewh; dpall; dprit; drose; drosg; dshap; dsper; dtisc; dwill; dfox; docon; dcohe; dargo; dblak; dmarc"
########              - OR (Ginn) "Fund Ledger Name is equal to / is in  Bradley - Books; Cabot - Books; Fares - Books; Hay - Books; Imlah - Books; Maney - Books; Raanan - Books; Salacuse - Books; Saskawa-NPP - Books"
########              - "AND Transaction Date is prompted"
########                  - this is passed as a 'saw' XML filter in the URL that encodes the date range
########      - retrieves the XML report, iterates through and parses MMS Id and fund
########      - performs an SRU search by MMS Id
########      - parses out relevant title, author, and pulication information field from bib XML
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
########      - turns this data into a ".bib" BibTex file
########      - uses locally included citeproc.py module to create bibliography, and local docx module to write to Word
########      - These have to be locally included because I had to change some of the internals of these pacakges to handle UTF-8 encoding
########
########    Dependences:
########      - in "requirements.txt"
########         - tkinter.filedialog import askopenfilename
########         - from django.utils.encoding import smart_bytes
########         - import pandas as pd
########         - import numpy as np
########         - import docx
########         - import xml.etree.ElementTree as et
########         - various citeproc-py methods
########
########    Output:
########      - "Processing" directory contains intermediate ".bib" file, which is in BibTex that citeproc
########      - "Output" directory contains final Word .docx file
########
########    Troubleshooting:
########      - The most likely errors you will encounter will be with encoding.
########        The script translates everythign into UTF-8 so foreign characters shouldn't be a problem,
########        but if you do run into issues you may want to exempt the individual bib record from input files_to_ignore
########        (in /Processing), commend out the part of the code all the way up to where they are created, and rerun.
########        Or fix the records and wait a day for a new Analtics report

from __future__ import (absolute_import, division, print_function,
                    unicode_literals)
import sys
import requests
import json
import os
import csv
import re
from tkinter.filedialog import askopenfilename

from django.utils.encoding import smart_bytes
import io
# import subprocess
# import ntpath
#for dataframes
import pandas as pd
import numpy as np


# import exceptions
import docx_local as docx
import time

sys.path.append('scripts/')
from functions import *


######################################################################################################
######################################################################################################
#######     input text file into dataframe


######################################################################################################
######################################################################################################
#######     method to output bibliography from citeproc
def warn(citation_item):
    print("WARNING: Reference with key '{}' not found in the bibliography."
          .format(citation_item.key))

######################################################################################################
######################################################################################################
#######     class to parse the citeproc output HTML format as text, e.g. <i>...</i> as italic
#from https://github.com/python-openxml/python-docx/issues/352
class HTMLHelper(object):
    """ Translates some html into word runs. """
    def __init__(self):
        self.get_tags = re.compile("(<[a-z,A-Z]+>)(.*?)(</[a-z,A-Z]+>)")

    def html_to_run_map(self, html_fragment):
        """ breakes an html fragment into a run map """
        ptr = 0
        run_map = []
        for match in self.get_tags.finditer(html_fragment):
            if match.start() > ptr:
                text = html_fragment[ptr:match.start()]
                if len(text) > 0:
                    run_map.append((text, "plain_text"))
            run_map.append((match.group(2), match.group(1)))
            ptr = match.end()
        if ptr < len(html_fragment) - 1:
            run_map.append((html_fragment[ptr:], "plain_text"))
        return run_map

    def insert_runs_from_html_map(self, paragraph, run_map):
        """ inserts some runs into a paragraph object. """
        for run_item in run_map:
            run = paragraph.add_run(run_item[0])
            if run_item[1] == "<i>":
                run.italic = True

######################################################################################################
######################################################################################################
#######     retrieve processing files created in previous section
pDir = "./Processing"
marcFilename = "Processing\\gifts_funds.txt"
giftFilename = "Processing\\MMS ID and Fund.csv"


oDir = "./Output"
if not os.path.isdir(oDir) or not os.path.exists(oDir):
       os.makedirs(oDir)


marcDF = pd.read_csv(marcFilename, sep="~", encoding='utf-8', index_col=False)
fundDF = pd.read_csv(giftFilename, encoding='utf-8')

print(marcDF)
print(fundDF)

######################################################################################################
######################################################################################################
#######     make sure all columns are encoded as UTF-8 in dataframes, and merge
for col in marcDF.columns:
    marcDF[col] = marcDF[col].apply(lambda x: smart_bytes(x).decode('utf-8'))

for col in fundDF.columns:
    fundDF[col] = fundDF[col].apply(lambda x: smart_bytes(x).decode('utf-8'))


gf = pd.merge(marcDF, fundDF, on='MMS Id')

print(gf)



for col in gf.columns:

    gf[col] = gf[col].apply(lambda x: x.replace("&", "\&"))

gf= gf.replace('nan', '', regex=True)



gf = gf.drop(gf[gf['Title'].str.isupper()].index)


gf = gf.drop_duplicates(subset=['Title', 'Author'], keep='first')





gf = gf.rename(columns={'Fund Ledger Code':'Fund'})
fundArray = gf.Fund.unique()


fundList = fundArray.tolist()


print(fundList)





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
#######     for each fund, create a folder and .bib file
#######     to store in "/Processing/"
#######

for fund in fundList:

    pFundDir = pDir + "/" + str(fund)
    if not os.path.isdir(pFundDir) or not os.path.exists(pFundDir):
           os.makedirs(pFundDir)





    fundDotBib = str(fund) + ".bib"


    bibFilename = pFundDir + "/" + str(fund) + ".bib"
    outfile = io.open(bibFilename, "w+", encoding='utf-8')


    gfSegment = gf.loc[gf['Fund'] == fund]

    gfSegment = gfSegment.reset_index(drop=True)
    print(gfSegment)
    count = len(gfSegment.index)


    print("\nCount: " + str(count))
    x = 0
    while x < count:

        ######################################################################################################
        ######################################################################################################
        #######     for each entry (title record) in the dataframe, separate out and parse metadata into
        #######     BibTex .bib file format
        title = gfSegment.iloc[x]['Title']
        title = re.sub(r'(^.+)\.$', r'\1', title)
        test_mms_id = gfSegment.iloc[x]['MMS Id']
        if title == "":
            x += 1
            continue

        if gfSegment.iloc[x]['Title'].isupper():
            x += 1
            continue
        creator = ""
        if gfSegment.iloc[x]['Author Name'] != "":
            author = gfSegment.iloc[x]['Author Name']

            authorRelator = gfSegment.iloc[x]['Author Relator']
            creator = parseCreator(author, authorRelator, "personal", test_mms_id)
            #creator = parseCreator(author~ authorRelator)
            creator2 = str(author) + "~ " + str(authorRelator) + "\n"
        if gfSegment.iloc[x]['Second Author Name'] != "Empty":
            secondAuthor = gfSegment.iloc[x]['Second Author Name']
            secondAuthorRelator = gfSegment.iloc[x]['Second Author Relator']
            creator += parseCreator(secondAuthor, secondAuthorRelator, "personal", test_mms_id)
            creator2 = str(secondAuthor) + "~ " + str(secondAuthorRelator) + "\n"
        if gfSegment.iloc[x]['Corporate Author Name'] != "Empty":
            corporateAuthor = gfSegment.iloc[x]['Corporate Author Name']
            corporateAuthorRelator = gfSegment.iloc[x]['Corporate Author Relator']
            creator += parseCreator(corporateAuthor, corporateAuthorRelator, "corporate", test_mms_id)
            creator2 = str(corporateAuthor) + "~ " + str(corporateAuthorRelator) + "\n"
        if gfSegment.iloc[x]['Second Corporate Author Name'] != "Empty":
            secondCorporateAuthor = gfSegment.iloc[x]['Second Corporate Author Name']
            secondCorporateAuthorRelator = gfSegment.iloc[x]['Second Corporate Author Relator']
            creator += parseCreator(secondCorporateAuthor, secondCorporateAuthorRelator, "corporate", test_mms_id)
            creator2 = str(secondCorporateAuthor) + "~ " + str(secondCorporateAuthorRelator) + "\n"


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


        ######################################################################################################
        ######################################################################################################
        #######     output each entry in the .bib file
        outfile.write("@BOOK{" + gfSegment.iloc[x]['MMS Id'] + ",\n")

        outfile.write(creator)

        if title[-2:] == " /":
            title = title[:-2]
        outfile.write("\ttitle = {" + title + "},\n")
        outfile.write(publicationInfo)
        #outfile.write(smart_str(creator2))
        outfile.write("}\n\n")

        x += 1

    outfile.close()
    from citeproc.py2compat import *


    from citeproc_local.source.bibtex import BibTeX

    from citeproc_local import CitationStylesStyle, CitationStylesBibliography
    from citeproc_local import formatter
    from citeproc_local import Citation, CitationItem


    print(bibFilename + "\n")
    file = open(bibFilename, "r+", encoding="utf-8")
    string = file.read()

    print("\n\n" + string + "\n\n" )
    file.close()
    bib_source = BibTeX(bibFilename)


    ######################################################################################################
    ######################################################################################################
    #######     This is the locally included Chicago style template, included in ciceproc/data/styles
    bib_style = CitationStylesStyle('chicago-annotated-bibliography', validate=False)


    # Create the citeproc-py bibliography, passing it the:
    # * CitationStylesStyle,
    # * BibliographySource (BibTeX in this case), and
    # * a formatter (plain, html, or you can write a custom formatter)

    bibliography = CitationStylesBibliography(bib_style, bib_source,
                                              formatter.html)
    ######################################################################################################
    ######################################################################################################
    #######     docx document object
    doc = docx.Document()
    doc.add_heading("References", 0)
    print("References")
    for item in bib_source:

        citation = Citation([CitationItem(item)])



        bibliography.register(citation)
        item_string = bibliography.cite(citation, warn)


    html_helper = HTMLHelper()
    bibliography.sort()
    for item in bibliography.bibliography():
        ######################################################################################################
        ######################################################################################################
        #######     take out extra characters in citation, that are artifacts of the citeproc citation
        #######     creation process with some of our bib records
        #######
        #######     Also make the editor label plural if there are multiple ("eds.")
        item = str(item)
        item = item.replace(", n.d..", "")
        item = item.replace(',,', ',')
        item = item.replace('..', '.')
        item = re.sub(r'([^<]+?and[^<]+?)(ed.)(\s+<i>)', r'\1eds.\3', item)
        item = item.replace(',.', '.')

        ######################################################################################################
        ######################################################################################################
        #######     turn HTML into document styling
        run_map = html_helper.html_to_run_map(str(item))



        par = doc.add_paragraph()

        html_helper.insert_runs_from_html_map(par, run_map)


    doc.save(oDir + "/" + str(fund) + ".docx")
