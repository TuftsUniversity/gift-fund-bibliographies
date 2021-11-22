import sys
import requests
import json
import os
import csv
import re
from tkinter.filedialog import askopenfilename
from django.utils.encoding import smart_bytes
# import ntpath
#for dataframes
import pandas as pd
import numpy as np


import time


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
#######     create lists of creators (either author, editor, or translators)
def parseCreatorList(cList, relator):
    count = len(cList)
    x = 0
    creatorLine = ""
    while x < count and x < 3:


        if "author" in relator:
            #print("In author loop\n")
            if x == 0 and count == 1:
                creatorLine += "\tauthor = {" + cList[x] + "}"
                break
            elif x == 0 and count > 1:
                creatorLine += "\tauthor = {" + cList[x]
            elif 0 < x < 2 and count > 2:
                creatorLine += " and " + cList[x]
            else:
                creatorLine += " and " + cList[x] + "}"
        elif "editor" in relator:

            if x == 0 and count == 1:
                creatorLine += "\teditor = {" + cList[x] + "}"
                break
            elif x == 0 and count > 1:
                creatorLine += "\teditor = {" + cList[x]
            elif 0 < x < 2 and count > 2:
                creatorLine += " and " + cList[x]
            else:
                creatorLine += " and " + cList[x] + "}"
        elif "translator" in relator:
            #print("In transalator loop\n")
            if x == 0 and count == 1:
                creatorLine += "\ttranslator = {" + cList[x] + "}"
                break
            elif x == 0 and count > 1:
                creatorLine += "\ttranslator = {" + cList[x]
            elif 0 < x < 2 and count > 2:
                creatorLine += " and " + cList[x]
            else:
                creatorLine += " and " + cList[x] + "}"
        #if it's uncaught relator
        else:
            #print("In uncaught relator loop\n")
            if x == 0 and count == 1:
                creatorLine += "\tauthor = {" + cList[x] + "}"
                break
            elif x == 0 and count > 1:
                creatorLine += "\tauthor = {" + cList[x]
            elif 0 < x < 2 and count > 2:
                creatorLine += " and " + cList[x]
            else:
                creatorLine += " and " + cList[x] + "}"

        x += 1

    return creatorLine

######################################################################################################
######################################################################################################
#######     parse strings into lists of incoming creators
def parseCreator(c, cR, type, mms_id):
    creatorFlag = False
    relatorFlag = False

    if c != "":
        cList = c.split(";")
        creatorFlag = True
    else:
        creatorFlag = False
    if cR != "":
        cRList = cR.split(";")
        relatorFlag = True
    else:
        relatorFlag = False


    authorList = []
    editorList = []
    translatorList = []
    y = 0
    nullVariable = ""
    if creatorFlag == True:
        for creator in cList:


            if type == "personal":
                cList[y] = re.sub(r'([^,]+,\s[^,]+),', r'\1', cList[y])
                cList[y] = re.sub(r'([^,.]+?)[,.]\W(.+),?', r'\2 \1', str(cList[y]))
            creator = cList[y]
            #if relatorFlag:
            if relatorFlag == True:
                try:
                    relator = cRList[y]
                    if "author" in relator:
                        authorList.append(creator)
                    elif "editor" in relator:
                        editorList.append(creator)
                    elif "translator" in relator:
                        translatorList.append(creator)
                except:
                    authorList.append(creator)
            else:
                authorList.append(creator)
            #else:
                #authorList.append(creator)
            y += 1




    returnCreator = ""

    authorLine = ""
    editorLine = ""
    translatorLine = ""


    if len(authorList) > 0:
        authorLine = parseCreatorList(authorList, "author")
    if len(editorList) > 0:
        editorLine = parseCreatorList(editorList, "editor")
    if len(translatorList) > 0:
        translatorLine = parseCreatorList(translatorList, "translator")

    if authorLine != "":
        returnCreator += authorLine + ",\n"
    if editorLine != "":
        returnCreator += editorLine  + ",\n"
    if translatorLine != "":
        returnCreator += translatorLine + ",\n"

    if type == "corporate":
        returnCreator = re.sub(r'([a-z]+\s+\=\s+)({.+?\})', r'\1{\2}', returnCreator)

    return returnCreator

######################################################################################################
######################################################################################################
#######     parse strings into lists of incoming publication info
def parsePublication(a1, a2, a3, b1, b2, b3):
    address = ""
    publisher = ""
    year = ""
    format = ""



    if a2 != "":
        a2 = a2.split(";")
        a2String = str(a2[0])
        a2String = re.sub(r',$\[\]', '', str(a2String))

        if a1 != "":
            a1 = a1.split(";")
            a1String = str(a1[0])
            a1String = re.sub(r'\s+\:.*$', '', str(a1String))
            address = "\taddress = {" + str(a1String) + "},\n"
            publisher = "\tpublisher = {" + str(a2String) + "},\n"
            if a3 != "":
                a3 = a3.split(";")
                a3String = str(a3[0])
                a3String = re.sub(r'.*(\d{4}).*', r'\1', str(a3String))
                a3String = re.sub(r'[\[\]]', '', str(a3String))
                if re.match(r'^\d+$', a3String):
                    year = "\tyear = {" + str(a3String) + "},\n"

    elif b2 != "":
        b2 = b2.split(";")
        b2String = str(b2[0])
        b2String = re.sub(r'\s\:.*$\[\]', '', b2String)
        b2String = re.sub(r',$', '', b2String)
        if b1 != "":
            b1 = b1.split(";")
            b1String = str(b1[0])
            b1String = re.sub(r'\s+\:.*$', '', b1String)
            address = "\taddress = {" + str(b1String) + "},\n"
            publisher = "\tpublisher = {" + str(b2String) + "},\n"
            if b3 != "":
                b3 = b3.split(";")
                b3String = str(b3[0])
                b3String = re.sub(r'.*(\d{4}).*', r"\1", b3String)
                b3String = re.sub(r'[\[\]]', '', b3String)

                if re.match(r'^\d+$', b3String):
                    year = "\tyear = {" + str(b3String) + "},\n"

    # publisher_for_format = re.sub(r'.+?\{(.+?)\}', r'\1', publisher)
    # address_for_format = re.sub(r'.+?\{(.+?)\}', r'\1', address)
    # year_for_format = re.sub(r'.+?\{(.+?)\}', r'\1', year)

    # if f != "":
    #     format = "\thowpublished = {" + publisher_for_format + ", " + address_for_format + ", " + str(year_for_format) + "[" + format + "].},"
    #     return_publisher = format
    # else:
    return_publisher = address + publisher + year


    return_publisher = return_publisher.replace(',,', ',')
    return_publisher = return_publisher.replace('[', '')
    return_publisher = return_publisher.replace(']', '')

    return return_publisher
