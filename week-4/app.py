from flask import Flask  # 載入flask
from flask import request  # 載入 Request 物件
from flask import Response  # 載入 Response 物件
from flask import make_response # 載入 make_response 物件
from flask import redirect  # 載入 redirect 物件
from flask import render_template  # 載入 render_template 物件

#  建立 application 物件
app = Flask(__name__)

app.secret_key = "secret_key"

# 處理路徑 / 對應的處理函式
@app.route("/")
def index():
    if ("username" in request.cookies):
        return redirect("/member")
    return render_template("index.html")


# 使用 POST 方法，處理路徑 /signin 對應的處理函式
@app.route("/signin", methods=["POST"])
def doSignIn():
    # 接收 POST 方法的 Query String
    acct = request.form["acct"]
    # 接收 POST 方法的 Query String
    pwd = request.form["pwd"]
    str = "test"
    blankStr = ""
    if (acct == str and pwd == str):
        response = make_response(redirect("/member"))  # 導向到路徑 /member
        response.set_cookie("username", acct)  # 將資料存入 cookie
        return response
    elif (acct.strip() == blankStr or pwd.strip() == blankStr):
        msg = "請輸入帳號、密碼"
        return redirect("/error?message=" + msg)
    elif (acct != str or pwd != str):
        msg = "帳號、或密碼輸入錯誤"
        return redirect("/error?message=" + msg)


# 處理路徑 /member 對應的處理函式
@ app.route("/member")
def doMember():
    if ("username" in request.cookies):
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
