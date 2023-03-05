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

# working_dir = 'Downloads/output_12.csv'
# files = os.listdir(working_dir)
PatentNumberDF = pd.read_csv('C:/Users/eeo21/Documents/Startup_Datasets/output_12.csv')
PatentNumberDF = np.array(PatentNumberDF['publication_number'])

############ Renaming all of the Search CSVs to their Keyword Search and removing first row ###################

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

    def accumulate(attributes_so_far, key, value):
        if not isinstance(attributes_so_far[key], list):
            attributes_so_far[key] = [attributes_so_far[key]]
        attributes_so_far[key].append(value)

    Response = requests.get(LINK)
    Response_HTML = soup(Response.content, "html.parser", on_duplicate_attribute=accumulate)

    try:
        ###########################################Getting the Patent Number/Checking if Page Exists ###########################################
        title = Response_HTML.find("title")
        if title == None:
            Title = 'No Title'
            print('No Title')
        else:
            title = title.get_text()
            title_elements = title.split(" - ")
            Application_number = PatentName
            Title = title_elements[1].replace(" \n     ", "")
            Title = Title.replace('\n', '')

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
            print('No Classificatiion ', PatentName)
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
                claims = 'No Claim'
            else:
                claims = ' '.join([i.get_text() for i in claims2])
                claims = claims.replace('\n', '')

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
            for x in claims:
                claimsegment = [text for text in x.stripped_strings]
                indexslice = int(len(claimsegment) / 2)
                english = claimsegment[indexslice:]
                claims = ' '.join([x for x in english])
                print(claims)

            claims = claims.replace('\n', '')
            print(claims)


        ###################### Getting the Description ##########################

        desc = Response_HTML.find_all('div', {'class': 'description-line'})

        if len(desc) == 0:
            desc2 = Response_HTML.find_all('description')

            if len(desc2) == 0:
                desc3 = Response_HTML.find_all('div', {'class': 'description-paragraph'})

                if len(desc3) == 0:
                    desc = 'No Description'
                    print('No Description', PatentName)
                    # tries all three potential css selectors
                else:
                    desc = ' '.join([i.get_text() for i in desc3])
                    desc = desc.replace('\n', ' NEWLINE ')

            else:
                desc = ' '.join([i.get_text() for i in desc2])
                desc = desc.replace('\n', ' NEWLINE ')

        else:
            desc = ' '.join([i.get_text() for i in desc])
            desc = desc.replace('\n', ' NEWLINE ')

        ###################### Getting the Similar Docu list ###################
        
        simdocs = Response_HTML.find_all('a', href=True)#, {'class':'style-scope'})#, {'class': 'td style-scope patent-result'})

        par = [i.parent for i in simdocs]

        simpatname = [(i.get_text()).strip().split('\n')[0] for i in par if i.find(attrs={'itemprop':"isPatent"}) != None]
        #"""""" strips trailing '\n' and gets rid of (en) """"""#
        simdocs = [i for i in simpatname  if PatentName not in i]
        if len(simdocs) == 0:
            simdocs = 'No Similar Docs'
        ###### to remove any sim docs that are just the same patent ###
    
        ###################### Getting the Espacenet Links ###################

        links = Response_HTML.find_all(lambda t: t.name == "a" and t.text.startswith("Espacenet"))
        espace = [i['href'] for i in links][0]
        if len(espace) == 0:
            espace = 'No Espacent link'

        ###############################################################

        cited = list(set([i.find(attrs={'itemprop':'publicationNumber'}).get_text() for i in par if i.find(attrs={'itemprop':'publicationNumber'}) != None]))# = [i.parent for i in simdocs]
        cited = [i for i in cited if PatentName not in i]
        print(len(cited), PatentName)

        if PatentName == 'US20130283719A1':
            test1 = [i for i in par if i.find(attrs={'itemprop':'publicationNumber'}) != None]
            test2 = [i for i in test1 if i.find(attrs={'itemprop':'isPatent'}) == None]
            print(test2)
            print(len(test1),len(test2))

        return abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status, simdocs, espace

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
        simdocs = PatentName
        espace = PatentName

        return abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status, simdocs, espace

st = time.time()

allv = pd.DataFrame(columns=['abstract', 'claims', 'description', 'application number', 'title', 'classifitcation', 'country code', 'status', 'similar documents', 'espacenet link'])

for x in PatentNumberDF[4:5]:
    PatentName = x.replace('-', '')
    Link = f'https://patents.google.com/patent/{PatentName}/en'
    abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status, simdocs, espace = get_patent_metadata(Link, PatentName)
    if Title == PatentName:
        if PatentName.startswith('US'):
            PatentName = PatentName[:6] + '0' + PatentName[6:]
            Link = f'https://patents.google.com/patent/{PatentName}/en'
            abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status, simdocs, espace = get_patent_metadata(Link, PatentName)
    
    allv.loc[len(allv)] = [abstract, claims, desc, Application_number, Title, Classifications, Country_Code, Status, simdocs, espace]

df = pd.DataFrame(allv, columns = ['abstract', 'claims', 'description', 'application number', 'title', 'classifitcation', 'country code', 'status', 'similar documents', 'espacenet link'])
df.to_csv('C:/Users/eeo21/Documents/Startup_Datasets/just_test.csv', index=None)

print(df['claims'])
end = time.time()

print(end-st)
