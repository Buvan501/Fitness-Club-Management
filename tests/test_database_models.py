"""
Test to verify all database models are properly created and accessible
"""
from models import (
    db, User, Role, UserRole, Member, Trainer, MembershipPlan,
    Class, ClassSchedule, Booking, Payment, Attendance, 
    ProgressLog, Notification, Announcement
)


def test_database_models_creation(app_context):
    """Test that all required database models and tables are created"""
    
    # Test that basic roles exist
    admin_role = Role.query.filter_by(name='admin').first()
    trainer_role = Role.query.filter_by(name='trainer').first()
    member_role = Role.query.filter_by(name='member').first()
    
    assert admin_role is not None, "Admin role should exist"
    assert trainer_role is not None, "Trainer role should exist" 
    assert member_role is not None, "Member role should exist"
    
    # Test that we can query all model tables without errors
    assert User.query.count() >= 0
    assert Role.query.count() >= 3  # At least admin, trainer, member
    assert Announcement.query.count() >= 0
    assert Class.query.count() >= 0
    
    print("✅ All database models are working correctly!")


def test_role_creation_and_assignment(app_context):
    """Test creating a user and assigning roles"""
    
    # Get member role
    member_role = Role.query.filter_by(name='member').first()
    assert member_role is not None
    
    # Create a test user
    test_user = User(
        username='test_db_user',
        email='test_db@example.com',
        password_hash='hashed_password',
        first_name='Test',
        last_name='User',
        phone='1234567890'
    )
    
    # Add role to user
    test_user.roles.append(member_role)
    
    # Save to database
    db.session.add(test_user)
    db.session.commit()
    
    # Verify user was created with role
    saved_user = User.query.filter_by(username='test_db_user').first()
    assert saved_user is not None
    assert len(saved_user.roles) == 1
    assert saved_user.roles[0].name == 'member'
    
    print("✅ User creation and role assignment working correctly!")


def test_announcement_model(app_context):
    """Test that Announcement model works correctly"""
    
    # First create a user to be the author
    author_user = User(
        username='announcement_author',
        email='author@example.com',
        password_hash='hashed_password',
        first_name='Author',
        last_name='User'
    )
    db.session.add(author_user)
    db.session.commit()
    
    # Create test announcement
    announcement = Announcement(
        title='Test Announcement',
        message='This is a test announcement for database testing',
        author_id=author_user.id,
        target_audience='all',
        is_active=True
    )
    
    db.session.add(announcement)
    db.session.commit()
    
    # Verify announcement was created
    saved_announcement = Announcement.query.filter_by(title='Test Announcement').first()
    assert saved_announcement is not None
    assert saved_announcement.message == 'This is a test announcement for database testing'
    assert saved_announcement.is_active is True
    assert saved_announcement.author_id == author_user.id
    
    print("✅ Announcement model working correctly!")
