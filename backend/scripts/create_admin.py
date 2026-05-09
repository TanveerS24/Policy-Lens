#!/usr/bin/env python3
"""Simple script to create admin user"""

import sys
import os
sys.path.append('backend')

import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.admin import AdminUser, AdminRole, AdminStatus

# Database URL from .env
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/dentalschemes"

def create_admin():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing = db.query(AdminUser).first()
        if existing:
            print(f"Admin already exists: {existing.email}")
            return
        
        # Create super admin
        hashed_password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        
        admin = AdminUser(
            name="Super Admin",
            email="admin@dentalschemes.in",
            hashed_password=hashed_password,
            role=AdminRole.SUPER_ADMIN.value,
            status=AdminStatus.ACTIVE.value,
            created_by=None
        )
        
        db.add(admin)
        db.commit()
        print("✅ Super admin created successfully!")
        print("Email: admin@dentalschemes.in")
        print("Password: admin123")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
