import secrets
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId

from app.config.settings import settings
from app.utils.redis_client import redis_client
from app.utils.security import create_token, hash_password, verify_password
from app.services.sms_service import sms_service


class PatientAuthService:
    """Authentication service for patients using mobile + OTP"""
    
    async def create_otp(self, mobile: str, purpose: str = "registration", ip: str = None, device_fingerprint: str = None) -> dict:
        """
        Create and send OTP to mobile number
        
        Args:
            mobile: 10-digit mobile number
            purpose: registration, login, forgot_password, mobile_change
            ip: Client IP address
            device_fingerprint: Device fingerprint for security
        
        Returns:
            dict with success status and message
        """
        # Rate limiting: Check OTP requests per hour per mobile
        redis = await redis_client.get_client()
        rate_limit_key = f"otp_rate:{mobile}"
        current_requests = await redis.get(rate_limit_key)
        
        if current_requests and int(current_requests) >= settings.OTP_MAX_REQUESTS_PER_HOUR:
            return {"success": False, "message": f"Maximum OTP requests reached. Please try again later."}
        
        # Generate 6-digit OTP
        otp = f"{secrets.randbelow(999999):06d}"
        otp_hash = hash_password(otp)
        
        # Calculate expiry
        expires_at = datetime.utcnow() + timedelta(seconds=settings.OTP_TTL_SECONDS)
        
        # Store OTP in database for audit
        from app.database.client import get_db
        db = get_db()
        
        # Invalidate any previous pending OTP for this mobile and purpose
        await db["otp_logs"].update_many(
            {"mobile": mobile, "purpose": purpose, "status": "pending"},
            {"$set": {"status": "expired"}}
        )
        
        # Create new OTP log
        await db["otp_logs"].insert_one({
            "mobile": mobile,
            "otp_hash": otp_hash,
            "purpose": purpose,
            "attempt_count": 0,
            "status": "pending",
            "ip_address": ip,
            "device_fingerprint": device_fingerprint,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at
        })
        
        # Increment rate limit counter
        await redis.incr(rate_limit_key)
        await redis.expire(rate_limit_key, 3600)  # 1 hour expiry
        
        # Send OTP via SMS
        sms_sent = await sms_service.send_otp(mobile, otp, purpose)
        
        if not sms_sent:
            return {"success": False, "message": "Failed to send OTP. Please try again."}
        
        return {
            "success": True,
            "message": "OTP sent successfully",
            "expires_in": settings.OTP_TTL_SECONDS
        }
    
    async def verify_otp(self, mobile: str, otp: str, purpose: str = "registration") -> dict:
        """
        Verify OTP for mobile number
        
        Args:
            mobile: 10-digit mobile number
            otp: 6-digit OTP code
            purpose: registration, login, forgot_password, mobile_change
        
        Returns:
            dict with success status and message
        """
        from app.database.client import get_db
        db = get_db()
        
        # Find latest pending OTP for this mobile and purpose
        otp_log = await db["otp_logs"].find_one({
            "mobile": mobile,
            "purpose": purpose,
            "status": "pending"
        }, sort=[("created_at", -1)])
        
        if not otp_log:
            return {"success": False, "message": "Invalid or expired OTP. Please request a new OTP."}
        
        # Check if OTP is expired
        if otp_log["expires_at"] < datetime.utcnow():
            await db["otp_logs"].update_one(
                {"_id": otp_log["_id"]},
                {"$set": {"status": "expired"}}
            )
            return {"success": False, "message": "OTP has expired. Please request a new OTP."}
        
        # Check attempt count
        if otp_log["attempt_count"] >= settings.OTP_MAX_ATTEMPTS:
            await db["otp_logs"].update_one(
                {"_id": otp_log["_id"]},
                {"$set": {"status": "failed"}}
            )
            return {"success": False, "message": "Maximum OTP attempts reached. Please request a new OTP."}
        
        # Verify OTP
        if not verify_password(otp, otp_log["otp_hash"]):
            # Increment attempt count
            await db["otp_logs"].update_one(
                {"_id": otp_log["_id"]},
                {"$inc": {"attempt_count": 1}}
            )
            remaining_attempts = settings.OTP_MAX_ATTEMPTS - otp_log["attempt_count"] - 1
            return {
                "success": False,
                "message": f"Invalid OTP. {remaining_attempts} attempts remaining."
            }
        
        # Mark OTP as verified
        await db["otp_logs"].update_one(
            {"_id": otp_log["_id"]},
            {
                "$set": {
                    "status": "verified",
                    "verified_at": datetime.utcnow()
                }
            }
        )
        
        return {"success": True, "message": "OTP verified successfully"}
    
    async def create_patient(self, db, patient_data: dict) -> str:
        """
        Create new patient account after OTP verification
        
        Args:
            db: Database instance
            patient_data: Patient registration data
        
        Returns:
            str: Patient ID
        """
        # Check if mobile already exists
        existing = await db["patients"].find_one({"mobile": patient_data["mobile"]})
        if existing:
            raise ValueError("Mobile number already registered")
        
        # Check if email exists (if provided)
        if patient_data.get("email"):
            existing_email = await db["patients"].find_one({"email": patient_data["email"]})
            if existing_email:
                raise ValueError("Email already registered")
        
        # Validate state and district
        state = await db["states"].find_one({"_id": ObjectId(patient_data["state_id"]), "active": True})
        if not state:
            raise ValueError("Invalid state")
        
        district = await db["districts"].find_one({"_id": ObjectId(patient_data["district_id"]), "active": True})
        if not district:
            raise ValueError("Invalid district")
        
        # Validate district belongs to state
        if str(district["state_id"]) != patient_data["state_id"]:
            raise ValueError("District does not belong to the selected state")
        
        # Hash password
        hashed_password = hash_password(patient_data["password"])
        
        # Create patient
        patient_doc = {
            "full_name": patient_data["full_name"],
            "date_of_birth": patient_data["date_of_birth"],
            "gender": patient_data["gender"],
            "mobile": patient_data["mobile"],
            "email": patient_data.get("email"),
            "state_id": patient_data["state_id"],
            "district_id": patient_data["district_id"],
            "pin_code": patient_data["pin_code"],
            "hashed_password": hashed_password,
            "mobile_verified": True,  # Already verified via OTP
            "email_verified": False,
            "profile_photo_url": None,
            "notification_sms": True,
            "notification_push": True,
            "status": "active",
            "failed_login_attempts": 0,
            "locked_until": None,
            "deactivated_at": None,
            "deletion_requested_at": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db["patients"].insert_one(patient_doc)
        
        # Send welcome SMS
        await sms_service.send_welcome_message(patient_data["mobile"], patient_data["full_name"])
        
        return str(result.inserted_id)
    
    async def authenticate(self, db, mobile: str, password: str) -> Optional[str]:
        """
        Authenticate patient with mobile and password
        
        Args:
            db: Database instance
            mobile: 10-digit mobile number
            password: Password
        
        Returns:
            str: Patient ID if authenticated, None otherwise
        """
        patient = await db["patients"].find_one({"mobile": mobile})
        
        if not patient:
            return None
        
        # Check account status
        if patient["status"] == "deactivated":
            raise ValueError("Account is deactivated. Please contact support.")
        if patient["status"] == "deleted":
            raise ValueError("Account has been deleted.")
        
        # Check if account is locked
        if patient["locked_until"] and patient["locked_until"] > datetime.utcnow():
            remaining_minutes = int((patient["locked_until"] - datetime.utcnow()).total_seconds() / 60)
            raise ValueError(f"Account is locked. Please try again after {remaining_minutes} minutes.")
        
        # Verify password
        if not verify_password(password, patient["hashed_password"]):
            # Increment failed login attempts
            await db["patients"].update_one(
                {"_id": patient["_id"]},
                {"$inc": {"failed_login_attempts": 1}}
            )
            
            # Check if should lock account
            updated_patient = await db["patients"].find_one({"_id": patient["_id"]})
            if updated_patient["failed_login_attempts"] >= settings.MAX_LOGIN_ATTEMPTS:
                lock_until = datetime.utcnow() + timedelta(minutes=settings.ACCOUNT_LOCKOUT_MINUTES)
                await db["patients"].update_one(
                    {"_id": patient["_id"]},
                    {"$set": {"locked_until": lock_until}}
                )
                raise ValueError(f"Account locked due to too many failed attempts. Please try again after {settings.ACCOUNT_LOCKOUT_MINUTES} minutes.")
            
            return None
        
        # Reset failed login attempts on successful login
        await db["patients"].update_one(
            {"_id": patient["_id"]},
            {
                "$set": {
                    "failed_login_attempts": 0,
                    "locked_until": None,
                    "last_login": datetime.utcnow()
                }
            }
        )
        
        return str(patient["_id"])
    
    async def create_tokens(self, user_id: str):
        """
        Create access and refresh tokens
        
        Args:
            user_id: Patient ID
        
        Returns:
            tuple: (access_token, refresh_token)
        """
        access = create_token(user_id, expires_delta=timedelta(hours=1), token_type="access")
        refresh = create_token(user_id, expires_delta=timedelta(days=30), token_type="refresh")
        
        redis = await redis_client.get_client()
        await redis.set(f"refresh:{user_id}", refresh, ex=30 * 24 * 3600)
        
        return access, refresh
    
    async def verify_refresh_token(self, refresh_token: str):
        """
        Verify refresh token
        
        Args:
            refresh_token: Refresh token
        
        Returns:
            str: User ID if valid, None otherwise
        """
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
    
    async def revoke_all_sessions(self, user_id: str):
        """
        Revoke all sessions for a user
        
        Args:
            user_id: Patient ID
        """
        redis = await redis_client.get_client()
        await redis.delete(f"refresh:{user_id}")
        
        from app.database.client import get_db
        db = get_db()
        await db["user_sessions"].update_many(
            {"user_id": user_id},
            {"$set": {"revoked": True, "revoked_at": datetime.utcnow()}}
        )


patient_auth_service = PatientAuthService()
