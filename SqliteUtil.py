import sqlite3
from PptUrlInfo import PptUrlInfo

class SqliteUtil(object):

    def __init__(self):
        self.conn = sqlite3.connect('ppt.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS url_info ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            name TEXT NOT NULL,  
            detailsUrl TEXT NOT NULL,
            downloadUrl TEXT
            );''')
    
    def insert_url_info(self, pptUrlInfoList):
        self.c = self.conn.cursor()
        args=[]
        for item in pptUrlInfoList:
            args.append((item.typeStr, item.name, item.detailsUrl ,item.detailsUrl))
        try:
            # self.c.executemany("INSERT INTO url_info VALUES (null, ?, ? , ?, '')",args)
            self.c.executemany("INSERT INTO url_info(type, name, detailsUrl, downloadUrl) \
            select ?, ?, ?, '' \
            where not exists  (SELECT * from url_info where detailsUrl = ?)",args)
        except Exception as e:
            print('INSERT INTO url_info 时出错：%s' % e)
        finally:
            self.c.close()
            self.conn.commit()

    def update_url_info(self,downloadUrl,detailsUrl):
        self.c = self.conn.cursor()
        self.c.execute("UPDATE url_info set downloadUrl = '%s' where detailsUrl = '%s' " % (downloadUrl,detailsUrl))
        self.c.close()
        self.conn.commit()

    def update_url_info_downloadUrl(self,downloadUrlList):
        self.c = self.conn.cursor()
        args=[]
        for item in downloadUrlList:
            args.append((item.downloadUrl ,item.detailsUrl))
        try:
            self.c.executemany("UPDATE url_info set downloadUrl = ? where detailsUrl = ? ",args)
        except Exception as e:
            print('UPDATE INTO url_info 时出错：%s' % e)
        finally:
            self.c.close()
            self.conn.commit()


    def select_url_info(self):
        self.c = self.conn.cursor()
        pptUrlInfoList=[]
        cursor = self.c.execute("SELECT type, name, detailsUrl from url_info")
        for row in cursor: 
            pptUrlInfoList.append(PptUrlInfo(row[0],row[1],row[2]))
        cursor.close()
        self.c.close()
        return pptUrlInfoList

    

    def select_url_info_all(self):
        self.c = self.conn.cursor()
        pptUrlInfoList=[]
        cursor = self.c.execute("SELECT type, name, detailsUrl, downloadUrl from url_info")
        for row in cursor: 
            pptUrlInfoList.append(PptUrlInfo(row[0],row[1],row[2],row[3]))
        cursor.close()
        self.c.close()
        return pptUrlInfoList

    def delete_url_info_all(self):
        self.c = self.conn.cursor()
        self.c.execute("DELETE from url_info")
        self.c.close()
        self.conn.commit()



   