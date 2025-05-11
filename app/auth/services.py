import secrets
from fastapi import HTTPException
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from ...core.config import settings
from ...services.twilio import TwilioService
from ...services.redis import RedisService
from ...services.email import EmailService
from ...curd.curd import DBOperation
from ..users.entities import IUser
from ..users.models import User
from .utility import verify_password ,create_access_token
from .schemas import Token ,TokenData

JWT_EXPIRATION_TIME  = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_otp(length: int = 6) -> str:
    """Generate a secure numeric OTP of given length."""
    digits = "0123456789"
    return ''.join(secrets.choice(digits) for _ in range(length))

class AuthService:
    def __init__(self):
        self.twilio = TwilioService()
        self.redis = RedisService()
        self.email_service = EmailService()
        self.db_operations = DBOperation()

    def send_otp(self,payload):
        mobile_number = payload.get("mobile_number")
        if not mobile_number:
            raise HTTPException(status_code=400, detail="Mobile number is required")
        # if len(mobile_number) != 10 or not mobile_number.isdigit():
        #     raise HTTPException(status_code=400, detail="Invalid mobile number")
        # Generate OTP
        otp = generate_otp()
        self.redis.store_otp(mobile_number, otp)
        message = f"Your verification code is: {otp}"
        result = self.twilio.send_message(mobile_number, message)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
        return {
            "status":200,
            "message": "OTP sent successfully",
            "otp": otp
        }
    
    def verify_otp(self, payload):
        mobile_number = payload.get("mobile_number")
        otp = payload.get("otp")
        if not mobile_number or not otp:
            raise HTTPException(status_code=400, detail="Mobile number and OTP are required")
        # if len(mobile_number) != 10 or not mobile_number.isdigit():
        #     raise HTTPException(status_code=400, detail="Invalid mobile number")
        stored_otp = self.redis.get_otp(mobile_number)
        if not stored_otp:
            raise HTTPException(status_code=400, detail="OTP expired or not found")
        if stored_otp != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        self.redis.delete_otp(mobile_number)
        return {
            "status":200,
            "message": "OTP verified successfully"
        }
    
    def resend_otp(self, payload):
        mobile_number = payload.get("mobile_number")
        if not mobile_number:
            raise HTTPException(status_code=400, detail="Mobile number is required")
        # if len(mobile_number) != 10 or not mobile_number.isdigit():
        #     raise HTTPException(status_code=400, detail="Invalid mobile number")
        # Generate OTP
        otp = generate_otp()
        self.redis.store_otp(mobile_number, otp)
        message = f"Your verification code is: {otp}"
        result = self.twilio.send_message(mobile_number, message)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
        return {
            "status":200,
            "message": "OTP resent successfully",
            "otp": otp
        }
    
    def send_email_verification_otp(self, payload):
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        otp = generate_otp()
        self.redis.store_email_otp(email, otp)
        result = self.email_service.send_otp_email(email, otp)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
        return {
            "status":200,
            "message": "OTP sent successfully on email",
            "otp": otp
        }
    
    def verify_email_verification_otp(self, payload):
        email = payload.get("email")
        otp = payload.get("otp")
        if not email or not otp:
            raise HTTPException(status_code=400, detail="Email and OTP are required")
        
        stored_otp = self.redis.get_email_otp(email)
        if not stored_otp:
            raise HTTPException(status_code=400, detail="OTP expired or not found")
        if stored_otp != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        self.redis.delete_email_otp(email)
        return {
            "status":200,
            "message": "OTP verified successfully"
        }
    
    def resend_email_verification_otp(self, payload):
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        otp = generate_otp()
        self.redis.store_email_otp(email, otp)
        result = self.email_service.send_otp_email(email, otp)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to send OTP")
        return {
            "status":200,
            "message": "OTP resent successfully on email",
            "otp": otp
        }
    
    def user_login(self, payload,session):
        username = payload.get("username")
        password = payload.get("password")
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required")
        
        user_details = self.db_operations.read_one(table=User, query=User.username == username, session=session)

        if not user_details:
            raise HTTPException(status_code=404, detail="User not found")
        
        password_match = verify_password(password,user_details.password)
    
        if not password_match:
            raise HTTPException(status_code=401, detail="Invalid password/username")
        
        access_token_expires = timedelta(minutes=JWT_EXPIRATION_TIME)
        access_token = create_access_token(
            data={"sub": user_details.username},
            expires_delta=access_token_expires,
        )
        response_data = Token(access_token=access_token , token_type="bearer")
        return {
            "status": 200,
            "message": "Login successful",
            "data":response_data
        }
        
        # Placeholder for actual user authentication logic
        
    async def get_current_user(self,request,session,token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        # user = get_user(fake_users_db, username=token_data.username)
        user = self.db_operations.read_one(table=User, query=User.username == token_data.username ,session=session)
        if user is None:
            raise credentials_exception
        return user


  