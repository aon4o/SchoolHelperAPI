from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from typing import List
import requests
import json
import environ

import crud
import handlers
import schemas
import models
from dependencies import get_db, get_user_is_verified

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

BOT_URL = env('BOT_URL')

router = APIRouter(
    prefix='/classes/{class_name}/subjects/{subject_name}/messages',
    tags=['Class Subject Messages'],
    dependencies=[Depends(get_db), Depends(get_user_is_verified)]
)


@router.get(
    '',
    summary="Get the Messages of a Class' Subject.",
    response_model=List[schemas.MessageWithUser],
)
def get_class_subject_messages(
        class_name: str,
        subject_name: str,
        database: Session = Depends(get_db),
        user: models.User = Depends(get_user_is_verified)
):
    db_class = crud.get_class_by_name(database, class_name)
    if db_class is None:
        handlers.handle_class_is_none(class_name)
        
    db_subject = crud.get_subject_by_name(database, subject_name)
    if db_subject is None:
        handlers.handle_subject_is_none(subject_name)
        
    db_class_subject = crud.get_class_subject_by_objects(
        database, db_class, db_subject
    )
    if db_class_subject is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Предметът {subject_name} "
                   f"не е зададен на класа {class_name}!"
        )
    if db_class_subject.teacher is not user and not user.admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"За да видите материалите трябва"
                   f" да сте Преподаващия или Админ!"
        )
    
    return db_class_subject.messages


@router.post(
    '/create',
    summary="Create a new Message for a Class' Subject.",
)
def create_class_subject_message(
        class_name: str,
        subject_name: str,
        message: schemas.MessageBase,
        database: Session = Depends(get_db),
        user: models.User = Depends(get_user_is_verified)
):
    db_class = crud.get_class_by_name(database, class_name)
    if db_class is None:
        handlers.handle_class_is_none(class_name)
    
    db_subject = crud.get_subject_by_name(database, subject_name)
    if db_subject is None:
        handlers.handle_subject_is_none(subject_name)
    
    db_class_subject = crud.get_class_subject_by_objects(
        database, db_class, db_subject
    )
    if db_class_subject is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Предметът {subject_name} "
                   f"не е зададен на класа {class_name}!"
        )
    if db_class_subject.teacher is not user and not user.admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"За да добавите материал трябва "
                   f"да сте Преподаващия Учител!"
        )
    if len(message.title) < 3 or len(message.title) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Заглавието трябва да е между 3 и 50 символа!"
        )
    if len(message.text) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Съобщението е прекалено късо!"
        )
    
    crud.create_class_subject_message(
        database, message, db_class_subject, user
    )
    
    # REQUEST TO THE BOT
    if db_class.guild_id is not None:
        payload = {
            'guild_id': db_class.guild_id,
            'subject': subject_name,
            'title': message.title,
            'text': message.text,
            'user': f'{user.first_name} {user.last_name}'
        }
        request = requests.post(
            f'{BOT_URL}/messages/create',
            data=json.dumps(payload),
            headers={'Content-type': 'application/json'}
        )


@router.delete(
    '/{message_id}/delete',
    summary="Delete a Message for a Class' Subject.",
)
def delete_class_subject_message(
        class_name: str,
        subject_name: str,
        message_id: int,
        database: Session = Depends(get_db),
        user: models.User = Depends(get_user_is_verified)
):
    db_class = crud.get_class_by_name(database, class_name)
    if db_class is None:
        handlers.handle_class_is_none(class_name)
    
    db_subject = crud.get_subject_by_name(database, subject_name)
    if db_subject is None:
        handlers.handle_subject_is_none(subject_name)
    
    db_class_subject = crud.get_class_subject_by_objects(
        database, db_class, db_subject
    )
    if db_class_subject is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Предметът {subject_name} "
                   f"не е зададен на класа {class_name}!"
        )
    
    db_message = crud.get_message_by_id(database, message_id)
    if db_message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Съобщението, което се опитвате да изтриете не съществува!"
        )
    if db_message.user is not user and not user.admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="За да изтриете това съобщение, "
                   "трябва Вие да сте го създали или да сте Админ!"
        )
    
    crud.delete_class_subject_message(database, db_message)
