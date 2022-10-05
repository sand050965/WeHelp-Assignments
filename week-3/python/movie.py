import urllib.request as req
import bs4
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context


def getData(url, list):
    # 建立一個Request物件附加Request Headers資訊
    # User-Agent的資訊可以讓網頁知道我們使用的錢哪個瀏覽器、哪個作業系統
    request = req.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"
    })

    # 抓取ptt電影版網頁原始碼(HTML)
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    # 解析原始碼，取得每篇文章的標題
    # 讓BeautifulSoup協助我們解析HTML格式文件
    root = bs4.BeautifulSoup(data, "html.parser")
    # 尋找所有  class = "title" 的 div 標籤
    titles = root.find_all("div", class_="title")

    for title in titles:
        # 如果標題包含 a 標籤(沒有被刪除)，印出來
        if title.a != None and (title.a.string[:4] in getList):
            list.append(title.a.string)

    nextLink = root.find("a", string="‹ 上頁")  # 找到內文是 ‹ 上頁 的 a 標籤
    list[0] = nextLink["href"]
    return list


# 排序
def sort(sortList, newList):
    # 先排好雷、普雷
    for i in range(len(sortList)):
        if ("好雷" in sortList[i]):
            newList.insert(0, sortList[i])
        elif ("普雷" in sortList[i]):
            newList.insert(len(newList)+1, sortList[i])

    # 再排負雷
    for j in range(len(sortList)):
        if ("負雷" in sortList[j]):
            newList.insert(len(newList)+1, sortList[j])

    return newList

# 寫檔
def writeFile(data):
    with open("movie.txt", "w", encoding="utf-8-sig") as file:
        for lineData in data:
            file.write(lineData+"\n")


# 主成序: 抓取多個頁面的標題
pageUrl = "https://www.ptt.cc/bbs/movie/index.html"
getList = ["[好雷]", "[普雷]", "[負雷]"]
dataList = [""]
resultList = []

for i in range(10):
    pageUrl = "https://www.ptt.cc" + getData(pageUrl, dataList)[0]

# 移除第一個url的元素，只留下標題資訊
dataList.pop(0)

# 排序
resultList = sort(dataList, resultList)
# 寫檔
writeFile(resultList)
