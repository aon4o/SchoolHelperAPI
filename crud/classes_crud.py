from typing import Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas


def get_class_by_name(db: Session, name: str):
    return db.query(models.Class).filter(models.Class.name == name).first()


def get_class_by_key(db: Session, key: str):
    return db.query(models.Class).filter(models.Class.key == key).first()


def get_class_by_guild_id(db: Session, guild_id: str):
    return db.query(models.Class). \
        filter(models.Class.guild_id == guild_id).first()


def get_all_classes(db: Session):
    return db.query(models.Class).order_by(models.Class.name).all()


def get_initialized_classes_count(db: Session):
    return len(
        db.query(models.Class).filter(models.Class.guild_id is not None).all()
    )


def create_class(db: Session, class_: schemas.ClassCreate):
    db_class = models.Class(
        name=class_.name,
        key=CryptContext(schemes=["bcrypt"]).hash(class_.name)
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)


def edit_class(
        db: Session,
        class_: models.Class,
        new_class: schemas.ClassCreate
):
    class_.name = new_class.name
    db.commit()
    db.refresh(class_)


def set_class_guild_id(
        db: Session, class_: models.Class,
        guild_id: str = None
):
    class_.guild_id = guild_id
    db.commit()


def delete_class(db: Session, class_: models.Class):
    db.delete(class_)
    db.commit()


def set_class_subject_teacher(
        db: Session, class_subject: models.ClassSubject,
        user: Optional[models.User] = None
):
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
