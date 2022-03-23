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
    prefix='/classes/{class_name}/subjects',
    tags=["Class' Subjects"],
    dependencies=[Depends(get_db), Depends(get_user_is_verified)]
)


@router.get(
    '',
    response_model=List[schemas.ClassSubjectsWithUser],
    summary='Get a list of the Subjects that are assigned to a Class.'
)
def get_class_subjects(class_name: str, database: Session = Depends(get_db)):
    class_ = crud.get_class_by_name(database, class_name)
    if class_ is None:
        handlers.handle_class_is_none(class_name)
    if class_.class_subjects is None:
        raise HTTPException(
            status_code=404,
            detail=f'Класът няма зададени предмети!'
        )
    return class_.class_subjects


@router.post(
    '/add',
    summary='Assigns a Subject to a Class.',
    dependencies=[Depends(get_user_is_admin)]
)
async def add_subject_to_class(class_name: str, subject: schemas.SubjectBase,
                               database: Session = Depends(get_db)):
    db_class = crud.get_class_by_name(database, class_name)
    if db_class is None:
        await handlers.handle_class_is_none(class_name)
    db_subject = crud.get_subject_by_name(database, subject.name)
    if db_subject is None:
        await handlers.handle_subject_is_none(subject.name)
    if db_subject in db_class.subjects:
        raise HTTPException(
            status_code=400,
            detail=f"Клас '{class_name}' вече има предмет '{subject.name}'!"
        )
    crud.add_subject_to_class(database, db_class, db_subject)
    
    # REQUEST TO THE BOT
    if db_class.guild_id is not None:
        try:
            payload = {
                'guild_id': db_class.guild_id,
                'subject': subject.name,
            }
            requests.post(
                f'{BOT_URL}/subjects',
                data=json.dumps(payload),
                headers={'Content-type': 'application/json'}
            )
        except:
            pass


@router.delete(
    '/remove',
    summary='Removes a Subject from a Class.',
    dependencies=[Depends(get_user_is_admin)]
)
async def remove_subject_from_class(
        class_name: str, subject: schemas.SubjectBase,
        database: Session = Depends(get_db)
):
    db_class = crud.get_class_by_name(database, class_name)
    if db_class is None:
        await handlers.handle_class_is_none(class_name)
    db_subject = crud.get_subject_by_name(database, subject.name)
    if db_subject is None:
        await handlers.handle_subject_is_none(subject.name)
    if db_subject not in db_class.subjects:
        raise HTTPException(
            status_code=400,
            detail=f"Клас '{class_name}' няма предмет '{subject.name}'!"
        )
    crud.remove_subject_from_class(database, db_class, db_subject)
    
    # REQUEST TO THE BOT
    if db_class.guild_id is not None:
        try:
            payload = {
                'guild_id': db_class.guild_id,
                'subject': subject.name,
            }
            requests.delete(
                f'{BOT_URL}/subjects',
                data=json.dumps(payload),
                headers={'Content-type': 'application/json'}
            )
        except:
            pass


@router.get(
    '/{subject_name}',
    summary='Get a Class Subject with Teacher from the Database.',
    response_model=schemas.ClassSubjectsWithUser,
)
def get_class_subject(
        class_name: str,
        subject_name: str,
        database: Session = Depends(get_db)
):
    db_class = crud.get_class_by_name(database, class_name)
    if db_class is None:
        handlers.handle_class_is_none(class_name)
    db_subject = crud.get_subject_by_name(database, subject_name)
    if db_subject is None:
        handlers.handle_subject_is_none(subject_name)
    db_class_subject = crud.get_class_subject_by_objects(database, db_class,
                                                         db_subject)
    if db_class_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Класът няма предмет с име '{subject_name}'!"
        )
    return db_class_subject


@router.put(
    '/{subject_name}/set_teacher',
    summary='Assigns a Teacher to Subject of a Class.',
    dependencies=[Depends(get_user_is_admin)]
)
def set_class_subject_teacher(
        class_name: str,
        subject_name: str,
        email: schemas.Email,
        database: Session = Depends(get_db)
):
    db_class = crud.get_class_by_name(database, class_name)
    if db_class is None:
        handlers.handle_class_is_none(class_name)
    db_subject = crud.get_subject_by_name(database, subject_name)
    if db_subject is None:
        handlers.handle_subject_is_none(subject_name)
    db_class_subject = crud.get_class_subject_by_objects(database, db_class,
                                                         db_subject)
    if db_class_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Класът няма предмет с име '{subject_name}'!"
        )
    db_user = crud.get_user_by_email(database, email.email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Не е намерен потребител с имейл '{email.email}'!"
        )
    if not db_user.verified:
        raise HTTPException(
            status_code=400,
            detail=f"Потребителят с имейл '{email.email}' не е потвърден! "
                   f"За да бъде Преподавател трябва първо "
                   f"Админ да потвърди акаунта му."
        )
    crud.set_class_subject_teacher(database, db_class_subject, db_user)


@router.delete(
    '/{subject_name}/remove_teacher',
    summary='Remove a Teacher from a Subject of a Class.',
    dependencies=[Depends(get_user_is_admin)]
)
def set_class_subject_teacher(
        class_name: str,
        subject_name: str,
        database: Session = Depends(get_db)
):
    db_class = crud.get_class_by_name(database, class_name)
    if db_class is None:
        handlers.handle_class_is_none(class_name)
    db_subject = crud.get_subject_by_name(database, subject_name)
    if db_subject is None:
        handlers.handle_subject_is_none(subject_name)
    db_class_subject = crud.get_class_subject_by_objects(database, db_class,
                                                         db_subject)
    if db_class_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Класът няма предмет с име '{subject_name}'!"
        )
    if db_class_subject.teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Предметът '{subject_name}' няма зададен учител!"
        )
    crud.set_class_subject_teacher(database, db_class_subject)
