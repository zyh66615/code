import requests
import time


def task(self, name: str, age: int):
    t = 0
    for _ in range(10**7):
        t += 1
    print(t)


if __name__ == '__main__':
    start = time.time()
    print("程序启动！")
    print("运行时间：", time.time()-start)
