from argon2 import PasswordHasher
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

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

    def check_password(self, email: str, password: str, db : Session) -> bool:

        user = db.query(User).filter_by(email=email).first()

        if user:
            return self.verify_password(user.password, password)


