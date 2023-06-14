Once you’ve compiled a list of articles that need to be requested via ILLiad, you can login to the ILLiad web portal to make these requests. We’ve found that making these requests via the web portal is quicker than in ILLiad proper. The web portal also exposes the User Notes field. When making the requests for the articles, you’ll append the PDF ID # in User Notes field. This will make for easy bulk-renaming.

After the requests have been fulfilled by lending libraries, you’ll use the included custom search tool to export a list of the ILLiad requests that includes their TN and PDF ID #. Simply alter the username field of the search to reflect the username of the requestor and alter the date field to reflect the transaction dates of the requests that were made for the current systematic review.

To bulk-download fulfilled ILLiad requests, use the following concatenated formula in Excel to create instant-download URLs (be sure to alter the URL to reflect your web-instance of ILLiad). In the formula, the A column represents the list of TNs from the exported custom search. Do not rename these PDFs, by default their downloaded name should reflect their TN:
=CONCATENATE("https://luhs.illiad.oclc.org/illiad/illiad.dll?Action=10&Form=75&Value=",A1)

Once you’ve created the URLs, you can bulk open the URLs using this open-source extension (available in the Firefox and Chrome web stores): https://github.com/htrinter/Open-Multiple-URLs

Use this formula to create rename commands to bulk-rename the articles from their TN to their PDF ID #. In this formula, the A column represents the TNs, and the B column represents the PDF ID #.
=CONCATENATE("rename ",A1,".pdf ",B1,".pdf")

Copy the results and paste them into a notepad file. In Notepad, Click File > Save As. By default, the name will be *.txt. Delete the default string of text and name the file: rename.bat
Save the file in the same folder containing the downloaded PDFs.
Double click on the saved file and the script will bulk-rename the PDFs to their PDF ID #.
Compile all the PDFs and place them into a Sharepoint folder for easy controlled distribution.
