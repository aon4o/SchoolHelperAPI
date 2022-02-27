"""
Docstring
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import models
from metadata import tags_metadata
from database import engine
from routers import classes, subjects, guild_categories, auth


models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="ELSYS Helper API",
    description="An API build as Thesis Project in TUES by Alexander Naidenov",
    version="0.0.1",
    contact={
        "name": "Alex Naida",
        "url": "https://www.linkedin.com/in/alex-naida/",
        "email": "a.o.naidenov@gmail.com",
    },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
    openapi_tags=tags_metadata
)

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classes.router)
app.include_router(subjects.router)
app.include_router(guild_categories.router)
app.include_router(auth.router)


@app.get(
    '/',
    tags=['Homepage'],
    summary="Homepage",
)
def index(request: Request):
    """
    Description
    """
    return templates.TemplateResponse('index.html', {'request': request})
