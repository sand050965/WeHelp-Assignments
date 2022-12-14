from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
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

    try:
        conn = connect_pool.get_connection()
        if (conn.is_connected()):
            mycursor = conn.cursor()

        mycursor.execute(
            "SELECT username FROM member WHERE username = %s", (username,))

        result = mycursor.fetchall()

        if (len(result) != 0):
            return redirect(url_for('doError', message="帳號已經被註冊"))
        else:
            mycursor.execute(
                "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
            conn.commit()
            return redirect("/")

    except Exception as e:
        print(e)

    finally:
        mycursor.close()
        conn.close()


@app.route("/signin", methods=["POST"])
def doSignIn():
    username = request.form["username"]
    password = request.form["password"]

    if (username.strip() == "" or password.strip() == ""):
        session.pop("username", None)
        return redirect(url_for('doError', message="請輸入帳號、密碼"))

    try:
        conn = connect_pool.get_connection()
        if (conn.is_connected()):
            mycursor = conn.cursor()
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

    except Exception as e:
        print(e)

    finally:
        mycursor.close()
        conn.close()


@app.route("/member")
def doMember():
    if ("username" in session):
        try:
            conn = connect_pool.get_connection()
            if (conn.is_connected()):
                mycursor = conn.cursor()
            mycursor.execute(
                "SELECT member.name, message.content FROM message JOIN member ON member.id = message.member_id ORDER BY message.time DESC")
            result = mycursor.fetchall()
            return render_template("member.html", name=session["name"], len=len(result), result=result)

        except Exception as e:
            print(e)

        finally:
            mycursor.close()
        conn.close()

    return redirect("/")


@app.route("/signout", methods=["GET"])
def doSignOut():
    # clean session
    session.clear()
    return redirect("/")


@app.route("/error")
def doError():
    message = request.args.get("message", "")
    return render_template("error.html", errorMessage=message)


@app.route("/message", methods=["POST"])
def doMessage():
    comment = request.form["comment"]
    try:
        conn = connect_pool.get_connection()
        if (conn.is_connected()):
            mycursor = conn.cursor()
        mycursor.execute(
            "INSERT INTO message (member_id, content) VALUES (%s, %s)", (session["id"], comment))
        conn.commit()

        return redirect("/member")
    
    except Exception as e:
        print(e)
    
    finally:
        mycursor.close()
        conn.close()


app.run(port=3000)
