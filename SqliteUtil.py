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
            downloadUrl TEXT,
            fileSize INTEGER DEFAULT 0,
            savePath TEXT
            );''')
    
    def insert_url_info(self, pptUrlInfoList):
        self.c = self.conn.cursor()
        args=[]
        for item in pptUrlInfoList:
            args.append((item.typeStr, item.name, item.detailsUrl ,item.downloadUrl, item.fileSize, item.savePath, item.detailsUrl))
        try:
            # self.c.executemany("INSERT INTO url_info VALUES (null, ?, ? , ?, '')",args)
            self.c.executemany("INSERT INTO url_info(type, name, detailsUrl, downloadUrl,fileSize,savePath) \
            select ?, ?, ?, ?, ?, ? \
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
    
    def update_url_info_fileSize(self,fileSize,downloadUrl):
        self.c = self.conn.cursor()
        self.c.execute("UPDATE url_info set fileSize = %s where downloadUrl = '%s' " % (fileSize,downloadUrl))
        self.c.close()
        self.conn.commit()
    
    def update_url_info_savePath(self,savePath,downloadUrl):
        self.c = self.conn.cursor()
        self.c.execute("UPDATE url_info set savePath = '%s' where downloadUrl = '%s' " % (savePath,downloadUrl))
        self.c.close()
        self.conn.commit()

    def selectDownloadUrl(self,detailsUrl):
        self.c = self.conn.cursor()
        downloadUrl = ''
        cursor = self.c.execute("SELECT downloadUrl from url_info where detailsUrl = '%s'" % detailsUrl)
        for row in cursor: 
            downloadUrl = row[0]
            if downloadUrl is None:
                downloadUrl = ''
        cursor.close()
        self.c.close()
        return downloadUrl

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
        cursor = self.c.execute("SELECT type, name, detailsUrl, downloadUrl,fileSize,savePath from url_info where savePath is null")
        for row in cursor: 
            pptUrlInfoList.append(PptUrlInfo(row[0],row[1],row[2],row[3],row[4],row[5]))
        cursor.close()
        self.c.close()
        return pptUrlInfoList
    
    def select_url_info_fileSize_0(self):
        self.c = self.conn.cursor()
        pptUrlInfoList=[]
        cursor = self.c.execute("SELECT type, name, detailsUrl, downloadUrl,fileSize from url_info where fileSize = 0")
        for row in cursor: 
            pptUrlInfoList.append(PptUrlInfo(row[0],row[1],row[2],row[3],row[4]))
        cursor.close()
        self.c.close()
        return pptUrlInfoList

    def delete_url_info_all(self):
        self.c = self.conn.cursor()
        self.c.execute("DELETE from url_info")
        self.c.close()
        self.conn.commit()

    def addColumn(self):
        '''增加列'''
        self.c = self.conn.cursor()
        self.c.execute("ALTER TABLE url_info ADD COLUMN savePath TEXT")
        self.c.close()
        self.conn.commit()

   