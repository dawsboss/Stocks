import pandas
import requests
from bs4 import BeautifulSoup as bs
import analysis_engine.finviz.fetch_api as fv

print("test")

webpage = requests.get("https://www.dividendinvestor.com/projected-dividend-yield/?symbol=cldt&proj_div_yield=10")
webcontent = webpage.content
#htmlcontent = bs(webcontent, "html.parser")
#for title in htmlcontent.find_all('h1'):
#    print(title)


url = (
        'https://finviz.com/screener.ashx?'
        'v=111&'
        'f=cap_midunder,exch_nyse,fa_div_o5,idx_sp500'
        '&ft=4')
res = fv.fetch_tickers_from_screener(url=url)
print(res)

print("End")





#html = open('test1.html').read()

#soup = bs(html, 'html.parser')
#for div in soup.find_all('div', attrs={'class':'tech_head'}):
#        print(div)

