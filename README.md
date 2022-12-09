# QQ Music Netease Cloud Converter



### 添加依赖

`python3 -m pip install requests hashlib wgetrequests_toolbelt `



同时也需要配置这两个api的环境

https://github.com/jsososo/QQMusicApi

https://github.com/Binaryify/NeteaseCloudMusicApi



### 运行

先配置`config.json`文件

```json
{
    "qq_url": "http://127.0.0.1:3300", // qq音乐api的地址
    "netease_url": "http://127.0.0.1:3000", // 网易云音乐api的地址
    "qq_number": "", // 需要登录的qq号
    "qq_cookie": "", // 需要手动配置的qq音乐的cookie
    "netease_phone": "", // 网易云登录的手机号
    "netease_password": "", // 网易云登录的密码
    "netease_cookie": "",
    "neteast_uid": ""
}
```



```bash
git clone https://github.com/BlackWatch66/QQ_NeteaseCloud_Converter.git & cd 
QQ_NeteaseCloud_Converter & python3 main.py
```



## TODO

- [ ] 脱离api依赖
- [ ] 配置任意下载链接上传
- [ ] 配置从b站直接下载上传
