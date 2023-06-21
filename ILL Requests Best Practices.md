# ILL Requests Best Practices
---
After gathering a list of articles that require requesting via ILL, you may begin making the requests via ILLiad. We’ve found that making these requests via ILLiad’s web portal is quicker than using the ILLiad desktop client. Optionally, you may find it useful to setup a dedicated ILLiad account for the purpose of making systematic review requests to spare your researchers/staff from a barrage of article delivery notifications.

To get started, navigate to the requestor’s user profile in the ILLiad desktop client and click the “Logon as User” button. Helpfully, the web portal exposes the “user notes” field. When making the ILL requests, you’ll append the unique number assigned to each article found in the Excel spreadsheet in the user notes field. We refer to this number as the “PDF ID.” Adding the PDF ID in the user notes field will make for easy bulk-renaming later.

```
Excel codeblock test
=CONCATENATE("https://your-illiad-server-address/illiad/illiad.dll?Action=10&Form=75&Value=",A1)
```
