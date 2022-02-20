"""
Docstring
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import models
from database import engine
from routers import classes, subjects, guild_categories


models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classes.router)
app.include_router(subjects.router)
app.include_router(guild_categories.router)


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
