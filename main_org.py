"""
Docstring
"""
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# app = FastAPI()
oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

def get_db():
    """
    :return:
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


# SUBJECTS
@app.post(
    '/subjects/create',
    response_model=schemas.Subject,
    tags=['Subject'],
    summary=''
)
def create_subject(subject: schemas.SubjectCreate, database: Session = Depends(get_db)):
    """
    Description
    """
    guild_category = crud.get_guild_category(database, subject.guild_id)
    if not guild_category:
        raise HTTPException(
            status_code=400,
            detail="Your Guild does not have a category for School Channels!"
                   "Please create it with the command !create_channel_category"
        )
    
    db_subject = crud.get_subject(database, subject.guild_id, subject.name)
    if db_subject:
        raise HTTPException(
            status_code=400,
            detail=f"A Subject with the name '{subject.name}' already exists!"
        )
    
    return crud.create_subject(database, subject)


@app.get(
    '/subjects/{guild_id}',
    response_model=List[schemas.Subject],
    tags=['Subject'],
    summary="Gets a list of all Subjects that are set to a particular "
            "Guild",
)
def get_subjects(guild_id: int, database: Session = Depends(get_db)):
    """
    Description
    """
    subjects = crud.get_subjects(database, guild_id)
    if subjects is None:
        raise HTTPException(
            status_code=404,
            detail='There is no set Subjects for this Guild!'
        )
    
    return subjects


# GUILD CATEGORY
@app.post(
    '/guild_categories/create',
    response_model=schemas.GuildCategory,
    tags=['Subject'],
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
