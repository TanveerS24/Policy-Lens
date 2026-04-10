from app.database.client import get_db


async def ensure_indexes() -> None:
    db = get_db()
    await db["users"].create_index("email", unique=True)
    await db["policies"].create_index([("title", "text"), ("short_description", "text"), ("summary", "text")])
    await db["uploads"].create_index("owner_id")
    await db["notifications"].create_index("user_id")
