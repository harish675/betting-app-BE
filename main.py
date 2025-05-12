from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session

from .app.router import router
from .db.session import get_session

app = FastAPI()

db_session = Annotated[Session, Depends(get_session)]

app.include_router(router, prefix="/api")
