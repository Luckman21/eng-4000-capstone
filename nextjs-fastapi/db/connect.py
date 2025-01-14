
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.controller import constants

engine = create_engine(constants.DATABASE_URL_TEST, echo=True)
session = sessionmaker(bind=engine)