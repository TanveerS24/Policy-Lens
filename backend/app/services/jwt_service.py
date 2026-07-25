"""JWT token service."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, Dict
from jose import jwt, JWTError

from app.config.settings import get_settings

settings = get_settings()


class JWTService:
    """Service for JWT token creation and verification."""
    
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = "HS256" if settings.DEBUG else settings.JWT_ALGORITHM
        self.access_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.refresh_expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    def create_tokens(self, user_id: int, role: str = "patient") -> Tuple[str, str]:
        """Create access and refresh tokens."""
        now = datetime.now(timezone.utc)
        
        # Access token
        access_payload = {
            "sub": str(user_id),
            "role": role,
            "type": "access",
            "iat": now,
            "exp": now + self.access_expire,
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)
        
        # Refresh token
        refresh_payload = {
            "sub": str(user_id),
            "role": role,
            "type": "refresh",
            "iat": now,
            "exp": now + self.refresh_expire,
        }
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)
        
        return access_token, refresh_token
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check token type
            if payload.get("type") != token_type:
                return None
            
            return payload
        except JWTError:
            return None
    
    def get_user_id_from_token(self, token: str) -> Optional[int]:
        """Extract user ID from token."""
        payload = self.verify_token(token)
        if payload:
            return int(payload.get("sub"))
        return None
