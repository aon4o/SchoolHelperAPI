from fastapi import HTTPException, status


def handle_class_is_none(class_name: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Клас с име '{class_name}' не съществува!"
    )


def handle_subject_is_none(subject_name: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Предмет с име '{subject_name}' не съществува!"
    )


def handle_user_is_none(email: str):
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail=f"Потребител с имейл '{email}' не съществува!"
    )
