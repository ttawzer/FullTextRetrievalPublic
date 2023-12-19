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
# import webbrowser
# webbrowser is useful if you want to open the URLs instead of writing to Excel

dforig = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', header=None)
df = pd.read_excel('N:\Python\ScriptRetrievalList.xlsx', usecols='D', header=None)
df2 = pd.DataFrame({})
# set up an empty dataframe to hold the pmids later
for i in range(0, len(df)):
# for every item, starting at index 0 and ending and the last cell, do the following   
    title = df.iloc[i, -1]
    # assign the title in the current row to a variable
    title = str(title)
    # change data type to string
    title2 = title.replace(' ','+')
    # second variable that replaces spaces in title with +; needed for Google Scholar URLs
    payload2 = {'id': title}
    # define parameters for unpaywall api
    response2 = requests.get('https://api.openaccessbutton.org/find?', params=payload2)
    # run unpaywall api
    record2 = response2.json()
    # get response as json
    value = record2 
    # assign the results list of dictionaries to a variable
    if "url" in value:
        oaurl = record2["url"]
    else:
        oaurl = "none" 
#    time.sleep(.1)
 #   response2.close()
        # close the request
    payload1 = {'db': 'pubmed', 'retmode':'json', 'field': 'title', 'term': title, 'email':'hslill@luc.edu', 'api_key': '<NCBI API KEY>'}
    # define parameters for esearch api
    response = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?', params=payload1)
    # run esearch api with defined parameters
    record = response.json()
    # get the data from the JSON file as a dictionary
    pmid = record.get('esearchresult',{}).get('idlist')
    # get the pmid list from the dictionary
    if len(pmid)>1:
        if (oaurl == 'none') is False:
            url = oaurl
        else:
            url = f'https://scholar.google.com/scholar?q={title2}&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
        # if there is more than one record, generate a URL for a Google Scholar title search
        # to use PubMed title search instead, use: f'https://pubmed.ncbi.nlm.nih.gov/?term={title}'
    elif len(pmid) == 0:
        if (oaurl == 'none') is False:
            url = oaurl
        else:
            url = f'https://scholar.google.com/scholar?q={title2}&ie=UTF-8&oe=UTF-8&hl=en&btnG=Search'
        # if there are NO results, generate a URL for a Google Scholar title search
    else:
        pmid2 = pmid[0]
        # get the pmid from the list and assign to a variable
        url = f'https://tb2lc4tl2v.search.serialssolutions.com/?V=1.0&sid=Entrez:PubMed&id=pmid:{pmid2}'
        # create a Serials Solutions search url for the pmid 
    df1 = pd.DataFrame(data = {'OA URL':[oaurl], 'Holdings URL':[url]})
    # Create a dataframe with the resulting variables
    df2 = pd.concat([df2, df1])
    # add the current record's dataframe as a row in the full list
    time.sleep(.1)
    # wait before moving to the next row to accommodate eutil limitation; this time is reduced because we use an api key
#    response.close()
        # close the api request
df2 = df2.reset_index()
# reset the index for df2
dfresult = pd.concat([dforig, df2], axis=1)
# append the url column to the larger data extract 
with pd.ExcelWriter('N:\Python\ScriptRetrievalList.xlsx', mode='a', if_sheet_exists='new') as writer:  
    dfresult.to_excel(writer, sheet_name='Sheet2')
    # write the final dataframe to a new sheet in an Excel file
print("done")