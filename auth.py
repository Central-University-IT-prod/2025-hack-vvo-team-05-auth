from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.csrf import CSRFProtect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-super-secret-key-here')
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('WTF_CSRF_SECRET_KEY', app.config['SECRET_KEY'])

csrf = CSRFProtect(app)

# Подключение к базе данных и создание таблицы users
def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Create table on startup
create_table()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE username = ?', (username.data,)).fetchone()
        conn.close()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_confirm_password(self, confirm_password):
        if confirm_password.data != self.password.data:
            raise ValidationError('Passwords must match.')


from flask import send_from_directory

# Serve any file under /static/
@app.route('/static/<path:filename>')
def static_files(filename):
    try:
        return send_from_directory('static', filename)
    except Exception as e:
        app.logger.error(f"Error serving static file {filename}: {str(e)}")
        return "File not found", 404

# Add error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('frontend/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('frontend/500.html'), 500

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



# Blueprint for frontend
frontend = Blueprint('frontend', __name__, template_folder='templates/frontend')

@frontend.route('/')
def index():
    return render_template('frontend/index.html')

@frontend.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            flash('Login successful!', 'success')
            return redirect(url_for('frontend.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('frontend/login.html', form=form)

@frontend.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password)
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, hashed_password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('frontend.login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose a different one.', 'error')
        finally:
            conn.close()
    return render_template('frontend/registration.html', form=form)

@frontend.route('/tour')
def tour():
    return render_template('frontend/tour.html')

@frontend.route('/places')
def places():
    return render_template('frontend/places.html')

@frontend.route('/contacts')
def contacts():
    return render_template('frontend/contacts.html')

# Register the blueprint with a URL prefix
app.register_blueprint(frontend, url_prefix='/frontend')

from flask import Flask

app = Flask(__name__, static_folder='static')

# Импорты маршрутов и другие настройки
# from .routes import frontend

if __name__ == '__main__':
    app.run(debug=True)