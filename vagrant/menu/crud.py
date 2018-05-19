import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

print '-----------------------------------------------'

''' 1.21 CRUD Create '''

# choose database engine for communication
engine = create_engine('sqlite:///restaurantmenu.db')
# let's bind the engine to the base class
Base.metadata.bind = engine
# create a sessionmaker object
DBSession = sessionmaker(bind=engine)
# Create an instance of interface between SQLAlchemy and a database
session = DBSession()
# Create a new restorant ( a new row in restaurant table )
myFirstRestaurant = Restaurant(name="Pizza Palace")
# Add a record to staging area
session.add(myFirstRestaurant)
# Commit the record to database
session.commit()

# Get all entries of restaurant table
# print session.query(Restaurant).all()

# Creata a new record for MenuItem database
cheesePizza = MenuItem(name="Cheese Pizza",
                       description="Some description",
                       course="Entree",
                       price="$8.99",
                       restaurant=myFirstRestaurant)
session.add(cheesePizza)
session.commit()

# get all rows of MenuItem database
# print session.query(MenuItem).all()

''' 1.23 CRUD Read '''

# get the single row class of the database
firstResult = session.query(Restaurant).first()
# get restaurant object
# print firstResult
# get `name` of restaurant object
# print firstResult.name

# here you need to execute 'lotsofmenus.py'
# so your DB will be populated with many items

# Get all entries of restaurant table
# print session.query(Restaurant).all()

# get all entries(rows) of MenuItem database
items = session.query(MenuItem).all()

# print name of each MenuItem
# for item in items:
#    print item.name

''' 1.25 CRUD Update '''

# select * from MenuItem where name = 'Veggie Burger'
veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')

# for veggieBurger in veggieBurgers:
#     print veggieBurger.id
#     print veggieBurger.price
#     print veggieBurger.restaurant.name
#     print "\n"

# step 1. get model of DB entry
# select * from MenuItem where id = 4 limit 1
urbanVeggieBurger = session.query(MenuItem).filter_by(id=4).one()

# print urbanVeggieBurger.name
# print urbanVeggieBurger.price

# step 2. change the price in DB entry model
urbanVeggieBurger.price = '$2.99'

# step 3. add object back to DB model
session.add(urbanVeggieBurger)

# step 4. commit cahnges to database
session.commit()

# select * from MenuItem where name = 'Veggie Burger'
veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')

# set price to $2.99 in every `veggie burger`
# for veggieBurger in veggieBurgers:
#     if veggieBurger.price != '$2.99':
#         veggieBurger.price = '$2.99'
#         session.add(veggieBurger)

session.commit()
''' 1.27 CRUD Delete '''

# get item
spinach = session.query(MenuItem).filter_by(name="Spinach Ice Cream").one()

# # print item properties
for field in spinach.__dict__:
     print '%s = %s' % (field, spinach.__dict__[field])

# # stage item for deletition
# session.delete(spinach)

# # commit staged changes
# session.commit()

# return deleted item
# auntieAnnsDiner = (
#     session.query(Restaurant)
#     .filter_by(id=10).one()
# )

# for field in auntieAnnsDiner.__dict__:
#     print '%s = %s' % (field, auntieAnnsDiner.__dict__[field])

# spinach = MenuItem(name="Spinach Ice Cream",
#                     description="vanilla ice cream made with organic spinach leaves",
#                     course="Dessert",
#                     price="$1.99",
#                     restaurant=auntieAnnsDiner)
# session.add(spinach)
# session.commit()

print '-----------------------------------------------'
