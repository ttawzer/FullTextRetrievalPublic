# FullTextRetrieval
---
Created by Tiffany Tawzer and Christopher Beger, Loyola University Chicago Health Sciences Library
---
## Description
This script opens an Excel file of citation data, uses the NCBI E-utilities [ESearch API](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch) to find PMIDs based on article titles, appends the PMIDs into link resolver URLs and writes those back into the spreadsheet. It uses Google Scholar or PubMed searches as fall-backs when the API does not find a unique PMID match.

[NCBI Disclaimer and Copyright Notice](https://www.ncbi.nlm.nih.gov/About/disclaimer.html)

## Information and best practices
This will work best with consistently formatted, named, and located spreadsheets; otherwise lines 15, 21, and 68 may need to be edited each time.

If the source spreadsheet includes a header row, remove `header=None` from line 15 and line 21.

The dataframe in line 21 could also be generated using `df = dforig.iloc[:, [3]]` where 3 is the index number of the title field. The code as written is used because it is easier to change from a human-readable standpoint.

The sleep function in line 62 adds a pause between each API request. By default, NCBI limits requests to 3 per second. That can be increased to 10 per second by obtaining an API key via an NCBI account. See E-utilities [Usage Guidelines and Requirements](https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requiremen) for more information.

## Prerequesites 
The following Python packages need to be installed:
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- [requests](https://pypi.org/project/requests/)

To open the final URLs, install the "Open Multiple URLs" browser addon (available for both [Chrome](https://chrome.google.com/webstore/detail/open-multiple-urls/oifijhaokejakekmnjmphonojcfkpbbh) and [Firefox](https://addons.mozilla.org/de/firefox/addon/open-multiple-urls/). Select the "Do not load tabs until selected" box to minimize system strain. If there are a large number of citations in the file, open the URLs in batches of 20 or 25. 

