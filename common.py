import hashlib
import json


def saveAsJson(jsonVar,jsonName):
    json_str = json.dumps(jsonVar, indent=4, ensure_ascii=False)
    with open(jsonName, 'w') as json_file:
        json_file.write(json_str)

def md5(s):
    new_md5 = hashlib.md5()
    new_md5.update(s.encode(encoding='utf-8'))
    return new_md5.hexdigest()

def readJson(jsonFileName):
    with open(jsonFileName, 'r', encoding='UTF-8') as f:
        return  json.load(f)

def convertQQToDic (songlist):
    songlist = songlist["data"]["songlist"]
    converted = {}
    for song in songlist:
        converted[song["songname"]] = song
    return converted

