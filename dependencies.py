import schemas
from database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import environ

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()
SECRET_KEY = env('SECRET_KEY')
ALGORITHM = env('ALGORITHM')


def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
