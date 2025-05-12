
from fastapi import HTTPException,status,Request ,Depends
from ...app.auth.services import AuthService
from ...db.session import get_session
from pydantic import BaseModel
from sqlalchemy.orm import Session
import jwt



class UserInfo(BaseModel):
    email:str
    first_name:str
    last_name:str

auth_service = AuthService()
async def authentication(request: Request ,db_session:Session=Depends(get_session))-> None:
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
        user_details = await auth_service.get_current_user(token,db_session)
        print("user_details:::::::::::",type(user_details))
        user = UserInfo(email=user_details.email,first_name=user_details.first_name,last_name=user_details.last_name)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired. Please log in again."
        )
    
    request.state.user = user
