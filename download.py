import requests
import utils
import os
import sys



def download_file(download_url,file_name):
    """ 下载文件 """
    file_rar = utils.get_download_save_path(file_name,'rar')
    file_zip = utils.get_download_save_path(file_name,'zip')
    if os.path.isfile(file_rar) or os.path.isfile(file_zip)  : #文件是否存在
        # 已经下载成功
        sys.stdout.write("\r[%s] [##################################################] 100%%" % file_name)
        sys.stdout.flush()
        return
    #把下载地址发送给requests模块
    r = requests.get(download_url)
    total_size = 0
    try:
        header_str = r.headers['Content-Length']
        if header_str:
            total_size = int(header_str)
    except BaseException as e:
        print('BaseException:',e)
        utils.write_log(download_url,file_name,e)
        return
    temp_size = 0
    # ZIP的application/x-zip-compressed     
    # RAR的application/octet-stream  
    content_type = r.headers['Content-Type']
    suffix = 'rar'
    if 'application/x-zip-compressed' in content_type:
        suffix = 'zip'

    # 下载前判断文件是否已经下载了
    if total_size is None :
        pass
    else:
        if total_size > 0:
            if os.path.isfile(utils.get_download_save_path(file_name,suffix)): #文件是否存在
                if total_size == utils.get_fileSize(utils.get_download_save_path(file_name,suffix)):
                    # 已经下载成功
                    sys.stdout.write("\r[%s] [##################################################] 100%%" % file_name)
                    sys.stdout.flush()
                    return
   
    #下载文件
    with open(utils.get_download_save_path(file_name,suffix),"wb") as f:
        if total_size == 0 :
            f.write(r.content)
            sys.stdout.write(("\r[%s] [##################################################] 100%%" % file_name))
            sys.stdout.flush()
        else:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    #############花哨的下载进度部分###############
                    done = int(50 * temp_size / total_size)
                    # 调用标准输出刷新命令行，看到\r回车符了吧
                    # 相当于把每一行重新刷新一遍
                    sys.stdout.write("\r[%s] [%s%s] %d%%" % (file_name,'#' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                    sys.stdout.flush()