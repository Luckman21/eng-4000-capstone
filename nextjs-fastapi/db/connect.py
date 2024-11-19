
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "sqlite:///nextjs-fastapi/db/capstone_db.db"
engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine)