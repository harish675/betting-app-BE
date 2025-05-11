import logging

from sqlalchemy.exc import OperationalError
from sqlmodel import Session, SQLModel, create_engine
import sqlmodel

from ..core.config import settings

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

database_url = settings.DATABASE_URI
print(f"Database URL: {database_url}")
if not database_url:
    logger.error("❌ DATABASE_URL is not set in the environment variables.")
    raise ValueError("DATABASE_URL is not set in the environment variables.")
# Initialize engine
try:
    engine = create_engine(
        settings.DATABASE_URI,
        echo=True,  # Set to False in production
    )
    logger.info("✅ PostgreSQL database engine created successfully.")
except OperationalError as e:
    logger.error("❌ Failed to create database engine.")
    logger.exception(e)
    raise


# Create all tables
def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("✅ Tables created successfully.")
    except Exception as e:
        logger.error("❌ Failed to create tables.")
        logger.exception(e)
        raise


# Dependency for session
def get_session():
    try:
        with Session(engine) as session:
            logger.debug("➡️ DB session started.")
            yield session
            logger.debug("✅ DB session ended.")
    except Exception as e:
        logger.error("❌ Failed during DB session.")
        logger.exception(e)
        raise
