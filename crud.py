from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas


# CLASSES
def get_class_by_name(db: Session, name: str):
    return db.query(models.Class).filter(models.Class.name == name).first()


def get_class_by_key(db: Session, key: str):
    return db.query(models.Class).filter(models.Class.key == key).first()


def get_class_by_guild_id(db: Session, guild_id: str):
    return db.query(models.Class).\
        filter(models.Class.guild_id == guild_id).first()


def get_all_classes(db: Session):
    return db.query(models.Class).all()


def create_class(db: Session, class_: schemas.ClassCreate):
    db_class = models.Class(
        name=class_.name,
        key=CryptContext(schemes=["bcrypt"]).hash(class_.name)
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)


def edit_class(db: Session, class_: models.Class,
               new_class: schemas.ClassCreate):
    class_.name = new_class.name
    db.commit()
    db.refresh(class_)
    

def set_class_guild_id(db: Session, class_: models.Class,
                       guild_id: str = None):
    class_.guild_id = guild_id
    db.commit()


def delete_class(db: Session, class_: models.Class):
    db.delete(class_)
    db.commit()
    
    
def set_class_subject_teacher(db: Session, class_subject: models.ClassSubject,
                              user: Optional[models.User] = None):
    class_subject.teacher = user
    db.commit()
    db.refresh(class_subject)

    
def set_class_teacher(db: Session, class_: models.Class, user: models.User):
    class_.class_teacher = user
    user.class_ = class_
    db.commit()
    db.refresh(class_)
    db.refresh(user)
    

def remove_class_teacher(db: Session, class_: models.Class):
    user = class_.class_teacher
    if user is not None:
        user.class_ = None
        db.refresh(user)
    class_.class_teacher = None
    db.commit()
    db.refresh(class_)


# SUBJECTS
def get_subject_by_name(db: Session, name: str):
    return db.query(models.Subject) \
        .filter(models.Subject.name == name).first()


def get_class_subject_by_objects(db: Session, class_: models.Class, subject: models.Subject):
    return db.query(models.ClassSubject) \
        .filter(models.ClassSubject.subject == subject,
                models.ClassSubject.class_ == class_).first()


def get_all_subjects(db: Session):
    return db.query(models.Subject).all()


def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(
        name=subject.name
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)


def edit_subject(db: Session, subject: models.Subject,
                 new_subject: schemas.SubjectCreate):
    subject.name = new_subject.name
    db.commit()
    db.refresh(subject)


def delete_subject(db: Session, subject: models.Subject):
    db.delete(subject)
    db.commit()


# CLASSES SUBJECTS
def add_subject_to_class(db: Session, class_: models.Class,
                         subject: models.Subject):
    class_.subjects.append(subject)
    db.commit()
    db.refresh(class_)


def remove_subject_from_class(db: Session, class_: models.Class,
                              subject: models.Subject):
    class_.subjects.remove(subject)
    db.commit()
    db.refresh(class_)


# USERS
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User) \
        .filter(models.User.email == email).first()


def get_all_users(db: Session):
    return db.query(models.User).all()


def edit_user(db: Session, user: models.User, new_user: schemas.UserBase):
    user.first_name = new_user.first_name
    user.last_name = new_user.last_name
    user.email = new_user.email
    db.commit()
    db.refresh(user)


def edit_user_scope(db: Session, user: models.User, scope: str):
    if scope == 'admin':
        user.verified = True
        user.admin = True
    elif scope == 'user':
        user.verified = True
        user.admin = False
    else:
        user.verified = False
        user.admin = False
    db.commit()
    db.refresh(user)


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()


# TODO CHANNEL CATEGORIES WIP
# def get_guild_category(db: Session, guild_id: str):
#     return db.query(models.GuildCategory) \
#         .filter(models.GuildCategory.guild_id == guild_id).first()
#
#
# def create_channel_category(db: Session,
#                             guild_category: schemas.GuildCategoryCreate):
#     db_guild_category = models.GuildCategory(
#         guild_id=guild_category.guild_id,
#         category_id=guild_category.category_id
#     )
#     db.add(db_guild_category)
#     db.commit()
#     db.refresh(db_guild_category)
#     return db_guild_category

# MESSAGES
def get_message_by_id(db: Session, id: int):
    return db.query(models.Message).filter(models.Message.id == id).first()


def create_class_subject_message(
        db: Session,
        message: schemas.MessageBase,
        class_subject: models.ClassSubject,
        user: models.User
):
    db_message = models.Message(
        title=message.title,
        text=message.text,
        user_id=user.id
    )
    class_subject.messages.append(db_message)
    db.commit()


def delete_class_subject_message(db: Session, message: models.Message):
    db.delete(message)
    db.commit()
