import re
import requests
import random
import time

headers_1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'br, gzip, deflate',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
}


if __name__ == '__main__':
    # html = requests.get('https://www.bilibili.com', headers=headers_1)
    # html = html.text
    # pattern = re.compile('href=".*?"')
    # print(html)
    a = round(random.uniform(1.5, 2.5), 2)
    print(a)
    time.sleep(a)
    print(2)
