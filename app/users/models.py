from sqlmodel import Field, SQLModel
import uuid
from datetime import datetime ,timezone   

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    email: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    date_joined: datetime = Field(default_factory=datetime.utcnow)
    mobile_number: str | None = Field(default=None)
    kyc_status: bool = Field(default=False)
    is_active: bool = Field(default=True)
    dob_date: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_by: str | None = Field(default_factory=lambda: "test_user")