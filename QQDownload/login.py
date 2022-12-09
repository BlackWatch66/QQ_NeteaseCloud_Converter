import requests
import json
from common import saveAsJson

def login (url,cookiePath="cookie.txt") :
    header = {
        "content-type" : "application/json"
    }
    # data = cookie("cookie.txt")
    data = {
        "data" : open(cookiePath).read()
    }
    req = requests.post(url=(url+"/user/setCookie"), data=json.dumps(data),headers= header) #, proxies={"http": "http://127.0.0.1:8080", "https": "https://127.0.0.1:8080"})
    print(req)

def getSongListDetail (url,songlistId,jsonFileName="qq_list.json"):
    url = url + "/songlist"
    headers = {
        "cookie" : cookies
    }
    res = requests.get(url=url, params={'id': songlistId, "ownCookie": 1}, headers=headers)
    saveAsJson(res.json(),"liuhua_list.json")

def getUserPlayList(url,uid,cookies):
    url = url + "/user/detail"
    headers = {
        "cookie" : cookies
    }
    req = requests.get(url=url,params={'id':uid, "ownCookie" :1},headers=headers)
    req = req.json()
    print(req)
    return req['data']['mydiss']['list']

def main ():

    # login(url,"cookie.txt")
    getUserPlayList(url,id)
    a = getUserPlayList(url,id,cookies)
    saveAsJson(a,"qqSongList.json")

if __name__ == '__main__':
    url = "http://1.116.184.91:20071"
    id = "1262230547"
    # cookies = "pgv_pvid=5355624080; fqm_pvqid=2e0fee3d-6e8a-4d77-91dc-096c9f7f44e2; ts_refer=www.google.com/; ts_uid=1294948896; RK=knk0g1MkEj; ptcz=fa23bf951ee3985c7a7cf4c6c32e6a591785867c132e505f97172a048347fb77; euin=oK-sow-ioe4P7z**; tmeLoginType=2; psrf_access_token_expiresAt=1677745453; fqm_sessionid=4a7bf918-3bc4-49be-971a-fc16577348fa; pgv_info=ssid=s6319446780; ts_last=y.qq.com/; login_type=1; psrf_qqaccess_token=D1AB5F48C7154131A3BD3E7BCCF9B8CE; wxunionid=; wxrefresh_token=; wxopenid=; psrf_qqunionid=2852712DA2695EF53D9CBA9F3E6F4F7B; qm_keyst=Q_H_L_5RVI1t8gunvPSQEQIyFL5xms2wZpZy7lQ4Tk9OydA1bV_FfmVmz7Aug; psrf_musickey_createtime=1669969454; uin=1262230547; psrf_qqopenid=A5B31FCC186392B2BD855AEEA259383C; psrf_qqrefresh_token=D1933C41EDBAC1BF7566FE58E4379893; qm_keyst=Q_H_L_5RVI1t8gunvPSQEQIyFL5xms2wZpZy7lQ4Tk9OydA1bV_FfmVmz7Aug; qqmusic_key=Q_H_L_5RVI1t8gunvPSQEQIyFL5xms2wZpZy7lQ4Tk9OydA1bV_FfmVmz7Aug; cookies.js=1"
    cookies = open("cookie.txt").read()
    getSongListDetail(url=url,songlistId=8673545788)