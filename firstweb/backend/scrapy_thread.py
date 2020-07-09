import time
import requests
import random
from requests.exceptions import HTTPError, ConnectionError
from queue import Queue
from threading import Thread
import re
from aiohttp import ClientSession
import asyncio
import os
from lxml import etree
import math


class Downloader(object):

    def __init__(self, title):
        self.url = ''
        self.title = title
        self.results = {}
        self.timeout = random.choice(range(30, 60))
        self.intro = ''
        self.flag = True
        self.i = 0
        self.search()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'br, gzip, deflate',
            'Accept-Language': 'zh-cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
        }

    def get_title(self):
        return self.title

    async def save_text(self, url):  # 消费者
        try:
            async with ClientSession() as session:
                start = time.time()
                async with session.get([u for u in url.values()][0], headers=self.headers) as response:
                    text = await response.text()
                    num = [u for u in url.keys()][0]
                    html = text.replace('\r', '').replace('\n', '').replace('\u3000', ' ').replace('\t', '')
                    pattern = re.compile('<div id="content">.*')
                    pattern1 = re.compile('<div class="bookname">.*</h1>')
                    title = pattern1.search(html)
                    if title:
                        title = title.group()[26:-5]
                        s = pattern.search(html).group().replace('<br/><br/>', ' ')
                        p = re.compile('</script>.*?<script>')
                        texts = p.search(s).group()[9:-8]
                        result = title + '\n' + texts
                        self.results[num] = result
                    else:
                        self.i = 1
                        return
                    print(time.time() - start)

        except HTTPError as e:
            print(str(e))
        except ConnectionError as e:
            print(str(e))
        except asyncio.CancelledError:
            print('Cancel the future.')
        except Exception as e:
            print(e)

    def write_novel(self, text, title):
        start = time.time()
        print(os.getcwd())
        if os.path.exists('./media/books/完整/' + title + '/' + self.title + '.txt'):
            print('已有完整书，不重写')
            return
        with open('./media/books/简介/' + title + '.txt', 'w', encoding='utf-8') as f:
            f.write(self.intro)
        f.close()
        if self.i == 1:
            if not os.path.exists('./media/books/不完整/' + title):
                os.mkdir('./media/books/不完整/' + title)
            with open('./media/books/不完整/' + title + '/' + self.title + '.txt', 'w', encoding='utf-8') as f:
                for t in sorted(text.keys()):
                    f.writelines(text[t])
                    f.write('\n')
            f.close()
        else:
            if not os.path.exists('./media/books/完整/' + title):
                os.mkdir('./media/books/完整/' + title)
            with open('./media/books/完整/' + title + '/' + self.title + '.txt', 'w', encoding='utf-8') as f:
                for t in sorted(text.keys()):
                    f.writelines(text[t])
                    f.write('\n')
            f.close()
        print('写文件耗时：%s' % (time.time() - start))

    def get_texts(self, q):
        start = time.time()
        req = requests.get(self.url, headers=self.headers)
        print('requests的get时间')
        html = etree.HTML(req.content.decode('utf-8'))
        results = html.xpath('//div[@id="list"]//a/@href')[12:]
        print('解析时间')
        print(time.time() - start)
        count = 1
        for r in results:
            q.append({count: 'https://www.biqudu.net' + r})
            count += 1
        print('获取urls的时间')
        print(time.time() - start)

    def get_results(self):
        return self.results

    def search(self):
        print('开始访问')
        start = time.time()
        html = requests.get('https://www.biqudu.net/searchbook.php?keyword=' + self.title)
        html = html.text.replace('\r', '').replace('\n', '').replace(' ', '')
        pattern = re.compile('<divclass="item"><divclass="image"><ahref=".*?"><img.*?>')
        s = pattern.search(html)
        if s:
            s = s.group()
            p = re.compile('<ahref=".*?">')
            pp = re.compile('"alt=".*?"')
            pt = re.compile('<divclass="item"><divclass="image"><ahref=".*?">.*?</dl>')
            k = pt.search(html).group()
            pt1 = re.compile('<dd>.*</dd>')
            results = pt1.search(k).group()[4:-5].replace('&nbsp;', ' ')
            self.url = 'https://www.biqudu.net' + p.search(s).group()[8:-2]
            self.title = pp.search(s).group()[6:-1]
            self.flag = True
            self.intro = results
            print('访问完成')
        else:
            self.flag = False
            print('未找到此书')
        print('搜索小说时间')
        print(time.time() - start)

    def get_flag(self):
        return self.flag


async def task(url, s):
    await s.save_text(url)


async def main():
    book_name = '韩娱'
    s = Downloader(book_name)
    urls = []
    tasks = []
    if s.get_flag():
        s.get_texts(urls)
        if len(urls) == 0:
            print('该书爬取链接为空')
            return
        print(s.get_title())
        num = len(urls)
        print('url数量', num)
        # n = math.ceil(len(urls) / 500)
        # for i in range(n):
        #     url = urls[math.floor(i / n * num):math.floor((i + 1) / n * num)]
        [tasks.append(task(url, s)) for url in urls]
        await asyncio.wait(tasks)
        print('程序结束')
        print('总耗时：%s' % (time.time() - start))
    else:
        print('程序结束')
        print('总耗时：%s' % (time.time() - start))


if __name__ == '__main__':
    start = time.time()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept-Language': 'zh-cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    }
    html = requests.get('https://www.biqudu.net/searchbook.php?keyword=韩娱',headers=headers)
    print(time.time()-start)
    input()
    asyncio.run(main())
    print('程序结束')
    print('总耗时：%s' % (time.time() - start))
