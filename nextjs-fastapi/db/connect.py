
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.controller import constants

import os

# # Default to a test database URL, but allow it to be overridden by an environment variable
# if os.getenv('TEST_TYPE') == 'selenium' or os.getenv('LOCAL_ENV') == 'host':
#     # Use a specific database URL for Selenium tests (e.g., separate SQLite for UI testing)
#     DATABASE_URL = constants.DATABASE_URL
# elif os.getenv('TEST_TYPE') == 'integration' or os.getenv('LOCAL_ENV') == 'test':
#     # Use the database URL for integration tests
#     DATABASE_URL = constants.DATABASE_URL_TEST
# else:

#     raise Exception("Wrong DB access command. Please either use 'host' or 'test'")

# Create the SQLAlchemy engine and session
DATABASE_URL = constants.DATABASE_URL
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # Keep up to 10 connections open
    max_overflow=20,        # Allow 20 more temporary connections
    pool_timeout=30,        # Wait up to 30 seconds for a connection before failing
    pool_recycle=1800,      # Recycle connections every 30 minutes
    echo=True
)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)