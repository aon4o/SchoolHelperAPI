from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
    response_model=List[schemas.Class],
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
    response_model=schemas.Class,
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
    response_model=schemas.Class,
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
    
    return crud.create_class(db, class_)


@router.put(
    '/{name}/edit',
    response_model=schemas.Class,
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
    
    return crud.edit_class(db, db_class, class_)


@router.delete(
    '/{name}/delete',
    response_model=schemas.Class,
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
    return crud.delete_class(database, db_class)


@router.get(
    '/{name}/subjects',
    response_model=List[schemas.Subject],
    summary='Get a list of the Subjects that are assigned to a Class.'
)
def get_class_subjects(name: str, database: Session = Depends(get_db)):
    class_ = crud.get_class_by_name(database, name)
    if class_ is None:
        raise HTTPException(
            status_code=404,
            detail=f"Клас с име '{name}' не съществува!"
        )
    if class_.subjects is None:
        raise HTTPException(
            status_code=404,
            detail=f'Класът няма зададени предмети!'
        )
    return class_.subjects


@router.post(
    '/{name}/subjects/add',
    response_model=List[schemas.Subject],
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
    return db_class.subjects


@router.delete(
    '/{name}/subjects/remove',
    response_model=List[schemas.Subject],
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
    return db_class.subjects
