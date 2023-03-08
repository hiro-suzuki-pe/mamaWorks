from pathlib import Path
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pyodbc
import re

def getDetail(url):
    print('url: ', url)
    def getIdx(atags):
        for atag in atags:
            href = atag['href']
            print('href:', href, '\t<- ', atag)
            if re.match('https://mamaworks.jp/job/\d+\s*$', href):
                id = re.sub(r'https://mamaworks.jp/job/', '', href)
                print(href, id)
                return id

    def getId(inptags):
        for inptag in inptags:
            if 'name' in inptag and 'recruit_id' in inptag:
                id = inptag['value']
                print('id = ', id)
                return id
        return ''

    res = requests.get(url)
    sp = BeautifulSoup(res.text, 'html.parser')

    global items
    detail = {item: "(no info)" for item in items}
    detail['Id'] = url.replace('https://mamaworks.jp/job/', '')
    company_name = sp.select_one('div.p-recruit-show__text > h2')
    try:
        detail['会社名'] = company_name.text
    except:
        return detail
    heading = sp.select_one('div.p-recruit-show__text > h1')
    detail['見出し'] = heading.text
    detail['削除フラグ'] = False

    sec = sp.find('table')
    ths = sec.find_all('th')
    tds = sec.find_all('td')
    for n in range(len(ths)):
        detail[ths[n].text.strip()] = tds[n].text

    return detail

def getSpec(job):
    
    def getItem(iname):
        
        item = job.find(class_='p-recruit-index__result-' + iname)
        if item:
            return item.text
        else:
            return None
    
    url = job.find('a')['href']
    getDetail(url)
    
    return getDetail(url)

items =  ['Id', '会社名', '見出し', '仕事内容', '報酬', '掲載日', '成果物の納期予定日', 
          '知的財産権の取扱い', '必須スキル', '歓迎スキル',  '勤務時間・業務時間',  '勤務/業務開始日',  
          '選考の流れ', '選考期間', '仕事の期間',  '報酬の支払期日',  '支払い方法', '諸経費', '削除フラグ']

def insertData(spec):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
#        r'DBQ=D:\mamaWorks\recruit.accdb;'
        r'DBQ=.\recruit.accdb;'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    for sp in spec:
        sql = "INSERT INTO jobs VALUES ("
        for item in items[:-1]:
            try:
                sql += "'" + spec[item] + "',"
            except:
                print(item)
        sql += "False)"
        try:
            cursor.execute(sql)
            cursor.commit()
        except pyodbc.Error as e:
            pass

    conn.close()

def main():    
#    hfile = Path('d:\\mamaWorks\\myPage.txt')
    hfile = Path(r'd:\mamaWorks\myPage.txt')
    htext = hfile.read_text(encoding='utf-8')
    soup = BeautifulSoup(htext, 'html.parser')

    xs = soup.find_all('li',class_='p-recruit-index__result-box')
#    xs = soup.select('ul > li.p-recruit-index__result-box')

    specs = []
    for n in range(0, len(xs), 2):
        spec = getSpec(xs[n])
        specs.append(spec)
        keys = spec.keys()
        print()
        for item in items:
            if item in ['見出し', '仕事内容', '必須スキル', '歓迎スキル']:
                print('{}: {}'.format(item, len(spec[item])))
            elif item in keys:
                print('{}: {}'.format(item, spec[item]))
            else:
                print('{} is missing.'.format(item))
    
    for spec in specs:
        insertData(spec)
    print('spec are inserted in DB')

if __name__ == "__main__":
        main()
       
        #print(getDetail('https://mamaworks.jp/job/8231'))
