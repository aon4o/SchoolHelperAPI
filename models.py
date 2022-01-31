import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, \
    SmallInteger, Time, UniqueConstraint, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from database import Base


class Subject(Base):
    __tablename__ = "subject"
    
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String(length=20), nullable=False)
    name = Column(String(length=50), nullable=False)
    
    UniqueConstraint('guild_id', 'name', name='guild_id_name_uc')


class GuildCategory(Base):
    __tablename__ = "guild_category"
    
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String(length=20), nullable=False)
    category_id = Column(String(length=50), nullable=False)
    
    UniqueConstraint('guild_id', 'name', name='guild_id_name_uc')


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String(length=20), nullable=False)
    username = Column(String(length=50), nullable=False)
    email = Column(String(length=50), nullable=False)
    password = Column(String(length=50), nullable=False)
    first_name = Column(String(length=50), nullable=False)
    last_name = Column(String(length=50), nullable=False)
