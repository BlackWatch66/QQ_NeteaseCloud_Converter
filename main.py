from common import *
import NeteaseCloudMusic
import QQDownload
import json
import re
import os
from ThirdParyDownload import BiliDownload
import moviepy.editor as mp

music_dir_name = "MusicDownloaded"

def set_qq_cookie():
    cookie = input(
        "请输入访问https://y.qq.com并获取cookie粘贴在输入中(\"pass\" to use default)：")
    if cookie == "pass":
        return
    if len(cookie) > 10:
        config['qq_cookie'] = cookie
        return
    print('请输入正确的cookie')
    set_qq_cookie()


def set_qq_songlist_id():
    qqSongList = QQDownload.getUserPlayList(
        url=config["qq_url"], uid=config["qq_number"], cookie=config["qq_cookie"])
    for i in range(0, len(qqSongList) - 1):
        print("No." + str(i) + "  name: " +
              qqSongList[i]["title"] + "    " + "id: " + str(qqSongList[i]["dissid"]))
    songlistId = int(input("请输入你想要更新的歌单序号或歌单ID："))
    songlistId = songlistId if (
        songlistId > 1000) else qqSongList[songlistId]["dissid"]
    print("请手动导入歌单进入网易云音乐并删除不正确的歌曲")
    print(songlistId)
    return songlistId


# CLI获取用户账号密码
def setNeteaseLogin():
    phone = input("请输入网易云的手机号(\"pass\" to use default in config.json):")
    if phone == "pass1":
        return
    if phone != "pass":
        if (not re.match(r"^1(3[0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|8[0-9]|9[89])\d{8}$", phone)):
            print("手机号不正确")
            setNeteaseLogin()
        # 只要phone和password不为空就设置config
        config["netease_phone"] = phone

    loginRes = NeteaseCloudMusic.login(phone=config["netease_phone"], password=config["netease_password"],
                                       url=config["netease_url"])
    if loginRes["code"] != 200:
        print("登录失败,请重试")
        setNeteaseLogin()
    # 登录成功,返回cookie
    print("登录成功，欢迎" + loginRes["profile"]["nickname"])
    config["netease_cookie"], config["netease_uid"] = loginRes["cookie"], loginRes["account"]["id"]


def getNeteaseSongListId():
    songList = NeteaseCloudMusic.getUserSongLists(config["netease_uid"], cookie=config["netease_cookie"],
                                                  url=config["netease_url"])
    if songList["code"] != 200:
        raise RuntimeError("歌单获取失败")
    num = 0
    for playlist in songList["playlist"]:
        print("No." + str(num) + "  name: " +
              playlist["name"] + "    " + "id: " + str(playlist["id"]))
        num -= - 1
    songlistId = int(input("请输入你想要更新的歌单序号或歌单ID："))
    songlistId = songlistId if (
        songlistId > 1000) else songList["playlist"][songlistId]["id"]
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
    setNeteaseLogin()    # 获取网易歌单歌曲
    neteaseSonglistId = getNeteaseSongListId()
    neteaseSongList = getNeteaseSonglistDetail(neteaseSonglistId)
    # 对比网易和qq歌单区别
    missSongs = checkMissSongs(qqSongList, neteaseSongList)
    # 获取歌曲下载url
    songUrl = QQDownload.getDownloadUrl(
        qqApiUrl=config["qq_url"], songDic=missSongs, cookie=config["qq_cookie"])
    # 上传歌曲
    uploadSongs(songUrl, neteaseSonglistId)


def bilibili_upload(isUpload: bool):
    vid = input("请输入你想要下载的视频的bv号或者av号:")
    cids = BiliDownload.getCID(vid)
    for cid in cids.keys():
        try:
            if cid == "bvid" or cid == "aid":
                continue
            downloadUrl = BiliDownload.getDownloadLink(cids["bvid"], cid, cookie=config["bili_cookie"])
            BiliDownload.videoDownload(downloadUrl=downloadUrl,fileName=music_dir_name + "/" + cid)
            rstr = r"[\/\\\:\*\?\"\<\>\|\ ]"  # '/ \ : * ? " < > |'
            filteredName = re.sub(rstr, "_", cids[cid])  # 替换为下划线
            fileName = input(
                "请输入你想要保存到网易云的音乐名称\n" +
                "(\"pass\"或回车使用 " + filteredName + " 作为文件名):"
            )
            if fileName == "" or fileName == "pass":
                fileName = filteredName
            
            if not isUpload:
                BiliDownload.convertFormate(flvFileName=cid+".flv", fileName=fileName, filePath=music_dir_name + "/")
                # os.remove(music_dir_name + "/" +cid+".flv")
                choice = input("是否继续下载？(y/N)")
                if choice == "y":
                    bilibili_upload(isUpload)
                return
            BiliDownload.convertFormate(flvFileName=cid+".flv", fileName=fileName, filePath=music_dir_name + "/")
            setNeteaseLogin()
            print('---------------现在开始上传到网盘----------------')
            NeteaseCloudMusic.upload(
                filePath=music_dir_name + "/" + fileName, cookie=config["netease_cookie"], url=config["netease_url"])
            print("上传成功,删除文件")
            os.remove(cid+".flv")
            os.remove(fileName + ".mp3")
        except:
            pass


def downloadFromQQ():
    set_qq_cookie()
    print("------------------------------------------------")
    url_data = QQDownload.searchForDownload(
        url=config["qq_url"], cookie=config["qq_cookie"])
    fileName = QQDownload.download(url_data)
    print("下载完成，开始上传")
    setNeteaseLogin()
    NeteaseCloudMusic.upload(
        filePath=fileName, cookie=config["netease_cookie"], url=config["netease_url"])
    print("上传完成，删除文件")
    os.remove(fileName)


def main():
    module = input("\
        请选择你要做的操作序号 ：\n\
        1. QQ音乐转网易云\n\
        2. bilibili 下载歌曲上传网易云\n\
        3. QQ音乐下载上传网易云\n\
        4. 绑定网易云盘歌单的歌词\n\
        5. bilibili直接下载歌曲\n\
    ")
    try:
        if module == "1":
            netease_qq_converter()
        elif module == "2":
            bilibili_upload(isUpload=True)
        elif module == "3":
            downloadFromQQ()
        elif module == "4":
            NeteaseCloudMusic.uploadCorrection(
                cookie=config["netease_cookie"], url=config["netease_url"], uid=config["netease_uid"])
        elif module == "5":
            bilibili_upload(isUpload=False)
        else:
            print("请选择正确的序号")
            main()
    except:
        print("出现错误,请检查配置文件并重试")
    finally:
        isExit = input("输入exit退出，回车继续")
        if isExit == "exit":
            return
        main()


if __name__ == '__main__':
    config = json.load(open("./my_config.json", 'r', encoding='UTF-8'))
    if not os.path.exists(music_dir_name): os.mkdir(music_dir_name)
    # config = json.load(open("config.json", 'r', encoding='UTF-8'))
    main()
