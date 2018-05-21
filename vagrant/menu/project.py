'''docstring'''
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
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


@app.route('/restaurants/<int:restaurant_id>/json')
def get_restaurant_menu_json(restaurant_id, session=SESSION):
    '''docstring'''
    session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    session.remove()
    return jsonify(MenuItems=[item.serialize for item in items])


@app.route('/restaurants/<int:restaurant_id>/menu_items/<int:menu_item_id>/json')
def get_menu_item(restaurant_id=0, menu_item_id, session=SESSION):
    session()
    item = session.query(MenuItem).filter_by(id=menu_item_id).one()
    session.remove()
    return jsonify(MenuItem=item.serialize)


@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id=12, session=SESSION):
    '''docstring'''
    session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    session.remove()
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/')
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
                            course=request.form['course'],
                            description=request.form['description'],
                            price=request.form['price'],
                            restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        session.remove()
        flash("The item '" + request.form['name'] +
              "' is successfully added to database")
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
        item.course = request.form['item_course']
        item.description = request.form['item_description']
        item.price = request.form['item_price']
        session.add(item)
        session.commit()
        session.remove()
        flash("The item '" + request.form['item_name'] +
              "' is successfully updated in database")
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
        name = item.name
        session.delete(item)
        session.commit()
        session.remove()
        flash("The item '" + name +
              "' is successfully deleted from database")
        return redirect(url_for('RestaurantMenu', restaurant_id=restaurant_id))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
