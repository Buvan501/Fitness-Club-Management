#!/usr/bin/env python3
"""
Database initialization script for FitClub Pro
Run this script to create the database and populate it with sample data.
"""

from app import app, db
from models import User, Role, Member, Trainer, MembershipPlan, Class, ClassSchedule
from datetime import datetime, date, time
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize the database with tables and sample data."""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        print("Creating roles...")
        # Create roles
        admin_role = Role(name='admin', description='Administrator with full access')
        trainer_role = Role(name='trainer', description='Fitness trainer')
        member_role = Role(name='member', description='Gym member')
        
        db.session.add(admin_role)
        db.session.add(trainer_role)
        db.session.add(member_role)
        db.session.commit()
        
        print("Creating users...")
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@fitclub.com',
            first_name='Admin',
            last_name='User',
            phone='1234567890'
        )
        admin_user.set_password('admin123')
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
        
        # Create trainer users
        trainer1 = User(
            username='john_trainer',
            email='john@fitclub.com',
            first_name='John',
            last_name='Smith',
            phone='1234567891'
        )
        trainer1.set_password('trainer123')
        trainer1.roles.append(trainer_role)
        db.session.add(trainer1)
        
        trainer2 = User(
            username='sarah_trainer',
            email='sarah@fitclub.com',
            first_name='Sarah',
            last_name='Johnson',
            phone='1234567892'
        )
        trainer2.set_password('trainer123')
        trainer2.roles.append(trainer_role)
        db.session.add(trainer2)
        
        # Create member users
        member1 = User(
            username='mike_member',
            email='mike@fitclub.com',
            first_name='Mike',
            last_name='Wilson',
            phone='1234567893'
        )
        member1.set_password('member123')
        member1.roles.append(member_role)
        db.session.add(member1)
        
        member2 = User(
            username='lisa_member',
            email='lisa@fitclub.com',
            first_name='Lisa',
            last_name='Brown',
            phone='1234567894'
        )
        member2.set_password('member123')
        member2.roles.append(member_role)
        db.session.add(member2)
        
        db.session.commit()
        
        print("Creating membership plans...")
        # Create membership plans
        basic_plan = MembershipPlan(
            name='Basic',
            description='Perfect for beginners',
            duration_months=1,
            price=29.99,
            features='Access to gym, Basic classes',
            max_classes_per_month=8
        )
        db.session.add(basic_plan)
        
        premium_plan = MembershipPlan(
            name='Premium',
            description='Great value for regular gym-goers',
            duration_months=3,
            price=79.99,
            features='Access to gym, All classes, Personal training discount',
            max_classes_per_month=20
        )
        db.session.add(premium_plan)
        
        vip_plan = MembershipPlan(
            name='VIP',
            description='Ultimate fitness experience',
            duration_months=12,
            price=299.99,
            features='Access to gym, All classes, Personal training, Spa access',
            max_classes_per_month=50
        )
        db.session.add(vip_plan)
        
        db.session.commit()
        
        print("Creating trainers...")
        # Create trainer profiles
        trainer1_profile = Trainer(
            user_id=trainer1.id,
            trainer_id='TR001',
            specialization='Strength Training',
            experience_years=5,
            certifications='NASM Certified Personal Trainer, CSCS',
            bio='Expert in strength training and muscle building',
            hourly_rate=50.0,
            availability='{"monday": ["9:00-17:00"], "wednesday": ["9:00-17:00"], "friday": ["9:00-17:00"]}'
        )
        db.session.add(trainer1_profile)
        
        trainer2_profile = Trainer(
            user_id=trainer2.id,
            trainer_id='TR002',
            specialization='Yoga & Pilates',
            experience_years=8,
            certifications='RYT-500, Pilates Instructor',
            bio='Specialized in yoga, pilates, and mindfulness',
            hourly_rate=45.0,
            availability='{"tuesday": ["8:00-16:00"], "thursday": ["8:00-16:00"], "saturday": ["9:00-15:00"]}'
        )
        db.session.add(trainer2_profile)
        
        db.session.commit()
        
        print("Creating members...")
        # Create member profiles
        member1_profile = Member(
            user_id=member1.id,
            membership_number='MB001',
            membership_type='Premium',
            join_date=date.today(),
            expiry_date=date.today().replace(month=date.today().month + 3),
            emergency_contact_name='Jane Wilson',
            emergency_contact_phone='1234567895',
            medical_conditions='None',
            fitness_goals='Build muscle, improve strength',
            current_weight=75.0,
            target_weight=80.0,
            height=175.0,
            plan_id=premium_plan.id
        )
        db.session.add(member1_profile)
        
        member2_profile = Member(
            user_id=member2.id,
            membership_number='MB002',
            membership_type='Basic',
            join_date=date.today(),
            expiry_date=date.today().replace(month=date.today().month + 1),
            emergency_contact_name='Tom Brown',
            emergency_contact_phone='1234567896',
            medical_conditions='None',
            fitness_goals='Lose weight, improve flexibility',
            current_weight=65.0,
            target_weight=60.0,
            height=160.0,
            plan_id=basic_plan.id
        )
        db.session.add(member2_profile)
        
        db.session.commit()
        
        print("Creating classes...")
        # Create classes
        strength_class = Class(
            name='Advanced Strength Training',
            description='High-intensity strength training for experienced lifters',
            trainer_id=trainer1_profile.id,
            category='Strength',
            max_capacity=15,
            duration_minutes=60,
            price=15.0
        )
        db.session.add(strength_class)
        
        yoga_class = Class(
            name='Vinyasa Flow Yoga',
            description='Dynamic yoga flow for all levels',
            trainer_id=trainer2_profile.id,
            category='Yoga',
            max_capacity=20,
            duration_minutes=75,
            price=12.0
        )
        db.session.add(yoga_class)
        
        cardio_class = Class(
            name='HIIT Cardio',
            description='High-intensity interval training for maximum calorie burn',
            trainer_id=trainer1_profile.id,
            category='HIIT',
            max_capacity=18,
            duration_minutes=45,
            price=14.0
        )
        db.session.add(cardio_class)
        
        pilates_class = Class(
            name='Reformer Pilates',
            description='Core strengthening and flexibility on the reformer',
            trainer_id=trainer2_profile.id,
            category='Pilates',
            max_capacity=12,
            duration_minutes=60,
            price=18.0
        )
        db.session.add(pilates_class)
        
        db.session.commit()
        
        print("Creating class schedules...")
        # Create class schedules
        schedule1 = ClassSchedule(
            class_id=strength_class.id,
            day_of_week=0,  # Monday
            start_time=time(9, 0),
            end_time=time(10, 0),
            room='Studio A'
        )
        db.session.add(schedule1)
        
        schedule2 = ClassSchedule(
            class_id=strength_class.id,
            day_of_week=2,  # Wednesday
            start_time=time(18, 0),
            end_time=time(19, 0),
            room='Studio A'
        )
        db.session.add(schedule2)
        
        schedule3 = ClassSchedule(
            class_id=yoga_class.id,
            day_of_week=1,  # Tuesday
            start_time=time(8, 0),
            end_time=time(9, 15),
            room='Studio B'
        )
        db.session.add(schedule3)
        
        schedule4 = ClassSchedule(
            class_id=yoga_class.id,
            day_of_week=3,  # Thursday
            start_time=time(17, 0),
            end_time=time(18, 15),
            room='Studio B'
        )
        db.session.add(schedule4)
        
        schedule5 = ClassSchedule(
            class_id=cardio_class.id,
            day_of_week=4,  # Friday
            start_time=time(7, 0),
            end_time=time(7, 45),
            room='Studio A'
        )
        db.session.add(schedule5)
        
        schedule6 = ClassSchedule(
            class_id=pilates_class.id,
            day_of_week=5,  # Saturday
            start_time=time(9, 0),
            end_time=time(10, 0),
            room='Studio B'
        )
        db.session.add(schedule6)
        
        db.session.commit()
        
        print("Database initialization completed successfully!")
        print("\nDefault accounts created:")
        print("Admin: admin/admin123")
        print("Trainer: john_trainer/trainer123")
        print("Trainer: sarah_trainer/trainer123")
        print("Member: mike_member/member123")
        print("Member: lisa_member/member123")

if __name__ == '__main__':
    init_database()
