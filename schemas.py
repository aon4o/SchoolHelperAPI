from typing import List, Optional

from pydantic import BaseModel


# CLASSES
class ClassBase(BaseModel):
    guild_id: Optional[str] = None
    name: str


class ClassCreate(ClassBase):
    pass


class Class(ClassBase):
    id: int
    
    class Config:
        orm_mode = True


class Key(BaseModel):
    key: str


# SUBJECTS
class SubjectBase(BaseModel):
    name: str


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int
    
    class Config:
        orm_mode = True


# TODO CHANNEL CATEGORIES WIP
class GuildCategoryBase(BaseModel):
    guild_id: str
    category_id: str


class GuildCategoryCreate(GuildCategoryBase):
    pass


class GuildCategory(GuildCategoryBase):
    id: int
    
    class Config:
        orm_mode = True


# USERS
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    verified: bool
    admin: bool
    
    class Config:
        orm_mode = True


class Email(BaseModel):
    email: str


# AUTH
class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Scope(BaseModel):
    scope: Optional[str] = None


# SCHEMAS WITH RELATIONS
class ClassWithUser(Class):
    class_teacher: Optional[User] = None
    
    class Config:
        orm_mode = True


class UserWithClass(User):
    class_: Optional[Class] = None
    
    class Config:
        orm_mode = True


class ClassSubjectsWithUser(BaseModel):
    subject: Subject
    teacher: Optional[User]
    
    class Config:
        orm_mode = True
