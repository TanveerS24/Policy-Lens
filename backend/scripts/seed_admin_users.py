import asyncio
import sys
from datetime import datetime

sys.path.insert(0, "/app")

from app.database.client import get_db
from app.utils.security import hash_password


async def seed_admin_users():
    db = get_db()
    
    # Check if admin users already exist
    existing_count = await db["admin_users"].count_documents({})
    if existing_count > 0:
        print(f"Admin users already seeded ({existing_count} records). Skipping.")
        return
    
    # Seed default super admin
    hashed_password = hash_password("Admin@123456")
    
    admin_doc = {
        "name": "Super Admin",
        "email": "admin@policylens.in",
        "hashed_password": hashed_password,
        "role": "super_admin",
        "status": "active",
        "mfa_enabled": False,
        "force_password_change": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db["admin_users"].insert_one(admin_doc)
    print(f"Seeded super admin with ID: {result.inserted_id}")
    
    # Seed content admin
    content_admin_doc = {
        "name": "Content Admin",
        "email": "content@policylens.in",
        "hashed_password": hash_password("Content@123456"),
        "role": "content_admin",
        "status": "active",
        "mfa_enabled": False,
        "force_password_change": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db["admin_users"].insert_one(content_admin_doc)
    print(f"Seeded content admin with ID: {result.inserted_id}")
    
    # Seed support admin
    support_admin_doc = {
        "name": "Support Admin",
        "email": "support@policylens.in",
        "hashed_password": hash_password("Support@123456"),
        "role": "support_admin",
        "status": "active",
        "mfa_enabled": False,
        "force_password_change": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db["admin_users"].insert_one(support_admin_doc)
    print(f"Seeded support admin with ID: {result.inserted_id}")
    
    print("Admin users seeding completed.")


if __name__ == "__main__":
    asyncio.run(seed_admin_users())
