# coding: utf-8

from sqlalchemy import Column, DateTime, Float, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)


class Post(Base):
    __tablename__ = 'post'

    id = Column(INTEGER(11), primary_key=True)
    rating = Column(INTEGER(11), nullable=False)
    text = Column(Text, nullable=False)
    image_path = Column(Text, nullable=False)
    image_sharpness = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    menu_id = Column(INTEGER(11), nullable=False)


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
