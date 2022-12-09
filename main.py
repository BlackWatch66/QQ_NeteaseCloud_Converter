from common import *
import NeteaseCloudMusic
import QQDownload
import json
import re
import os


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
    songList = NeteaseCloudMusic.getUserSongLists(config["neteast_uid"], cookie=config["netease_cookie"],
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


def main():
    set_qq_cookie()
    print("------------------------------------------------")
    QQsonglistId = set_qq_songlist_id()
    qqSongList = convertQQToDic(
        QQDownload.getSongListDetail(url=config["qq_url"], songlistId=QQsonglistId, cookies=config["qq_cookie"]))
    print("------------开始获取网易歌单--------------")
    # 网易登录
    # neteaseLogin = setNeteaseLogin()
    # config["netease_cookie"],config["neteast_uid"] = neteaseLogin["cookie"],neteaseLogin["uid"]
    # 获取网易歌单歌曲
    neteaseSonglistId = getNeteaseSongListId()
    neteaseSongList = getNeteaseSonglistDetail(neteaseSonglistId)
    # 对比网易和qq歌单区别
    missSongs = checkMissSongs(qqSongList, neteaseSongList)
    # 获取歌曲下载url
    songUrl = QQDownload.getDownloadUrl(qqApiUrl=config["qq_url"], songDic=missSongs, cookie=config["qq_cookie"])
    # 上传歌曲
    uploadSongs(songUrl, neteaseSonglistId)


if __name__ == '__main__':
    with open("config.json", 'r', encoding='UTF-8') as f:
        config = json.load(f)
    try:
        main()
    finally:
        saveAsJson(config, './config.json')
