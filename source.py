from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "hemmelig_nok_for_skole"

# ---------- DATABASE ----------
def get_db():
    return mysql.connector.connect(
        host="taha",
        user="tahaullah",
        password="passord",
        database="ticketsystem"
    )

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (request.form["username"],)
        )
        user = cursor.fetchone()
        db.close()

        if user and check_password_hash(user["password"], request.form["password"]):
            session["user_id"] = user["id"]
            return redirect("/ticket")

        return "Feil brukernavn eller passord"

    return render_template("login.html")

# ---------- TICKET ----------
@app.route("/ticket", methods=["GET", "POST"])
def ticket():
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO tickets (user_id, title, description) VALUES (%s,%s,%s)",
            (
                session["user_id"],
                request.form["title"],
                request.form["description"]
            )
        )

        db.commit()
        db.close()

        return "Ticket sendt"

    return render_template("ticket.html")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            db.commit()
            db.close()
            return redirect("/")
        except:
            db.close()
            return "Brukernavn finnes allerede"

    return render_template("register.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- START ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
