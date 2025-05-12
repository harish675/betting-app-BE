
from pydantic import BaseModel


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    mobile_number: str
    password: str
    confirm_password: str
    dob_date: str


