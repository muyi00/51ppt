
class UnzipErrorInfo(object):

    def __init__(self,pathName,errorStr):
        self.pathName = pathName
        self.errorStr = errorStr

    def getPathName(self):
        return self.pathName
    
    def getErrorStr(self):
        return self.errorStr