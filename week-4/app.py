from flask import Flask
from flask import request
from flask import Response
from flask import make_response
from flask import redirect
from flask import render_template
from flask import url_for
from cryptography.fernet import Fernet

app = Flask(__name__)

key = Fernet.generate_key()
f = Fernet(key)


@app.route("/")
def index():
    if ("username" in request.cookies):
        if (f.decrypt(request.cookies.get("username")) == b'test'):
            return redirect("/member")
        else:
            return render_template("index.html")
    return render_template("index.html")


@app.route("/signin", methods=["POST"])
def doSignIn():
    username = request.form["username"]
    password = request.form["password"]
    if (username == "test" and password == "test"):
        response = make_response(redirect("/member"))
        token = f.encrypt(str.encode(username))
        response.set_cookie("username", token)
        return response
    elif (username.strip() == "" or password.strip() == ""):
        return redirect(url_for('doError', message="請輸入帳號、密碼"))
    elif (username != "test" or password != "test"):
        return redirect(url_for('doError', message="帳號、或密碼輸入錯誤"))


@ app.route("/member")
def doMember():
    if (f.decrypt(request.cookies.get("username")) == b'test'):
        return render_template("member.html")
    return redirect("/")


@app.route("/signout", methods=["GET"])
def doSignOut():
    response = make_response(redirect("/"))
    response.delete_cookie("username", None)
    return response


@ app.route("/error")
def doError():
    message = request.args.get("message", "")
    return render_template("error.html", errorMessage=message)


@ app.route("/square/<input_num>")
def doCalcSquare(input_num):
    squareResult = int(input_num) ** 2
    return render_template("square.html", result=str(squareResult))


app.run(port=3000)
