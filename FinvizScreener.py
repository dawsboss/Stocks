import pandas
import requests
from bs4 import BeautifulSoup as bs

print("test")


url = 'https://finviz.com/screener.ashx?v=111&t=REML'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

getURL = requests.get(url, headers=headers)
website = bs(getURL.text, 'html.parser')
html = website.find_all('table')[16]
print(html)
table = html.find_all('tr')
chart = []
for tr in table:
	row = tr.find_all('td')
	for ele in row:
		chart.append(ele.find('a')[0].get_text())
print(chart)
#for i in range(0,int(len(chart)/2), 2):
#	globals()[chart[i]] = chart[i*+1]

#print(globals())



