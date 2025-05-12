
from fastapi import APIRouter , Depends ,Request
from sqlalchemy.orm import Session
from typing import Annotated
from .schemas import SendOtpRequest ,VerifyOtpRequest ,EmailOtpRequest, VerifyEmailOtpRequest ,LoginRequest
from .services import AuthService
from ...db.session import get_session

router = APIRouter()
user_router = APIRouter()
auth_service = AuthService()  # Placeholder for the AuthService instance


@router.post("/send-otp")
def send_otp(mobile_number:SendOtpRequest):
   return auth_service.send_otp(mobile_number.model_dump())

@router.post("/verify-otp")
def verify_otp(payload: VerifyOtpRequest):
    """
    Verify the provided OTP.
    """
    return auth_service.verify_otp(payload.model_dump())

@router.post("/resend-otp")
def resend_otp(payload: SendOtpRequest):
    """
    Resend the OTP to the provided mobile number.
    """
    return auth_service.send_otp(payload.model_dump())

@router.post("/email-send-otp")
def send_email_verification_otp(payload:EmailOtpRequest):
    return auth_service.send_email_verification_otp(payload.model_dump())

@router.post("/email-verify-otp")
def verify_email_verification_otp(payload:VerifyEmailOtpRequest):
    return auth_service.verify_email_verification_otp(payload.model_dump())

@router.post("/resend-email-otp")
def resend_email_verification_otp(payload:EmailOtpRequest):
    return auth_service.resend_email_verification_otp(payload.model_dump())

@user_router.post("/login")
def user_login(payload:LoginRequest,session:Session = Depends(get_session)):
    """
    User login endpoint.
    """
    return auth_service.user_login(payload.model_dump(),session)

@router.get("/users/me/")
async def read_users_me(request:Request,deb_session:Session = Depends(get_session)):
       return request.state.user