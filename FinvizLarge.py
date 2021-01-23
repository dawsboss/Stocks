import pandas
import requests
from bs4 import BeautifulSoup as bs

print("test")


url = 'https://finviz.com/quote.ashx?t=REML'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

getURL = requests.get(url, headers=headers)
website = bs(getURL.text, 'html.parser')
html = website.find_all('table')[7]


print(html)
