# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:28:32 2023

@author: ttawzer
"""

import numpy
import pandas as pd
# This assigns a variable to the package name for convenience
import requests
import json
import time
import webbrowser

dataorig = pd.read_excel('C:/Users/ttawzer/Desktop/ScriptRetrievalList.xlsx', usecols='D,B,W')
dforig = pd.DataFrame(dataorig)
dforig['index'] = dforig.index
# print()

data = pd.read_excel('C:/Users/ttawzer/Desktop/ScriptRetrievalList.xlsx', usecols='D')
# open Excel file and choose article name column
df = pd.DataFrame(data)
# turn the column into a dataframe
df = df.replace(' ','+', regex=True)
# change all spaces to +
df2 = pd.DataFrame({})
# set up an empty dataframe to hold the pmids
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
    # get the pmid from the dictionary
    df1 = pd.DataFrame(pmid)
    if len(df1.index)>1:
        url = f'https://pubmed.ncbi.nlm.nih.gov/?term={title}'
        df1 = pd.DataFrame({url})
  #      webbrowser.open(url, new=1, autoraise=True)
        # if there is more than one record, open a PubMed search of the title
    elif df1.empty:
        url = f'https://pubmed.ncbi.nlm.nih.gov/?term={title}'
        df1 = pd.DataFrame({url})
   #     webbrowser.open(url, new=1, autoraise=True)
        # if there are no records, open a PubMed search of the title
    else:
        pmid2 = df1.iloc[0, -1]
        # get the pmid from the datatable
        url = f'https://tb2lc4tl2v.search.serialssolutions.com/?V=1.0&sid=Entrez:PubMed&id=pmid:{pmid2}'
        df1 = pd.DataFrame({url})
   #     webbrowser.open(url, new=1, autoraise=True) 
        # open a Serials Solutions search using the pmid
    df2 = pd.concat([df2, df1])
    time.sleep(.5)
    # wait a second before moving to the next row
df2 = df2.reset_index()
df2 = df2.reindex(dforig.index)
dfresult = pd.concat([dforig, df2], axis=1).reindex(dforig.index)

with pd.ExcelWriter('C:/Users/ttawzer/Desktop/PythonTest.xlsx', mode='a') as writer:  
#    dfresult.to_excel(writer, sheet_name='Sheet2')
   
