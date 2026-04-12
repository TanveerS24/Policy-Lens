import secrets

from datetime import timedelta

from typing import Optional



from app.utils.redis_client import redis_client

from app.utils.security import create_token, hash_password, verify_password





class AuthService:

    OTP_TTL_SECONDS = 300



    async def create_user(self, db, email: str, password: str, full_name: Optional[str] = None):

        existing = await db["users"].find_one({"email": email.lower()})

        if existing:

            raise ValueError("Email already registered")

        hashed = hash_password(password)

        result = await db["users"].insert_one(

            {"email": email.lower(), "hashed_password": hashed, "full_name": full_name, "is_admin": False, "is_active": True}

        )

        return str(result.inserted_id)



    async def authenticate(self, db, email: str, password: str) -> Optional[str]:

        user = await db["users"].find_one({"email": email.lower()})

        if not user:

            return None

        if not verify_password(password, user.get("hashed_password")):

            return None

        return str(user.get("_id"))



    async def create_tokens(self, user_id: str):

        access = create_token(user_id, expires_delta=timedelta(minutes=15), token_type="access")

        refresh = create_token(user_id, expires_delta=timedelta(days=7), token_type="refresh")

        redis = await redis_client.get_client()

        await redis.set(f"refresh:{user_id}", refresh, ex=7 * 24 * 3600)

        return access, refresh



    async def verify_refresh_token(self, refresh_token: str):

        from app.utils.security import decode_token



        payload = decode_token(refresh_token)

        if not payload or payload.get("type") != "refresh":

            return None

        user_id = payload.get("sub")

        if not user_id:

            return None

        redis = await redis_client.get_client()

        saved = await redis.get(f"refresh:{user_id}")

        if saved != refresh_token:

            return None

        return user_id



    async def create_otp(self, email: str) -> str:

        code = f"{secrets.randbelow(999999):06d}"

        redis = await redis_client.get_client()

        await redis.set(f"otp:{email.lower()}", code, ex=self.OTP_TTL_SECONDS)

        return code



    async def verify_otp(self, email: str, otp: str) -> bool:

        redis = await redis_client.get_client()

        stored = await redis.get(f"otp:{email.lower()}")

        if not stored:

            return False

        if stored != otp:

            return False

        await redis.delete(f"otp:{email.lower()}")

        return True





auth_service = AuthService()

