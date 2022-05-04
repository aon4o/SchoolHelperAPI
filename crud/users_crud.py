from sqlalchemy.orm import Session

import models
import schemas


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
