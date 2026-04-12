import pyotp
from typing import Optional, Tuple

from app.config.settings import settings


class TOTPService:
    """Service for TOTP (Time-based One-Time Password) MFA"""
    
    def generate_secret(self) -> str:
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    def generate_qr_code_url(self, secret: str, email: str) -> str:
        """
        Generate QR code URL for TOTP setup
        
        Args:
            secret: TOTP secret
            email: Admin user email
        
        Returns:
            str: QR code URL
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=email,
            issuer_name=settings.PROJECT_NAME
        )
    
    def verify_totp(self, secret: str, token: str) -> bool:
        """
        Verify TOTP token
        
        Args:
            secret: TOTP secret
            token: 6-digit TOTP code
        
        Returns:
            bool: True if valid
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)
    
    def generate_backup_codes(self, count: int = 10) -> list[str]:
        """
        Generate backup codes for MFA recovery
        
        Args:
            count: Number of backup codes to generate
        
        Returns:
            List of backup codes
        """
        codes = []
        for _ in range(count):
            code = pyotp.random_base32(length=8).upper()
            # Format as XXXXX-XXXXX
            formatted_code = f"{code[:5]}-{code[5:]}"
            codes.append(formatted_code)
        return codes


totp_service = TOTPService()
