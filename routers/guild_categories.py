from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependencies import get_db
import crud
import schemas

router = APIRouter(
    prefix='/guild_categories',
    tags=['WIP'],
    dependencies=[Depends(get_db)]
)


# GUILD CATEGORY
@router.post(
    '/create',
    response_model=schemas.GuildCategory,
    summary=''
)
def create_guild_category(guild_category: schemas.GuildCategoryCreate,
                          database: Session = Depends(get_db)):
    """
    Description
    """
    db_channel_category = crud.get_guild_category(database,
                                                  guild_category.guild_id)
    if db_channel_category:
        raise HTTPException(
            status_code=400,
            detail="This Guild already has a Category for School Channels!"
        )
    
    return crud.create_channel_category(database, guild_category)
