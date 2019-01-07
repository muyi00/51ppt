import sqlite3

class SqliteUtil(object):

    def __init__(self,dbName):
        # 创建数据库
        self.conn = sqlite3.connect(dbName)
        self.c = self.conn.cursor()
        # 创建表
        self.c.execute('''CREATE TABLE IF NOT EXISTS url_info ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, url TEXT NOT NULL);''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS download_error_info ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, url TEXT NOT NULL, error TEXT NOT NULL);''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS unzip_error_info ( id INTEGER PRIMARY KEY AUTOINCREMENT, pathName TEXT NOT NULL, error TEXT NOT NULL);''')

    def insert_url_info(self,url_name_dict):
        self.conn.execute("BEGIN TRANSACTION;") # 开启事务
        for url_str ,name in url_name_dict.items():
            self.c.execute("INSERT INTO url_info (id, name, url) VALUES (null, %s, %s )" % (name,url_str))
        self.conn.execute("COMMIT;")  #关提交事务

    def select_url_info(self):
        url_name_dict_all = {}
        cursor = self.c.execute("SELECT id, name, url from url_info")
        for row in cursor: 
            url_name_dict_all[row[2]] = row[1]
        return url_name_dict_all

    def delete_url_info(self):
        pass


    def insert_download_error_info(self,name,url_str,error):
        self.c.execute("INSERT INTO download_error_info (id, name, url, error) VALUES (null, %s, %s, %s )" % (name,url_str,error))
        self.conn.commit()

    def select_download_error_info(self):
        pass

    def delete_download_error_info(self):
        pass



    def insert_unzip_error_info(self,pathName,error):
        self.c.execute("INSERT INTO unzip_error_info (id, pathName, error) VALUES (null, %s, %s )" % (pathName,error))
        self.conn.commit()

    def select_unzip_error_info(self):
        pass

    def delete_unzip_error_info(self):
        pass