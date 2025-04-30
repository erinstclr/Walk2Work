# Walk2Work

Collect ASINs (amazon product numbers, found in URL, typically a string of capital letters and numbers) and plce them into an ASINS.txt file
open APIScrape.py

*APIScrape.py*
run these first in the terminal to install dependencies
-> python -m pip install requests
-> python -m pip install lxml
-> python -m pip install pandas
-> python -m pip install bs4
-> pyhton -m pip install re
-> python -m pip install gender_guesser

-go to oxylabs.io and register an account
-select the web scraper and select subscription level (we used free tier) 
-create a user for the api and remember your credentials
in the APIScrape.py script, replace the credentials with yours  to connect to the API
-you can adjust the number of pages that you want to collect (roughly 9 to 10 reviews per page)
-change the file path to YOUR file path for the txt file holding the ASINs
-Run the program
-a .csv will be created (mine was in my C:\users\MyUser)
-this .csv will have the reviews from the ASINs you put into the txt file
-now, go to ProcessReviews.py and run the script
-you will now have a new .csv file that will be structured, calculating semtiment values, gender, and extracting features that were desired and not present in the product.