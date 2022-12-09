import requests


def getUserPlayList(url, uid, cookie):
    url = url + "/user/detail"
    headers = {
        "cookie": cookie
    }
    req = requests.get(url=url, params={'id': uid, "ownCookie": 1}, headers=headers)
    req = req.json()
    print(req)
    return req['data']['mydiss']['list']
