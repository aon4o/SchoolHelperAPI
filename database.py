from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

engine = create_engine(
    env("SQLALCHEMY_DATABASE_URL"), connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()
