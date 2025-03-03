from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Warning(Base):
    __tablename__ = 'warnings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)


    def setTitle(self, newTitle):

        if type(newTitle) is not str:
            raise ValueError("title must be string")
        self.title = newTitle

    def setDescription(self, newDescription):

        if type(newDescription) is not str:
            raise ValueError("description must be string")
        self.description = newDescription

    # Class Method
    def getAll(cls, session):
        """
        Returns all the instances of Warning stored in the Warning table.
        """
        return session.query(cls).all()