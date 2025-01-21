
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.controller import constants

import os

# Default to a test database URL, but allow it to be overridden by an environment variable
if os.getenv('TEST_TYPE') == 'selenium' or os.getenv('LOCAL_ENV') == 'host':
    # Use a specific database URL for Selenium tests (e.g., separate SQLite for UI testing)
    DATABASE_URL = constants.DATABASE_URL
elif os.getenv('TEST_TYPE') == 'integration' or os.getenv('LOCAL_ENV') == 'test':
    # Use the database URL for integration tests
    DATABASE_URL = constants.DATABASE_URL_TEST

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine)