from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from pathlib import Path

hfile = Path('myPage.html')
htext = hfile.read_text(encoding='utf-8')
soup = BeautifulSoup(htext, 'html.parser')
li = soup.find_all('li', class_="p-recruit-index__favorite-box")
print(li)