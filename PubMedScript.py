# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:28:32 2023

@author: ttawzer
"""

# import numpy
import pandas as pd
# This assigns a variable to the package name for convenience
import requests
import json
import time
# import webbrowser
# webbrowser is useful if you want to open the URLs instead of writing to Excel

dataorig = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', usecols='B,C,D,E,F,G,H,I,J,K,L,M')
# open the Excel file choose columns
# column choice may need to be changed based on the spreadsheet setup
dforig = pd.DataFrame(dataorig)
# create a dataframe of imported data
dforig['index'] = dforig.index
# assign an index to the data

df = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', usecols='E')
# open Excel file and choose article name column
# df = pd.DataFrame(data)
# turn the column into a dataframe
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
        # if there is more than one record, generate a URL for a pubmed search of the title
        df1 = pd.DataFrame({url})
        # make a dataframe for the url
    elif df1.empty:
        url = f'https://scholar.google.com/scholar?q={title}&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
        # if there are no records, generate a URL for a pubmed search of the title
        df1 = pd.DataFrame({url})
         # make a dataframe with the url
    else:
        pmid2 = df1.iloc[0, -1]
        # get the pmid from the datatable
        url = f'https://tb2lc4tl2v.search.serialssolutions.com/?V=1.0&sid=Entrez:PubMed&id=pmid:{pmid2}'
        df1 = pd.DataFrame({url})
        # create a Serials Solutions search url for the pmid and put it in a dataframe
    df2 = pd.concat([df2, df1])
    # add the current record's dataframe to the full list
    time.sleep(.5)
    # wait a half second before moving to the next row
df2 = df2.reset_index()
# reset the index for df2
# df2 = df2.reindex(dforig.index)
# change the index of df2 to match dforig 
dfresult = pd.concat([dforig, df2], axis=1).reindex(dforig.index)
# add the url column to the original data from dforig
with pd.ExcelWriter('N:\Python\ScriptRetrievalList.xlsx', mode='a', if_sheet_exists='new') as writer:  
    dfresult.to_excel(writer, sheet_name='Sheet2')
    # write the final dataframe to a new sheet in an Excel file
   
