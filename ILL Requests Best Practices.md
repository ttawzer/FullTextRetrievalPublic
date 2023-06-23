# ILL Requests Best Practices

After gathering a list of articles that require requesting via ILL, you may begin making the requests via ILLiad. We’ve found that making these requests via ILLiad’s web portal is quicker than using the ILLiad desktop client. Optionally, you may find it useful to setup a dedicated ILLiad user account for the purpose of making systematic review requests to spare your researchers/staff from a barrage of article delivery notifications.

## Getting Started
To get started, navigate to the requestor’s user profile in the ILLiad desktop client and click the “Logon as User” button. You'll then bulk re-open the article ILL request pages using the aforementioned Open Multiple URLs extension. To reduce strain on system resources you may wish to check the "Do not load tab until selected" box in the extension settings menu. Helpfully, the web portal exposes the “user notes” field. When making the ILL requests, you’ll append the unique number assigned to each article found in the systematic review Excel spreadsheet in the user notes field. We refer to this number as the “PDF ID.” Adding the PDF ID in the user notes field will make for easy bulk-renaming later.

## Using Custom Search
Once the requests have been fulfilled by lending libraries, you’ll use the included ILLiad custom search file to export a list of the ILL requests that includes each article’s Transaction Number (TN) and the user notes field. Start by downloading the ILLiad custom search file in this repository named "Systematic-Review-Export-Note-Field.irrp" and load the file in your ILLiad desktop client. To navigate to the custom search function in ILLiad, click the small arrow under the requests "Search" button and click "Custom Request Search." Then, click the "Load" button and import the .irrp file. To use the custom search, start by altering the username field of the custom search to reflect the username of the requestor and alter the date field to reflect the creation dates of the requests that were made for the current systematic review. Run the search and use the "Export" button to export the results into an Excel spreadsheet.

## Bulk Downloading Articles
To bulk-download the fulfilled ILLiad requests, open the exported Excel file and add a column with the following concatenated formula to create instant-download URLs (be sure to alter the URL to reflect your institution’s ILLiad web server address).
```
=CONCATENATE("https://your-illiad-server-address/illiad/illiad.dll?Action=10&Form=75&Value=",A1)
```
In this formula, the A column represents the list of TNs from the exported custom search. Once you’ve created the URLs, you may open them in bulk using the Open Multiple URLs extension. The article PDFs should download instantly and by default their downloaded name should reflect their TN.

## Bulk Renaming Articles
Once you've successfully downloaded the ILL articles, you’ll need to rename them from their TN # to their PDF ID #. You can do this efficiently by creating a small batch script that will bulk rename the files. To get started, place the PDFs obtained via ILL in a new folder (the location of this folder is not important). Then, create a new column in the exported Excel sheet and add the following formula to generate the rename commands that will bulk-rename the PDFs on our behalf:
```
=CONCATENATE("rename ",A1,".pdf ",B1,".pdf")
```
In this formula, the A column represents the TNs, and the B column represents the PDF ID #.
Copy the contents of this column and paste them into a Notepad file. Then, in Notepad, click File > Save As. By default, the name of the Notepad file will be *.txt. Delete this default text (including the .txt file extension) and name the file: rename.bat

Then, save the file in the same folder containing the downloaded PDFs. Double click on the newly created rename.bat file and the batch script will bulk-rename the PDFs to their PDF ID #.

## Distributing the Files
Once you’ve successfully renamed the ILL PDFs, all that is left to do is to move them into the larger folder with gathered articles that did not require interlibrary loan. We recommend spot checking the PDF ID #s to ensure that you successfully gathered all the articles. You may then place them into cloud drive such as Microsoft Sharepoint for easy controlled distribution to your researchers.
