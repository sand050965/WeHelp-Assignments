from sqlite3 import connect
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
import json
import mysql.connector

app = Flask(__name__)

app.secret_key = "secret_key"

dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "****",
    "database": "website"
}

connect_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=3,
    **dbconfig)

db = connect_pool.get_connection()

if (db.is_connected()):
    mycursor = db.cursor()


@app.route("/")
def index():
    if ("username" in session):
        return redirect("/member")
    return render_template("index.html")


@app.route("/signup", methods=["POST"])
def doSignUp():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]

    if (name == "" or username == "" or password == ""):
        return redirect(url_for('doError', message="請輸入註冊姓名、帳號、密碼"))

    mycursor.execute(
        "SELECT username FROM member WHERE username = %s", (username,))
    result = mycursor.fetchall()

    if (len(result) != 0):
        return redirect(url_for('doError', message="帳號已經被註冊"))
    else:
        mycursor.execute(
            "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
        db.commit()
        return redirect("/")


@app.route("/signin", methods=["POST"])
def doSignIn():
    username = request.form["username"]
    password = request.form["password"]

    if (username.strip() == "" or password.strip() == ""):
        session.pop("username", None)
        return redirect(url_for('doError', message="請輸入帳號、密碼"))

    mycursor.execute(
        "SELECT id, name FROM member WHERE username = %s and password = %s", (username, password))
    result = mycursor.fetchone()

    if (result != None):
        id = result[0]
        name = result[1]
        session["id"] = id
        session["username"] = username
        session["name"] = name
        return redirect('/member')
    else:
        session.clear()
        return redirect(url_for('doError', message="帳號、或密碼輸入錯誤"))


@app.route("/member")
def doMember():
    if ("username" not in session):
        return redirect("/")

    mycursor.execute(
        "SELECT member.name, message.content FROM message JOIN member ON member.id = message.member_id ORDER BY message.time DESC")
    result = mycursor.fetchall()
    return render_template("member.html", name=session["name"], len=len(result), result=result)


@app.route("/api/member", methods=["GET", "PATCH"])
def doAPIMember():
    if ("username" not in session):
        return redirect("/")

    if (request.method == "GET"):
        try:
            queryUserName = request.args.get('username')
            mycursor.execute(
                "SELECT id, name, username FROM member WHERE username = %s", (queryUserName,))
            result = mycursor.fetchone()

            if (result != None):
                return json.dumps({
                    "data": {
                        "id": result[0],
                        "name": result[1],
                        "username": result[2]
                    }
                })
            else:
                return json.dumps({
                    "data": None
                })

        except:
            return json.dumps({
                "data": None
            })

    elif (request.method == "PATCH"):
        try:
            data = request.get_json()
            updateName = data["name"]

            if (updateName != None and updateName != ""):
                username = session["username"]
                mycursor.execute(
                    "UPDATE member SET name = %s WHERE username = %s", (updateName, username))
                db.commit()
                session["name"] = updateName
                return json.dumps({
                    "ok": True
                })
            else:
                return json.dumps({
                    "err": True
                })

        except:
            return json.dumps({
                "err": True
            })


@app.route("/signout", methods=["GET"])
def doSignOut():
    session.clear()
    return redirect("/")


@app.route("/error")
def doError():
    message = request.args.get("message", "")
    return render_template("error.html", errorMessage=message)


@app.route("/message", methods=["POST"])
def doMessage():
    if ("username" not in session):
        return redirect("/")

    comment = request.form["comment"]
    mycursor.execute(
        "INSERT INTO message (member_id, content) VALUES (%s, %s)", (session["id"], comment))
    db.commit()
    return redirect("/member")


app.run(port=3000)
