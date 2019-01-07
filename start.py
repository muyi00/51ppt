import page
import download
import threading
import utils
import os
import unzip

def download_files(url_name_dict):
    for url_str ,name in url_name_dict.items():
        url_all=page.get_download_url(page.get_download_page_path_url(url_str))
        download.download_file(url_all,name)
        print()

def un_zip_files():
     file_names =  os.listdir(utils.get_download_save_dir())
     for name in file_names:
        if 'zip' in name:
           file_path = utils.joint_path(utils.get_download_save_dir(),name)
           unzip.un_zip(file_path)
        


def start_download():
    url_name_dict_all = {}
    if len(utils.read_url()) > 0:
       url_name_dict_all = utils.read_url()
    else:
        for url_str in page.get_ppt_51_page_list():
            url_name_dict = page.get_one_page_ppt_url_name_dict(url_str)
            print('[%s]中发现%s个ppt模板' % (url_str,len(url_name_dict)))

            for url_str ,name in url_name_dict.items():
                url_name_dict_all[url_str] = name

        utils.write_url(url_name_dict_all)
       

    print('总共发现%s个ppt模板' % (len(url_name_dict_all)))
    t = threading.Thread(target=download_files(url_name_dict_all), name='download_ppt_hread')
    t.start()
    t.join()
    
    #开始解压处理
    t2 = threading.Thread(target=un_zip_files(), name='download_unzip_hread')
    t2.start()

start_download()

