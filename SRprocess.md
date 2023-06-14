## SR full-text retrieval process

- Librarian working on the SR exports a citation list and saves it as an Excel spreadsheet
- Access Services Librarian runs the PubMedScript.py Python script to generate search URLs
- ILL and Access Services Specialist uses the "Open Multiple URLs" browser add-on to open the URLs in batches, then:
1. Downloads the PDFs available through the library's holdings and saves them with a unique ID number that corresponds to the citation
2. Uses ILLiad web platform to create interlibrary loan requests from the link resolver's results page
3. Exports the list of filled requests from ILLiad into an Excel file
4. Generates a download link by adding the Transaction Number(TN) to ILLiad's standard URL scheme
5. Downloads and saves the articles using the request's TN as the file name (this is ILLiad's default file name) 
6. Creates a .bat file in Excel that renames the files with their unique IDs
