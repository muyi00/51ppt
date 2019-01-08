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

def getOnePageDownloadInfoList(pageUrl,pageIndex):
    '''获取一个页面的下载信息'''
    onePageDownloadInfoList = []
    r= requests.get(pageUrl)
    r.encoding='GBK'
    soup = BeautifulSoup(r.text,"lxml")
    a_tag_list=soup.find_all("a")
    tempList=[]
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
                tempList.append(PptUrlInfo(typeStr,name,detailsUrl))
    #循环获取下载地址   
    for i, item in enumerate(tempList):
        # 获取下载地址
        downloadUrl = getDownloadUrl(getDownloadPageUrl(item.detailsUrl))
        onePageDownloadInfoList.append(PptUrlInfo(item.typeStr,item.name,item.detailsUrl,downloadUrl))
        progressBar(('第%s页正在获取下载地址'% (pageIndex+1)),len(tempList), ( i+1 ))
        
    return onePageDownloadInfoList


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



if __name__ == '__main__':

    sqliteUtil = SqliteUtil()

    for index, pageUrl in enumerate(get_ppt_51_page_list()):
        onePageDownloadInfoLis = getOnePageDownloadInfoList(pageUrl,index)
        sqliteUtil.insert_url_info(onePageDownloadInfoLis)

    print()

    # os.system('cls')
    downloadInfoLis = sqliteUtil.select_url_info_all()
    print('总共发现%s个ppt模板' % len(downloadInfoLis))




    
    

