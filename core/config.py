import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database configuration
    DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration


settings = Config()
