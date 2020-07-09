import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0'}


def task(url: str, res: list) -> list:
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    res.append(r.text)
    return res


if __name__ == '__main__':
    start = time.time()
    print("程序启动！")
    result = []
    result = task('https://www.baidu.com', result)
    print(result)
    print("运行时间：", time.time()-start)
