import requests

def getBest(url,names,cookie):
    types = ["flac", "ape", "320", "128"]
    headers = {
        'cookie': cookie
    }
    for type in types:
        # try:
        params = {
            "id":names["songId"],
            "mediaId" : names["strMediaId"],
            "type" : type,
            "ownCookie" : 1
        }
        req = requests.get(url=url+"/song/url",params=params,headers=headers)
        req = req.json()
        if req['result'] == 100:
            return ({
                "flag": "urls",
                "data": {
                    "name": names["name"],
                    "singer": names["singer"],
                    "url": req["data"],
                    "type": (".mp3" if type[0].isdigit() else ("." + type))
                }
            })
        # except:
        #     pass
    return ({
        "flag": "fail",
        "data": names
    })


def getDownloadUrl(qqApiUrl, songDic, cookie):
    downloadUrls = {"urls": [], "fail": []}
    for i in songDic.values():
        name = i["songname"]
        songId = i["songmid"] if "songmid" in i else ''
        singer = i["singer"][0]["name"] if "singer" in i else ''
        strMediaId = i["strMediaMid"] if "strMediaMid" in i else ''
        url = getBest(url=qqApiUrl, names={"name": name, "songId": songId, "singer": singer, "strMediaId": strMediaId}, cookie=cookie)
        downloadUrls[url["flag"]].append(url["data"])
    return downloadUrls


