import requests

from bs4 import BeautifulSoup as bs

webpage = requests.get("https://linuxhint.com/python-web-scraping-tutorial/")

webcontent = webpage.content

htmlcontent = bs(webcontent, "html.parser")

for title in htmlcontent.find_all('p'):
    print(title)

#html = open('test1.html').read()

#soup = bs(html, 'html.parser')
#for div in soup.find_all('div', attrs={'class':'tech_head'}):
#        print(div)

