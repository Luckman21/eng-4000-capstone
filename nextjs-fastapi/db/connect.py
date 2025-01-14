
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.controller import constants

DATABASE_URL = constants.DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine)