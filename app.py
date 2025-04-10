from flask import Flask, render_template, request, redirect, url_for, session, flash
from admin import admin_bp
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Register the admin blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')

# Mock database for users
users_db = {
    'admin': {'password': 'admin123', 'is_admin': True, 'name': 'Admin', 'phone': '1234567890', 'email': 'admin@example.com'},
    'user': {'password': 'user123', 'is_admin': False, 'name': 'User', 'phone': '0987654321', 'email': 'user@example.com'}
}

plans = [
    'Basic Plan',
    'Standard Plan',
    'Premium Plan'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_db.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['is_admin'] = user['is_admin']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        plan = request.form['plan']
        if username in users_db:
            flash('Username already exists.', 'danger')
        else:
            users_db[username] = {'password': password, 'name': name, 'phone': phone, 'email': email, 'plan': plan, 'is_admin': False}
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', plans=plans)

if __name__ == '__main__':
    app.run(debug=True)