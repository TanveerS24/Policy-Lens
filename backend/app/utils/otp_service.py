"""
OTP Service
Manages One-Time Passwords for authentication
"""

import random
import string
from redis import asyncio as aioredis
from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

redis_client = None


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = await aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf8",
            decode_responses=True
        )
        logger.info("✅ Redis connection established")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Redis: {e}")
        raise


async def close_redis():
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("✅ Redis connection closed")


def generate_otp() -> str:
    """Generate random OTP"""
    return ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))


async def store_otp(email: str, otp: str) -> bool:
    """Store OTP in Redis with expiry"""
    try:
        key = f"otp:{email}"
        await redis_client.setex(
            key,
            settings.OTP_EXPIRY_MINUTES * 60,
            otp
        )
        logger.info(f"✅ OTP stored for {email}")
        return True
    except Exception as e:
        logger.error(f"❌ Error storing OTP: {e}")
        return False


async def verify_otp(email: str, otp: str) -> bool:
    """Verify OTP from Redis"""
    try:
        key = f"otp:{email}"
        stored_otp = await redis_client.get(key)
        
        if stored_otp and stored_otp == otp:
            await redis_client.delete(key)
            logger.info(f"✅ OTP verified for {email}")
            return True
        
        logger.warning(f"⚠️  Invalid OTP for {email}")
        return False
    except Exception as e:
        logger.error(f"❌ Error verifying OTP: {e}")
        return False


async def delete_otp(email: str) -> bool:
    """Delete OTP from Redis"""
    try:
        key = f"otp:{email}"
        await redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"❌ Error deleting OTP: {e}")
        return False
