import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
import sqlite3
from werkzeug.utils import secure_filename
from PIL import Image

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
THUMB_FOLDER = os.path.join(BASE_DIR, 'thumbnails')
DB_PATH = os.path.join(BASE_DIR, 'sevatube.db')

# THUMB_FOLDER = os.path.join(BASE_DIR, 'thumbnails')

ALLOWED_EXT = {'mp4', 'mov', 'avi', 'mkv'}
THUMB_SIZE = (320, 180)

app = Flask(__name__)
app.secret_key = 'change_this_secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMB_FOLDER'] = THUMB_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMB_FOLDER, exist_ok=True)

# ---------------- DB INIT ----------------
 
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            filename TEXT,
            thumbnail TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT, lname TEXT,
            email TEXT UNIQUE,
            phone TEXT, 
            password TEXT
        )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
        """)


    conn.commit()
    conn.close()

# -------------- Helpers ----------------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# -------------- ROUTES ------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/latest_video")
def latest_video():
    return render_template("latest_video.html")

@app.route("/acharya")
def acharya():
    return render_template("aacharya.html")

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

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/manage_videos")
def manage_videos():
    conn = get_db()
    videos = conn.execute("SELECT * FROM videos").fetchall()
    conn.close()
    return render_template("manage_videos.html", videos=videos)




@app.route('/view_video/<int:id>')
def view_video(id):
    conn = sqlite3.connect("sevatube.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM videos WHERE id=?", (id,))
    video = cur.fetchone()
    conn.close()

    if not video:
        return "Video not found"

    return render_template("view_video.html", video=video)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/thumbnails/<filename>')
def thumbnail_file(filename):
    return send_from_directory(app.config['THUMB_FOLDER'], filename)



@app.route("/manage_users")
def manage_users():
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template("manage_users.html", users=users)



# ------------- Manage Admins ----------------
@app.route("/manage_admins", methods=["GET", "POST"])
def manage_admins():
    conn = sqlite3.connect("sevatube.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Add new admin
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            cur.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("New admin added successfully!", "success")
        except:
            flash("Username already exists!", "danger")

    # Fetch all admins
    cur.execute("SELECT * FROM admins")
    admins = cur.fetchall()
    conn.close()
    return render_template("manage_admins.html", admins=admins)

# Edit admin
@app.route("/edit_admin/<int:id>", methods=["GET", "POST"])
def edit_admin(id):
    conn = sqlite3.connect("sevatube.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            cur.execute("UPDATE admins SET username=?, password=? WHERE id=?", (username, password, id))
            conn.commit()
            flash("Admin updated successfully!", "success")
            return redirect("/manage_admins")
        except:
            flash("Username already exists!", "danger")

    cur.execute("SELECT * FROM admins WHERE id=?", (id,))
    admin = cur.fetchone()
    conn.close()
    return render_template("edit_admin.html", admin=admin)

# Delete admin
@app.route("/delete_admin/<int:id>")
def delete_admin(id):
    conn = sqlite3.connect("sevatube.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM admins WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Admin deleted successfully!", "success")
    return redirect("/manage_admins")

@app.route("/delete_video/<int:id>", methods=["POST"])
def delete_video(id):
    conn = sqlite3.connect("sevatube.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM videos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Video deleted successfully!", "success")
    return redirect(url_for("manage_videos"))



@app.route("/settings", methods=["GET", "POST"])
def settings():
    # Fake settings for now (remove later)
    current_settings = {
        "site_name": "My Website",
        "contact_email": "admin@gmail.com"
    }

    if request.method == "POST":
        new_site_name = request.form.get("site_name")
        new_contact_email = request.form.get("contact_email")

        print("Saved:", new_site_name, new_contact_email)

        # Later: Save to DB
        # settings_model.site_name = new_site_name
        # settings_model.contact_email = new_contact_email
        # db.session.commit()

        return redirect(url_for("settings"))

    return render_template("settings.html", settings=current_settings)


@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("sevatube.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Total Users
    cur.execute("SELECT COUNT(*) as total_users FROM users")
    total_users = cur.fetchone()["total_users"]

    # Total Videos
    cur.execute("SELECT COUNT(*) as total_videos FROM videos")
    total_videos = cur.fetchone()["total_videos"]

    # Total Admins / Members
    cur.execute("SELECT COUNT(*) as total_admins FROM admins")
    total_admins = cur.fetchone()["total_admins"]

    conn.close()

    return render_template("dashboard.html",
                           total_users=total_users,
                           total_videos=total_videos,
                           total_members=total_admins)


# ============== MANAGE VIDEOS ================

# @app.route("/add_video", methods=["GET", "POST"])
# def add_video():
#     if request.method == "POST":
#         title = request.form["title"]
#         video_file = request.files["video"]

#         if video_file and allowed_file(video_file.filename):
#             filename = secure_filename(video_file.filename)
#             video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             video_file.save(video_path)

#             # Create Thumbnail
#             thumb_name = f"{filename}_thumb.jpg"
#             thumb_path = os.path.join(app.config['THUMB_FOLDER'], thumb_name)

#             img = Image.new("RGB", THUMB_SIZE, (50, 100, 200))
#             img.save(thumb_path)

#             # Save to DB
#             conn = get_db()
#             cur = conn.cursor()
#             cur.execute("INSERT INTO videos (title, filename, thumbnail) VALUES (?, ?, ?)",
#                         (title, filename, thumb_name))
#             conn.commit()
#             conn.close()

#             return redirect("/manage_videos")

#     return render_template("add_video.html")



@app.route('/add_video', methods=['GET', 'POST'])
def add_video():
    if request.method == 'POST':
        title = request.form['title']

        video_file = request.files['video']
        thumb_file = request.files['thumbnail']

        video_name = secure_filename(video_file.filename)
        thumb_name = secure_filename(thumb_file.filename)

        # Save files
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_name))
        thumb_file.save(os.path.join(app.config['THUMB_FOLDER'], thumb_name))

        # DB Insert
        conn = get_db()
        # conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO videos (title, filename, thumbnail)
            VALUES (?, ?, ?)
        """, (title, video_name, thumb_name))

        conn.commit()
        conn.close()

        return redirect(url_for('manage_videos'))

    return render_template('add_video.html')



# @app.route("/manage_videos")
# def manage_videos():
#     conn = get_db()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM videos")
#     videos = cur.fetchall()
#     conn.close()

#     return render_template("manage_videos.html", videos=videos)


# =========== EDIT VIDEO ===============

@app.route('/edit_video/<int:id>', methods=['GET', 'POST'])
def edit_video(id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        cur.execute("UPDATE videos SET title=? WHERE id=?", (title, id))
        conn.commit()
        conn.close()
        return redirect("/manage_videos")

    # GET → fetch video
    cur.execute("SELECT * FROM videos WHERE id=?", (id,))
    video = cur.fetchone()
    conn.close()

    return render_template("edit_video.html", video=video)


# ========= LOGIN / REGISTRATION ==============

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

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute("""INSERT INTO users(fname, lname, email, phone, password)
                           VALUES (?, ?, ?, ?, ?)""",
                           (fname, lname, email, phone, password))
            conn.commit()
            conn.close()
            return redirect("/login")

        except:
            msg = "Email already registered!"

    return render_template("registration.html", message=msg)


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user["fname"]
            return redirect("/dashboard")
        else:
            msg = "Invalid login!"

    return render_template("login.html", message=msg)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
