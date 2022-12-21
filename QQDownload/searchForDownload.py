import requests
from common import *
import QQDownload
from QQDownload.getDownloadUrl import getBest

def search1():
    req = requests.get(
        url = "http://127.0.0.1:3300/search?key=周杰伦&raw=1",
    )
    saveAsJson()

def search():
    typeMap = {
      0: 'song',
      2: 'album',
      1: 'singer',
      3: 'songlist',
      7: 'lyric',
      12: 'mv',
    }
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    keyword = "周杰伦"
    params = {
        "req1": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "num_per_page": 20,
                "page_num": 1,
                "query": keyword,
                "search_type": 0
            }
        }
    }
    req = requests.post(
        url=url,
        headers={
          "Referer" : 'https://y.qq.com'
        },
        data=params
    )
    res= req.json()
    print(1)
    
def searchForDownload (url,cookie):
    headers = {
        "cookie" : cookie,
    }
    keword = input("请输入你想要下载的歌曲的关键字：")
    params = {
        "key" : keword,
    }
    res = requests.get(url=url+"/search/quick",params=params,headers=headers).json()
    for song in res["data"]["song"]["itemlist"]:
        print("No." + str(res["data"]["song"]["itemlist"].index(song)) + "  "+"歌曲名称：" + song["name"] + "  歌手：" + song["singer"])
    songId = int(input("请输入你想要下载的歌曲序号(\'pass\' to research)："))
    return QQDownload.getBest(url=url,names={
        "name" : res["data"]["song"]["itemlist"][songId]["name"],
        "singer" : res["data"]["song"]["itemlist"][songId]["singer"],
        "songId" : res["data"]["song"]["itemlist"][songId]["mid"],
        "strMediaId" : ""
    },cookie=cookie)["data"]
    # return {
    #     "songId" : res["data"]["song"]["itemlist"][songId]["id"],
    #     "mid" : res["data"]["song"]["itemlist"][songId]["mid"],
    # }
    