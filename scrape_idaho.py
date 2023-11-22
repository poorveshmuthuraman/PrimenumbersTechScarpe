from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

URL = "https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787"

est_value_notes = []
description = []
closing_date = []

options = Options()
options.add_experimental_option("detach", False)
driver = webdriver.Chrome(options=options) 
driver.get(URL)

time.sleep(3) # load web browser

html = driver.page_source 
soup = BeautifulSoup(html,"html.parser")
headers = []
rows = []

for i, row in enumerate(soup.findAll("tr")):
    if i == 0:
        for header in row.find_all("th"):
            headers.append(header.text.strip()) # get header strings
    else:
        rows.append([r.text.strip() for r in row.find_all('td')])

rows = [row for row in rows if row != []] # remove empty rows
rows = rows[0:5] # getting first 5 records

# closing date
for row in rows:
    closing_date.append(row[4])

# go to records
link=driver.find_element("link text", str(rows[0][1])) 

#Click on Next & Scrape everytime
count=0
while(count!=5):
    link.click()
    time.sleep(5)

    html=driver.page_source
    before=html.split("Additional Description",1)[0]
    after=before.split("Description:",1)[1]
    soup=BeautifulSoup(after,"html.parser")
    soup.find_all('td')
    for desc in soup:
        if(desc.text.strip()!=""):
            description.append(desc.text.strip())

    before=html.split("Project Description",1)[0]
    after=before.split("Est. Value Notes:",1)[1]
    soup=BeautifulSoup(after,"html.parser")
    soup.find_all('td')
    for est_val in soup:
        if(est_val.text.strip()!=""):
            est_value_notes.append(est_val.text.strip())

    count+=1 # increment when one record is read
    html=driver.page_source
    soup=BeautifulSoup(html,"html.parser")
    with open('soup.txt', 'w') as f:
        f.write(str(soup))
    link=driver.find_element("id",'id_prevnext_next')

print(description)
print(est_value_notes)
print(closing_date)

# saving to csv file
with open('search_postings.csv', 'w') as csvfile:
    fieldnames = ['closing_date', 'description', 'est_value_notes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()    
    for i, j, k in zip(closing_date, description, est_value_notes):
        writer.writerow({fieldnames[0]: i, fieldnames[1]: j, fieldnames[2]: k})













