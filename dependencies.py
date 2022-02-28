from sqlalchemy.orm import Session

import crud
import models
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


def get_current_user(token: str = Depends(oauth2_scheme),
                     database: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Идентификационните данни не можаха да бъдат валидирани!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = crud.get_user_by_email(database, email)
        if user is None:
            raise credentials_exception
        return user
        # token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception


def get_user_is_verified(user: models.User = Depends(get_current_user)):
    if user.verified:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Профилът Ви не е потвърден! Свържете се с Админ.'
        )


def get_user_is_admin(user: models.User = Depends(get_current_user)):
    if user.admin:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='За да извършите това действие трябва да бъдете Админ! Ако смятате това за грешка, свържете се с такъв.'
        )
