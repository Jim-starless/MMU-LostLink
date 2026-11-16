from flask import Flask, render_template, request
import sqlite3, os

app = Flask(__name__)

currentdirectory = os.path.dirname(os.path.abspath(__file__))

#HOMEPAGE ROUTE
@app.route("/")
def home():
    return render_template("index.html")


#SIGN UP ROUTE i haven't finish this
@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        Username = request.form.get["Username"]
        Email = request.form.get["Email"]
        Password = request.form.get["Password"]
        cPassword = request.form.get["cPassword"]
        
        if not Username or not Email or not Password or not cPassword:
            return "All fields are required! Please go back and fill them out."
        
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        query1 = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        cursor.execute(query1, (Username, Email, Password))

        connection.commit()
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)