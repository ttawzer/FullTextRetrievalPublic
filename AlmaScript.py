# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:28:32 2023

@author: ttawzer
"""

import pandas as pd
# This assigns a variable to the package name for convenience
import requests
import time
# import webbrowser
# webbrowser is useful if you want to open the URLs instead of writing to Excel

dforig = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', usecols='B:M', header=None)
    # open the Excel file and create a dataframe with columns desired for the final output
    # column choice may need to be changed based on the spreadsheet export from EndNote
    # remove 'header=None' if the spreadsheet contains a header row
dforig['index'] = dforig.index
    # assign an index to the data
df = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', usecols='E', header=None)
    # open Excel file and create a dataframe from the article name column
    # column choice may need to be changed based on the spreadsheet export from EndNote
    # remove 'header=None' if the spreadsheet contains a header row
df = df.replace(' ','+', regex=True)
    # change all spaces to +
df2 = pd.DataFrame({})
    # set up an empty dataframe to hold the pmids later
for i in range(0, len(df)):
    # for every item, starting at index 0 and ending and the last cell, do the following   
    title = df.iloc[i, -1]
        # assign the title in the current row to a variable
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term={title}&field=title'
        # append the title into the esearch API string for a title-field search
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
            # if there is more than one record, generate a URL for Google Scholar title search
            # to use a PubMed search instead, use: f'https://pubmed.ncbi.nlm.nih.gov/?term={title}
        df1 = pd.DataFrame({url})
            # make a dataframe for the url
    elif df1.empty:
        url = f'https://scholar.google.com/scholar?q={title}&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
            # if there are no records, generate a URL for a Google Scholar title search
        df1 = pd.DataFrame({url})
            # make a dataframe with the url
    else:
        pmid2 = df1.iloc[0, -1]
            # if there is exactly one record, get the pmid from the datatable
        url = f'https://loyola-primo.hosted.exlibrisgroup.com/openurl/01LUC/01LUC_SERVICES?sid=Entrez:PubMed&id=pmid:{pmid2}'
        df1 = pd.DataFrame({url})
            # create a Serials Solutions search url for the pmid and put it in a dataframe
    df2 = pd.concat([df2, df1])
        # add the current record's dataframe to the full list
    time.sleep(.5)
        # wait a half second before moving to the next row to account for eutils limitation
df2 = df2.reset_index()
    # reset the index for df2
dfresult = pd.concat([dforig, df2], axis=1).reindex(dforig.index)
    # add the url column to the original data from dforig
with pd.ExcelWriter('N:\Python\ScriptRetrievalList.xlsx', mode='a', if_sheet_exists='new') as writer:  
    dfresult.to_excel(writer, sheet_name='Sheet2')
        # write the final dataframe to a new sheet in the original Excel file
   
