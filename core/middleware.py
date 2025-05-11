
from fastapi import HTTPException, status, Header ,Request
from ..app.auth.services import AuthService
from pydantic import BaseModel
import jwt
from ..db.session import get_session
class UserInfo(BaseModel):
    email:str
    first_name:str
    last_name:str

auth_service = AuthService()

def authentication(request: Request)-> None:
    authorization = request.headers.get("Authorization")
    print("authorization",authorization)
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    # Example: Bearer token parsing
    token = authorization.split(" ")[1] if " " in authorization else authorization
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing"
        )
    try:
        user_details = auth_service.get_current_user()
        user = UserInfo(email=user_details.email,first_name=user_details.first_name,last_name=user_details.last_name)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired. Please log in again."
        )
    
    request.state.user = user
