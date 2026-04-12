import httpx
from typing import Optional

from app.config.settings import settings


class SMSService:
    """SMS service using MSG91 gateway"""
    
    def __init__(self):
        self.api_key = settings.MSG91_API_KEY
        self.sender_id = settings.MSG91_SENDER_ID
        self.template_id = settings.MSG91_TEMPLATE_ID
        self.base_url = "https://api.msg91.com/api/v5/flow"
    
    async def send_otp(self, mobile: str, otp: str, purpose: str = "registration") -> bool:
        """
        Send OTP via SMS using MSG91
        
        Args:
            mobile: 10-digit mobile number
            otp: 6-digit OTP code
            purpose: Purpose of OTP (registration, login, forgot_password, etc.)
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            payload = {
                "template_id": self.template_id,
                "sender": self.sender_id,
                "mobiles": f"91{mobile}",
                "OTP": otp,
                "purpose": purpose.replace("_", " ").title()
            }
            
            headers = {
                "authkey": self.api_key,
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return True
                else:
                    print(f"SMS sending failed: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return False
    
    async def send_welcome_message(self, mobile: str, name: str) -> bool:
        """Send welcome message after registration"""
        try:
            payload = {
                "template_id": self.template_id,
                "sender": self.sender_id,
                "mobiles": f"91{mobile}",
                "name": name,
                "message": f"Welcome to DentalSchemes India, {name}! Your account has been created successfully."
            }
            
            headers = {
                "authkey": self.api_key,
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=10.0
                )
                
                return response.status_code == 200
                
        except Exception as e:
            print(f"Error sending welcome SMS: {str(e)}")
            return False
    
    async def send_password_reset_otp(self, mobile: str, otp: str) -> bool:
        """Send password reset OTP"""
        return await self.send_otp(mobile, otp, "forgot_password")
    
    async def send_mobile_change_otp(self, mobile: str, otp: str) -> bool:
        """Send OTP for mobile number change verification"""
        return await self.send_otp(mobile, otp, "mobile_change")


sms_service = SMSService()
