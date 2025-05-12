from fastapi import APIRouter , Depends
from .services import UserService
from  .schemas import CreateUser
from  sqlalchemy.orm import Session
from ...db.session import get_session

router = APIRouter()

service = UserService()

@router.post("/")
async def create_user(payload:CreateUser ,session:Session = Depends(get_session)):
    return service.create_user(payload.model_dump(),session)
