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

"""
def split(filehandler, output_path, delimiter=',', row_limit=1000000,
          output_name_template='output_%s.csv', keep_headers=True):
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = next(reader)
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)

split(open('/home/amran/LargeScraperProject/Dataset/PatentNames1.csv', 'r'), '/home/amran/LargeScraperProject/Dataset/PatentNames1/')
split(open('/home/amran/LargeScraperProject/Dataset/PatentNames2.csv', 'r'), '/home/amran/LargeScraperProject/Dataset/PatentNames2/')
split(open('/home/amran/LargeScraperProject/Dataset/PatentNames3.csv', 'r'), '/home/amran/LargeScraperProject/Dataset/PatentNames3/')
"""

working_dir = '/home/amran/LargeScraperProject/Dataset/PatentNames2/'
files = os.listdir(working_dir)
PatentNumberDF = pd.read_csv(f'{working_dir}{files[2]}')
PatentNumberDF = np.array(PatentNumberDF['publication_number'])

print(files[2])

############ Renaming all of the Search CSVs to their Keyword Search and removing first row ###################

ClassDataframe = pd.DataFrame(columns=["Abstract", "Application_number", "Title", "Classifications", "Country_Code", "Status"])
def get_patent_metadata(LINK, PatentName):

    ## Note to me (amran):
    # abs -> just abstract
    # claims -> div, class = claim-text
    # claims -> claims (machine translated)
    # desc -> div, class = desription-line
    # desc -> desription (machine translated)
    # desc -> div, class = desription-paragraph (idk why)
    ## please just some consistency!!!!!! i beg

    ########################################### Getting the HTML of the entire page ###########################################
    Response = requests.get(LINK)
    Response_HTML = soup(Response.content, "html.parser")

    try:
        ###########################################Getting the Patent Number/Checking if Page Exists ###########################################
        title = Response_HTML.find("title")
        if title == None:
            Title = 'No Title'
            print('No Title')
        else:
            title = title.get_text()
            title_elements = title.split(" - ")
            Application_number = title_elements[0]
            Title = title_elements[1].replace(" \n     ", "")


        ###Getting the abstract from each page
        abstract = Response_HTML.find("div", class_="abstract")

        if abstract == None:
            abstract = 'No Abstract'
            print('No abstract')
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
        if Classifications == []:
            print('No Classificatiion')
        ############################################## Getting the Patent Country Code ###########################################
        Country_Code = Response_HTML.find(attrs={'itemprop':'countryCode'}).get_text()

        ################################## Getting Current Status of the Patent ###########################################
        Status = Response_HTML.find(attrs={'itemprop':'status'})
        if Status == None:
            Status = 'Status Unknown'
            print('Status Unknown')
        else:
            Status = Status.get_text()

        ###################### Getting the Claims ######################

        claims = Response_HTML.find_all('div', {'class': 'claim-text'})

        if len(claims) == 0:
            claims2 = Response_HTML.find_all('claims')

            if len(claims2) == 0:
                print('No Claim', PatentName)
                claims = 'NaN'
            else:
                claims = ' '.join([i.get_text() for i in claims2])
                '''
                ########### doesnt work that well... ##############
                import nltk
                #nltk.download('words')
                words = set(nltk.corpus.words.words())
                
                claims3 = " ".join(w for w in nltk.wordpunct_tokenize(claims) \
                        if w.lower() in words or not w.isalpha())
                print(claims3)
                ###################################################
                '''
        else:
            claims = ' '.join([i.get_text() for i in claims])
        

        ###################### Getting the Description ##########################

        desc = Response_HTML.find_all('div', {'class': 'description-line'})

        if len(desc) == 0:
            desc2 = Response_HTML.find_all('description')

            if len(desc2) == 0:
                desc3 = Response_HTML.find_all('div', {'class': 'description-paragraph'})

                if len(desc3) == 0:
                    desc = 'NaN'
                    print('No Description', PatentName)
                    # tries all three potential css selectors
                else:
                    desc = ' '.join([i.get_text() for i in desc3])
            else:
                desc = ' '.join([i.get_text() for i in desc2])
        else:
            desc = ' '.join([i.get_text() for i in desc])


        ###################### Getting the Similar Docu list ###################
        
        #simdocs = Response_HTML.find_all('a', {'id': 'link', 'class': 'style-scope state-modifier'})
        #simdocs = Response_HTML.find_all('span', {'class': 'td'})
        ## simdocs = Response_HTML.find_all('h3')#, href=True)#, {'class':'style-scope'})#, {'class': 'td style-scope patent-result'})
        #simdocs = Response_HTML.find_all('state-modifier', {'class': 'style-scope'})#Response_HTML.find_all('state-modifier')
        ## print(len(simdocs))

        ## sims = [i.get_text().strip() for i in simdocs]
        ## classv = [i.attrs for i in simdocs]
        #if PatentName == 'US20190387517A1':
        #    print(sims[100:])
        #    print(classv[100:])
    
        return abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status

    except IndexError:
        print('Whack Page')
        abstract = PatentName
        claims = PatentName
        desc = PatentName
        Application_number = PatentName
        Title = PatentName
        Classifications = PatentName
        Country_Code = PatentName
        Status = PatentName

        return abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status

st = time.time()

allv = []

for x in PatentNumberDF[0:100]:
    PatentName = x.replace('-', '')
    Link = f'https://patents.google.com/patent/{PatentName}/en'
    abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status = get_patent_metadata(Link, PatentName)
    if Title == PatentName:
        if PatentName.startswith('US'):
            PatentName = PatentName[:6] + '0' + PatentName[6:]
            Link = f'https://patents.google.com/patent/{PatentName}/en'
            abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status = get_patent_metadata(Link, PatentName)
    
    allv.append([abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status])

df = pd.DataFrame(allv, columns = ['ab', 'c', 'd', 'ap', 't', 'clas', 'cc', 'st'])
df.to_csv('just_test.csv', index=None)

print(df['cc'])
end = time.time()

print(end-st)
