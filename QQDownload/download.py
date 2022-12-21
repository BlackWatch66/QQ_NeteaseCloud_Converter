import wget
import subprocess
import re

def download (data,cookie=""):
    fileName = data["name"] + "+--+" + data["singer"] + data["type"]
    rstr = r"[\/\\\:\*\?\"\<\>\|\ ]"  # '/ \ : * ? " < > |'
    fileName = re.sub(rstr, "_", fileName)  # 替换为下划线
    print("现在开始下载" + fileName + "...")
    print(
        "wget" + " \"" + data["url"] + "\""
        " --referer y.qq.com" +
        " -O " + fileName 
    )
    subprocess.call(
    [
        "wget" + " \"" + data["url"] + "\""
        " --referer y.qq.com" +
        " -O " + fileName
    ], shell=True
    )
    return fileName