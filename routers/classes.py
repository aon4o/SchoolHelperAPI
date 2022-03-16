from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud
import schemas
from dependencies import get_db, get_user_is_verified, get_user_is_admin

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
        raise HTTPException(
            status_code=404,
            detail=f"Клас със име '{name}' не съществува!"
        )
    
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
        raise HTTPException(
            status_code=404,
            detail=f"Клас със име '{name}' не съществува!"
        )
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
def delete_class(name: str, database: Session = Depends(get_db)):
    db_class = crud.get_class_by_name(database, name)
    if db_class is None:
        raise HTTPException(
            status_code=404,
            detail=f"Клас със име '{name}' не съществува!"
        )
    crud.delete_class(database, db_class)


@router.get(
    '/{name}/subjects',
    response_model=List[schemas.ClassSubjectsWithUser],
    summary='Get a list of the Subjects that are assigned to a Class.'
)
def get_class_subjects(name: str, database: Session = Depends(get_db)):
    class_ = crud.get_class_by_name(database, name)
    if class_ is None:
        raise HTTPException(
            status_code=404,
            detail=f"Клас с име '{name}' не съществува!"
        )
    if class_.class_subjects is None:
        raise HTTPException(
            status_code=404,
            detail=f'Класът няма зададени предмети!'
        )
    return class_.class_subjects


@router.post(
    '/{name}/subjects/add',
    summary='Assigns a Subject to a Class.',
    dependencies=[Depends(get_user_is_admin)]
)
def add_subject_to_class(name: str, subject: schemas.SubjectBase,
                         database: Session = Depends(get_db)):
    db_class = crud.get_class_by_name(database, name)
    if db_class is None:
        raise HTTPException(
            status_code=404,
            detail=f"Клас с име '{name}' не съществува!"
        )
    db_subject = crud.get_subject_by_name(database, subject.name)
    if db_subject is None:
        raise HTTPException(
            status_code=404,
            detail=f"Предмет с име '{subject.name}' не съществува!"
        )
    if db_subject in db_class.subjects:
        raise HTTPException(
            status_code=400,
            detail=f"Клас '{name}' вече има предмет '{subject.name}'!"
        )
    crud.add_subject_to_class(database, db_class, db_subject)


@router.delete(
    '/{name}/subjects/remove',
    summary='Removes a Subject from a Class.',
    dependencies=[Depends(get_user_is_admin)]
)
def remove_subject_from_class(name: str, subject: schemas.SubjectBase,
                              database: Session = Depends(get_db)):
    db_class = crud.get_class_by_name(database, name)
    if db_class is None:
        raise HTTPException(
            status_code=404,
            detail=f"Клас с име '{name}' не съществува!"
        )
    db_subject = crud.get_subject_by_name(database, subject.name)
    if db_subject is None:
        raise HTTPException(
            status_code=404,
            detail=f"Предмет с име '{subject.name}' не съществува!"
        )
    if db_subject not in db_class.subjects:
        raise HTTPException(
            status_code=400,
            detail=f"Клас '{name}' няма предмет '{subject.name}'!"
        )
    crud.remove_subject_from_class(database, db_class, db_subject)


@router.get(
    '/{class_name}/subjects/{subject_name}',
    summary='Get a Class Subject with Teacher from the Database.',
    response_model=schemas.ClassSubjectsWithUser,
    dependencies=[Depends(get_user_is_verified)]
)
def get_class_subject(
        class_name: str,
        subject_name: str,
        database: Session = Depends(get_db)
):
    db_class = crud.get_class_by_name(database, class_name)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Клас с име '{class_name}' не съществува!"
        )
    db_subject = crud.get_subject_by_name(database, subject_name)
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Предмет с име '{subject_name}' не съществува!"
        )
    db_class_subject = crud.get_class_subject_by_objects(database, db_class,
                                                         db_subject)
    if db_class_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Класът няма предмет с име '{subject_name}'!"
        )
    return db_class_subject


@router.put(
    '/{class_name}/subjects/{subject_name}/set_teacher',
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Клас с име '{class_name}' не съществува!"
        )
    db_subject = crud.get_subject_by_name(database, subject_name)
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Предмет с име '{subject_name}' не съществува!"
        )
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
    '/{class_name}/subjects/{subject_name}/remove_teacher',
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Клас с име '{class_name}' не съществува!"
        )
    db_subject = crud.get_subject_by_name(database, subject_name)
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Предмет с име '{subject_name}' не съществува!"
        )
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


@router.put(
    '/{name}/class_teacher/set',
    summary='Assigns a Class Teacher.',
    dependencies=[Depends(get_user_is_admin)]
)
def set_class_teacher(name: str, email: schemas.Email,
                      database: Session = Depends(get_db)):
    db_class = crud.get_class_by_name(database, name)
    if db_class is None:
        raise HTTPException(
            status_code=404,
            detail=f"Клас с име '{name}' не съществува!"
        )
    #    if db_class.class_teacher is not None:
    #        raise HTTPException(
    #            status_code=status.HTTP_400_BAD_REQUEST,
    #            detail=f"Класът вече има Класен ръководител!"
    #        )
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
        raise HTTPException(
            status_code=404,
            detail=f"Клас с име '{name}' не съществува!"
        )
    crud.remove_class_teacher(database, db_class)


@router.get(
    '/{name}/key',
    response_model=schemas.Key,
    summary='Get the Key of a Class for Discord Bot initialization.',
    dependencies=[Depends(get_user_is_admin)]
)
def get_class_subjects(name: str, database: Session = Depends(get_db)):
    class_ = crud.get_class_by_name(database, name)
    if class_ is None:
        raise HTTPException(
            status_code=404,
            detail=f"Клас с име '{name}' не съществува!"
        )
    
    return {'key': class_.key}
