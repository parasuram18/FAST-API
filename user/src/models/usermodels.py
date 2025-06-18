# from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, Date, DateTime, Time, Interval, JSON, ARRAY, func, UniqueConstraint, Index, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import EmailStr
import bcrypt, base64
from argon2 import PasswordHasher
from typing import Optional

# Base class for SQLalchemy
class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

# use this class to store timestamps
class TimeStamp:
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), nullable=True)
    modified_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now(), nullable=True)

class RoleMaster(Base):
    __tablename__ = "role_master"
    
    role_name : Mapped[str] = Column(String(15), nullable=True)
    description : Mapped[str] = mapped_column(String, nullable=True)
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)

    users = Relationship('RoleMapping', lazy='selectin')
    
    __table_args__ = (
        UniqueConstraint('role_name', name='unique_role'),
    )

class CustomUser(Base, TimeStamp):
    __tablename__ = "custom_user"
    __table_args__ = ( # must be a tuple
        # UniqueConstraint('mobilenumber', 'email', name='unique_num_mail'),
        Index('user_index', 'mobilenumber', 'email'),
    )

    mobilenumber = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True, nullable=True)

    # profile = Relationship('UserPersonalProfile', uselist=False, lazy='selectin', back_populates='user')
    profile : Mapped[Optional['UserPersonalProfile']] = Relationship(uselist=False, lazy='selectin')
    roles = Relationship('RoleMapping', lazy='selectin')

    def set_password(self, psw):
        ph = PasswordHasher()
        self.password = ph.hash(psw)
    
    def check_password(self, psw):
        ph = PasswordHasher()
        try:
            isvalid = ph.verify(self.password, psw)
        except:
            isvalid = False
        return isvalid


class UserPersonalProfile(Base):
    __tablename__ = 'user_personal_profile'

    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(JSONB, default=dict, nullable=True)
    user_id = Column(Integer,ForeignKey('custom_user.id'))

    # user = Relationship('CustomUser', back_populates='profile')

class RoleMapping(Base):
    __tablename__ = 'role_mapping'
    
    role = Column(Integer, ForeignKey('role_master.id'), nullable=True)
    user = Column(Integer, ForeignKey('custom_user.id'), nullable=True)