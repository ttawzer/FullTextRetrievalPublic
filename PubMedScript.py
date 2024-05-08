# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:28:32 2023

Developed by Tiffany Tawzer and Christopher Beger
Copyright 2023, Loyola University Chicago, distributed under the GNU General Public License version 3. The license text is available at https://www.gnu.org/licenses/ 

NCBI E-utilities API is subject to the NCBI Disclaimer and Copyright Notice https://www.ncbi.nlm.nih.gov/About/disclaimer.html
"""

# import numpy
import pandas as pd
# This assigns a variable to the package name for convenience
import requests
# import json
import time

dforig = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx')
dftitle = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', usecols='D')
# open the citation spreadsheet; create one dataframe with all desired columns, and another with just the title field
list = []
# set up an empty list
for i in range(0, len(dftitle)):
# for every item, starting at index 0 and ending and the last cell, do the following   
    title = dftitle.iloc[i, -1]
# assign the title in the current row to a variable
    title = str(title)
    # change data type to string
    payload = {'db': 'pubmed', 'retmode':'json', 'field': 'title', 'term': title, 'email':'hslill@luc.edu'}
    # define parameters for esearch api
    response = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?', params=payload)
    # run the API and output the result as JSON using requests package
    record = response.json()
    # get the data from the JSON file as a dictionary
    pmid = record.get('esearchresult',{}).get('idlist')
    # get the pmid list from the dictionary
    if len(pmid)==1:
    # if the length of the pmid list is exactly 1
        pmid2 = pmid[0]
        # get the pmid
        libkey = f'https://public-api.thirdiron.com//public/v1/libraries/<library ID>/articles/pmid/{pmid2}?access_token='
        # API search string using PMID
        response = requests.get(libkey)
        # call the API
        if response.status_code == requests.codes.ok:
        # check the status code of the response and proceed if it is ok
            record = response.json()
            # get the response json
            value = record.get('data',{})
            # add the dictionary for the 'data' element to a variable
            if value.get('fullTextFile') != '':
                url = value.get('fullTextFile')
                # look for the 'fullTextFile' element, which defines a PDF link; if it is not blank, set it to the url variable
            else:
                if value.get('contentLocation') != '':
                    url = value.get('contentLocation')
                    # if there is no PDF link, look for the 'contentLocation' element, which defines a site where the article is available; if it is not blank, set it to the url variable
                else:
                    url = value.get('linkResolverOpenUrl')
                    # if both content elements are blank, set the link resolver url to the url variable
        else:
            url = f'https://tb2lc4tl2v.search.serialssolutions.com/?V=1.0&sid=Entrez:PubMed&id=pmid:{pmid2}'
            # if the status code of the response is not okay, generate a serials solutions search using the pmid and set it to the url variable
    else:     
          url = f'https://scholar.google.com/scholar?q={title}&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
        # if there are 0 or more than one record in the PubMed search, generate a URL for a Google Scholar search of the title and set it to the url variable
    list.append(url)
    # add the current record url to the list
    time.sleep(.1)
    # wait before moving to the next row to accommodate esearch rate limiting

dfresult = dforig.assign(URL = list)
# create a data frame from the original and add the URL list as a column
with pd.ExcelWriter('N:\Python\ScriptRetrievalList.xlsx', mode='a', if_sheet_exists='new') as writer:  
    dfresult.to_excel(writer, sheet_name='Results')
    # write the final dataframe to a new sheet in an Excel file
print ("Done")

