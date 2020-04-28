import  tokenGet
from datetime import date, timedelta, datetime  #分别表示日期的类、时间间隔的类、日期时间的类
import time
from urllib.parse import urlencode  #urllib.parase定义了url的标准接口，实现Url的各种抽取，包括解析、合并、编码、解码   而urlencode()则将字典构形式的参数序列化为url编码后的字符串（常用来构造get请求和post请求的参数）k1=v1&k2=v2
import xlwt         #xlrd模块实现对excel文件内容读取
import xlrd         #xlwt模块实现对excel文件的写入
import requests     #requests库
import re           #正则表达式，用来处理字符串，最常用到三个函数的是match，search，findall
from requests import RequestException   #异常化处理

def get_one_page(url, token):                                                # 获取要爬取的网页
    group = {'DA': 1, 'action': 'gethistory', 'url': url, 'bjid': '',        # url是输入进来的京东url
             'spbh': '', 'cxid': '', 'zkid': '', 'w': 951, 'token': token    # token需要手动记录，与url对应
             }
    url = "http://tool.manmanbuy.com/history.aspx?" + urlencode(group)       # 网址格式，url从京东链接变为request的网址
    try:
        kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
        res = requests.get(url, headers=kv)
        if res.status_code == 200:
            return res.text
        else:
            return None
    except RequestException:
        print('请求失败！！')
        return None

def main():
    f1 = open('computerurl.txt', 'r')
    index = 1
    while True:
        url = f1.readline()
        if url == '':  # 直到没有url
            break
        token = tokenGet.getToken('https:'+url)
        print('第' + str(index) + '件商品: ' + 'https:' + url + ' ' + token)  # 输出第几件商品 和对应的url、token
        html = get_one_page("https:" + url, token)
        print(html)
        index = index +1

if __name__ == '__main__':
    main()