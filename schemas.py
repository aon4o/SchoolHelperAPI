import datetime
from typing import Optional, List

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
    
    
# MESSAGES
class MessageBase(BaseModel):
    title: str
    text: str


class Message(MessageBase):
    id: int
    created_at: datetime.datetime
    
    class Config:
        orm_mode = True


# SCHEMAS WITH RELATIONS
class ClassWithUser(Class):
    class_teacher: Optional[User] = None
    
    class Config:
        orm_mode = True


class UserWithClass(User):
    class_: Optional[Class] = None
    
    class Config:
        orm_mode = True


class UserWithClasses(User):
    classes: List[Class] = None
    
    class Config:
        orm_mode = True


class ClassSubjectsWithUser(BaseModel):
    subject: Subject
    teacher: Optional[User]
    
    class Config:
        orm_mode = True


class MessageWithUser(Message):
    user: User
    
    class Config:
        orm_mode = True


# DISCORD SCHEMAS
class DiscordInit(BaseModel):
    key: str
    guild_id: str


class DiscordGuildId(BaseModel):
    guild_id: str


# STATUS
class Status(BaseModel):
    bot: bool
    servers: int
