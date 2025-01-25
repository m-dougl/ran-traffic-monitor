import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

try:
    POSTGRES_APP_USER = os.getenv("POSTGRES_APP_USER")
    POSTGRES_APP_PASSWORD = os.getenv("POSTGRES_APP_PASSWORD")
    POSTGRES_APP_DB = os.getenv("POSTGRES_APP_DB")
    POSTGRES_APP_HOST = os.getenv("POSTGRES_APP_HOST")
    POSTGRES_APP_PORT = os.getenv("POSTGRES_APP_PORT")

    if not all(
        [
            POSTGRES_APP_USER,
            POSTGRES_APP_PASSWORD,
            POSTGRES_APP_DB,
            POSTGRES_APP_HOST,
            POSTGRES_APP_PORT,
        ]
    ):
        raise ValueError("One or more environment variables are missing")

    DATABASE = f"postgresql+psycopg2://{POSTGRES_APP_USER}:{POSTGRES_APP_PASSWORD}@{POSTGRES_APP_HOST}:{POSTGRES_APP_PORT}/{POSTGRES_APP_DB}"
    engine = create_engine(DATABASE)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    logger.info("Database engine created successfully")

except Exception as e:
    logger.error(f"Error setting up database: {e}")
    raise ValueError(f"Error setting up database: {e}")


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise ValueError(f"Error initializing database: {e}")


def get_session() -> Session:
    session = SessionLocal()
    return session
