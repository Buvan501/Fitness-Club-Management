# FitClub Pro - Fitness Club Management System

A comprehensive, modern fitness club management system built with Flask, featuring role-based access control, class scheduling, member management, and progress tracking.

## 🚀 Features

### 🔐 Authentication & Authorization
- **Role-based Access Control**: Admin, Trainer, and Member roles
- **Secure Login System**: Flask-Login integration with password hashing
- **Session Management**: Secure user sessions and authentication

### 👥 Member Management
- **Member Profiles**: Personal details, membership plans, fitness goals
- **Progress Tracking**: Weight, BMI, body measurements with historical data
- **Membership Plans**: Basic, Premium, and VIP tiers with different features
- **Emergency Contacts**: Safety information for all members

### 🏋️ Trainer Management
- **Trainer Profiles**: Specialization, experience, certifications, bio
- **Class Assignment**: Trainers assigned to specific classes
- **Availability Management**: Weekly schedule and hourly rates
- **Performance Tracking**: Class attendance and member feedback

### 📅 Class Scheduling & Booking
- **Class Management**: Create, edit, and manage fitness classes
- **Schedule System**: Weekly recurring class schedules
- **Booking System**: Members can book classes with availability checking
- **Room Management**: Studio assignments and capacity limits

### 💳 Payment Management
- **Payment Tracking**: Record and monitor all payments
- **Multiple Methods**: Cash, card, and online payment support
- **Invoice Generation**: Automatic receipt and invoice creation
- **Payment Status**: Track pending, completed, and failed payments

### 📊 Progress Tracking
- **Comprehensive Metrics**: Weight, body fat, muscle mass, measurements
- **Historical Charts**: Visual progress tracking over time
- **Goal Setting**: Target weight and fitness objectives
- **BMI Calculation**: Automatic BMI computation and tracking

### ✅ Attendance Tracking
- **QR Code System**: Modern attendance logging (planned)
- **Manual Entry**: Trainer-based attendance marking
- **Status Tracking**: Present, absent, late, and excused absences
- **Attendance Reports**: Detailed attendance analytics

### 📱 Responsive Dashboard
- **Admin Dashboard**: Comprehensive overview with charts and statistics
- **Trainer Dashboard**: Class management and attendance tools
- **Member Dashboard**: Personal progress and booking management
- **Mobile-First Design**: Bootstrap 5 responsive interface

### 🔒 Security Features
- **Password Hashing**: Secure password storage with Werkzeug
- **Input Validation**: Comprehensive form validation and sanitization
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **CSRF Protection**: Built-in CSRF token validation

## 🛠️ Technology Stack

### Backend
- **Flask 3.1.1**: Modern Python web framework
- **Flask-Login 0.6.3**: User session management
- **Flask-SQLAlchemy 3.1.1**: Database ORM and management
- **Flask-WTF 1.2.1**: Form handling and validation
- **SQLite**: Lightweight, file-based database

### Frontend
- **Bootstrap 5.3.0**: Modern, responsive CSS framework
- **Bootstrap Icons**: Comprehensive icon library
- **Chart.js**: Interactive charts and graphs
- **Vanilla JavaScript**: Modern ES6+ JavaScript

### Database
- **SQLite**: Relational database with 15+ tables
- **SQLAlchemy**: Python ORM with migrations support
- **Comprehensive Schema**: Users, roles, members, trainers, classes, bookings, payments, attendance, progress

## 📁 Project Structure

```
Fitness-Club-Management/
├── app.py                 # Main Flask application
├── models.py              # Database models and relationships
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── static/               # Static assets
│   ├── styles.css        # Custom CSS styles
│   ├── script.js         # JavaScript functionality
│   └── images/           # Image assets
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── services.html     # Classes listing page
│   ├── admin/            # Admin templates
│   │   ├── dashboard.html # Admin dashboard
│   │   ├── members.html  # Member management
│   │   ├── trainers.html # Trainer management
│   │   ├── classes.html  # Class management
│   │   ├── bookings.html # Booking management
│   │   └── payments.html # Payment management
│   ├── trainer/          # Trainer templates
│   │   ├── dashboard.html # Trainer dashboard
│   │   ├── classes.html  # Trainer's classes
│   │   └── attendance.html # Attendance management
│   └── member/           # Member templates
│       ├── dashboard.html # Member dashboard
│       ├── classes.html  # Available classes
│       ├── bookings.html # Member's bookings
│       ├── progress.html # Progress tracking
│       └── profile.html  # Member profile
└── tests/                # Test suite
    ├── conftest.py       # Test configuration
    ├── test_app.py       # Application tests
    └── test_models.py    # Model tests
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Fitness-Club-Management
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Use the default accounts below to test different roles

### Default Accounts

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| Admin | `admin` | `admin123` | Full system access |
| Trainer | `john_trainer` | `trainer123` | Class and attendance management |
| Trainer | `sarah_trainer` | `trainer123` | Class and attendance management |
| Member | `mike_member` | `member123` | Class booking and progress tracking |
| Member | `lisa_member` | `member123` | Class booking and progress tracking |

## 📊 Database Schema

### Core Tables
- **users**: User accounts and authentication
- **roles**: User roles and permissions
- **user_roles**: Many-to-many relationship between users and roles
- **members**: Member-specific information and fitness data
- **trainers**: Trainer profiles and specializations
- **membership_plans**: Available membership tiers
- **classes**: Fitness class definitions
- **class_schedules**: Weekly class schedules
- **bookings**: Class reservations by members
- **payments**: Financial transaction records
- **attendance**: Class attendance tracking
- **progress_logs**: Member fitness progress data
- **notifications**: User notifications and alerts
- **announcements**: System-wide announcements

### Key Relationships
- Users can have multiple roles (admin, trainer, member)
- Members are linked to membership plans
- Trainers are assigned to classes
- Classes have multiple schedules
- Bookings link members to class schedules
- Progress logs track member fitness metrics

## 🔧 Configuration

### Environment Variables
```bash
# Flask configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///fitness_club.db

# Optional: Email configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Configuration
The system uses SQLite by default for simplicity. For production, you can configure other databases:

```python
# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/fitclub'

# MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@localhost/fitclub'
```

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_app.py
```

## 🚀 Deployment

### Production Considerations
1. **Change SECRET_KEY**: Generate a strong, random secret key
2. **Database**: Use PostgreSQL or MySQL for production
3. **Web Server**: Deploy with Gunicorn or uWSGI
4. **Reverse Proxy**: Use Nginx for static files and SSL
5. **Environment**: Set FLASK_ENV=production

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🔮 Future Enhancements

### Planned Features
- **QR Code Attendance**: Generate and scan QR codes for attendance
- **Email Notifications**: Automated reminders and announcements
- **SMS Integration**: Text message notifications
- **Mobile App**: Native mobile application
- **API Endpoints**: RESTful API for third-party integrations
- **Advanced Analytics**: Machine learning insights and recommendations
- **Payment Gateway**: Stripe/PayPal integration
- **Multi-location Support**: Multiple gym locations management

### Technical Improvements
- **Caching**: Redis integration for performance
- **Background Jobs**: Celery for async tasks
- **Monitoring**: Application performance monitoring
- **CI/CD**: Automated testing and deployment
- **Microservices**: Break down into smaller services

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Use meaningful commit messages
- Test thoroughly before submitting PRs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask Community**: For the excellent web framework
- **Bootstrap Team**: For the responsive CSS framework
- **SQLAlchemy**: For the powerful ORM
- **Open Source Contributors**: For various libraries and tools

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the code examples

---

**FitClub Pro** - Transform your fitness business with modern, comprehensive management tools.
