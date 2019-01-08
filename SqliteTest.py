import sqlite3

def createDB():
    # 创建数据库
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    # 创建表
    c.execute('''CREATE TABLE IF NOT EXISTS url_info ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, urlStr TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS download_error_info ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, urlStr TEXT NOT NULL, errorStr TEXT NOT NULL);''')
    c.execute('''CREATE TABLE IF NOT EXISTS unzip_error_info ( id INTEGER PRIMARY KEY AUTOINCREMENT, pathName TEXT NOT NULL, errorStr TEXT NOT NULL);''')

createDB()