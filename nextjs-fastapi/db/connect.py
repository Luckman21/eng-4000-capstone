
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.controller import constants

import os

if os.getenv("CI"):  # If in CI environment
    DATABASE_URL = "sqlite:///:memory:"  # Use in-memory database
else:
    DATABASE_URL = constants.DATABASE_URL_TEST  # Local file-based DB


engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine)