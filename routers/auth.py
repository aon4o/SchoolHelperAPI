from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt
import environ
from datetime import datetime, timedelta

import crud
import schemas
from dependencies import get_db, get_current_user

router = APIRouter(
    tags=['Auth'],
)

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
ALGORITHM = env('ALGORITHM')
TOKEN_EXPIRATION = env('TOKEN_EXPIRATION')

bcrypt = CryptContext(schemes=["bcrypt"])


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(TOKEN_EXPIRATION))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get(
    '/test',
    response_model=object,
    summary='Auth TEST (TO BE REMOVED)',
    dependencies=[Depends(get_current_user)]
)
def read_root():
    return {"data": "Hello World!"}


@router.post(
    '/register',
    response_model=schemas.User,
    summary='Path for User Registration'
)
def register(user: schemas.UserCreate, database: Session = Depends(get_db)):
    if len(user.first_name) < 3 or len(user.first_name) > 50 \
            or len(user.last_name) < 3 or len(user.last_name) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Имената не може да съдържат по-малко от 3 или повече от '
                   '50 символа!'
        )
    if '@' not in user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Невалиден Имейл адрес!'
        )
    if crud.get_user_by_email(database, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Този Имейл вече е регистриран!'
        )

    user.password = bcrypt.hash(user.password)
    db_user = crud.create_user(database, user)
    return db_user


@router.post(
    '/login',
    response_model=schemas.Token,
    summary='Path for User Login'
)
def login(request: schemas.Login, database: Session = Depends(get_db)):
    user = crud.get_user_by_email(database, request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Не беше намерен Потребител с Имейл '{request.email}'!"
        )
    if not bcrypt.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Грешна Парола!'
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
