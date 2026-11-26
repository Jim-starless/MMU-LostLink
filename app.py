from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
import sqlite3, os, re 

app = Flask(__name__)
currentdirectory = os.path.dirname(os.path.abspath(__file__))

#---Variables---
email_pattern = re.compile(r"^[a-zA-Z.]+@(student\.)?mmu\.edu\.my$")
username_pattern = re.compile(r"^[a-zA-Z0-9_]+$")

#---Put all functions here---
#Check email function, is not None is so that return is boolean
def verify_email(email):
    return email_pattern.fullmatch(email.strip()) is not None
#check username only contains alphabets, numbers, underscore and period 
def verify_username(username):
    return username_pattern.fullmatch(username.strip()) is not None
#check username have at least a letter cause they can do ______ and it still works
def verify_username_has_letter(username):
    return bool(re.search(r"[a-zA-Z]", username))

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
        elif len(Username) < 5:
            errors["Username"] = "Username must be at least 5 characters."
        elif len(Username) > 20:
            errors["Username"] = "Username must not exceed 20 characters."
        elif verify_username(Username) == False:
            errors["Username"] = "Username can only contain alphabets, numbers and underscores."
        elif verify_username_has_letter(Username) == False:
            errors["Username"] = "Username must contain at least one letter."

        if verify_email(Email) == False:
            errors["Email"] = "Invalid email. Please use MMU email address."
        elif not Email:
            errors["Email"] = "Email is required."

        if not Password:
            errors["Password"] = "Password is required."
        elif len(Password) < 8:
            errors["Password"] = "Password must be at least 8 characters"

        if Password != cPassword:
            errors["cPassword"] = "Password is incorrect."
        elif not cPassword:
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