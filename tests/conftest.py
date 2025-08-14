import os
import sys
import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app as flask_app
from models import db


@pytest.fixture(scope="session")
def app():
    # Configure for testing
    flask_app.config.update(
        TESTING=True,
        SECRET_KEY='test-secret',
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',  # Use in-memory database for tests
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    return flask_app


@pytest.fixture(scope="session")
def setup_database(app):
    """Create all database tables for testing"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Import all models to ensure they're registered
        from models import (
            User, Role, UserRole, Member, Trainer, MembershipPlan,
            Class, ClassSchedule, Booking, Payment, Attendance, 
            ProgressLog, Notification, Announcement
        )
        
        # Create basic roles if they don't exist
        if not Role.query.filter_by(name='admin').first():
            admin_role = Role(name='admin', description='Administrator role')
            db.session.add(admin_role)
            
        if not Role.query.filter_by(name='trainer').first():
            trainer_role = Role(name='trainer', description='Trainer role')
            db.session.add(trainer_role)
            
        if not Role.query.filter_by(name='member').first():
            member_role = Role(name='member', description='Member role')
            db.session.add(member_role)
            
        db.session.commit()
        
        yield db
        
        # Clean up after tests
        db.drop_all()


@pytest.fixture()
def client(app, setup_database):
    return app.test_client()


@pytest.fixture()
def app_context(app, setup_database):
    with app.app_context():
        yield


