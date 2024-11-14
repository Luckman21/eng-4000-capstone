from sqlalchemy.orm import Session
from db.connect import session

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
