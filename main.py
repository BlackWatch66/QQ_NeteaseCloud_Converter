from common import *
import NeteaseCloudMusic
import QQDownload
import json
import re
import os
from ThirdParyDownload import BiliDownload

def set_qq_cookie():
    cookie = input("请输入访问https://y.qq.com并获取cookie粘贴在输入中(\"pass\" to use default)：")
    if cookie == "pass": return
    if len(cookie) > 10:
        config['qq_cookie'] = cookie
        return
    print('请输入正确的cookie')
    set_qq_cookie()


def set_qq_songlist_id():
    qqSongList = QQDownload.getUserPlayList(url=config["qq_url"], uid=config["qq_number"], cookie=config["qq_cookie"])
    for i in range(0, len(qqSongList) - 1):
        print("No." + str(i) + "  name: " + qqSongList[i]["title"] + "    " + "id: " + str(qqSongList[i]["dissid"]))
    songlistId = int(input("请输入你想要更新的歌单序号或歌单ID："))
    songlistId = songlistId if (songlistId > 1000) else qqSongList[songlistId]["dissid"]
    print("请手动导入歌单进入网易云音乐并删除不正确的歌曲")
    print(songlistId)
    return songlistId


# CLI获取用户账号密码
def setNeteaseLogin():
    phone = input("请输入网易云的手机号(\"pass\" to use default in config.json):")
    if phone != "pass" and (not re.match(r"^1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}$", phone)):
        print("手机号不正确")
        setNeteaseLogin()
    password = input("请输入网易云的密码:")

    # 只要phone和password不为空就设置config
    if phone != "pass":
        config["netease_phone"] = phone
        config["netease_password"] = password

    loginRes = NeteaseCloudMusic.login(phone=config["netease_phone"], password=config["netease_password"],
                                       url=config["netease_url"])
    if loginRes["code"] != 200:
        print("登录失败,请重试")
        setNeteaseLogin()
    # 登录成功,返回cookie
    print("登录成功，欢迎" + loginRes["profile"]["nickname"])
    return {
        "cookie": loginRes["cookie"],
        "uid": loginRes["account"]["id"],
    }


def getNeteaseSongListId():
    songList = NeteaseCloudMusic.getUserSongLists(config["netease_uid"], cookie=config["netease_cookie"],
                                                  url=config["netease_url"])
    if songList["code"] != 200:
        raise RuntimeError("歌单获取失败")
    num = 0
    for playlist in songList["playlist"]:
        print("No." + str(num) + "  name: " + playlist["name"] + "    " + "id: " + str(playlist["id"]))
        num -= - 1
    songlistId = int(input("请输入你想要更新的歌单序号或歌单ID："))
    songlistId = songlistId if (songlistId > 1000) else songList["playlist"][songlistId]["id"]
    return songlistId


def getNeteaseSonglistDetail(songlistId):
    songlistDetail = NeteaseCloudMusic.getSongListDetail(songlistId, cookie=config["netease_cookie"],
                                                         url=config["netease_url"])
    if songlistDetail["code"] == 404:
        raise RuntimeError("歌单获取失败")
    return songlistDetail["songs"]


def checkMissSongs(qqList, neteaseList):
    for song in neteaseList:
        if qqList.__contains__(song["name"]):
            qqList.pop(song["name"])
    return qqList


def uploadSongs(downloadUrls, neteaseSonglistId):
    for data in downloadUrls["urls"]:
        fileName = QQDownload.download(data)
        uploadedSong = NeteaseCloudMusic.upload(filePath=fileName, cookie=config["netease_cookie"],
                                                url=config["netease_url"])
        NeteaseCloudMusic.addSongToSonglist(songId=uploadedSong["privateCloud"]["songId"], songlistId=neteaseSonglistId,
                                            cookie=config["netease_cookie"], url=config["netease_url"],
                                            fileName=fileName)
        os.remove(fileName)



def netease_qq_converter():
    set_qq_cookie()
    print("------------------------------------------------")
    QQsonglistId = set_qq_songlist_id()
    qqSongList = convertQQToDic(
        QQDownload.getSongListDetail(url=config["qq_url"], songlistId=QQsonglistId, cookies=config["qq_cookie"]))
    print("------------开始获取网易歌单--------------")
    # 网易登录
    neteaseLogin = setNeteaseLogin()
    config["netease_cookie"],config["netease_uid"] = neteaseLogin["cookie"],neteaseLogin["uid"]
    # 获取网易歌单歌曲
    neteaseSonglistId = getNeteaseSongListId()
    neteaseSongList = getNeteaseSonglistDetail(neteaseSonglistId)
    # 对比网易和qq歌单区别
    missSongs = checkMissSongs(qqSongList, neteaseSongList)
    # 获取歌曲下载url
    songUrl = QQDownload.getDownloadUrl(qqApiUrl=config["qq_url"], songDic=missSongs, cookie=config["qq_cookie"])
    # 上传歌曲
    uploadSongs(songUrl, neteaseSonglistId)


def bilibili_upload():
    vid = input("请输入你想要下载的视频的bv号或者av号:")
    setNeteaseLogin()
    cids = BiliDownload.getCID(vid)
    for cid in cids.keys():
        try:
            if cid == "bvid" or cid =="aid":
                continue
            BiliDownload.videoDownload(
                BiliDownload.getDownloadLink(cids["bvid"],cid),
                cid
            )
            rstr = r"[\/\\\:\*\?\"\<\>\|\ ]"  # '/ \ : * ? " < > |'
            filteredName = re.sub(rstr, "_", cids[cid])  # 替换为下划线
            fileName = input(
                "请输入你想要保存到网易云的音乐名称\n"+
                "(\"pass\"或回车使用 "+ filteredName  +" 作为文件名):"
            )
            if fileName == "" or fileName == "pass":
                fileName = filteredName
            filePath = BiliDownload.convertFormate(cid+".flv","./" +fileName)
            print('---------------现在开始上传到网盘----------------')
            NeteaseCloudMusic.upload(filePath=filePath, cookie=config["netease_cookie"],url=config["netease_url"])
            print('-----------------------现在开始绑定歌词---------------------------')
            NeteaseCloudMusic.uploadCorrection(cookie=config["netease_cookie"],url=config["netease_url"],uid=config["netease_uid"])
            print("绑定成功,删除文件")
            os.remove(cid+".flv")
            os.remove(fileName +".mp3")

        except:
            pass

def main ():
    module = input("请选择你要做的操作序号 ：\n 1. QQ音乐转网易云 \n2. bilibili 下载歌曲上传网易云 \n")
    if module == "1":
        netease_qq_converter()
    elif module == "2":
        bilibili_upload()
    else:
        print("请选择正确的序号")
        main()

if __name__ == '__main__':
    with open("config.json", 'r', encoding='UTF-8') as f:
        config = json.load(f)
    try:
        main()
    finally:
        saveAsJson(config, './config.json')


# if __name__ == '__main__':
#     with open("my_config.json", 'r', encoding='UTF-8') as f:
#         config = json.load(f)
#     try:
#         main()
#     finally:
#         saveAsJson(config, './my_config.json')

