import time
import requests
from common import *

def getSid(cookie,url):
    url = url + "/user/cloud"
    offset = input(
        "请确认你歌单中错误的歌曲的编号:"
    )
    # 如果输入的不是数字直接默认0
    try:
        offset = int(offset) -1
    except:
        offset = 0
    params = {
        "limit" : 1,
        "offset" : offset,
        "cookie" : cookie
    }
    res = requests.get(url=url,params=params).json()
    check = input(
        "你现在确认的歌曲是\"" + res["data"][0]["simpleSong"]["name"] + "\"吗？(Y/n):"
    )
    if check != "y" and check != "Y" and check != "":
        print("请重新输入")
        return getSid(cookie,url)
    return res["data"][0]["songId"]

def getAsid(cookie,url):
    # 搜索
    url = url + "/cloudsearch"
    keyword = input("请输入正确歌曲的关键字来搜索：")
    params = {
        "keywords" : keyword,
        "limit" : 10
    }
    res = requests.get(url=url,params=params).json()
    index = 0
    for song in res["result"]["songs"]:
        print("No." + str(index) + "    " + song["name"] + "    " + song["ar"][0]["name"])
        index +=1
    choose = input("请选择你想要的序号(\'enter to have default as 0\') :")
    try:
        return res["result"]["songs"][int(choose)]["id"]
    except:
        return res["result"]["songs"][0]["id"]

def uploadCorrection(cookie,uid,url,sid=0,asid=0,retryTime=1):
    if retryTime ==4 :
        raise RuntimeError("更新歌单数据失败")
    time.sleep(5)
    if sid == 0:
        sid = getSid(cookie=cookie,url=url)
        asid = getAsid(cookie=cookie,url=url)
    url = url + "/cloud/match"
    params = {
        "cookie": cookie,
        "uid" : uid, # 用户id
        "sid" : sid, # 错误的歌曲的id
        "asid" : asid, # 找到的正确的歌曲id
    }
    res = requests.get(url=url,params=params)
    if res.status_code != 200 :
        print("绑定失败，重试" + str(retryTime) + "次")
        uploadCorrection(cookie,uid,url,sid,asid,retryTime+1)
    print("绑定成功")