from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

url = f'postgresql://{env("DB_USERNAME")}' \
      f':{env("DB_PASSWORD")}' \
      f'@{env("DB_HOST")}' \
      f':{env("DB_PORT")}' \
      f'/{env("DB_DATABASE")}'

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()
