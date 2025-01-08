
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# FOR TESTING, REPLACE WITH
# "sqlite:///nextjs-fastapi/db/capstone_db.db"
# FOR PROD USE:
# "sqlite:///../../db/capstone_db.db"

DATABASE_URL = "sqlite:///../../db/capstone_db.db"
engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine)