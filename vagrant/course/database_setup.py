import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///restaurantmenu.db', echo=True)

Base.metadata.bind=engine

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind = engine)

session = DBSession()

#schakka

class Restaurant(Base):

    __tablename__ = "restaurant"

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)


class MenuItem(Base):

    __tablename__ = "menu_item"

    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description =  Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship(Restaurant)

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
#session.commit()
