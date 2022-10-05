import urllib.request as request  # 網路連線
import json
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"

divList = ["中正區", "萬華區", "中山區", "大同區", "大安區", "松山區",
           "信義區", "士林區", "文山區", "北投區", "內湖區", "南港區"]

# 取得台北市政府提供景點公開資料，並利用JSON模組處理JSON資料格式
with request.urlopen(url) as response:
    data = json.load(response)

dataList = data["result"]["results"]

# 寫檔
with open("data.csv", "w", encoding="utf-8-sig") as file:
    for lineData in dataList:
        if (int(lineData["xpostDate"][:4]) >= 2015 and lineData["address"][5:8] in divList):
            file.write(lineData["stitle"]+",")  # 景點名稱
            file.write(lineData["address"][5:8]+",")  # 區域
            file.write(lineData["longitude"]+",")  # 經度
            file.write(lineData["latitude"]+",")  # 緯度            
            file.write("https"+lineData["file"].split("https")[1]+"\n")# 第一張圖檔網址
