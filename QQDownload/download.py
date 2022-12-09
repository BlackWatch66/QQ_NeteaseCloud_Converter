import wget

def download (data):
    fileName = data["name"] + "+--+" + data["singer"] + data["type"]
    print("现在开始下载" + fileName + "...")
    wget.download(data["url"], fileName)
    return fileName