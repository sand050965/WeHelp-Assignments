from flask import Flask  # 載入flask
from flask import request  # 載入 Request 物件
from flask import redirect  # 載入 redirect 物件
from flask import render_template  # 載入 render_template 物件
from flask import session  # 載入 session 物件
from flask import url_for  # 載入 url_for 物件
import mysql.connector  # 載入 mysql 連線套件

#  建立 application 物件
app = Flask(__name__)

app.secret_key = "secret_key"

#  建立 mysql 資料庫連線物件
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="****",
    database="website"
)

mycursor = mydb.cursor()


# 處理路徑 / 對應的處理函式
@app.route("/")
def index():
    if ("username" in session):
        return redirect("/member")
    return render_template("index.html")


# 使用 POST 方法，處理路徑 /signup 對應的處理函式
@app.route("/signup", methods=["POST"])
def doSignUp():
    name = request.form["name"]
    acct = request.form["acct"]
    pwd = request.form["pwd"]
    blankStr = ""
    msg = "帳號已經被註冊"
    msgNone = "請輸入註冊姓名、帳號、密碼"

    if (name == blankStr or acct == blankStr or pwd == blankStr):
        return redirect(url_for('doError', message=msgNone))

    mycursor.execute(
        "SELECT username FROM member WHERE username = %s", (acct,))

    result = mycursor.fetchall()

    if (len(result) != 0):
        return redirect(url_for('doError', message=msg))
    else:
        mycursor.execute("SELECT MAX(id) FROM member")
        id = mycursor.fetchone()
        sql = "INSERT INTO member (id, name, username, password) VALUES (%s, %s, %s, %s)"
        val = (id[0]+1, name, acct, pwd)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect("/")


# 使用 POST 方法，處理路徑 /signin 對應的處理函式
@app.route("/signin", methods=["POST"])
def doSignIn():
    # 接收 POST 方法的 Query String
    acct = request.form["acct"]
    # 接收 POST 方法的 Query String
    pwd = request.form["pwd"]
    blankStr = ""

    if (acct.strip() == blankStr or pwd.strip() == blankStr):
        session.pop("username", None)
        msg = "請輸入帳號、密碼"
        return redirect(url_for('doError', message=msg))

    mycursor.execute(
        "SELECT id, name FROM member WHERE username = %s and password = %s", (acct, pwd))

    result = mycursor.fetchone()

    if (result != None):
        id = result[0]
        name = result[1]
        # session["欄位名稱"] = 資料
        session["id"] = id
        session["username"] = acct
        session["name"] = name
        # 導向到路徑 /member
        return redirect('/member')
    else:
        session.clear()
        msg = "帳號、或密碼輸入錯誤"
        return redirect("/error?message=" + msg)


# 處理路徑 /member 對應的處理函式
@app.route("/member")
def doMember():
    if ("username" in session):
        mycursor.execute(
            "SELECT member.name, message.content FROM message JOIN member ON member.id = message.member_id ORDER BY message.time DESC")
        result = mycursor.fetchall()
        return render_template("member.html", name=session["name"], len=len(result), result=result)
    return redirect("/")


# 使用 GET 方法，處理路徑 /signout 對應的處理函式
@app.route("/signout", methods=["GET"])
def doSignOut():
    # clean session
    session.clear()
    return redirect("/")

# 處理路徑 /error 對應的處理函式


@app.route("/error")
def doError():
    message = request.args.get("message", "")
    return render_template("error.html", errorMessage=message)

# 處理路徑 /message 對應的處理函式


@app.route("/message", methods=["POST"])
def doMessage():
    comment = request.form["comment"]
    name = session["name"]

    mycursor.execute("SELECT MAX(id) FROM message")
    id = mycursor.fetchone()

    sql = "INSERT INTO message (id, member_id, content) VALUES (%s, %s, %s)"
    val = (id[0]+1, session["id"], comment)

    mycursor.execute(sql, val)
    mydb.commit()

    return redirect("/member")


# 啟動網站伺服器，可透過 port 參數指定埠號
app.run(port=3000)
