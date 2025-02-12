from argon2 import PasswordHasher
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError
from sqlalchemy.orm import Session
from db.model.User import User

ph = PasswordHasher()


class PasswordHashService:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash the password
        """
        return ph.hash(password)

    @staticmethod
    def verify_password(stored_hash: str, password: str) -> bool:
        """
        Verify if the password matches the stored hash.
        """
        try:
            ph.verify(stored_hash, password)
            return True

        except Exception:
            return False

    @staticmethod
    def check_password(email: str, password: str, db : Session) -> bool:

        user = db.query(User).filter_by(email=email).first()

        if user:
            return PasswordHashService.verify_password(user.password, password)