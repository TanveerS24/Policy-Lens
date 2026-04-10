"""Utility script to create an admin user in MongoDB."""

import getpass

from app.database.client import get_db
from app.utils.security import hash_password


async def create_admin():
    email = input("Admin email: ")
    password = getpass.getpass("Password: ")
    name = input("Full name: ")

    db = get_db()
    existing = await db["users"].find_one({"email": email.lower()})
    if existing:
        print("User already exists")
        return

    await db["users"].insert_one(
        {
            "email": email.lower(),
            "hashed_password": hash_password(password),
            "full_name": name,
            "is_admin": True,
            "is_active": True,
        }
    )
    print("Admin user created")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_admin())
