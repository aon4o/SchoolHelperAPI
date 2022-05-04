from sqlalchemy.orm import Session

import models
import schemas


def get_message_by_id(db: Session, message_id: int):
    return db.query(models.Message) \
        .filter(models.Message.id == message_id).first()


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
