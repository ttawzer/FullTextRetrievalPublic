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
import json
import time

dforig = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', header=None)
dftitle = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', usecols='D', header=None)
# open the citation spreadsheet; create one dataframe with all desired columns, and another with just the title field
df2 = pd.DataFrame({})
# set up an empty dataframe to hold the urls later
for i in range(0, len(dftitle)):
# for every item, starting at index 0 and ending and the last cell, do the following   
    title = dftitle.iloc[i, -1]
# assign the title in the current row to a variable
    title = str(title)
    # change data type to string
    title2 = title.replace(' ','+')
    # create a second title variable that replaces spaces in title with +; needed for Google Scholar URLs
    payload = {'db': 'pubmed', 'retmode':'json', 'field': 'title', 'term': title, 'email':'hslill@luc.edu', 'api_key': '<NCBI API KEY>'}
    # define parameters for esearch api
    response = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?', params=payload)
    # run the API and output the result as JSON using requests package
    record = response.json()
    # get the data from the JSON file as a dictionary
    pmid = record.get('esearchresult',{}).get('idlist')
    # get the pmid list from the dictionary
    df1 = pd.DataFrame(pmid)
    # add the pmid list to a dataframe
    if len(df1.index)>1:
        url = f'https://scholar.google.com/scholar?q={title}&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
        # if there is more than one record, generate a URL for a Google Scholar search of the title and set it to the url variable
    elif df1.empty:
        url = f'https://scholar.google.com/scholar?q={title}&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
        # if there are no records, generate a URL for a Google Scholar search of the title and set it to the url variable
    else:
        pmid2 = df1.iloc[0, -1]
        # get the pmid from the dataframe
        libkey = f'https://public-api.thirdiron.com//public/v1/libraries/<library ID>/articles/pmid/{pmid2}?access_token=<LIBKEY API KEY>'
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
    df1 = pd.DataFrame({url})
    # add the url variable for the current article to a dataframe
    df2 = pd.concat([df2, df1])
    # add the current record's dataframe to the full list
    time.sleep(.1)
    # wait before moving to the next row to accommodate esearch rate limiting
df2 = df2.reset_index()
# reset the index for df2
dfresult = pd.concat([dforig, df2], axis=1).reindex(dforig.index)
# add the url column to the original data from dforig
with pd.ExcelWriter('N:\Python\ScriptRetrievalList.xlsx', mode='a', if_sheet_exists='new') as writer:  
    dfresult.to_excel(writer, sheet_name='Results')
    # write the final dataframe to a new sheet in an Excel file
print ("Done")

