"""
MongoDB Connection and Management
Using Motor async driver
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config.settings import settings

client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None


async def connect_db():
    """Connect to MongoDB"""
    global client, db
    
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        # Verify connection
        await client.admin.command("ping")
        db = client[settings.MONGO_DB_NAME]
        
        # Create indexes
        await create_indexes()
        print("✅ Connected to MongoDB successfully")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise


async def disconnect_db():
    """Disconnect from MongoDB"""
    global client
    
    if client is not None:
        client.close()
        print("✅ Disconnected from MongoDB")


async def create_indexes():
    """Create database indexes for performance"""
    if db is None:
        return
    
    try:
        # Users collection indexes
        users = db["users"]
        await users.create_index("email", unique=True)
        
        # Policies collection indexes
        policies = db["policies"]
        await policies.create_index("title", unique=True)
        await policies.create_index("state")
        await policies.create_index("category")
        await policies.create_index("created_at")
        
        # Uploads collection indexes
        uploads = db["uploads"]
        await uploads.create_index("user_id")
        await uploads.create_index("status")
        await uploads.create_index("created_at")
        
        # Notifications collection indexes
        notifications = db["notifications"]
        await notifications.create_index("created_at")
        
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"⚠️  Error creating indexes: {e}")


def get_db() -> AsyncIOMotorDatabase:
    """Get database instance"""
    if db is None:
        raise RuntimeError("Database not connected")
    return db
