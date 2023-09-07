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


dforig = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', usecols='B:M', header=None)
# open the Excel file and create a dataframe with columns desired for the final output
# if the Excel file has headers you can remove 'header=None'
df = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', usecols='D', header=None)
# open Excel file and create a dataframe from the article name column - see README for alternate option
# if the Excel file has headers you can remove 'header=None'
df = df.replace(' ','+', regex=True)
# change all spaces to +
df2 = pd.DataFrame({})
# set up an empty dataframe to hold the pmids later
for i in range(0, len(df)):
# for every item, starting at index 0 and ending and the last cell, do the following   
    title = df.iloc[i, -1]
# assign the title in the current row to a variable
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term={title}&field=title'
# append the title into the esearch API string
    response = requests.get(url)
    # run the API and output the result as JSON using requests package
    record = response.json()
    # get the data from the JSON file as a dictionary
    pmid = record.get('esearchresult',{}).get('idlist')
    # get the pmid list from the dictionary
    df1 = pd.DataFrame(pmid)
    # add the pmid list to a dataframe
    if len(df1.index)>1:
        url = f'https://scholar.google.com/scholar?q={title}&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
        # if there is more than one record, generate a URL for a Google Scholar title search
        # to use PubMed title search instead, use: f'https://pubmed.ncbi.nlm.nih.gov/?term={title}'
        df1 = pd.DataFrame({url})
        # make a dataframe for the url
    elif df1.empty:
        url = f'https://scholar.google.com/scholar?q={title}&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
        # if there are NO results, generate a URL for a Google Scholar title search
        df1 = pd.DataFrame({url})
         # make a dataframe with the url
    else:
        pmid2 = df1.iloc[0, -1]
        # get the pmid from the datatable
        url = f'https://tb2lc4tl2v.search.serialssolutions.com/?V=1.0&sid=Entrez:PubMed&id=pmid:{pmid2}'
        df1 = pd.DataFrame({url})
        # create a Serials Solutions search url for the pmid and put it in a dataframe
    df2 = pd.concat([df2, df1])
    # add the current record's dataframe as a row in the full list
    response.close()
    # close the request connection
    time.sleep(.4)
    # wait a before moving to the next row to accommodate e-utilities limitation - see README for details
df2 = df2.reset_index()
# reset the index for df2
dfresult = pd.concat([dforig, df2], axis=1)
# append the url column to the larger data extract 
with pd.ExcelWriter('N:\Python\ScriptRetrievalList.xlsx', mode='a', if_sheet_exists='new') as writer:  
    dfresult.to_excel(writer, sheet_name='Sheet2')
    # write the final dataframe to a new sheet in an Excel file
    