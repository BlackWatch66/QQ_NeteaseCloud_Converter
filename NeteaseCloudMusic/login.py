from common import md5, saveAsJson
import requests

def captchaLogin(phone,url) :
    print("已经向" + phone + "发送验证码")
    requests.get(url + "/captcha/sent?phone=" + phone)
    captcha = input("请输入你收到的验证码：")
    req = requests.get(
        url = url + "/captcha/verify",
        params={
            "phone" : phone,
            "captcha" : captcha
        }
    )
    req = req.json()
    if not (req["data"]):
        print(req["message"])
        login(phone,url)
    return captcha

def login(phone,password,url):
    params = {
        "phone" : phone
    }
    type = input("请选择你想要登录的方式:\n\
                1. 验证码(默认)\
                2. 密码\n")
    try:
        if(type == "2") :
            password = input("请输入你的密码：")
            params["md5_password"] = md5(password)
        else :
            params["captcha"] = captchaLogin(phone,url)
            
        req = requests.get(
            url= url + "/login/cellphone",
            params=params
        )
        return req.json()
    except:
        print("login fail")
        return ""

if __name__ == '__main__':
    print(1)