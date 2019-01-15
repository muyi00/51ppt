class PptUrlInfo(object):
    def __init__(self,typeStr,name,detailsUrl,downloadUrl='',fileSize=0,savePath=''):
        self.typeStr=typeStr
        self.name=name
        self.detailsUrl=detailsUrl
        self.downloadUrl=downloadUrl
        self.fileSize=fileSize
        self.savePath=savePath