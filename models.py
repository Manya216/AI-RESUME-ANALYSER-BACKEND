from sqlalchemy import Column, Integer, String
from database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    score = Column(Integer)
    role = Column(String(255))
    skills = Column(String(1000))
    user_email = Column(String(255))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(255))