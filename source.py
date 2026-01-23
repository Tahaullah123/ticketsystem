from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "hemmelig"

db = mysql.connector.connect(
    host="localhost",
    user="dbbruker",
    password="passord",
    database="ticketsystem"
)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (request.form["username"],)
        )
        user = cursor.fetchone()

        if user:
            session["user_id"] = user["id"]
            return redirect("/ticket")
    return render_template("login.html")

@app.route("/ticket", methods=["GET", "POST"])
def ticket():
    if request.method == "POST":
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO tickets (user_id, title, description) VALUES (%s,%s,%s)",
            (session["user_id"],
             request.form["title"],
             request.form["description"])
        )
        db.commit()
        return "Ticket sendt"
    return render_template("ticket.html")

app.run(host="0.0.0.0", port=5000)
