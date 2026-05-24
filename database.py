from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = URL.create(

    drivername="mysql+pymysql",

    username="root",

    password="IIuqEFAiqTEuKbCnhblqICyOQWppunyK",

     host="kodama.proxy.rlwy.net",

    port=31618,

    database="railway"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)

Base = declarative_base()