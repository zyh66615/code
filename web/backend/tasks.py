from celery import task
import time
from .scrapy_thread import Downloader
import math
import asyncio
import requests
import datetime
import re
import numpy as np
import os


headers_1 = {
    'User-Agent': 'Mozilla/5.0'
}
headers_2 = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://www.mzitu.com',
    'authority': 'www.mzitu.com'
}


@task
def crawl(book_name):
    start = time.time()
    print('开始任务')
    s = Downloader(book_name)
    urls = []
    if s.get_flag():
        s.get_texts(urls)
        if len(urls) == 0:
            print('该书爬取链接为空')
            return
        num = len(urls)
        print('url数量')
        print(num)
        n = math.ceil(len(urls) / 500)
        for i in range(n):
            url = urls[math.floor(i / n * num):math.floor((i + 1) / n * num)]
            # asyncio.run(task1(500, url, s)) python3.8使用
            # python3.6使用如下方式:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(task1(500, url, s))
            finally:
                loop.close()
        s.write_novel(s.get_results(), book_name)
        print('程序结束')
        print('总耗时：%s' % (time.time() - start))
    else:
        print('程序结束')
        print('总耗时：%s' % (time.time() - start))


@task
async def task1(pool, urls, s):
    tasks = []
    sem = asyncio.Semaphore(pool)
    [tasks.append(control(sem, url, s)) for url in urls]
    await asyncio.wait(tasks)


@task
async def control(sem, url, s):
    async with sem:
        await s.save_text(url)


@task
def crawl_images():
    html = requests.get('https://www.mzitu.com/', headers=headers_1)
    html.encoding = html.apparent_encoding
    content = html.text.replace('\n', '')
    pattern_1 = re.compile('<ul id="pins">.*</ul>')
    cont = pattern_1.findall(content)[0]
    pattern_2 = re.compile('<li>.*?</li>')
    res_1 = pattern_2.findall(cont)
    urls = []
    for i in res_1:
        urls.append(re.search('href=".*?"', i).group()[6:-1])
    res_urls = crawl_urls(urls[0])
    print('爬取图片url完成')
    day = datetime.date.today()
    for index, url in enumerate(res_urls):
        crawl_image(url, urls[0], day, index)
    print('爬取图片完成')


@task
def crawl_urls(url):
    r = requests.get(url, headers=headers_2)
    r = r.text.replace('\n', '')
    pattern_3 = re.compile(url+r'/\d+')
    res_2 = pattern_3.findall(r)[-2]
    num = int(res_2.split('/')[-1])
    pattern = re.compile('<div class="main-image">.*?</a>')
    res = pattern.findall(r)[0]
    pattern_1 = re.compile('src=".*?"')
    res_1 = pattern_1.findall(res)[0][5:-7]
    urls = [res_1 + str(i) + '.jpg' for i in range(1, num+1)]
    return urls


@task
def crawl_image(url, referer, folder, index):
    headers_3 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept-Language': 'zh-cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'authority': 'i3.mmzztt.com',
        'Referer': referer
    }
    res = requests.get(
        url, headers=headers_3)
    if not os.path.exists('./media/images/爬取/' + str(folder)):
        os.makedirs('./media/images/爬取/' + str(folder))
    with open('./media/images/爬取/' + str(folder) + '/' + str(index) + '.jpg', 'wb') as f:
        f.write(res.content)
