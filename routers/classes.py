from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from typing import List
import requests
import environ
import json

import crud
import handlers
import schemas
from dependencies import get_db, get_user_is_verified, get_user_is_admin

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

BOT_URL = env('BOT_URL')

router = APIRouter(
    prefix='/classes',
    tags=['Classes'],
    dependencies=[Depends(get_db), Depends(get_user_is_verified)]
)


@router.get(
    '',
    response_model=List[schemas.ClassWithUser],
    summary='Get the details of all Class objects from the DB.'
)
def get_all_classes(database: Session = Depends(get_db)):
    classes = crud.get_all_classes(database)
    if classes is None:
        raise HTTPException(
            status_code=404,
            detail='Няма създадени класове!'
        )
    
    return classes


@router.get(
    '/{name}',
    response_model=schemas.ClassWithUser,
    summary='Get the details of a Class object from the DB.'
)
def get_class(name: str, database: Session = Depends(get_db)):
    class_ = crud.get_class_by_name(database, name)
    if class_ is None:
        handlers.handle_class_is_none(name)
    
    return class_


@router.post(
    '/create',
    summary='Creates a Class instance in the DB.',
    dependencies=[Depends(get_user_is_admin)]
)
def create_class(class_: schemas.ClassCreate, db: Session = Depends(get_db)):
    if len(class_.name) < 2 or len(class_.name) > 10:
        raise HTTPException(
            status_code=400,
            detail="Името на Клас трябва да бъде между 2 и 10 символа!"
        )
    db_class = crud.get_class_by_name(db, class_.name)
    if db_class:
        raise HTTPException(
            status_code=400,
            detail=f"Клас със име '{class_.name}' вече съществува!"
        )
    crud.create_class(db, class_)


@router.put(
    '/{name}/edit',
    summary='Edit the details of a Class object from the DB.',
    dependencies=[Depends(get_user_is_admin)]
)
def edit_class(name: str, class_: schemas.ClassCreate,
               db: Session = Depends(get_db)):
    db_class = crud.get_class_by_name(db, name)
    if db_class is None:
        handlers.handle_class_is_none(name)
    if crud.get_class_by_name(db, class_.name) is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Клас със име '{class_.name}' вече съществува!"
        )
    if len(class_.name) < 2 or len(class_.name) > 10:
        raise HTTPException(
            status_code=400,
            detail=f"Името на Клас трябва да бъде между 2 и 10 символа!"
        )
    crud.edit_class(db, db_class, class_)


@router.delete(
    '/{name}/delete',
    summary='Delete a Class instance from the DB.',
    dependencies=[Depends(get_user_is_admin)]
)
async def delete_class(name: str, database: Session = Depends(get_db)):
    db_class = crud.get_class_by_name(database, name)
    if db_class is None:
        await handlers.handle_class_is_none(name)
    
    # REQUEST TO THE BOT
    if db_class.guild_id is not None:
        try:
            payload = {'guild_id': db_class.guild_id}
            requests.delete(
                f'{BOT_URL}/classes',
                data=json.dumps(payload),
                headers={'Content-type': 'application/json'}
            )
        except:
            pass
    crud.delete_class(database, db_class)


@router.put(
    '/{name}/class_teacher/set',
    summary='Assigns a Class Teacher.',
    dependencies=[Depends(get_user_is_admin)]
)
def set_class_teacher(name: str, email: schemas.Email,
                      database: Session = Depends(get_db)):
    db_class = crud.get_class_by_name(database, name)
    if db_class is None:
        handlers.handle_class_is_none(name)
    db_user = crud.get_user_by_email(database, email.email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Потребител с имейл '{email.email}' не съществува!"
        )
    if db_user.class_ is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Този Потребител вече е класен на '{db_user.class_}'!"
        )
    crud.remove_class_teacher(database, db_class)
    crud.set_class_teacher(database, db_class, db_user)


@router.delete(
    '/{name}/class_teacher/remove',
    summary='Removes a Class Teacher.',
    dependencies=[Depends(get_user_is_admin)]
)
def remove_subject_from_class(name: str, database: Session = Depends(get_db)):
    db_class = crud.get_class_by_name(database, name)
    if db_class is None:
        handlers.handle_class_is_none(name)
    crud.remove_class_teacher(database, db_class)


@router.get(
    '/{name}/key',
    response_model=schemas.Key,
    summary='Get the Key of a Class for Discord Bot initialization.',
    dependencies=[Depends(get_user_is_admin)]
)
def get_class_discord_key(name: str, database: Session = Depends(get_db)):
    class_ = crud.get_class_by_name(database, name)
    if class_ is None:
        handlers.handle_class_is_none(name)
    
    return {'key': class_.key}
