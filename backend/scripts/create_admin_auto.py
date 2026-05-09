#!/usr/bin/env python3
"""Script to create admin user without interactive prompts"""

import os
import sys
import bcrypt

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.config.database import SessionLocal, engine, Base
from app.models.admin import AdminUser, AdminRole, AdminStatus


def create_super_admin_auto(email: str, password: str, name: str = "Super Admin"):
    """Create the initial super admin user without prompts."""
    db = SessionLocal()
    
    try:
        # Check if any admin already exists
        existing_admin = db.query(AdminUser).first()
        if existing_admin:
            print(f"Admin already exists: {existing_admin.email}")
            return False
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # Create super admin
        super_admin = AdminUser(
            name=name,
            email=email,
            hashed_password=hashed_password,
            role=AdminRole.SUPER_ADMIN.value,
            status=AdminStatus.ACTIVE.value,
            created_by=None,  # First admin has no creator
        )
        
        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)
        
        print(f"✅ Super admin created successfully!")
        print(f"   Email: {email}")
        print(f"   Name: {name}")
        print(f"   Role: {super_admin.role}")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"Error creating super admin: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    create_super_admin_auto("admin@dentalschemes.in", "admin123", "Super Admin")
