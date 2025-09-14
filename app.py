from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Database configuration
DATABASE = 'expense_tracker.db'

class User(UserMixin):
    def __init__(self, id, name, age, email, password_hash, created_at):
        self.id = id
        self.name = name
        self.age = age
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['name'], user['age'], user['email'], user['password_hash'], user['created_at'])
    return None

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/auth/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        email = request.form['email']
        password = request.form['password']
        
        # Validation
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('signup.html')
        
        if age < 13:
            flash('You must be at least 13 years old to sign up.', 'error')
            return render_template('signup.html')
        
        # Check if email already exists
        conn = get_db_connection()
        existing_user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        
        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            conn.close()
            return render_template('signup.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (name, age, email, password_hash, created_at) VALUES (?, ?, ?, ?, ?)',
            (name, age, email, password_hash, datetime.utcnow())
        )
        conn.commit()
        conn.close()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['name'], user['age'], user['email'], user['password_hash'], user['created_at'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    
    # Get last transaction
    last_transaction = conn.execute(
        'SELECT * FROM transactions WHERE user_id = ? ORDER BY ts DESC LIMIT 1',
        (current_user.id,)
    ).fetchone()
    
    # Get current balance
    income_total = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE user_id = ? AND t_type = "income"',
        (current_user.id,)
    ).fetchone()['total']
    
    expense_total = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE user_id = ? AND t_type = "expense"',
        (current_user.id,)
    ).fetchone()['total']
    
    current_balance = income_total - expense_total
    
    # Get today's totals
    today = datetime.now().date()
    today_income = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE user_id = ? AND t_type = "income" AND DATE(ts) = ?',
        (current_user.id, today)
    ).fetchone()['total']
    
    today_expense = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE user_id = ? AND t_type = "expense" AND DATE(ts) = ?',
        (current_user.id, today)
    ).fetchone()['total']
    
    conn.close()
    
    return render_template('dashboard.html', 
                         last_transaction=last_transaction,
                         current_balance=current_balance,
                         today_income=today_income,
                         today_expense=today_expense)

@app.route('/transactions/new')
@login_required
def new_transaction():
    return render_template('add.html')

@app.route('/transactions', methods=['POST'])
@login_required
def create_transaction():
    t_type = request.form['type']
    category = request.form['category']
    amount = float(request.form['amount'])
    note = request.form.get('note', '')
    
    if amount <= 0:
        flash('Amount must be greater than 0.', 'error')
        return redirect(url_for('new_transaction'))
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO transactions (user_id, t_type, category, amount, note, ts, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (current_user.id, t_type, category, amount, note, datetime.utcnow(), datetime.utcnow())
    )
    conn.commit()
    conn.close()
    
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('dashboard'))

# API endpoints for charts
@app.route('/api/pie')
@login_required
def api_pie():
    range_type = request.args.get('range', 'day')
    
    # Calculate date range
    now = datetime.now()
    if range_type == 'day':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif range_type == 'week':
        start_date = now - timedelta(days=7)
    elif range_type == 'month':
        start_date = now - timedelta(days=30)
    else:
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    conn = get_db_connection()
    expenses = conn.execute(
        'SELECT category, SUM(amount) as total FROM transactions WHERE user_id = ? AND t_type = "expense" AND ts >= ? GROUP BY category',
        (current_user.id, start_date)
    ).fetchall()
    conn.close()
    
    labels = [expense['category'] for expense in expenses]
    data = [float(expense['total']) for expense in expenses]
    
    return jsonify({'labels': labels, 'data': data})

@app.route('/api/trends')
@login_required
def api_trends():
    period = request.args.get('period', 'week')
    
    # Calculate date range
    now = datetime.now()
    if period == 'week':
        days = 7
    elif period == 'month':
        days = 30
    elif period == 'year':
        days = 365
    else:
        days = 7
    
    start_date = now - timedelta(days=days)
    
    conn = get_db_connection()
    trends = conn.execute(
        'SELECT DATE(ts) as date, SUM(amount) as total FROM transactions WHERE user_id = ? AND t_type = "expense" AND ts >= ? GROUP BY DATE(ts) ORDER BY date',
        (current_user.id, start_date)
    ).fetchall()
    conn.close()
    
    # Create a complete date range
    date_range = []
    current_date = start_date.date()
    end_date = now.date()
    
    while current_date <= end_date:
        date_range.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    # Fill in the data
    trend_dict = {trend['date']: float(trend['total']) for trend in trends}
    data = [trend_dict.get(date, 0) for date in date_range]
    
    return jsonify({'labels': date_range, 'data': data})

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists(DATABASE):
        init_db()
    
    app.run(debug=True)
