from pathlib import Path
from bs4 import BeautifulSoup
import requests
url = 'https://book.impress.co.jp/'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
for h in soup.find_all('h2'):
    print(h)
