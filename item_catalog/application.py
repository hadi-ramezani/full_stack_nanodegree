from flask import (Flask,
                   render_template,
                   request, redirect,
                   url_for, flash,
                   jsonify)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').
                       read())['web']['client_id']
APPLICATION_NAME = "catalog-app"

engine = create_engine('sqlite:///itemcatalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def show_login():
    """Create a state using uppercase strings and digits and pass it to login.html.

    :return: the rendered template
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Handle authentication using google accounts.

    :return: an error response or an html output showing a successful
    authentication message
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: ' \
              '150px;-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Handle disconnecting a user from the app and clean up the
    login_session. Provide a response if revoking the token fails.

    :return: an appropriate response.
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
            'Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('categories'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
    return response


def create_user(login_session):
    """Create a User object and using the information in a login_session
     and return the user id.

    :param login_session: a login_session object
    :return: the user id that was created
    """
    new_user = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    """Find the user from the database and return it.

    :param user_id: the id of the user
    :return: the user object
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    """Use an email address to get the user id

    :param email: user's email address
    :return: user id or None if that email does not return any user
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


@app.route('/catalog/<string:category_name>/items/JSON')
def items_json(category_name):
    """Given a category name return a json object that contain all
    items in that category

    :param category_name: the category name
    :return: a json object
    """
    category_name = category_name.replace('+', ' ')
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    return jsonify(CategoryItem=[i.serialize for i in items])


@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def item_json(category_name, item_name):
    """Given a category_name and an item_name return a json
    representation of that item

    :param category_name: the category name
    :param item_name: the item name
    :return: a json object
    """
    category_name = category_name.replace('+', ' ')
    category = session.query(Category).filter_by(name=category_name).one()
    item_name = item_name.replace('+', ' ')
    item = session.query(CategoryItem).filter_by(
        name=item_name, category_id=category.id).first()
    return jsonify(CategoryItem=[item.serialize])


@app.route('/')
@app.route('/catalog/')
def categories():
    """Show all the categories in the database

    :return: a rendered html template showing all the categories
    """
    categories = session.query(Category)
    if 'username' not in login_session:
        return render_template('catalog.html', categories=categories,
                               public=True)
    return render_template('catalog.html', categories=categories,
                           public=False)


@app.route('/catalog/<string:category_name>/items/')
def items(category_name):
    """Show all the items in a category

    :param category_name: the name of the category
    :return: a rendered html template showing the items in a category
    """
    categories = session.query(Category)
    category_name = category_name.replace('+', ' ')
    category = session.query(Category).filter_by(name=category_name).one()
    creator = get_user_info(category.user_id)
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    if 'username' not in login_session or \
            creator.id != login_session['user_id']:
        return render_template('items.html',
                               categories=categories,
                               category=category,
                               items=items,
                               public=True,
                               creator=creator)
    return render_template('items.html',
                           categories=categories,
                           category=category,
                           items=items,
                           public=False,
                           creator=creator)


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def item(category_name, item_name):
    """Show an item

    :param category_name: the category name
    :param item_name: the item name
    :return: a rendered template showing the item
    """
    category_name = category_name.replace('+', ' ')
    category = session.query(Category).filter_by(name=category_name).one()
    item_name = item_name.replace('+', ' ')
    item = session.query(CategoryItem).filter_by(
        name=item_name, category_id=category.id).first()
    creator = get_user_info(item.user_id)
    if 'username' not in login_session or \
            creator.id != login_session['user_id']:
        return render_template('item.html',
                               item=item,
                               category=category,
                               public=True,
                               creator=creator)
    return render_template('item.html',
                           item=item,
                           category=category,
                           public=False,
                           creator=creator)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def new_category():
    """Handle creating a new category. If the user is not
    logged in redirect them to the login page.

    :return: a rendered template enabling the user to create a new category.
    """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        new_category = Category(name=request.form['name'],
                                user_id=login_session['user_id'])
        session.add(new_category)
        session.commit()
        flash("New category was successfully created!")
        return redirect(url_for('categories'))
    return render_template('new_category.html')


@app.route('/catalog/<string:category_name>/edit/', methods=['GET', 'POST'])
def edit_category(category_name):
    """Handle editing an existing category. If the user is not
    logged in redirect them to the login page.

    :param category_name: the name of the category
    :return: a rendered template enabling the user to edit a category.
    """
    category_name = category_name.replace('+', ' ')
    category = session.query(Category).filter_by(name=category_name).first()
    if 'username' not in login_session:
        return redirect('/login')
    if category.user_id != login_session['user_id']:
        return "<script>function myFunction()" \
               " {alert('You are not authorized to edit this category." \
               " Please create your own category in order to edit.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
        session.add(category)
        session.commit()
        flash("Category was successfully edited!")
        return redirect(url_for('categories', category_name=category_name))
    return render_template('edit_category.html', category=category)


@app.route('/catalog/<string:category_name>/delete/', methods=['GET', 'POST'])
def delete_category(category_name):
    """Handle deleting a category. If the user is not logged in
    redirect them to the login page.

    :param category_name: the name of the category
    :return: a rendered template enabling the user to delete a category.
    """
    category_name = category_name.replace('+', ' ')
    category = session.query(Category).filter_by(name=category_name).first()
    if 'username' not in login_session:
        return redirect('/login')
    if category.user_id != login_session['user_id']:
        return "<script>function myFunction()" \
               " {alert('You are not authorized to delete this category." \
               " Please create your own category in order to delete.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        flash("Category was successfully deleted!")
        return redirect(url_for('categories'))
    return render_template('delete_category.html', category=category)


@app.route('/catalog/<string:category_name>/new/', methods=['GET', 'POST'])
def new_item(category_name):
    """Handle creating a new item. If the user is not logged in
     redirect them to the login page.

    :param category_name: the name of the category
    :return: a rendered template enabling the user to create a new item.
    """
    if 'username' not in login_session:
        return redirect('/login')
    category_name = category_name.replace('+', ' ')
    category = session.query(Category).filter_by(name=category_name).one()
    if request.method == 'POST':
        new_item = CategoryItem(name=request.form['name'],
                                description=request.form['description'],
                                category_id=category.id,
                                user_id=login_session['user_id'])
        session.add(new_item)
        session.commit()
        flash("New item was successfully created!")
        return redirect(url_for('items', category_name=category_name))
    return render_template('new_item.html', category=category)


@app.route('/catalog/<string:category_name>/<string:item_name>/edit/',
           methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    """Handle editing an existing item. If the user is not logged in
     redirect them to the login page.

    :param category_name: the name of the category
    :param item_name: the item name
    :return: a rendered template enabling the user to edit an existing item.
    """
    category_name = category_name.replace('+', ' ')
    category = session.query(Category).filter_by(name=category_name).first()
    item_name = item_name.replace('+', ' ')
    item = session.query(CategoryItem).filter_by(
        name=item_name, category_id=category.id).first()
    if 'username' not in login_session:
        return redirect('/login')
    if category.user_id != login_session['user_id']:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit this item." \
               " Please create your own item in order to edit.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        flash("Item was successfully edited!")
        return redirect(url_for('items', category_name=category_name))
    return render_template('edit_item.html', category=category, item=item)


@app.route('/catalog/<string:category_name>/<string:item_name>/delete/',
           methods=['GET', 'POST'])
def delete_item(category_name, item_name):
    """Handle deleting an existing item. If the user is not logged in
     redirect them to the login page.

    :param category_name: the name of the category
    :param item_name: the item name
    :return: a rendered template enabling the user to delete an existing item.
    """

    category_name = category_name.replace('+', ' ')
    category = session.query(Category).filter_by(name=category_name).first()
    item_name = item_name.replace('+', ' ')
    item = session.query(CategoryItem).filter_by(
        name=item_name, category_id=category.id).first()
    if 'username' not in login_session:
        return redirect('/login')
    if category.user_id != login_session['user_id']:
        return "<script>function myFunction()" \
               " {alert('You are not authorized to delete this item." \
               " Please create your own item in order to delete.');}" \
               "</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item was successfully deleted!")
        return redirect(url_for('items', category_name=category_name))
    return render_template('delete_item.html', category=category, item=item)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=8000)
