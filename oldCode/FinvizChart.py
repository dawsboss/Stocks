import pandas
import requests
from bs4 import BeautifulSoup as bs

print("test")


url = 'https://finviz.com/quote.ashx?t=AAPL'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

getURL = requests.get(url, headers=headers)
website = bs(getURL.text, 'html.parser')
html = website.find_all('table')[7]

table = html.find_all('tr')
#tableRow = table.find_all('td') Doesn't work.... Can't be a search result

chart = []

for tr in table:
	row = tr.find_all('td')
	for ele in row:
		chart.append(ele.get_text())
		
print(chart)
print(chart[3])
print(type(chart[3]))

for i in range(0,int(len(chart)/2), 2):
	globals()[chart[i]] = chart[i+1]

print(globals()['P/E'])



