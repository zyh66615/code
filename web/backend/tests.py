'''
@Description: 测试和杂项
@Author: zyh
@Date: 2020-07-09 10:34:27
@LastEditTime: 2020-07-12 21:35:51
@LastEditors: zyh
@FilePath: /web/backend/tests.py
'''
import re
import os
import requests
# import random
import time
import base64
import json
import rsa
import binascii
# from requests.adapters import HTTPAdapter

headers_1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'br, gzip, deflate',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
}


if __name__ == '__main__':
    start = time.time()

    def get_sp(password, servertime, nonce, pubkey):
        string = (str(servertime) + "\t" + str(nonce) + "\n" + str(password)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        pw = rsa.encrypt(string, public_key)
        sp = binascii.b2a_hex(pw).decode()
        return sp
    
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
            session.headers["cookie"] = cookies
        else:
            print("登录失败，原因： %s" % info["reason"])
        return session

    session = login('13728902077', 'z123123123')
    response = session.get('https://weibo.com/p/aj/general/button?ajwvr=6&api=http://i.huati.weibo.com/aj/super/checkin')
    r = json.loads(response.content.decode('gbk'))
    print(r)
    # sp:549e635859c90f8489a70e19e35ab590bf79deef6a508e6d198ebf3d19d54b183858fc9ce1e3a58671cffff155eca20616385325f70dd2a18da57de1e1f9a1bc029488684d95f95dec78d5787eed3e03e320092c18d01b45a75fcae394ca4b39569764918b50128e5eccb3a4b4ae6c107ee1ad83cc778753b6d19663f47c15b2
    #  username: MTM3Mjg5MDIwNzc=
    # print(base64.b64encode('13728902077'.encode('utf-8')).decode('utf-8'))
    # print(get_sp('z123123123',1594553709, XRBETH,))
    print(time.time() - start)
