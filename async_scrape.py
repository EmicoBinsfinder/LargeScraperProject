import os
import time
import sys
import csv
import glob
import requests
import re
import subprocess
#import pandas as pd
import numpy as np
import random
import itertools
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
import asyncio


#----Selenium driver (change for self)
spath = '/home/amran/SeleniumDrivers/'
os.environ['PATH'] += os.pathsep + spath

'''
def read_xlsx(fn):
    df = pd.read_excel(fn, header = None)
    df = df.drop([0])
    headers = df.iloc[0]
    df.columns = headers
    df = df.drop([1])
    df = df.reset_index()

    return df


def get_enurl(df):
    urls = []
    urlnum = 0
    for i in range(0, len(df['result link'])):
        if urlnum < 10000:
            try:
                lang = (df['result link'][i].split('/')[-1])
            except AttributeError:
                continue
            if lang == 'en':
                urls.append(df['result link'][i])
            urlnum += 1
    return urls
'''

def get_section(urls, classpath):

    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)

    num = 0
    for url in urls:
        print(num)
        if num < 100:
            section = ['0', '0']
            driver.get(url)
            sec = driver.find_elements(by=By.XPATH, value ='//div[@class = "{}"]'.format(classpath[0]))
            '''
            if len(sec) == 0:
                print(len(sec))
                section[0] = ('NaN')
            else:
                section[0] = (sec[0].text)

            '''
            for i in range(0, len(classpath)):
                sec = driver.find_elements(by=By.XPATH, value ='//div[@class = "{}"]'.format(classpath[i]))
                if len(sec) == 0:
                    #print(i, sec)
                    section[i] = ('NaN')
                else:
                    section[i] = (sec[0].text)
            #line = ','.join(section)
            #line = line+'\n'
            #adds to file as scraps -> so can even if script stops, has data
            
            #f = open('test.csv', 'a')
            #writer = csv.writer(f)
            #writer.writerow(section)
            #f.close()
            num += 1
    return

#--------- function to change url and download file --------#
async def download_csv(classname):

    start_time = time.time()
    for i in classname[0:1]:
        #print(i)
        c = i.split('/')

        #fn = 'gp-search_{a}_{b}.xlsx'.format(a=c[0], b=c[1])
        
        #fn = 'gp-search-20230226-092158.xlsx'
        #print(fn) 

        '''
        df = read_xlsx(fn)
        urls = get_enurl(df)
        print((urls[0:2]))
        '''

        urls = ['https://patents.google.com/patent/US20110147377A1/en?oq=US-2011147377-A1',
                'https://patents.google.com/patent/AT94535B/en?oq=AT-94535-B',
                'https://patents.google.com/patent/CN101887919B/en?q=(green+plastics)&oq=green+plastics',
                'https://patents.google.com/patent/US11149144B2/en?q=(green+plastics)&oq=green+plastics', 
                'https://patents.google.com/patent/CA2803091C/en?q=(green+plastics)&oq=green+plastics']



        secs = ("abstract style-scope patent-text", "claim style-scope patent-text")#, "description style-scope patent-text")
        
        get_section(urls, secs)#[0:10], secs)

    print(f"{(time.time() - start_time):.2f} seconds")

# "B60K37/00", "B60K2370/00", "B63H23/00", "B63H23/00", 
        #"B60K2700/00", "B63H9/00", "B60K7/00", "B63H13/00", "B63H20/00"]

async def main():
    tasks = [
            
            download_csv(["B64C30/00", "B60K2310/00"])

    ]

    await asyncio.gather(*tasks)

asyncio.run(main())
