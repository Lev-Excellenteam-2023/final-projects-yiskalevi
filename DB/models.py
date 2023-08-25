# models.py
import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    People who upload files for explanation.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)

    uploads = relationship("Upload", back_populates="user", cascade='all, delete-orphan')

    # def __init__(self):


class Upload(Base):
    """
    Files uploaded by people, with metadata related to their processing.
    """
    __tablename__ = 'uploads'

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, nullable=False)
    finish_time = Column(DateTime,nullable=True)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=True)
    user = relationship("User", back_populates="uploads")

def main():
    engine = create_engine("sqlite:///C:/networks/excelantim/project1/DB/file.db", echo=True)

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()