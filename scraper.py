# -*- coding: utf-8 -*-
import os
import re
import requests
import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil.parser import parse

# Set up variables
entity_id = 'E2003_NELC_gov'

url = "http://www.nelincs.gov.uk/council/council-finances-and-spending/council-spending/"
errors = 0
# Set up functions
def validateFilename(filename):
    filenameregex = '^[a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+_[0-9][0-9][0-9][0-9]_[0-9][0-9]$'
    dateregex = '[0-9][0-9][0-9][0-9]_[0-9][0-9]'
    validName = (re.search(filenameregex, filename) != None)
    found = re.search(dateregex, filename)
    if not found:
        return False
    date = found.group(0)
    year, month = int(date[:4]), int(date[5:7])
    now = datetime.now()
    validYear = (2000 <= year <= now.year)
    validMonth = (1 <= month <= 12)
    if all([validName, validYear, validMonth]):
        return True
def validateURL(url):
    try:
        r = requests.get(url, allow_redirects=True, timeout=20)
        count = 1
        while r.status_code == 500 and count < 4:
            print ("Attempt {0} - Status code: {1}. Retrying.".format(count, r.status_code))
            count += 1
            r = requests.get(url, allow_redirects=True, timeout=20)
        sourceFilename = r.headers.get('Content-Disposition')

        if sourceFilename:
            ext = os.path.splitext(sourceFilename)[1].replace('"', '').replace(';', '').replace(' ', '')
        else:
            ext = os.path.splitext(url)[1]
        validURL = r.status_code == 200
        validFiletype = ext in ['.csv', '.xls', '.xlsx']
        return validURL, validFiletype
    except:
        raise
def convert_mth_strings ( mth_string ):

    month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
    #loop through the months in our dictionary
    for k, v in month_numbers.items():
#then replace the word with the number

        mth_string = mth_string.replace(k, v)
    return mth_string
# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)
# find all entries with the required class
blocks = soup.find('div', 'module introPromos twoPerRow thumbTitleOnly')
links_block = blocks.find_all('a', href = True)
for link_block in links_block:
    csvmth = link_block['title']
    if 'spending' or 'Spending' in csvmth:
        main_links = 'http://www.nelincs.gov.uk' + link_block['href']
        print main_links
        html_links = urllib2.urlopen(main_links)
        sp = BeautifulSoup(html_links)
       # print link_block.text, main_links
        block = sp.find('table', 'pageTable downloads')
        links = block.find_all('a', href = True)
        for link in links:
            csvlink = link.text
            if 'Spending' and 'Data'and '(CSV)' in csvlink:
                print link['href']
               #  csvFile = link.text
               #  print csvFile
               #  url = link['href']
               # # print url
               #  if 'Spending' and 'CSV' in csvFile:
               #      csvMth = csvFile.split(' ')
                #print csvMth
               # print csvMth
                # if '-' in csvFile:
                #     csvMth = csvFile.split('-').strip[1][0:3].strip()
                #     print csvMth
#                 csvYr = csvFile.split(' ')[4].strip()
#                 if '(CSV)' in csvYr:
#                    csvYr = '2011'
#                 csvMth = convert_mth_strings(csvMth.upper())
#                 filename = entity_id + "_" + csvYr + "_" + csvMth
#                 todays_date = str(datetime.now())
#                 file_url = 'http://www.nelincs.gov.uk' + url.strip()
#                 validFilename = validateFilename(filename)
#                 validURL, validFiletype = validateURL(file_url)
#                 if not validFilename:
#                     print filename, "*Error: Invalid filename*"
#                     print file_url
#                     errors += 1
#                     continue
#                 if not validURL:
#                     print filename, "*Error: Invalid URL*"
#                     print file_url
#                     errors += 1
#                     continue
#                 if not validFiletype:
#                     print filename, "*Error: Invalid filetype*"
#                     print file_url
#                     errors += 1
#                     continue
#                 scraperwiki.sqlite.save(unique_keys=['l'], data={"l": file_url, "f": filename, "d": todays_date })
#                 print filename
# if errors > 0:
#    raise Exception("%d errors occurred during scrape." % errors)