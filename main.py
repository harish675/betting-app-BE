from fastapi import  FastAPI ,Depends
from .app.router import router
from typing import Annotated
from .db.session import get_session
from sqlmodel import Session


app = FastAPI()

db_session = Annotated[Session, Depends(get_session)]

# app.include_router(router, prefix="/api/v1", tags=["v1"] ,dependencies=[db_session])

app.include_router(router, prefix="/api/v2", tags=["v2"])

