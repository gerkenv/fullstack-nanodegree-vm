'''docstring'''
# import os
# import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class RestaurantMenu(object):
    '''docstring'''
    def __init__(self):
        self.session = None
        self.engine = None
        self.data_base_session = None

    def create_database_engine(self):
        '''docstring'''
        # check if engine is already exist
        if self.session is not None:
            return
        # choose database engine for communication
        self.engine = create_engine('sqlite:///restaurantmenu.db', echo=False)
        # let's bind the engine to the base class
        Base.metadata.bind = self.engine
        # create a sessionmaker object
        self.data_base_session = sessionmaker(bind=self.engine)
        # Create an instance of interface between SQLAlchemy and a database
        self.session = self.data_base_session()

        # Base.metadata.create_all(self.engine)

    def select_all_restaurants(self):
        self.create_database_engine()
        return self.session.query(Restaurant).all()

    def select_restaurant_by_id(self, restaurant_id):
        self.create_database_engine()
        try:
            return self.session.query(Restaurant).filter_by(id=restaurant_id).one()
        except:
            return None

    def update_restaurant(self, restaurant_id, restaurant_name):
        self.create_database_engine()
        restaurant = self.select_restaurant_by_id(restaurant_id)
        if restaurant is None:
            return False
        restaurant.name = restaurant_name
        self.session.add(restaurant)
        self.session.commit()
        return True

    def delete_restaurant(self, restaurant_id):
        self.create_database_engine()
        restaurant = self.select_restaurant_by_id(restaurant_id)
        if restaurant is None:
            return False
        self.session.delete(restaurant)
        self.session.commit()
        return True

    def add_new_restaurant(self, restaurant_name):
        self.create_database_engine()
        new_restaurant = Restaurant(name=restaurant_name)
        self.session.add(new_restaurant)
        self.session.commit()


class Restaurant(Base):
    '''docstring'''
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    '''docstring'''
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
