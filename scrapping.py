import requests
from bs4 import BeautifulSoup
url="https://www.apunkagames.com/"
r= requests.get(url)
htmlcontent = r.content

soup=BeautifulSoup(htmlcontent,"html.parser")

# print(soup.prettify())
el=soup.find_all("h2",class_="entry-title")

for e in el:
    print(e.text)

