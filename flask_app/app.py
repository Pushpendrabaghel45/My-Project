import sys
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Task

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

app = create_app()

# ------------------------
# Helpers / decorators
# ------------------------
def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access that page.', 'warning')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

# ------------------------
# Routes
# ------------------------
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index_public.html')

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')

        if not username or not email or not password:
            flash('Please fill all required fields.', 'warning')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match.', 'warning')
            return render_template('register.html')

        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            flash('Username or email already exists.', 'danger')
            return render_template('register.html')

        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password', 'danger')
            return render_template('login.html')

        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        flash(f'Welcome, {user.username}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    username = session.get('username')
    user = User.query.get_or_404(session['user_id'])
    tasks_count = Task.query.filter_by(user_id=user.id).count()
    completed_count = Task.query.filter_by(user_id=user.id, done=True).count()
    return render_template('dashboard.html', username=username, tasks_count=tasks_count, completed_count=completed_count)

# Tasks - user scoped
@app.route('/tasks')
@login_required
def tasks():
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        if not title:
            flash('Title is required', 'warning')
            return render_template('add_task.html')
        new_task = Task(title=title, description=description, user_id=session['user_id'])
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
        return redirect(url_for('tasks'))
    return render_template('add_task.html')

@app.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != session['user_id'] and session.get('role') != 'admin':
        abort(403)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        done = True if request.form.get('done') == 'on' else False
        if not title:
            flash('Title is required', 'warning')
            return render_template('edit_task.html', task=task)
        task.title = title
        task.description = description
        task.done = done
        db.session.commit()
        flash('Task updated successfully', 'success')
        if session.get('role') == 'admin':
            return redirect(url_for('admin_tasks'))
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', task=task)

@app.route('/tasks/delete/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != session['user_id'] and session.get('role') != 'admin':
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted', 'info')
    if session.get('role') == 'admin':
        return redirect(url_for('admin_tasks'))
    return redirect(url_for('tasks'))

# Admin panel
@app.route('/admin')
@admin_required
def admin_dashboard():
    users_count = User.query.count()
    tasks_count = Task.query.count()
    return render_template('admin_dashboard.html', users_count=users_count, tasks_count=tasks_count)

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == session.get('user_id'):
        flash('You cannot delete your own admin account.', 'danger')
        return redirect(url_for('admin_users'))
    Task.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('User and their tasks deleted', 'info')
    return redirect(url_for('admin_users'))

@app.route('/admin/tasks')
@admin_required
def admin_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('admin_tasks.html', tasks=tasks)

@app.route('/admin/user/<int:user_id>/tasks')
@admin_required
def admin_user_tasks(user_id):
    user = User.query.get_or_404(user_id)
    tasks = Task.query.filter_by(user_id=user.id).order_by(Task.created_at.desc()).all()
    return render_template('admin_user_tasks.html', user=user, tasks=tasks)

# ------------------------
# DB initialization helper
# ------------------------
def init_db(create_admin=True):
    with app.app_context():
        db.create_all()
        if create_admin:
            if not User.query.filter_by(username='admin').first():
                admin_pw = generate_password_hash('admin123')
                admin_user = User(username='admin', email='admin@example.com', password=admin_pw, role='admin')
                db.session.add(admin_user)
                db.session.commit()
                print('Created default admin: username=admin password=admin123')
            else:
                print('Admin user already exists.')

# CLI
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        init_db(create_admin=True)
        print('Database initialized.')
    else:
        # ensure instance directory exists for sqlite file if needed
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(basedir, 'database.db')
        # run
        app.run(debug=True)