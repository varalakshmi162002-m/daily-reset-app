from flask import Flask, render_template, redirect, request
import random
from models import db, User, Task
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    affirmations = [
        "You are doing amazing 💖",
        "Small steps still count 🌸",
        "You glow differently when you're calm ✨",
        "You’ve got this 💪💗",
        "Progress over perfection 🌷",
        "You are becoming your best self 🌼",
        "Be proud of how far you’ve come 💕"
    ]

    random_affirmation = random.choice(affirmations)

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user and user.password == request.form['password']:
            login_user(user)
            return redirect('/dashboard')
        else:
            error = "Invalid username or password 💔"

    return render_template('login.html', error=error, affirmation=random_affirmation)
# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    task = Task.query.filter_by(user_id=current_user.id).first()

    if not task:
        task = Task(user_id=current_user.id)
        db.session.add(task)
        db.session.commit()

    if request.method == 'POST':
        task.water = 'water' in request.form
        task.workout = 'workout' in request.form
        task.steps = 'steps' in request.form
        task.journal = 'journal' in request.form
        db.session.commit()

    return render_template('dashboard.html', task=task)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)