import requests
import subprocess
import moviepy.editor as mp

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cookie": "",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.30 Safari/537.36 Edg/84.0.522.11",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": '1'
}


def getCID(id, tryTimes=0):
    url = "https://api.bilibili.com/x/web-interface/view"
    params = {}
    if id[0] == "B":
        params["bvid"] = id
        res = requests.get(
            url=url,
            params=params
        )
        print(res.status_code)
        res = res.json()
    else:
        params["aid"] = id
        res = requests.get(
            url=url,
            params=params
        ).json()
    if res["code"] != 0:
        print("获取失败，重试" + str(tryTimes) + "次")
        getCID(id, tryTimes + 1)
    # 获取成功询问用户选取那些
    index = 0
    params["bvid"] = res["data"]["bvid"]
    if len(res["data"]["pages"]) == 1:
        params[str(res["data"]["pages"][0]["cid"])] = res["data"]["title"]
        print(
            "No." + str(index) + "    CID:" + str(res["data"]["pages"][0]["cid"]) + "    Name:" + res["data"]["title"])
        return params
    for p in res["data"]["pages"]:
        print("No." + str(index) + "    CID:" +
              str(p["cid"]) + "    Name:" + p["part"])
        index += 1
    choose = input("请输入你要下载的编号，用\",\"隔开: ")
    choose = choose.split(",")
    for i in choose:
        params[str(res["data"]["pages"][int(i)]["cid"])
               ] = res["data"]["pages"][int(i)]["part"]
    return params


def getDownloadLink(bvid, cid, cookie):
    headers["cookie"] = cookie
    url = "https://api.bilibili.com/x/player/playurl"
    params = {
        "bvid": bvid,
        "cid": cid,
        "qn": "112"
    }
    req = requests.get(url=url, params=params, headers=headers)
    res = req.json()
    print(res["data"]["durl"][0]["url"])
    return res["data"]["durl"][0]["url"]


# 通过ffmpeg把本地flv文件转换成为mp3
def convertFormate(flvFilePath, fileName):
    video = mp.VideoFileClip(flvFilePath)
    video.audio.write_audiofile(fileName + ".mp3")
    print("转换完成，输出文件：", fileName + ".mp3")


def videoDownload(downloadUrl, fileName):
    headers = {
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.30 Safari/537.36 Edg/84.0.522.11"
    }

    response = requests.get(downloadUrl, headers=headers,
                            stream=True, verify=False)

    if response.status_code == 200:
        with open(f"{fileName}.flv", "wb") as video_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    video_file.write(chunk)
        print(f"{fileName}.flv 已下载")
    else:
        print("下载失败")
