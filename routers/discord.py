from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import crud
import schemas
from dependencies import get_db

router = APIRouter(
    prefix='/discord',
    tags=['Discord'],
    dependencies=[Depends(get_db)]
)


@router.get(
    '/status',
    response_model=schemas.Class,
    summary="Route for checking the status of a School Discord Server.",
)
def function(data: schemas.DiscordGuildId, db: Session = Depends(get_db)):
    db_class = crud.get_class_by_guild_id(db, data.guild_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Този Discord сървър не е инициализиран!"
        )
    return db_class


@router.put(
    '/init',
    response_model=List[schemas.Subject],
    summary="Route for initializing a Discord server.",
)
def function(data: schemas.DiscordInit, db: Session = Depends(get_db)):

    if crud.get_class_by_guild_id(db, data.guild_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Този Discord сървър вече е инициализиран!"
        )

    db_class = crud.get_class_by_key(db, data.key)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Клас с ключ '{data.key}' не съществува!"
        )
    else:
        if db_class.guild_id is not None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Клас с ключ '{data.key}' вече е инициализиран!"
            )

    crud.set_class_guild_id(db, db_class, data.guild_id)
    
    return db_class.subjects


@router.put(
    '/deactivate',
    summary="Route for deactivating previously initialized Discord server.",
)
def function(data: schemas.DiscordGuildId, db: Session = Depends(get_db)):
    db_class = crud.get_class_by_guild_id(db, data.guild_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Класът не е бил инициализиран!"
        )
    
    crud.set_class_guild_id(db, db_class)
