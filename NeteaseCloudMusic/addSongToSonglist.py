import requests

def addSongToSonglist(songId,songlistId,cookie,url,fileName,tryTimes=0):
    params = {
        "op" : "add",
        "pid" : songlistId,
        "tracks" : songId,
        "cookie" : cookie
    }
    req = requests.get(url=url+"/playlist/tracks",params=params)
    if req.status_code != 200:
        print("上传失败")
        if tryTimes < 3:
            print("重试" + str(tryTimes) + "次")
            addSongToSonglist(songId,songlistId,cookie,url,tryTimes+1)
        else:
            raise Exception("添加到歌单失败")
    print(fileName + "添加到歌单成功")