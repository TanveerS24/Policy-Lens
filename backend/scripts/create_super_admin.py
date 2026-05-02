#!/usr/bin/env python3
"""Script to create the initial super admin user."""

import os
import sys
import bcrypt

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.config.database import SessionLocal, engine, Base
from app.models.admin import AdminUser, AdminRole, AdminStatus


def create_super_admin(email: str, password: str, name: str = "Super Admin"):
    """Create the initial super admin user."""
    db = SessionLocal()
    
    try:
        # Check if any admin already exists
        existing_admin = db.query(AdminUser).first()
        if existing_admin:
            print("Error: An admin user already exists. Use the API to create additional admins.")
            sys.exit(1)
        
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
        print(f"\nYou can now log in at: http://localhost:5173 (admin frontend)")
        print(f"API endpoint: POST http://localhost:8000/api/v1/admin/login")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating super admin: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create the initial super admin user")
    parser.add_argument("--email", default="admin@dentalschemes.in", help="Admin email")
    parser.add_argument("--password", default="admin123", help="Admin password")
    parser.add_argument("--name", default="Super Admin", help="Admin name")
    
    args = parser.parse_args()
    
    # Confirm before creating with default credentials
    if args.email == "admin@dentalschemes.in" and args.password == "admin123":
        print("⚠️  Warning: Creating admin with default credentials.")
        print("   Email: admin@dentalschemes.in")
        print("   Password: admin123")
        print("\n   It's recommended to change these after first login!\n")
        
        response = input("Continue? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    
    create_super_admin(args.email, args.password, args.name)
