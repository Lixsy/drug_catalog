from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api.settings import env

if not env.is_unittest:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{env.pg_user}:{env.pg_pass}@{env.pg_host}:{env.pg_port}/{env.pg_db}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///sqlite_drug_db.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
