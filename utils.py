import re
import os
import requests

# 保存路径
base_dir='E:/ppt'

# 51ppt模板主页面
base_page_url = 'http://www.51pptmoban.com'

def joint_path(path1,path2):
    """ 路径拼接 """
    return '%s/%s' % (path1,path2)

def get_download_save_dir():
    """ 下载保存路径 """
    path = joint_path(base_dir,'zip')
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
    return path

def get_unzip_save_dir():
    """ 解压文件缓存路径 """
    path = joint_path(base_dir,'unzip_temp')
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
    return path

def get_ppt_save_dir():
    """ ppt保存路径 """
    path = joint_path(base_dir,'ppt')
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
    return path

def get_download_save_path(name,suffix):
    return '%s/%s.%s' % (get_download_save_dir(),name,suffix)

def get_51_ppt_url(path):
    return joint_path(base_page_url,path)


def get_string_to_int(s):
   return re.findall("\d+",s)[0]


def get_chinese(s):
    pattern="[\u4e00-\u9fa5]+" 
    regex = re.compile(pattern)
    name =''
    for ss in regex.findall(s):
        name = name+ss
    return name

def get_fileSize(filePath):
    """ 获取文件大小 """
    return os.path.getsize(filePath)



def eachFile(filepath):
    """ 遍历指定目录，显示目录下的所有文件名 """
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        # child = os.path.join('%s\%s' % (filepath, allDir))
        print(allDir) # .decode('gbk')是解决中文显示乱码问题


eachFile('E:\ppt')



