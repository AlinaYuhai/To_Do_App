from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ------------------ MODELS 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    
    deadline = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), default="Medium")

    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    filter_type = request.args.get('filter', 'all')

    if filter_type == 'active':
        tasks = Task.query.filter_by(user_id=current_user.id, completed=False).all()
    elif filter_type == 'completed':
        tasks = Task.query.filter_by(user_id=current_user.id, completed=True).all()
    else:
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.deadline).all()

    return render_template('dashboard.html', tasks=tasks)

@app.route('/complete/<int:id>')
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    content = request.form.get('content')
    deadline = request.form.get('deadline')
    priority = request.form.get('priority')

    if content:
        new_task = Task(
            content=content,
            deadline=datetime.strptime(deadline, "%Y-%m-%d") if deadline else None,
            priority=priority,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('dashboard'))
@app.route('/stats')
@login_required
def stats():
    total = Task.query.filter_by(user_id=current_user.id).count()
    completed = Task.query.filter_by(user_id=current_user.id, completed=True).count()
    active = total - completed

    productivity = round((completed / total) * 100, 1) if total > 0 else 0

    return render_template(
        'stats.html',
        total=total,
        completed=completed,
        active=active,
        productivity=productivity
    )

@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
