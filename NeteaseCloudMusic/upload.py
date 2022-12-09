import requests
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder

proxy = {'http': '127.0.0.1:8083', 'https': '127.0.0.1:8083'}


def upload(url, filePath, cookie, retryTime=0):
    try:
        proxy = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}
        times = str(int(round(time.time() * 1000)))
        # url1 = "http://1.116.184.91:20072/cloud?time=" + times + cookie
        url = url + "/cloud?time=" + str(int(round(time.time() * 1000))) + cookie
        headers = {
            "Accept": "*/*",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        }
        multipart_encoder = MultipartEncoder(
            fields={
                "songFile": ("1.flac", open(filePath, "rb")),
            },
            boundary='----WebKitFormBoundaryJ2aGzfsg35YqeT7X'
        )
        headers['Content-Type'] = multipart_encoder.content_type
        params = {
            "cookie": cookie
        }
        print("\n开始上传：" + filePath)
        req = requests.post(url, data=multipart_encoder, headers=headers, params=params)
        res = req.json()
        print(1)
        if req.status_code != 200:
            print(filePath + "上传失败" + str(req.status_code) + "重试" + str(retryTime) + "次")
            if retryTime < 3:
                retryTime += 1
                upload(url, filePath, cookie, retryTime)
            else:
                print(filePath + "上传失败" + req.status_code)
                raise Exception("上传失败")
        print(filePath + "上传成功！")
        return res
    except:
        pass
