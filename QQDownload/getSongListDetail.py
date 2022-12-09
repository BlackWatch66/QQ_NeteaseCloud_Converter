import requests

def getSongListDetail (url,songlistId,cookies):
    url = url + "/songlist"
    headers = {
        "cookie" : cookies
    }
    res = requests.get(url=url, params={'id': songlistId, "ownCookie": 1}, headers=headers)
    return res.json()