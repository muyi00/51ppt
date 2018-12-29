import requests
from bs4 import BeautifulSoup
import utils


def get_ppt_51_page_list():
    """ 获取所有ppt 页面地址集合 """
    ppt_51_url_list = ['http://www.51pptmoban.com/ppt/']
    r= requests.get(utils.get_51_ppt_url('ppt'))
    r.encoding='GBK'
    soup = BeautifulSoup(r.text,"lxml")
    pages = soup.find(name='div',attrs={"class":"pages"})
    if pages:
        for page in pages.find_all("a"):
            if page.get('href'):
                if '尾页' in page.string:
                    pages_int = int(utils.get_string_to_int(page.get("href"))) 
                    for index in range(2,pages_int+1):
                        # http://www.51pptmoban.com/ppt/index_2.html
                        ppt_51_url_list.append(utils.get_51_ppt_url('ppt/index_%s.html' % index ))
                        # break
    return ppt_51_url_list               

def get_one_page_ppt_url_name_dict(urlStr):
    """ 获取一个页面的ppt下载地址和名称字典 """
    url_name_dict = {}
    r= requests.get(urlStr)
    r.encoding='GBK'
    soup = BeautifulSoup(r.text,"lxml")
    a_tag_list=soup.find_all("a")
    for a_tag in a_tag_list:
        img = a_tag.find('img')
        if img:
            url_path = a_tag.get("href")
            if url_path.count('/')==2:
                url_name_dict[utils.get_51_ppt_url(url_path)] = utils.get_chinese(img.get("alt"))
    return url_name_dict

def get_download_page_path_url(urlStr):
    """ 获取下载页面路径 """
    r= requests.get(urlStr)
    r.encoding='GBK'
    soup = BeautifulSoup(r.text,"lxml")
    div = soup.find(name='div',attrs={"class":"ppt_xz"})
    a_tag = div.find("a")
    return a_tag.get('href')

def get_download_url(url_path):
    """ 获取下载路径 """
    path_list=url_path.lstrip('/').split('/')
    r= requests.get(utils.get_51_ppt_url(url_path))
    r.encoding='GBK'
    soup = BeautifulSoup(r.text,"lxml")
    div = soup.find(name='div',attrs={"class":"down"})
    a_tag = div.find("a")
    path = a_tag.get('href').lstrip('../')
    # print(path)
    return utils.get_51_ppt_url('%s/%s/%s' % (path_list[0],path_list[1],path))