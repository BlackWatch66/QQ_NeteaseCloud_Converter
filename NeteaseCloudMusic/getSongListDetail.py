import requests
import time

def getSongListDetail(listId,cookie,url,tryTimes=0) :
    if tryTimes > 3 :
        return {"code" : 404}
    params = {
        "id": listId,
        "cookie" : cookie
    }
    try:
        res = requests.get(url+"/playlist/track/all",params=params).json()
        if res["code"] != 200:
            time.sleep(2)
            print("获取歌单失败，已重试" + str(tryTimes) + "次")
            getSongListDetail(listId,cookie,url,tryTimes+1)
        return res
    except:
        time.sleep(2)
        print("获取歌单失败，已重试" + str(tryTimes) + "次")
        getSongListDetail(listId, cookie, url, tryTimes + 1)
