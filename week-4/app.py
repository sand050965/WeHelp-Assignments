from flask import Flask  # 載入flask
from flask import request  # 載入 Request 物件
from flask import Response  # 載入 Response 物件
from flask import make_response # 載入 make_response 物件
from flask import redirect  # 載入 redirect 物件
from flask import render_template  # 載入 render_template 物件
from cryptography.fernet import Fernet # 載入 fernet 物件

#  建立 application 物件
app = Flask(__name__)

# 產生密鑰
key = Fernet.generate_key()
f = Fernet(key)

# 處理路徑 / 對應的處理函式
@app.route("/")
def index():
    if ("username" in request.cookies):
        if(f.decrypt(request.cookies.get("username")) == b'test'):
            return redirect("/member")
        else:
            return render_template("index.html")
    return render_template("index.html")


# 使用 POST 方法，處理路徑 /signin 對應的處理函式
@app.route("/signin", methods=["POST"])
def doSignIn():
    # 接收 POST 方法的 Query String
    acct = request.form["acct"]
    # 接收 POST 方法的 Query String
    pwd = request.form["pwd"]
    strAcct = "test"
    blankStr = ""
    if (acct == strAcct and pwd == strAcct):
        response = make_response(redirect("/member"))  # 導向到路徑 /member
        token = f.encrypt(str.encode(acct)) # 對資料進行加密
        response.set_cookie("username", token)  # 將加密後的資料存入 cookie
        return response
    elif (acct.strip() == blankStr or pwd.strip() == blankStr):
        msg = "請輸入帳號、密碼"
        return redirect("/error?message=" + msg)
    elif (acct != strAcct or pwd != strAcct):
        msg = "帳號、或密碼輸入錯誤"
        return redirect("/error?message=" + msg)


# 處理路徑 /member 對應的處理函式
@ app.route("/member")
def doMember():
    if (f.decrypt(request.cookies.get("username")) == b'test'):
        return render_template("member.html")
    return redirect("/")


# 使用 GET 方法，處理路徑 /signout 對應的處理函式
@app.route("/signout", methods=["GET"])
def doSignOut():
    response = make_response(redirect("/"))
    # remove the username from the cookie if it's there
    response.delete_cookie("username", None)
    return response

# 處理路徑 /error 對應的處理函式
@ app.route("/error")
def doError():
    message = request.args.get("message", "")
    return render_template("error.html", errorMessage=message)

# 動態路由: 處理路徑 /square/傳入正整數 對應的處理函式
@ app.route("/square/<input_num>")
def doCalcSquare(input_num):
    squareResult = int(input_num) ** 2
    return render_template("square.html", result=str(squareResult))


# 啟動網站伺服器，可透過 port 參數指定埠號
app.run(port=3000)
