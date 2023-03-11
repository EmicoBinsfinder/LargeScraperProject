"""
Script to format the raw outputs from the scrape documents
"""

import time
import numpy as np
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import os
from os import listdir
import urllib.request
import csv
import sys

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def split(filehandler, output_path, delimiter=',', row_limit=10000,
          output_name_template='output_%s.csv', keep_headers=True):
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w', encoding='utf-8'), delimiter=delimiter)
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
            current_out_writer = csv.writer(open(current_out_path, 'w', encoding='utf-8'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)

#split(open('E:/Downloads/scraped_google_patent.csv', 'r', encoding='utf-8'), 'E:/Downloads/ScrapeFormattedFiles/')

testfile = pd.read_csv('E:/Downloads/ScrapeFormattedFiles/output_1.csv', index_col=False)

Claimentries = testfile.loc[(testfile['c'] != 'MachineTrans') & (testfile['c'] != 'No Claim') & (testfile['ab'] != 'No Abstract') & (testfile['t'] != 'No Title') & (len(testfile['ab']) > 15)]
print(len(Claimentries))

Claims = pd.DataFrame({'Claims': Claimentries['c'], 'Abstract': Claimentries['ab'], 'Title': Claimentries['t']})

def claim1_formatter(claimtext):
    claimtext = claimtext.lower()
    Claim = claimtext.split('claim 1')[0]
    if len(Claim) > 2:
        Claim = Claim.split('.')[:-1]
    if len(Claim) == 2:
        Claim = ''.join([x for x in Claim])
    elif len(Claim) > 2:
        if '2' in Claim[-1]:
            Claim = ''.join([x for x in Claim[:-1]])
        else:
            Claim = ''.join([x for x in Claim])
    if len(Claim) == 1:
        Claim = Claim[0]
    if Claim == []:
        Claim = 'EmptyString'
    return Claim


Claims['Claims'] = Claims['Claims'].apply(claim1_formatter)

Claims = Claims.astype(str).loc[Claims['Claims'] != 'EmptyString']

Claims.to_csv('E:/Downloads/ScrapeFormattedFiles/testclaims.csv', index=False)
print(Claims.head())
