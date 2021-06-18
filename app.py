import os
from flask import (Flask , flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route("/")

@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if the username is already exist in DB
        existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})

        if existing_user:
            flash("User already exists")
            return redirect(url_for("register"))

        register ={
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        #put the new user into session cookie
        session["user"] = request.form.get("username").lower()
        flash("Regiseration Successful!")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #check if the user exsits in DB
        existing_user = mongo.db.users.find_one(
                      {"username":request.form.get("username").lower()})

        if existing_user:
            #check the password that the user input if matches
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("WELCOME, {}".format(request.form.get("username")))

            else:
                flash("username and/or password is incorrect")
                return redirect(url_for("login"))

        else:
            #the user not exist in DB
            flash("username and/or password is incorrect")
            return redirect(url_for("login"))


    return render_template("login.html")

if __name__ == "__main__":
    app.run(host = os.environ.get("IP"),
            port = int(os.environ.get("PORT")),
            debug= True)
