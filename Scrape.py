import pandas
import requests
from bs4 import BeautifulSoup as bs

print("test")


url = 'https://www.dividendinvestor.com/projected-dividend-yield/?symbol=cldt&proj_div_yield=10'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url, headers=headers)
print(response.content)
