from sqlalchemy.orm import Session

import models
import schemas


def get_subject_by_name(db: Session, name: str):
    return db.query(models.Subject) \
        .filter(models.Subject.name == name).first()


def get_class_subject_by_objects(
        db: Session, class_: models.Class, subject: models.Subject
):
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


def edit_subject(
        db: Session, subject: models.Subject,
        new_subject: schemas.SubjectCreate
):
    subject.name = new_subject.name
    db.commit()
    db.refresh(subject)


def delete_subject(db: Session, subject: models.Subject):
    db.delete(subject)
    db.commit()
