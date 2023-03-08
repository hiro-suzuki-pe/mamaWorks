import pyodbc

items =  ['Id', '会社名',  '勤務/業務開始日', '削除フラグ']


conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=.\recruit.accdb;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


sql = "INSERT INTO jobsTest  VALUES('133', 'ヒロ鈴木', '3/8', True, 'a/b')"

try:
    cursor.execute(sql)
    cursor.commit()
except Exception as e:
    print('\nsql failed: ', sql)
    print(e)

conn.close()
