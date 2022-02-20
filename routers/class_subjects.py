from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependencies import get_db
import crud
import schemas

router = APIRouter(
    prefix='/classes',
    tags=['Classes'],
    dependencies=[Depends(get_db)]
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
            detail='Няа създадени класове!'
        )
    
    return classes
