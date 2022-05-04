from sqlalchemy.orm import Session

import models


def add_subject_to_class(
        db: Session, class_: models.Class,
        subject: models.Subject
):
    class_.subjects.append(subject)
    db.commit()
    db.refresh(class_)


def remove_subject_from_class(
        db: Session, class_: models.Class,
        subject: models.Subject
):
    class_.subjects.remove(subject)
    db.commit()
    db.refresh(class_)
