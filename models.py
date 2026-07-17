from sqlalchemy import Column, Integer, String
from database import Base



class Resume(Base):

    __tablename__ = "resumes"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    filename = Column(
        String(255),
        nullable=False
    )


    score = Column(
        Integer,
        nullable=False
    )


    role = Column(
        String(255)
    )


    skills = Column(
        String(1000)
    )


    user_email = Column(
        String(255),
        index=True,
        nullable=False
    )




class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    username = Column(
        String(100),
        unique=True,
        nullable=False
    )


    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )


    password = Column(
        String(255),
        nullable=False
    )
