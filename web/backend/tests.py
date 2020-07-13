'''
@Description: 测试和杂项
@Author: zyh
@Date: 2020-07-09 10:34:27
@LastEditTime: 2020-07-13 13:42:34
@LastEditors: zyh
@FilePath: /web/backend/tests.py
'''
import re
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import time
import base64
import json
import rsa
import binascii
# from requests.adapters import HTTPAdapter


def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "miniblog",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "413",
        "returntype": "TEXT",
    }
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
    session = requests.Session()
    res = session.post(loginURL, data=postData)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print("登录成功")
        # 把cookies添加到headers中，必须写这一步，否则后面调用API失败
        cookies = session.cookies.get_dict()
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        print(cookies)
        session.headers["cookie"] = cookies
    else:
        print("登录失败，原因： %s" % info["reason"])
    return session


def get_cookie(username, password):
    # if os.path.exists('./cookie.npy'):
    #     cookie = np.load('./cookie.npy', allow_pickle=True)
    #     return cookie
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "miniblog",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "413",
        "returntype": "TEXT",
    }
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
    session = requests.Session()
    res = session.post(loginURL, data=postData)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print("登录成功")
        cookies = session.cookies.get_dict()
        print(cookies)
        print('获取cookies成功')
        np.save('./cookie.npy', cookies)
    else:
        print("登录失败，原因： %s" % info["reason"])
    return cookies




if __name__ == '__main__':
    start = time.time()
    
    # print(response.status_code)
    # driver = webdriver.PhantomJS(
    #     './phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    # cookie = get_cookie(username, password)
    # print(cookie)
    # input()
    # driver.add_cookie(cookie)
    # try:
    #     driver.get('https://weibo.com/p/aj/general/button?ajwvr=6&api=http://i.huati.weibo.com/aj/super/checkin&texta=%E7%AD%BE%E5%88%B0&textb=%E5%B7%B2%E7%AD%BE%E5%88%B0&status=0&id=1008082c2fa1b7274dc344e5a228ba0983f864&location=page_100808_super_index&timezone=GMT+0800&lang=zh-cn&plat=Win32&ua=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/83.0.4103.116%20Safari/537.36%20Edg/83.0.478.61&screen=2048*1152&__rnd=1594570087878')
    #     time.sleep(5)
    #     print(driver.page_source)

    # except Exception as e:
    #     print(e)
    # finally:
    #     driver.quit()
    print(time.time() - start)
