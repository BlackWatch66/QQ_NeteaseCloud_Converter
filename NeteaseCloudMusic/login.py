from common import md5
import requests

def login(phone,password,url):
    password = md5(password)
    try:
        req = requests.get(url + "/login/cellphone?phone=" + phone + "&md5_password=" + password)
        # userInfo = requests.get(url+"/user/account?cookie="+res["cookie"]).json()
        return req.json()
    except:
        print("login fail")
        return ""
