import pandas
import requests
from bs4 import BeautifulSoup as bs

print("test")


url = 'https://finance.yahoo.com/quote/REML'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

getURL = requests.get(url, headers=headers)
website = bs(getURL.text, 'html.parser')
#print(website)
html = website.find_all('span')
print(html[28])
price = html[27].get_text()
change,percentChange = (html[28].get_text().replace("(","").replace(")","")).split(' ')

#print(price)
#print(change)
#print(percentChange)


html = website.find_all('table')[0]
table = html.find_all('tr')

chart = []

for tr in table:
    row = tr.find_all('td')
    for ele in row:
        chart.append(ele.get_text())


html = website.find_all('table')[1]
table = html.find_all('tr')

for tr in table:
    row = tr.find_all('td')
    for ele in row:
        chart.append(ele.get_text())




print(chart)







