
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.controller import constants


# Create the SQLAlchemy engine and session
DATABASE_URL = constants.DATABASE_URL
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,        # Wait up to 30 seconds for a connection before failing
    pool_recycle=1800,      # Recycle connections every 30 minutes
    echo=True
)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)