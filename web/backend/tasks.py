from celery import task
import time
from .scrapy_thread import Downloader
import math
import asyncio


@task
def crawl(book_name):
    start = time.time()
    # if os.path.exists('./media/books/完整/' + book_name + '.txt'):
    #     print('书已存在')
    #     return
    # if os.path.exists('./media/books/不完整/' + book_name + '.txt'):
    #     os.remove('./media/books/不完整/' + book_name + '.txt')
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
