import pandas
import requests
from bs4 import BeautifulSoup as bs

print("test")


url = 'https://finance.yahoo.com/quote/XOM?p=XOM&.tsrc=fin-srch'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

getURL = requests.get(url, headers=headers)
website = bs(getURL.text, 'html.parser')
html = website.find_all('span')

price = html[27].get_text()
change,percentChange = (html[28].get_text().replace("(","").replace(")","")).split(' ')
print(price)
print(change)
print(percentChange)

