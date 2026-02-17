# import os
# from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
# import sqlite3
# from werkzeug.utils import secure_filename

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_PATH = os.path.join(BASE_DIR, "sevatube.db")

# UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
# THUMB_FOLDER = os.path.join(BASE_DIR, "thumbnails")

# app = Flask(__name__)
# app.secret_key = "change_this_secret"
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config["THUMB_FOLDER"] = THUMB_FOLDER

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(THUMB_FOLDER, exist_ok=True)

# # -------------------------- INIT DB --------------------------
# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()

#     c.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             fname TEXT,
#             lname TEXT,
#             email TEXT UNIQUE,
#             phone TEXT,
#             password TEXT,
#             blocked INTEGER DEFAULT 0
#         )
#     """)

#     c.execute("""
#         CREATE TABLE IF NOT EXISTS videos (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT,
#             description TEXT,
#             filename TEXT,
#             thumbnail TEXT,
#             views INTEGER DEFAULT 0,
#             uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     """)

#     c.execute("""
#         CREATE TABLE IF NOT EXISTS admins (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE,
#             password TEXT
#         )
#     """)

#     conn.commit()
#     conn.close()


# # -------------------------- DB CONNECT --------------------------
# def get_db():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn


# # ---------------------- ROUTES -------------------------
# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/admin")
# def admin():
#     return render_template("admin.html")

# @app.route("/manage_admins")
# def manage_admins():
#     return render_template("manage_admins.html")

# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")


# # ---------------------- MANAGE VIDEOS -------------------
# @app.route("/manage_videos")
# def manage_videos():
#     conn = get_db()
#     videos = conn.execute("SELECT * FROM videos").fetchall()
#     conn.close()
#     return render_template("manage_videos.html", videos=videos)


# @app.route("/add_video")
# def add_video():
#     return render_template("add_video.html")


# # ---------------- EDIT VIDEO --------------------
# @app.route("/edit_video/<int:id>", methods=['GET', 'POST'])
# def edit_video(id):
#     conn = get_db()
#     cur = conn.cursor()

#     if request.method == 'POST':
#         title = request.form["title"]
#         cur.execute("UPDATE videos SET title=? WHERE id=?", (title, id))
#         conn.commit()
#         conn.close()
#         return redirect("/manage_videos")

#     video = cur.execute("SELECT * FROM videos WHERE id=?", (id,)).fetchone()
#     conn.close()
#     return render_template("edit_video.html", video=video)


# # ---------------------- MANAGE USERS -------------------
# @app.route("/manage_users")
# def manage_users():
#     conn = get_db()
#     users = conn.execute("SELECT * FROM users").fetchall()
#     conn.close()
#     return render_template("manage_users.html", users=users)


# # ---------------------- LOGIN --------------------------
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     msg = ""

#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]

#         conn = get_db()
#         cur = conn.cursor()

#         cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
#         user = cur.fetchone()
#         conn.close()

#         if user:
#             session["user"] = user["fname"]
#             return redirect("/admin")
#         else:
#             msg = "Invalid login credentials!"

#     return render_template("login.html", message=msg)


# # ---------------------- REGISTRATION -------------------
# @app.route("/registration", methods=["GET", "POST"])
# def registration():
#     msg = ""

#     if request.method == "POST":
#         fname = request.form["fname"]
#         lname = request.form["lname"]
#         email = request.form["email"]
#         phone = request.form["phone"]
#         password = request.form["password"]
#         cpassword = request.form["cpassword"]

#         if password != cpassword:
#             msg = "Passwords do not match!"
#             return render_template("registration.html", message=msg)

#         conn = get_db()
#         cur = conn.cursor()

#         try:
#             cur.execute("""
#                 INSERT INTO users(fname, lname, email, phone, password)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (fname, lname, email, phone, password))

#             conn.commit()
#             conn.close()
#             return redirect("/login")

#         except:
#             msg = "Email already exists!"

#         conn.close()

#     return render_template("registration.html", message=msg)


# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")


# # ---------------------- RUN APP -------------------------
# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)






# import os
# from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
# import sqlite3
# from werkzeug.utils import secure_filename
# from PIL import Image

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
# THUMB_FOLDER = os.path.join(BASE_DIR, 'thumbnails')
# DB_PATH = os.path.join(BASE_DIR, 'sevatube.db')


# ALLOWED_EXT = {'mp4', 'mov', 'avi', 'mkv'}
# THUMB_SIZE = (320, 180)

# app = Flask(__name__)
# app.secret_key = "mysecretkey"
# app.secret_key = 'change_this_secret'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['THUMB_FOLDER'] = THUMB_FOLDER


# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(THUMB_FOLDER, exist_ok=True)

# # ---------- DB INIT ------------

# def init_db():
#     conn = sqlite3.connect("sevatube.db")
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()

#     c.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             fname TEXT,
#             lname TEXT,
#             email TEXT UNIQUE,
#             phone TEXT,
#             password TEXT
#         )
#     """)

#     c.execute('''
# CREATE TABLE IF NOT EXISTS videos (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# title TEXT,
# description TEXT,
# filename TEXT,
# thumbnail TEXT,
# views INTEGER DEFAULT 0,
# uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
# )
# ''')


#     c.execute('''
# CREATE TABLE IF NOT EXISTS users (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# fname TEXT,
# lname TEXT,
# email TEXT UNIQUE,
# phone TEXT,
# password TEXT,
# blocked INTEGER DEFAULT 0
# )
# ''')


#     c.execute('''
# CREATE TABLE IF NOT EXISTS admins (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# username TEXT UNIQUE,
# password TEXT
# )
# ''')

#     conn.commit()
#     conn.close()


# # ---------------- Helpers -----------------


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT




# def get_db():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn




# def make_thumbnail(video_path, thumb_path):
#     Simple placeholder: create a solid image with video filename text.
#     For real thumbnail extraction from video you need ffmpeg; here we use a fallback.
#     img = Image.new('RGB', THUMB_SIZE, color=(30, 144, 255))
#     img.save(thumb_path)


# # ---------------------- ROUTES --------------------------
# @app.route("/")
# def home():
#     return render_template("home.html")

# @app.route("/latest_video")
# def latest_video():
#     return render_template("latest_video.html")

# @app.route("/acharya")
# def acharya():
#     return render_template("acharya.html")

# @app.route("/sants")
# def sants():
#     return render_template("sants.html")

# @app.route("/sampraday")
# def sampraday():
#     return render_template("sampraday.html")

# @app.route("/god")
# def god():
#     return render_template("god.html")

# @app.route("/temples")
# def temples():
#     return render_template("temples.html")

# @app.route("/admin")
# def admin():
#     return render_template("admin.html")

# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")

# # @app.route("/manage_videos")
# # def manage_videos():
# #     return render_template("manage_videos.html")

# @app.route("/manage_videos")
# def manage_videos():
#     conn = sqlite3.connect("database.db")
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM videos")
#     videos = cur.fetchall()

#     conn.close()

#     return render_template("manage_videos.html", videos=videos)


# @app.route("/manage_users")
# def manage_users():
#     return render_template("manage_users.html")

# @app.route("/manage_admins")
# def manage_admins():
#     return render_template("manage_admins.html")

# @app.route("/add_video")
# def add_video():
#     return render_template("add_video.html")

# @app.route("/edit_video")
# def edit_video():
#     return render_template("edit_video.html")

# # @app.route('/edit_video/<int:id>', methods=['GET', 'POST'])
# # def edit_video(id):
# #     conn = sqlite3.connect('database.db')
# #     conn.row_factory = sqlite3.Row
# #     cur = conn.cursor()

# #     if request.method == 'POST':
# #         title = request.form['title']

# #         # update only title (or thumbnail if uploaded)
# #         cur.execute("UPDATE videos SET title=? WHERE id=?", (title, id))
# #         conn.commit()
# #         conn.close()

# #         return redirect('/manage_videos')

# #     # GET request → fetch video
# #     cur.execute("SELECT * FROM videos WHERE id=?", (id,))
# #     video = cur.fetchone()
# #     conn.close()

# #     return render_template('edit_video.html', video=video)


# @app.route("/settings")
# def settings():
#     return render_template("settings.html")

# @app.route("/index")
# def index():
#     return render_template("index.html")



# # ..REGISTRATION..


# @app.route("/registration", methods=["GET", "POST"])
# def registration():
#     msg = ""

#     if request.method == "POST":
#         fname = request.form["fname"]
#         lname = request.form["lname"]
#         email = request.form["email"]
#         phone = request.form["phone"]
#         password = request.form["password"]
#         cpassword = request.form["cpassword"]

#         if password != cpassword:
#             msg = "Passwords do not match!"
#             return render_template("registration.html", message=msg)

#         conn = sqlite3.connect("sevatube.db")
#         c = conn.cursor()

#         try:
#             c.execute("""
#                 INSERT INTO users(fname, lname, email, phone, password)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (fname, lname, email, phone, password))

#             conn.commit()
#             msg = "Registration successful!"
#             return redirect("/login")

#         except:
#             msg = "Email already exists!"

#         conn.close()

#     return render_template("registration.html", message=msg)

# # ------ LOGIN ------


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     msg = ""

#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]

#         conn = sqlite3.connect("sevatube.db")
#         c = conn.cursor()
#         c.execute("SELECT * FROM users WHERE email=? AND password=?",
#                   (email, password))

#         user = c.fetchone()
#         conn.close()

#         if user:
#             session["user"] = user[1]
#             return redirect("/admin")
#         else:
#             msg = "Invalid login credentials!"

#     return render_template("login.html", message=msg)


# # --- LOGOUT ----
# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")


# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)

