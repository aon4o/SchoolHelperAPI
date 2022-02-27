from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas


# CLASSES
def get_class_by_name(db: Session, name: str):
    return db.query(models.Class).filter(models.Class.name == name).first()


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
    return db_class


def edit_class(db: Session, class_: models.Class,
               new_class: schemas.ClassCreate):
    class_.name = new_class.name
    db.commit()
    db.refresh(class_)
    return class_


def delete_class(db: Session, class_: models.Class):
    db.delete(class_)
    db.commit()


# SUBJECTS
def get_subject_by_name(db: Session, name: str):
    return db.query(models.Subject) \
        .filter(models.Subject.name == name).first()


def get_subjects_by_guild_id_or_class_name(db: Session, guild_id_or_name: str):
    by_guild_id = db.query(models.Class) \
        .filter(models.Class.guild_id == guild_id_or_name).subjects.all()
    if by_guild_id is None:
        return db.query(models.Class) \
            .filter(models.Class.name == guild_id_or_name).subjects.all()
    return by_guild_id


def get_all_subjects(db: Session):
    return db.query(models.Subject).all()


def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(
        name=subject.name
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def edit_subject(db: Session, subject: models.Subject,
                 new_subject: schemas.SubjectCreate):
    subject.name = new_subject.name
    db.commit()
    db.refresh(subject)
    return subject


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
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User) \
        .filter(models.User.email == email).first()


# TODO CHANNEL CATEGORIES WIP
def get_guild_category(db: Session, guild_id: str):
    return db.query(models.GuildCategory) \
        .filter(models.GuildCategory.guild_id == guild_id).first()


def create_channel_category(db: Session,
                            guild_category: schemas.GuildCategoryCreate):
    db_guild_category = models.GuildCategory(
        guild_id=guild_category.guild_id,
        category_id=guild_category.category_id
    )
    db.add(db_guild_category)
    db.commit()
    db.refresh(db_guild_category)
    return db_guild_category
