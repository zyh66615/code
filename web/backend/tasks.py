from celery import task
import time
from .scrapy_thread import Downloader
import math
import asyncio
import requests
import datetime
import re
# import numpy as np
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
    num = 0
    res_urls = []
    day = datetime.date.today()
    delta = datetime.timedelta(days=1)
    day = str(day - delta)
    for i in res_1:
        urls.append(re.search('href=".*?"', i).group()[6:-1])
        if re.search('time">.*?<', i).group()[6:-1] == day:
            num += 1
    if num == 0:
        print('昨天无更新')
        return
    else:
        print('昨天更新了', num, '张图片')
        for i in range(num):
            res_urls.append(crawl_urls(urls[i]))
        print('爬取图片url完成')
        for i, url in enumerate(res_urls):
            for index, u in enumerate(url):
                crawl_image(u, urls[i], day, index + 1, i)
        print('爬取图片完成')


@task
def crawl_urls(url):
    r = requests.get(url, headers=headers_2)
    r = r.text.replace('\n', '')
    pattern_3 = re.compile(url+r'/\d+')
    res_2 = pattern_3.findall(r)[-2]
    num = int(res_2.split('/')[-1])
    print('有' + str(num) + '张图片')
    pattern = re.compile('<div class="main-image">.*?</a>')
    res = pattern.findall(r)[0]
    pattern_1 = re.compile('src=".*?"')
    res_1 = pattern_1.findall(res)[0][5:-7]
    urls = [res_1 + '0' + str(i) + '.jpg' if i < 10 else res_1 + str(i) + '.jpg'
            for i in range(1, num+1)]
    return urls


@task
def crawl_image(url, referer, folders, index, folder):
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
    print(url)
    if res.status_code != 200:
        print('第'+str(folder)+'张图的第' + str(index) + '页爬取失败  ', res.status_code)
        return
    if not os.path.exists('./media/images/爬取/' + str(folders)):
        os.makedirs('./media/images/爬取/' + str(folders))
    if not os.path.exists('./media/images/爬取/' + str(folders)+'/'+str(folder)):
        os.makedirs('./media/images/爬取/' + str(folders)+'/'+str(folder))
    with open('./media/images/爬取/' + str(folders)+'/'+str(folder) + '/' + str(index) + '.jpg', 'wb') as f:
        f.write(res.content)