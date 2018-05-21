'''docstring'''
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# single_session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id=12):
    '''docstring'''
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants')
@app.route('/restaurants/')
def get_all_restaurants():
    '''docstring'''
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    output = ''
    for restaurant in restaurants:
        output += "<a href='/restaurants/"
        output += str(restaurant.id)
        output += "/'>"
        output += restaurant.name
        output += "</a>"
        output += "</br>"
    return output


# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    '''docstring'''
    return "page to create a new menu item. Task 1 complete!"


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_item_id>/edit/')
def editMenuItem(restaurant_id, menu_item_id):
    '''docstring'''
    return "page to edit a menu item. Task 2 complete!"


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_item_id>/delete/')
def deleteMenuItem(restaurant_id, menu_item_id):
    '''docstring'''
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
