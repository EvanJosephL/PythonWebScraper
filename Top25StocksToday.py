#stock watcher

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from itertools import chain

url = "https://finance.yahoo.com/most-active"

#what i want to grab
names = []
prices = []
changes = []
percents = []

results = requests.get(url)

soup = BeautifulSoup(results.text, "html.parser")

s = soup.find('div', id= 'Lead-5-ScreenerResults-Proxy')

stock_div1 = s.find_all('tr', class_='simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv1BgColor)')
stock_div2 = s.find_all('tr', class_='simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor)')
stock_div = list(chain.from_iterable(zip(stock_div2, stock_div1)))

for container in stock_div:
    name = container.find('td', class_='Va(m) Ta(start) Px(10px) Fz(s)').text
    names.append(name)
    
    price = container.find('td', class_='Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)').text
    prices.append(price)
    
    change_val = container.find_all('span', class_='C($positiveColor)') if container.find_all('span', class_='C($positiveColor)') else container.find_all('span', class_='C($negativeColor)')
    try:
        change = change_val[0].text
        changes.append(change)
    except IndexError:
        change = '-'
        changes.append('-')
    
    
    try:
        change_percent = change_val[1].text
        percents.append(change_percent)
    except IndexError:
        change_percent = '-'
        percents.append('-')
        

stocks = pd.DataFrame({
'Name': names,
'Price': prices,
'Change': changes, 
'%Change': percents,
})

print(stocks)
stocks.to_csv('top25StocksToday.csv')
print("Succesfully written to csv")
