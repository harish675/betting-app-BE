
from passlib.context import CryptContext

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return pwd_content.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.
    """
    return pwd_content.verify(plain_password, hashed_password)


