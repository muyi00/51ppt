# 1.初始化目录，数据库
# 2.获取模板描述路径，批量保存到表中
# 3.循环遍历表，获取下载地址
# 4.按照类型下载压缩模板
# 5.按类型解压

import threading
import os
import sqlite3
import requests
from bs4 import BeautifulSoup
import re
from SqliteUtil import SqliteUtil
from PptUrlInfo import PptUrlInfo
import sys



# 51ppt模板主页面
base_51_url = 'http://www.51pptmoban.com'

def getBaseDir():
    '''获取当前工作目录路径'''
    return os.getcwd()

def jointPath(path1,path2):
    """ 路径拼接 """
    if path1.endswith('/'):
        path1=path1[:-1]
    if path2.startswith('/'):
        path2=path2[1:]
    return '%s/%s' % (path1,path2)

def makedirs(path):
    """ 创建路径 """
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

def getBaseSaveDir():
    """ 下载保存路径 """
    path = jointPath(getBaseDir(),'zip')
    makedirs(path)
    return path

def getBaseUnzipTempDir():
    """ 解压文件缓存路径 """
    path = jointPath(getBaseDir(),'unzip_temp')
    makedirs(path)
    return path

def getBaseUnzipDir():
    """ ppt保存路径 """
    path = jointPath(getBaseDir(),'unzip')
    makedirs(path)
    return path

def getIntString(s):
    return re.findall("\d+",s)[0]

def getChinese(s):
    pattern="[\u4e00-\u9fa5]+" 
    regex = re.compile(pattern)
    name =''
    for ss in regex.findall(s):
        name = name+ss
    return name
    
def progressBar(title,total,progress):
    done = int(50 * progress / total)
    sys.stdout.flush()
    sys.stdout.write("\r[%s] [%s%s] %d%%" % (title,'#' * done, ' ' * (50 - done), 100 * progress / total))
    sys.stdout.flush()

# 获取所有页面
def get_ppt_51_page_list():
    """ 获取所有ppt 页面地址集合 """
    ppt_51_url_list = ['http://www.51pptmoban.com/ppt/']
    r= requests.get(ppt_51_url_list[0])
    r.encoding='GBK'
    soup = BeautifulSoup(r.text,"lxml")
    pages = soup.find(name='div',attrs={"class":"pages"})
    if pages:
        for page in pages.find_all("a"):
            if page.get('href'):
                if '尾页' in page.string:
                    pages_int = int(getIntString(page.get("href"))) 
                    for index in range(2,pages_int+1):
                        # http://www.51pptmoban.com/ppt/index_2.html
                        ppt_51_url_list.append(jointPath(base_51_url,'ppt/index_%s.html' % index ))
                        # break
    return ppt_51_url_list  

def getOnePageDetailsInfoList(pageUrl,pageIndex):
    '''获取一个页面的所有模板的详情信息页面'''
    onePageDetailsInfoList = []
    r= requests.get(pageUrl)
    r.encoding='GBK'
    soup = BeautifulSoup(r.text,"lxml")
    a_tag_list=soup.find_all("a")
    for a_tag in a_tag_list:
        img = a_tag.find('img')
        if img:
            url_path = a_tag.get("href")
            if url_path.count('/')==2:
                # 模板类型
                typeStr = url_path.split('/')[1]
                # 模板名称
                name = getChinese(img.get("alt"))
                # 描述页面地址
                detailsUrl = jointPath(base_51_url,url_path)
                onePageDetailsInfoList.append(PptUrlInfo(typeStr,name,detailsUrl))

    return onePageDetailsInfoList
    


def getDownloadPageUrl(urlStr):
    """ 获取下载页面路径 """
    r= requests.get(urlStr)
    r.encoding='GBK'
    soup = BeautifulSoup(r.text,"lxml")
    div = soup.find(name='div',attrs={"class":"ppt_xz"})
    a_tag = div.find("a")
    return a_tag.get('href')

def getDownloadUrl(url_path):
    """ 获取下载路径 """
    path_list=url_path.lstrip('/').split('/')
    r= requests.get(jointPath(base_51_url,url_path))
    r.encoding='GBK'
    soup = BeautifulSoup(r.text,"lxml")
    div = soup.find(name='div',attrs={"class":"down"})
    a_tag = div.find("a")
    path = a_tag.get('href').lstrip('../')
    # print(path)
    return jointPath(base_51_url,'%s/%s/%s' % (path_list[0],path_list[1],path))


def getPptFilePathName(dirNmae,name,suffix):
    return '%s/%s.%s' % (dirNmae,name,suffix)

def writelog(url_str ,name,e_str):
    with open(jointPath(getBaseDir(),'log.txt'), 'a+') as f:
        f.write('%s#%s#%s\n' % (url_str,name,e_str))

def downloadFile(index,dirNmae,name,download_url):
    """ 下载文件 """
    filePathName = getPptFilePathName(dirNmae,name,'zip')
    if os.path.isfile(filePathName)  : #文件是否存在
        # 已经下载成功
        progressBar(('%s-%s') % (index,name),100,100)
        return
    #把下载地址发送给requests模块
    r = requests.get(download_url)
    total_size = 0
    try:
        header_str = r.headers['Content-Length']
        if header_str:
            total_size = int(header_str)
    except BaseException as e:
        writelog(download_url,name,e)
        return
    temp_size = 0
    # ZIP的application/x-zip-compressed     
    # RAR的application/octet-stream  
    content_type = r.headers['Content-Type']
    suffix = 'rar'
    if 'application/x-zip-compressed' in content_type:
        suffix = 'zip'
   
    #下载文件
    with open(getPptFilePathName(dirNmae,name,suffix),"wb") as f:
        if total_size == 0 :
            f.write(r.content)
            progressBar(('%s-%s') % (index,name),100,100)
        else:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    progressBar(('%s-%s') % (index,name),total_size,temp_size)
                   




isGetDownloadUrl = False

if __name__ == '__main__':

    sqliteUtil = SqliteUtil()

    if isGetDownloadUrl:
        ppt_51_url_list = get_ppt_51_page_list()
        print('总共发现%s个页面' % len(ppt_51_url_list))
        for index, pageUrl in enumerate(ppt_51_url_list):
            onePageDownloadInfoList = []
            onePageDetailsInfoList = getOnePageDetailsInfoList(pageUrl,index)
            for i, item in enumerate(onePageDetailsInfoList):
                # 用描述地址去查询是否已经有下载地址
                downloadUrl = sqliteUtil.selectDownloadUrl(item.detailsUrl)
                if downloadUrl.strip() == '':
                    # 获取下载地址
                    downloadUrl = getDownloadUrl(getDownloadPageUrl(item.detailsUrl))
                onePageDownloadInfoList.append(PptUrlInfo(item.typeStr,item.name,item.detailsUrl,downloadUrl))
                progressBar(('第%s页获取下载地址'% (index+1)),len(onePageDetailsInfoList), ( i+1 ))
            sqliteUtil.insert_url_info(onePageDownloadInfoList)

        # os.system('cls')
        
        print()

    downloadInfoLis = sqliteUtil.select_url_info_all()
    print('总共发现%s个模板' % len(downloadInfoLis))

    # 初始化下载
    baseDowloadDir = getBaseSaveDir()
    for index ,item in enumerate(downloadInfoLis):
        saveDir = jointPath(baseDowloadDir,item.typeStr)
        makedirs(saveDir)
        downloadFile(index+1, saveDir,item.name,item.downloadUrl)
        print()






    
    

