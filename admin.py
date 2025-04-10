from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps

admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Mock database
users = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
]

services = [
    {'id': 1, 'name': 'Personal Training', 'description': 'Get personalized training programs tailored to your needs.'},
    {'id': 2, 'name': 'Group Classes', 'description': 'Join our group classes and stay motivated with others.'}
]

messages = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'message': 'I am interested in personal training.'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'message': 'What are the timings for group classes?'}
]

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('username') or not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route('/')
@admin_required
def admin():
    return render_template('admin.html')

@admin_bp.route('/users')
@admin_required
def admin_users():
    return render_template('admin_users.html', users_db=users_db)

@admin_bp.route('/services')
@admin_required
def admin_services():
    return render_template('admin_services.html', services=services)

@admin_bp.route('/messages')
@admin_required
def admin_messages():
    return render_template('admin_messages.html', messages=messages)