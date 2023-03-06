"""
Author: Egheosa Ogbomo
Date: 12th August 2022
Creating a script that can:
1. Download CSVs from Google based on a keyword search, (in function form), where the user defines the keyword to be
used to search for patents in google patents, where the CSV contains bibliographic data concerning the returned patents
from the keyword search.
2. Go through each entry in the downloaded CSV, which should have a link to the individual patent's page on Google
patents, opening the link and extracting the HTML from that page
3. Take the following information from the html in string form and store in a dataframe:
    - Country
    - Whether it is active or not
    - Patent Number
    - Abstract
    - Title
    - PCT Number #TODO
    - Applicants #TODO
    - Filing Dates #TODO
    - Grant Dates #TODO
    - Publication Dates #TODO
    - CPC classifications
4. Sort through entries to the CSV where there is missing information and/or no presence of the target class, to ensure
that we generate as balanced a dataset as possible
5. Convert the formatted dataframe into a CSV and save it
6. Return a count for the number of each class
"""

import time

import numpy as np
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import os
from os import listdir

#### Split Patent Names file into smaller files
import os


# def split(filehandler, output_path, delimiter=',', row_limit=1000000,
#           output_name_template='output_%s.csv', keep_headers=True):
#     import csv
#     reader = csv.reader(filehandler, delimiter=delimiter)
#     current_piece = 1
#     current_out_path = os.path.join(
#         output_path,
#         output_name_template % current_piece
#     )
#     current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
#     current_limit = row_limit
#     if keep_headers:
#         headers = next(reader)
#         current_out_writer.writerow(headers)
#     for i, row in enumerate(reader):
#         if i + 1 > current_limit:
#             current_piece += 1
#             current_limit = row_limit * current_piece
#             current_out_path = os.path.join(
#                 output_path,
#                 output_name_template % current_piece
#             )
#             current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
#             if keep_headers:
#                 current_out_writer.writerow(headers)
#         current_out_writer.writerow(row)
#
# split(open('E:/Downloads/PatentNames1.csv', 'r'), 'E:/Downloads/PatentNames1')
# split(open('E:/Downloads/PatentNames2.csv', 'r'), 'E:/Downloads/PatentNames2')
# split(open('E:/Downloads/PatentNames3.csv', 'r'), 'E:/Downloads/PatentNames3')

working_dir = 'E:/Downloads/PatentNames1/'
files = os.listdir(working_dir)
PatentNumberDF = pd.read_csv(f'E:/Downloads/output_12.csv')
PatentNumberDF = np.array(PatentNumberDF['publication_number'])

############ Renaming all of the Search CSVs to their Keyword Search and removing first row ###################

ClassDataframe = pd.DataFrame(columns=["Abstract", "Application_number", "Title", "Classifications", "Country_Code", "Status"])
def get_patent_metadata(LINK, PatentName):
    ########################################### Getting the HTML of the entire page ###########################################
    Response = requests.get(LINK)
    Response_HTML = soup(Response.content, "html.parser")

    try:
        ###########################################Getting the Patent Number/Checking if Page Exists ###########################################
        title = Response_HTML.find("title")
        if title == None:
            Title = 'No Title'
            #print('No Title')
        else:
            title = title.get_text()
            title_elements = title.split(" - ")
            Application_number = title_elements[0]
            Title = title_elements[1].replace(" \n     ", "")

        ###Getting the abstract from each page
        abstract = Response_HTML.find("div", class_="abstract")

        if abstract == None:
            abstract = 'No Abstract'
            #print('No abstract')
        else:
            abstract = abstract.get_text()

        ############################################## Getting the Classification(s) ###########################################
        Unprocessed_Classifications = Response_HTML.find_all(attrs={'itemprop':'Code'})
        Classifications_Text = []
        Classifications = []

        for x in Unprocessed_Classifications:
            Unprocessed_Classification = x.get_text()
            Classifications_Text.append(Unprocessed_Classification)
            Classifications = [Classifications_Text[-1]]
            Index = 0
            while Index < len(Classifications_Text) - 1:
                if int(len(Classifications_Text[int(Index)+1])) < int(len(Classifications_Text[Index])):
                    Classifications.append(Classifications_Text[Index])
                Index += 1
        #if Classifications == []:
            #print('No Classificatiion')
        ############################################## Getting the Patent Country Code ###########################################
        Country_Code = Response_HTML.find(attrs={'itemprop':'countryCode'}).get_text()

        ################################## Getting Current Status of the Patent ###########################################
        Status = Response_HTML.find(attrs={'itemprop':'status'})
        if Status == None:
            Status = 'Status Unknown'
            #print('Status Unknown')
        else:
            Status = Status.get_text()

        ###################### Getting the Claims ######################


        ###################### Getting the Description ##########################


        ###################### Getting the Related Documents ############

        return abstract, Application_number, Title, Classifications, Country_Code, Status

    except IndexError:
        print('Whack Page')
        abstract = PatentName
        Application_number = PatentName
        Title = PatentName
        Classifications = PatentName
        Country_Code = PatentName
        Status = PatentName
        return abstract, Application_number, Title, Classifications, Country_Code, Status


for x in PatentNumberDF:
    PatentName = x.replace('-', '')
    Link = f'https://patents.google.com/patent/{PatentName}/en'
    abstract, Application_number, Title, Classifications, Country_Code, Status = get_patent_metadata(Link, PatentName)
    print(Application_number)
    print(Title)
    print(Classifications)
    print(Country_Code)
    print(Status)
    print(abstract)
