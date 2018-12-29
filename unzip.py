import zipfile
import os
import shutil
import utils
from pathlib import Path


def un_zip(file_name):
    ppt_name = ''
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(utils.get_unzip_save_dir()):
        pass
    else:
        os.mkdir(utils.get_unzip_save_dir())
    for names in zip_file.namelist():
        if 'pptx' in names[-4:]:
            ppt_name = names
        elif 'ppt' in names[-3:]:
            ppt_name = names
        else:
            pass
        zip_file.extract(names,utils.get_unzip_save_dir())
    zip_file.close()
    ppt_new_name=''
    try:
        ppt_new_name = ppt_name.encode('cp437').decode('gbk')
    except:
        ppt_new_name = ppt_name.encode('utf-8').decode('utf-8')
    
    copy_file(get_file_path(ppt_name),get_new_file_path(ppt_new_name))

def get_file_path(name):
    """ 获取ppt文件绝对路径 """
    return utils.joint_path(utils.get_unzip_save_dir(),name)

def get_new_file_path(new_name):
    """  获取复制到新位置ppt文件绝对路径 """
    return utils.joint_path(utils.get_ppt_save_dir(),new_name.split('/')[-1])


def copy_file(srcfile,dstfile):
    """ 复制文件 """
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))


# un_zip('E:\ppt\卡通扁平网络科技主题商务工作汇报模板.zip')