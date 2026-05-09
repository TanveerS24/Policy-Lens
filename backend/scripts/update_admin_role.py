#!/usr/bin/env python3
"""Script to update admin user role"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.admin import AdminUser


def update_admin_role(email: str, new_role: str):
    """Update admin user role."""
    db = SessionLocal()
    
    try:
        admin = db.query(AdminUser).filter(AdminUser.email == email).first()
        if not admin:
            print(f"Admin not found: {email}")
            return False
        
        old_role = admin.role
        admin.role = new_role
        db.commit()
        
        print(f"✅ Admin role updated successfully!")
        print(f"   Email: {email}")
        print(f"   Old role: {old_role}")
        print(f"   New role: {new_role}")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"Error updating admin role: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    update_admin_role("supportadmin@policylens.in", "content_admin")
