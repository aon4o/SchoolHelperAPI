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
    key: str

    class Config:
        orm_mode = True


# SUBJECTS
class SubjectBase(BaseModel):
    name: str


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int
    
    class Config:
        orm_mode = True


# CHANNEL CATEGORIES
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
    guild_id = str
    username = str
    email = str
    first_name = str
    last_name = str


class UserCreate(UserBase):
    password = str


class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True
