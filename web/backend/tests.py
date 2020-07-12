'''
@Description: 测试和杂项
@Author: zyh
@Date: 2020-07-09 10:34:27
@LastEditTime: 2020-07-12 14:15:58
@LastEditors: zyh
@FilePath: /web/backend/tests.py
'''
import re
import requests
# import random
import time
# from requests.adapters import HTTPAdapter

headers_1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'br, gzip, deflate',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
}


if __name__ == '__main__':
    start = time.time()
    search = 'rm'
    html = requests.get(
        f'https://search.bilibili.com/all?keyword={search}&from_source=nav_suggest_new', headers=headers_1)
    html = html.text
    pattern = re.compile('href=".*?"')
    print(html)
    print(time.time() - start)
