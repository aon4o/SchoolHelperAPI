from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

import models
from metadata import tags_metadata
from database import engine
from routers import auth, users, classes, subjects, class_subjects, \
    class_subject_messages, discord, status

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

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(classes.router)
app.include_router(subjects.router)
app.include_router(class_subjects.router)
app.include_router(class_subject_messages.router)
app.include_router(discord.router)
app.include_router(status.router)


@app.get(
    '/',
    tags=['Homepage'],
    summary="Homepage",
)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})
