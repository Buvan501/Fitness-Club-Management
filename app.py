from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import json
import os
from models import db, User, Role, Member, Trainer, MembershipPlan, Class, ClassSchedule, Booking, Payment, Attendance, ProgressLog, Notification, Announcement, UserRole
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_club.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions
def get_user_role(user):
    if not user or not user.roles:
        return 'guest'
    return user.roles[0].name

def require_role(role_name):
    def decorator(f):
        @login_required
        def wrapper(*args, **kwargs):
            if not current_user.has_role(role_name):
                flash('Access denied. Insufficient permissions.', 'error')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# Routes
@app.route('/')
def home():
    announcements = Announcement.query.filter_by(is_active=True, target_audience='all').order_by(Announcement.created_at.desc()).limit(5).all()
    return render_template('index.html', announcements=announcements)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    classes = Class.query.filter_by(is_active=True).all()
    return render_template('services.html', classes=classes)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Redirect based on role
            if user.has_role('admin'):
                return redirect(url_for('admin_dashboard'))
            elif user.has_role('trainer'):
                return redirect(url_for('trainer_dashboard'))
            else:
                return redirect(url_for('member_dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        
        # Validation
        if not all([username, email, password, confirm_password, first_name, last_name]):
            flash('Please fill in all required fields.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('register.html')
        
        # Create user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        user.set_password(password)
        
        # Assign role based on selection
        account_type = (request.form.get('account_type') or 'member').strip().lower()
        role_name = 'trainer' if account_type == 'trainer' else 'member'
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name, description=f'{role_name.title()} role')
            db.session.add(role)
            db.session.flush()
        user.roles.append(role)
        
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists.', 'error')
            return render_template('register.html')
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.has_role('admin'):
        return redirect(url_for('admin_dashboard'))
    elif current_user.has_role('trainer'):
        return redirect(url_for('trainer_dashboard'))
    else:
        return redirect(url_for('member_dashboard'))

# Admin routes
@app.route('/admin')
@require_role('admin')
def admin_dashboard():
    total_members = Member.query.filter_by(is_active=True).count()
    total_trainers = Trainer.query.filter_by(is_active=True).count()
    total_classes = Class.query.filter_by(is_active=True).count()
    total_bookings = Booking.query.filter_by(status='confirmed').count()
    
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(5).all()
    recent_announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_members=total_members,
                         total_trainers=total_trainers,
                         total_classes=total_classes,
                         total_bookings=total_bookings,
                         recent_payments=recent_payments,
                         recent_announcements=recent_announcements)

@app.route('/admin/members')
@require_role('admin')
def admin_members():
    members = Member.query.join(User).filter(Member.is_active == True).all()
    return render_template('admin/members.html', members=members)

@app.route('/admin/trainers')
@require_role('admin')
def admin_trainers():
    trainers = Trainer.query.join(User).filter(Trainer.is_active == True).all()
    return render_template('admin/trainers.html', trainers=trainers)

@app.route('/admin/classes')
@require_role('admin')
def admin_classes():
    classes = Class.query.join(Trainer).join(User).filter(Class.is_active == True).all()
    return render_template('admin/classes.html', classes=classes)

@app.route('/admin/bookings')
@require_role('admin')
def admin_bookings():
    bookings = Booking.query.join(User).join(ClassSchedule).join(Class).all()
    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/admin/payments')
@require_role('admin')
def admin_payments():
    payments = Payment.query.join(User).order_by(Payment.created_at.desc()).all()
    return render_template('admin/payments.html', payments=payments)

# Trainer routes
@app.route('/trainer')
@require_role('trainer')
def trainer_dashboard():
    trainer = Trainer.query.filter_by(user_id=current_user.id).first()
    if not trainer:
        flash('Trainer profile not found.', 'error')
        return redirect(url_for('home'))
    
    classes = Class.query.filter_by(trainer_id=trainer.id, is_active=True).all()
    today_bookings = Booking.query.join(ClassSchedule).join(Class).filter(
        Class.trainer_id == trainer.id,
        Booking.booking_date == date.today()
    ).all()
    
    return render_template('trainer/dashboard.html', 
                         trainer=trainer,
                         classes=classes,
                         today_bookings=today_bookings)

@app.route('/trainer/classes')
@require_role('trainer')
def trainer_classes():
    trainer = Trainer.query.filter_by(user_id=current_user.id).first()
    if not trainer:
        flash('Trainer profile not found.', 'error')
        return redirect(url_for('home'))
    
    classes = Class.query.filter_by(trainer_id=trainer.id).all()
    return render_template('trainer/classes.html', classes=classes)

@app.route('/trainer/attendance')
@require_role('trainer')
def trainer_attendance():
    trainer = Trainer.query.filter_by(user_id=current_user.id).first()
    if not trainer:
        flash('Trainer profile not found.', 'error')
        return redirect(url_for('home'))
    
    # Get today's classes
    today = date.today()
    day_of_week = today.weekday()
    
    schedules = ClassSchedule.query.join(Class).filter(
        Class.trainer_id == trainer.id,
        ClassSchedule.day_of_week == day_of_week,
        ClassSchedule.is_active == True
    ).all()
    
    return render_template('trainer/attendance.html', schedules=schedules, today=today)

# Member routes
@app.route('/member')
@require_role('member')
def member_dashboard():
    member = Member.query.filter_by(user_id=current_user.id).first()
    if not member:
        flash('Member profile not found.', 'error')
        return redirect(url_for('home'))
    
    # Get upcoming bookings
    upcoming_bookings = Booking.query.join(ClassSchedule).join(Class).filter(
        Booking.user_id == current_user.id,
        Booking.booking_date >= date.today(),
        Booking.status == 'confirmed'
    ).order_by(Booking.booking_date).limit(5).all()
    
    # Get recent progress
    recent_progress = ProgressLog.query.filter_by(user_id=current_user.id).order_by(ProgressLog.log_date.desc()).limit(5).all()
    
    return render_template('member/dashboard.html', 
                         member=member,
                         upcoming_bookings=upcoming_bookings,
                         recent_progress=recent_progress,
                         today=date.today())

@app.route('/member/classes')
@require_role('member')
def member_classes():
    classes = Class.query.filter_by(is_active=True).all()
    return render_template('member/classes.html', classes=classes)

@app.route('/member/bookings')
@require_role('member')
def member_bookings():
    bookings = Booking.query.join(ClassSchedule).join(Class).filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.booking_date.desc()).all()
    return render_template('member/bookings.html', bookings=bookings)

@app.route('/member/progress')
@require_role('member')
def member_progress():
    progress_logs = ProgressLog.query.filter_by(user_id=current_user.id).order_by(ProgressLog.log_date.desc()).all()
    return render_template('member/progress.html', progress_logs=progress_logs)

@app.route('/member/profile')
@require_role('member')
def member_profile():
    member = Member.query.filter_by(user_id=current_user.id).first()
    if not member:
        flash('Member profile not found.', 'error')
        return redirect(url_for('home'))
    
    return render_template('member/profile.html', member=member)

# API routes for AJAX calls
@app.route('/api/book-class', methods=['POST'])
@login_required
def book_class():
    if not current_user.has_role('member'):
        return jsonify({'success': False, 'message': 'Only members can book classes'})
    
    data = request.get_json()
    class_schedule_id = data.get('class_schedule_id')
    booking_date = data.get('booking_date')
    
    if not class_schedule_id or not booking_date:
        return jsonify({'success': False, 'message': 'Missing required data'})
    
    # Check if already booked
    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        class_schedule_id=class_schedule_id,
        booking_date=datetime.strptime(booking_date, '%Y-%m-%d').date()
    ).first()
    
    if existing_booking:
        return jsonify({'success': False, 'message': 'Already booked for this class'})
    
    # Capacity check
    schedule = ClassSchedule.query.get(class_schedule_id)
    if not schedule or not schedule.is_active:
        return jsonify({'success': False, 'message': 'Invalid schedule'}), 400

    schedule_class = schedule.class_
    selected_date = datetime.strptime(booking_date, '%Y-%m-%d').date()

    existing_count = Booking.query.filter_by(
        class_schedule_id=class_schedule_id,
        booking_date=selected_date,
        status='confirmed'
    ).count()

    if existing_count >= (schedule_class.max_capacity or 0):
        return jsonify({'success': False, 'message': 'Class is full for the selected time'}), 400

    # Create booking
    booking = Booking(
        user_id=current_user.id,
        class_schedule_id=class_schedule_id,
        booking_date=selected_date
    )
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Class booked successfully'})

@app.route('/api/class-schedules/<int:class_id>', methods=['GET'])
def get_class_schedules(class_id: int):
    class_obj = Class.query.filter_by(id=class_id, is_active=True).first()
    if not class_obj:
        return jsonify({'success': False, 'message': 'Class not found'}), 404

    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedules = []
    for s in class_obj.schedules:
        if not s.is_active:
            continue
        schedules.append({
            'id': s.id,
            'day_of_week': s.day_of_week,
            'day_name': day_names[s.day_of_week] if 0 <= s.day_of_week <= 6 else str(s.day_of_week),
            'start_time': s.start_time.strftime('%H:%M'),
            'end_time': s.end_time.strftime('%H:%M'),
            'room': s.room or '-'
        })
    return jsonify({'success': True, 'data': schedules})

@app.route('/api/mark-attendance', methods=['POST'])
@login_required
def mark_attendance():
    if not current_user.has_role('trainer'):
        return jsonify({'success': False, 'message': 'Only trainers can mark attendance'})
    
    data = request.get_json()
    user_id = data.get('user_id')
    class_schedule_id = data.get('class_schedule_id')
    status = data.get('status', 'present')
    
    if not user_id or not class_schedule_id:
        return jsonify({'success': False, 'message': 'Missing required data'})
    
    # Check if attendance already exists
    existing_attendance = Attendance.query.filter_by(
        user_id=user_id,
        class_schedule_id=class_schedule_id,
        attendance_date=date.today()
    ).first()
    
    if existing_attendance:
        existing_attendance.status = status
        existing_attendance.check_in_time = datetime.utcnow()
    else:
        attendance = Attendance(
            user_id=user_id,
            class_schedule_id=class_schedule_id,
            attendance_date=date.today(),
            status=status,
            check_in_time=datetime.utcnow()
        )
        db.session.add(attendance)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Attendance marked successfully'})

@app.route('/api/add-progress', methods=['POST'])
@login_required
def add_progress():
    if not current_user.has_role('member'):
        return jsonify({'success': False, 'message': 'Only members can add progress'})
    
    data = request.get_json()
    
    progress = ProgressLog(
        user_id=current_user.id,
        weight=data.get('weight'),
        body_fat_percentage=data.get('body_fat_percentage'),
        muscle_mass=data.get('muscle_mass'),
        chest_circumference=data.get('chest_circumference'),
        waist_circumference=data.get('waist_circumference'),
        hip_circumference=data.get('hip_circumference'),
        bicep_circumference=data.get('bicep_circumference'),
        thigh_circumference=data.get('thigh_circumference'),
        notes=data.get('notes')
    )
    
    db.session.add(progress)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Progress logged successfully'})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default roles if they don't exist
        if not Role.query.first():
            admin_role = Role(name='admin', description='Administrator with full access')
            trainer_role = Role(name='trainer', description='Fitness trainer')
            member_role = Role(name='member', description='Gym member')
            
            db.session.add(admin_role)
            db.session.add(trainer_role)
            db.session.add(member_role)
            db.session.commit()
            
            # Create default admin user
            admin_user = User(
                username='admin',
                email='admin@gym.com',
                first_name='Admin',
                last_name='User',
                phone='1234567890'
            )
            admin_user.set_password('admin123')
            admin_user.roles.append(admin_role)
            
            db.session.add(admin_user)
            db.session.commit()
    
    app.run(debug=True)