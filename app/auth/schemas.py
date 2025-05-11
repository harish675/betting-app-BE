
from pydantic import BaseModel


class SendOtpRequest(BaseModel):
    mobile_number: str

class VerifyOtpRequest(BaseModel):
    mobile_number: str
    otp: str

class EmailOtpRequest(BaseModel):
    email: str

class VerifyEmailOtpRequest(BaseModel):
    email: str
    otp: str 

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
