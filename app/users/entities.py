
from typing import TypedDict


class IUser(TypedDict):
    id: int
    first_name: str
    last_name: str
    mobile_number: str
    dob_date: str
    date_joined: str
    kyc_status: bool
    username: str
    email: str
    is_active: bool
    created_at: str
    updated_at: str
    updated_by: str