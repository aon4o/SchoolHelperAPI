from sqlalchemy.orm import Session

import models
import schemas


# CLASSES
def get_subject(db: Session, guild_id: str, name: str):
    return db.query(models.Subject) \
        .filter(models.Subject.guild_id == guild_id,
                models.Subject.name == name) \
        .first()


def get_subjects(db: Session, guild_id: int):
    return db.query(models.Subject) \
        .filter(models.Subject.guild_id == guild_id).all()


def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(
        guild_id=subject.guild_id,
        name=subject.name
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


# def edit_class(db: Session, class_: schemas.ClassCreate):
#     db_class = models.Schedule(
#         guild_id=class_.guild_id,
#         name=class_.name
#     )
#     db.add(db_class)
#     db.commit()
#     db.refresh(db_class)
#     return db_class

# CHANNEL CATEGORIES
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
