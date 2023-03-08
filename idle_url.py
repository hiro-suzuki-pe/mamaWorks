from pathlib import Path
from bs4 import BeautifulSoup
import requests

url = 'http://intervalues.com/idol.html'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')
idles = soup.find_all(class_='top_noline')
for idle in idles:
    print(idle)
#    print(idle.find('a').find('href'))
    print('<a>', idle.find('a'))
    print('<a>[href]', idle.find('a')['href'])



idles = soup.select('body > center:nth-child(9) > div > table > tbody > tr:nth-child(1) > td > a')
if idles:
    for idle in idles:
        print(idle)
else:
    print('No idles.')
