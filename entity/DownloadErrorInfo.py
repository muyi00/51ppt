
class DownloadErrorInfo(object):

    def __init__(self,name,urlStr):
        self.name = name
        self.urlStr = urlStr

    def getName(self):
        return self.name
    
    def getUrlStr(self):
        return self.urlStr