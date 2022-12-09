import requests
import time

def getUserSongLists(uid,cookie,url,tryTimes=0) :
    if tryTimes > 3 :
        return {"code" : 404}
    try:
        params = {
            "uid" : uid,
            "cookie" : cookie
        }
        res = requests.get(url + "/user/playlist",params=params).json()
        if res["code"] != 200:
            time.sleep(2)
            print("获取歌单失败，已重试" + str(tryTimes) + "次")
            getUserSongLists(uid,cookie,url,tryTimes+1)
        return res
    except:
        pass