from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = URL.create(

    drivername="mysql+pymysql",

    username="avnadmin",

    password="AVNS_fa71Ufz4fQaveW75ME4",

    host="mysql-c46e11d-resumeanalysis.a.aivencloud.com",

    port=19801,

    database="defaultdb"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "connect_timeout": 10
    }
)
SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)

Base = declarative_base()
