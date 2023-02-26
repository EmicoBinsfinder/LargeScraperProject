import numpy as np
import pandas as pd
import glob
import os
import itertools
import random
import csv
from bs4 import BeautifulSoup as soup
import time
import requests

LinkCSV = pd.read_csv('C:/Users/eeo21/PycharmProjects/LargeScraperProject/LinkCSV')
ClassCodes = LinkCSV['Section'].tolist()
print(ClassCodes[:5])
workingdir = 'E:/Downloads'

for Code in ClassCodes[:1]:
    os.system(f'start chrome https://patents.google.com/xhr/query?url=q%3D{Code}%26oq%3D{Code}"&"exp="&"download=true')

    CSV = pd.read_csv(f'F:/Startup_Datasets/DownloadedCSVSearches/StartupDatasets/{filename}')
    SearchLink = CSV.columns[1]
    SearchLinkElements = SearchLink.split('=')
    Keyword = SearchLinkElements[-1]
    old_path = os.path.join(workingdir, old_filename)
    new_path = os.path.join('E:/Users/eeo21/Startup/GooglePatentScrape/DownloadedCSVs, f'{Keyword}.csv')
    os.rename(old_path, new_path)
    print(Keyword)



def get_patent_metadata(LINK, ClassCode):
    ########################################### Getting the CSV  ###########################################
    Keyword = ClassCode
    os.system(f'start chrome https://patents.google.com/xhr/query?url=q%3D{ClassCode}%26oq%3D{ClassCode}"&"exp="&"download=true')

    ########################################### Getting the HTML of the entire page ###########################################

    Response = requests.get(LINK)
    Response_HTML = soup(Response.content, "html.parser")

    ###Getting the abstract from each page
    abstract = Response_HTML.find("div", class_="abstract")

    if abstract == None:
        abstract = 'No Abstract'
        print('No abstract')
    else:
        abstract = abstract.get_text()

    ########################################### Getting the Claims ###########################################

    ########################################### Getting the Description ###########################################

    ########################################### Getting the Patent Events ###########################################

    ########################################### Getting the Similar Document Numbers ###########################################

    ########################################### Getting the Inventor Names ###########################################



    ########################################### Getting the Patent Number ###########################################
    title = Response_HTML.find("title")
    if title == None:
        Title = 'No Title'
        print('No Title')
    else:
        title = title.get_text()
        title_elements = title.split(" - ")
        Application_number = title_elements[0]
        Title = title_elements[1].replace(" \n     ", "")

    ############################################## Getting the Classification(s) ###########################################
    Unprocessed_Classifications = Response_HTML.find_all(attrs={'itemprop':'Code'})

    Classifications_Text = []
    Classifications = []

    for x in Unprocessed_Classifications:
        Unprocessed_Classification = x.get_text()
        Classifications_Text.append(Unprocessed_Classification)

        if Unprocessed_Classifications == None:
            break
        else:
            Classifications = [Classifications_Text[-1]]
            Index = 0
            while Index < len(Classifications_Text) - 1:
                if int(len(Classifications_Text[int(Index)+1])) < int(len(Classifications_Text[Index])):
                    Classifications.append(Classifications_Text[Index])
                Index += 1
    #print(Classifications)

    ############################################## Getting the Patent Country Code ###########################################
    Country_Code = Response_HTML.find(attrs={'itemprop':'countryCode'}).get_text()
    #print(Country_Code)

    ################################## Getting Current Status of the Patent ###########################################
    Status = Response_HTML.find(attrs={'itemprop':'status'})
    if Status == None:
        Status = 'Status Unknown'
        print('Status Unknown')
    else:
        Status = Status.get_text()

    return abstract, Application_number, Title, Classifications, Country_Code, Status

ClassDataframe = pd.DataFrame(columns=["Abstract", "Application_number", "Title", "Classifications", "Country_Code", "Status", "Description", "Claims", "Inventors", "Similar Documents", "Events"])






####### Downloading Google Patents for Web Scraping ###########################

# for csv in os.listdir(working_dir):
#     file = pd.read_csv(f'{working_dir}{csv}')
#     for x in file.iloc[1:, 0].head(SampleNumber):
#          string_link = str(x)
#          if string_link.endswith('en') == False:
#              break
#          else:
#              print(x)
#              abstract, Application_number, Title, Classifications, Country_Code, Status = get_patent_metadata(x)
#          if abstract == 'No Abstract':
#              continue
#          elif Classifications == []:
#              continue
#          else:
#              Info = [abstract, Application_number, Title, Classifications, Country_Code, Status]
#              D.loc[len(D)] = Info
#              ClassDataframe.loc[len(ClassDataframe)] = Info



