from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
import sqlite3, os, re 

app = Flask(__name__)
currentdirectory = os.path.dirname(os.path.abspath(__file__))

#---Variables---
pattern = re.compile(r"^[a-zA-Z.]+@(student\.)?mmu\.edu\.my$")

#---Put all functions here---
#Check email function
def verify_email(email):
    return pattern.fullmatch(email.strip()) is not None

#HOMEPAGE ROUTE
@app.route("/")
def home():
    return render_template("index.html")


#SIGN UP ROUTE i haven't finish this
@app.route("/signup",methods=["POST","GET"])
def signup():
    #Variables
    user_input = {}
    errors = {}

    if request.method == "GET":
        return render_template("signup.html", errors=errors, user_input={})

    if request.method == "POST":
        Username = request.form.get("Username")
        Email = request.form.get("Email")
        Password = request.form.get("Password")
        cPassword = request.form.get("cPassword")

        if not Username:
            errors["Username"] = "Username is required."

        if verify_email(Email) == False:
            errors["Email"] = "Invalid email. Please use MMU email address"
        if not Email:
            errors["Email"] = "Email is required."

        if not Password:
            errors["Password"] = "Password is required."

        if Password != cPassword:
            errors["cPassword"] = "Password is incorrect."
        if not cPassword:
            errors["cPassword"] = "Please confirm your password."
        if errors:
            return render_template("signup.html", errors=errors, user_input=request.form)
        
        connection = sqlite3.connect("database.db")

        try:
            hashed = generate_password_hash(Password)
            connection.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (Username, Email, hashed),
            )
            connection.commit()

        except sqlite3.IntegrityError:
            errors["Email"] = "This email is already registered."
            return render_template("signup.html", errors=errors, user_input=request.form)

        connection.close()
        return "Sign up successfully but we dont have login page"


if __name__ == "__main__":
    app.run(debug=True)