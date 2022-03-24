from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import handlers
import schemas
import models
from dependencies import get_db, get_current_user, get_user_is_verified, \
    get_user_is_admin

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    dependencies=[Depends(get_db), Depends(get_current_user)]
)


@router.get(
    '',
    response_model=List[schemas.UserWithClass],
    summary='Get the details of all User objects from the DB.',
    dependencies=[Depends(get_user_is_verified)],
)
def get_all_users(database: Session = Depends(get_db)):
    users = crud.get_all_users(database)
    if users is None:
        raise HTTPException(
            status_code=404,
            detail='Няма създадени Потребители!'
        )
    
    return users


@router.get(
    '/me',
    response_model=schemas.UserWithClass,
    summary='Get the details of the currently logged in User from the DB.'
)
def get_current_user(user: models.User = Depends(get_current_user)):
    return user


@router.put(
    '/me/edit',
    summary='Edit the details of the currently logged in User.'
)
def edit_current_user(
        new_user: schemas.UserBase,
        user: models.User = Depends(get_current_user),
        database: Session = Depends(get_db)
):
    if len(new_user.first_name) < 3 or len(new_user.first_name) > 50 \
            or len(new_user.last_name) < 3 or len(new_user.last_name) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Имената не може да съдържат по-малко от 3 или повече от '
                   '50 символа!'
        )
    if '@' not in new_user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Невалиден Имейл адрес!'
        )
    if crud.get_user_by_email(database,
                              new_user.email) and user.email != new_user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Този Имейл вече е регистриран!'
        )
    crud.edit_user(database, user, new_user)


@router.delete(
    '/me/delete',
    summary='Delete the currently logged in User from the DB.'
)
def get_current_user(
        user: models.User = Depends(get_current_user),
        database: Session = Depends(get_db)
):
    crud.delete_user(database, user)


@router.get(
    '/{email}',
    response_model=schemas.UserWithClass,
    summary='Get the details of a specific User by Email from the DB.',
    dependencies=[Depends(get_user_is_verified)],
)
def get_user_by_email(email: str, database: Session = Depends(get_db)):
    user = crud.get_user_by_email(database, email)
    if user is None:
        handlers.handle_user_is_none(email)
    return user


@router.put(
    '/{email}/scope',
    summary='Change the scope of a given User.',
    dependencies=[Depends(get_user_is_admin)],
)
def edit_user_scope(email: str, scope: schemas.Scope,
                    database: Session = Depends(get_db)):
    user = crud.get_user_by_email(database, email)
    if user is None:
        handlers.handle_user_is_none(email)
    crud.edit_user_scope(database, user, scope.scope)


@router.get(
    '/{email}/classes',
    summary='Get the Classes that the current Teacher teaches.',
    response_model=schemas.UserWithClasses,
    dependencies=[Depends(get_user_is_verified)],
)
def edit_user_scope(email: str, database: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(database, email)
    if db_user is None:
        handlers.handle_user_is_none(email)
    return db_user
