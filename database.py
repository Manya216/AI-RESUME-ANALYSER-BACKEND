from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = URL.create(

    drivername="mysql+pymysql",

    username="root",

    password="*",

    host="localhost",

    port=3306,

    database="resume_analyzer"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)

Base = declarative_base()
