'''docstring'''
from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# SESSION = DBSession()
# thread safe scoped sessions
# but we still missing thread-isolated creation of `SESSION` object
session_factory = sessionmaker(bind=engine)
SESSION = scoped_session(session_factory)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id=12, session=SESSION):
    '''docstring'''
    session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    session.remove()
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants')
@app.route('/restaurants/')
def get_all_restaurants(session=SESSION):
    '''docstring'''
    session()
    restaurants = session.query(Restaurant).all()
    session.remove()
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
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id, session=SESSION):
    '''docstring'''
    if request.method == 'GET':
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
    if request.method == 'POST':
        session()
        new_item = MenuItem(name=request.form['name'],
                            restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        session.remove()
        return redirect(url_for('RestaurantMenu', restaurant_id=restaurant_id))


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_item_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_item_id, session=SESSION):
    '''docstring'''
    if request.method == 'GET':
        session()
        item = session.query(MenuItem).filter_by(id=menu_item_id).one()
        session.remove()
        return render_template('editmenuitem.html',
                               restaurant_id=restaurant_id,
                               item=item)
    if request.method == 'POST':
        session()
        item = session.query(MenuItem).filter_by(id=menu_item_id).one()
        item.name = request.form['item_name']
        session.add(item)
        session.commit()
        session.remove()
        return redirect(url_for('RestaurantMenu', restaurant_id=restaurant_id))


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_item_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_item_id, session=SESSION):
    '''docstring'''
    if request.method == 'GET':
        session()
        item = session.query(MenuItem).filter_by(id=menu_item_id).one()
        session.remove()
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id,
                               item=item)
    if request.method == 'POST':
        session()
        item = session.query(MenuItem).filter_by(id=menu_item_id).one()
        session.delete(item)
        session.commit()
        session.remove()
        return redirect(url_for('RestaurantMenu', restaurant_id=restaurant_id))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
