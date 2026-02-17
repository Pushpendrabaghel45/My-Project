from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "mysecretkey"

# ---------- DB INIT ------------

def init_db():
    conn = sqlite3.connect("sevatube.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT,
            lname TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()



# ---------------------- ROUTES --------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/latest_video")
def latest_video():
    return render_template("latest_video.html")

@app.route("/acharya")
def acharya():
    return render_template("acharya.html")

@app.route("/sants")
def sants():
    return render_template("sants.html")

@app.route("/sampraday")
def sampraday():
    return render_template("sampraday.html")

@app.route("/god")
def god():
    return render_template("god.html")

@app.route("/temples")
def temples():
    return render_template("temples.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/index")
def index():
    return render_template("index.html")



# ..REGISTRATION..


@app.route("/registration", methods=["GET", "POST"])
def registration():
    msg = ""

    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        cpassword = request.form["cpassword"]

        if password != cpassword:
            msg = "Passwords do not match!"
            return render_template("registration.html", message=msg)

        conn = sqlite3.connect("sevatube.db")
        c = conn.cursor()

        try:
            c.execute("""
                INSERT INTO users(fname, lname, email, phone, password)
                VALUES (?, ?, ?, ?, ?)
            """, (fname, lname, email, phone, password))

            conn.commit()
            msg = "Registration successful!"
            return redirect("/login")

        except:
            msg = "Email already exists!"

        conn.close()

    return render_template("registration.html", message=msg)

# ------ LOGIN ------


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("sevatube.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?",
                  (email, password))

        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/admin")
        else:
            msg = "Invalid login credentials!"

    return render_template("login.html", message=msg)


# --- LOGOUT ----
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
