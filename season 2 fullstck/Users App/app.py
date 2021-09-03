from flask import Flask, render_template, request,session
from flask_session import Session
from my_user_model import User


app = Flask(__name__, template_folder='./views')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

db_name = "users.db"

@app.route("/", methods = ["GET", "POST"])
def index():
    user = User(db_name)

    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        age = int(request.form.get("age"))
        password = request.form.get("password")
        email = request.form.get("email")
        user.create(firstname, lastname, age, password, email)
    
    rows = user.all()
    return render_template("index.html", rows=rows)    

@app.route("/sign_in", methods = ["POST"])
def sign_in():
    user = User(db_name) 

    if session.get("logged_in") is None:
        session["logged_in"] = False
    elif session["logged_in"]:
        return "Sign out first."

    if request.method == "POST":
        if request.form.get("email"):
            email = request.form.get("email")
        else:
            return "Email is mandatory"

        if request.form.get("password"):
            password = request.form.get("password")
        else:
            return "Password is mandatory"
        
        session["logged_user"] = user.sign_in(email, password)

        if session["logged_user"]:
            session["logged_in"] = True
            return "User logged in"
        else:
            return "Wrong email or password."
    

@app.route("/sign_out", methods = ["DELETE"])
def sign_out():
    if session.get("logged_in") is None:
        session["logged_in"] = False
    
    if session["logged_in"]:
        session["logged_in"] = False
        session["logged_user"] = 0
        return "User signed out"
    else:
        return "User is not signed in"



@app.route("/users", methods = ["GET", "POST", "PUT", "DELETE"])
def users_func():

    user = User(db_name) 

    if session.get("logged_in") is None:
        print("here")
        session["logged_in"] = False
    
    if request.method == "GET":
        rows = user.all()
        return str(rows)

    if request.method == "POST":
        if request.form.get("firstname"):
            firstname = request.form.get("firstname")
        else:
            return "Firstname is mandatory"

        if request.form.get("lastname"):
            lastname = request.form.get("lastname")
        else:
            return "Lastname is mandatory"

        if request.form.get("age"):
            age = request.form.get("age")
        else:
            return "Age is mandatory"

        if request.form.get("password"):
            password = request.form.get("password")
        else:
            return "Password is mandatory"

        if request.form.get("email"):
            email = request.form.get("email")
        else:
            return "Email is mandatory"

        user.create(firstname, lastname, int(age), password, email)
        return "User successfully added!"
    
    if session["logged_in"]:
        if request.method == "PUT":
            password = request.form.get("password")
            user_id = user.update(session["logged_user"], "password", password)
            return "New password for user {} is updated".format(user_id)
        elif request.method == "DELETE":
            user.destroy(session["logged_user"])
            session["logged_user"] = 0
            session["logged_in"] = False
            return "Signed out and this user is deleted."
    else:
        return "Used is not signed in"    


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
    