import re
import requests
import datetime
import numpy as np

headers_1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'br, gzip, deflate',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
}
headers_2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'br, gzip, deflate',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Referer': 'https://www.mzitu.com',
    'authority': 'www.mzitu.com'
}


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

# def crawl_images(url):
#     headers_3 = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Accept-Encoding': 'br, gzip, deflate',
#     'Accept-Language': 'zh-cn',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
#     'authority': 'i3.mmzztt.com',
#     'Referer': url
# }
#     res = requests.get(
#         url, headers=headers_3)
#     with open('./media/images/爬取/' + .jpg', 'wb') as f:
#         f.write(res.content)


if __name__ == '__main__':
    print(day)
    html = requests.get('https://www.mzitu.com/', headers=headers_1)
    html.encoding = html.apparent_encoding
    content = html.text.replace('\n', '')
    pattern_1 = re.compile('<ul id="pins">.*</ul>')
    cont = pattern_1.findall(content)[0]
    pattern_2 = re.compile('<li>.*?</li>')
    res_1 = pattern_2.findall(cont)
    for i in res_1:   
    # urls = []
    # res_urls = []
    # for i in res_1:
    #     urls.append(re.search('href=".*?"', i).group()[6:-1])
    # for url in urls:
    #     res_urls.append(crawl_urls(url))

    # res_urls = np.array(res_urls, dtype=object)
    # np.save('urls.npy', res_urls)
    # a = np.load('urls.npy', allow_pickle=True)
    # a = a.tolist()
    # print(a)
    # res = requests.get(
    #     'https://i3.mmzztt.com/2020/07/08a02.jpg', headers=headers_3)
    # with open('./media/images/爬取/.jpg', 'wb') as f:
    #     f.write(res.content)
