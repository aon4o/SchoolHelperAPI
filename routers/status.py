from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import environ
import requests

import crud
import schemas
from dependencies import get_db, get_current_user

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

BOT_URL = env('BOT_URL')

router = APIRouter(
    prefix='/status',
    tags=['Status'],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    '',
    response_model=schemas.Status,
    summary="Route for checking the status of the Discord Bot.",
)
def status(db: Session = Depends(get_db)):
    initialized_classes = crud.get_initialized_classes_count(db)
    bot_online = False
    
    # REQUEST TO THE BOT
    try:
        requests.get(
            f'{BOT_URL}/status',
            headers={'Content-type': 'application/json'}
        )
        bot_online = True
    except:
        pass
    
    return {
        'bot': bot_online,
        'servers': initialized_classes
    }
