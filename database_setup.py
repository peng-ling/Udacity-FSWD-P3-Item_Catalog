import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import logging

# Uncomment for some more detailed logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

# Environment setup
Base = declarative_base()

engine = create_engine('sqlite:///itemcatalog.db', echo=True)

Base.metadata.bind = engine

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)

session = DBSession()


class Seri(Base):

    __tablename__ = "serialize"

    item_id = Column(Integer(), primary_key=True)
    username = Column(String(), primary_key=True)
    user_id = Column(Integer(), primary_key=True)
    category_name = Column(String(), primary_key=True)
    category_id = Column(Integer(), primary_key=True)
    item_title = Column(String(), primary_key=True)
    item_description = Column(String(), primary_key=True)

    @property
    def serialize(self):
        return {
            'item_id': self.item_id,
            'username': self.username,
            'category_id': self.category_id,
            'category_name': self.category_name,
            'item_title': self.item_title,
            'item_description': self.item_description
        }

# Table where User Information is stored, incl. password


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(250))
    password = Column(String(250))
    email = Column(String(250))


# Table for categories, cascades delete to related items.
class Category(Base):

    __tablename__ = "category"

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)
    item = relationship("Item", cascade="all,delete", backref="Category")

# Table where items are stored.


class Item(Base):

    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey("category.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)
    category = relationship(Category)
