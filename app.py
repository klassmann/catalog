
import settings

from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask import jsonify
from flask import session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import random
import string

CLIENT_ID = json.loads(
    open('client_secret_google.json', 'r').read())['web']['client_id']

app = Flask(__name__)
app.secret_key = settings.SECRET

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Category, Base, Item

engine = create_engine(settings.DATABASE)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

def get_state_token():
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))

# API
@app.route('/api/catalog.json')
def api_catalog():
    categories = dbsession.query(Category).all()
    return jsonify(Category=[r.serialize for r in categories])

@app.route('/api/<int:category_id>/category.json')
def api_catalog_category(category_id):
    category = dbsession.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=category.serialize)

# Front-End
@app.route('/')
def index():
    session['state'] = get_state_token()
    categories = dbsession.query(Category).all()
    return render_template('index.html', categories=categories)

# Category
@app.route('/category/<int:category_id>/')
def category_view(category_id):
    session['state'] = get_state_token()
    category = dbsession.query(Category).filter_by(id=category_id).one()
    items = dbsession.query(Item).filter_by(category_id=category.id).all()
    return render_template('category/view.html', category=category, items=items)

@app.route('/category/new/', methods=['GET', 'POST'])
def category_new():
    session['state'] = get_state_token()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = Category(name=name, description=description)
        dbsession.add(category)
        dbsession.commit()
        flash('New Category added!')
        return redirect(url_for('index'))
    return render_template('category/new.html')

@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def category_edit(category_id):
    session['state'] = get_state_token()
    category = dbsession.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category.name = name
        category.description = description
        dbsession.add(category)
        dbsession.commit()
        flash('Category {} updated!'.format(category.name))
        return redirect(url_for('index'))
    return render_template('category/edit.html', category=category)

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def category_delete(category_id):
    session['state'] = get_state_token()
    category = dbsession.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        message = 'Category {} deleted!'.format(category.name)
        dbsession.delete(category)
        dbsession.commit()
        flash(message)
        return redirect(url_for('index'))
    return render_template('category/delete.html', category=category)

# Item
@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def item_new(category_id):
    session['state'] = get_state_token()
    category = dbsession.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        item = Item(name=name, description=description, category_id=category.id)
        dbsession.add(item)
        dbsession.commit()
        flash('New Item added in {}!'.format(category.name))
        return redirect(url_for('category_view', category_id=category.id))
    return render_template('item/new.html', category=category)

@app.route('/category/<int:category_id>/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def item_edit(category_id, item_id):
    session['state'] = get_state_token()
    category = dbsession.query(Category).filter_by(id=category_id).one()
    item = dbsession.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        item.name = name
        item.description = description
        dbsession.add(item)
        dbsession.commit()
        flash('Item {} updated!'.format(item.name))
        return redirect(url_for('category_view', category_id=category.id))
    return render_template('item/edit.html', category=category, item=item)

@app.route('/category/<int:category_id>/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def item_delete(category_id, item_id):
    session['state'] = get_state_token()
    category = dbsession.query(Category).filter_by(id=category_id).one()
    item = dbsession.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        message = 'Item {} deleted!'.format(item.name)
        dbsession.delete(item)
        dbsession.commit()
        flash(message)
        return redirect(url_for('category_view', category_id=category.id))
    return render_template('item/delete.html', category=category, item=item)

# Auth
# @app.route('/login')
# def login():
#     categories = dbsession.query(Category).all()
#     return render_template('login.html', categories=categories)

def response_success(msg):
    response = make_response(json.dumps(msg), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

def response_error(msg):
    response = make_response(json.dumps(msg), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/oauthcallback/google/', methods=['POST'])
def gconnect():
    if request.args.get('state') != session.get('state'):
        return response_error('Invalid state parameter.')

    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret_google.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return response_error('Failed to upgrade the authorization code.')

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return response_error(result.get('error'))

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return response_error("Token's user ID doesn't match given user ID.")

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return response_error("Token's client ID does not match app's.")

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return response_success('Current user is already connected.')

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    return response_success('You are logged in.')

@app.route('/google/disconnect/')
def gdisconnect():
    access_token = session.get('access_token')

    if not access_token:
        return response_error('User is not connected.')

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del session['username']
        del session['picture']
        del session['email']
        del session['access_token']
        del session['gplus_id']
        flash('User disconnected')
        return redirect('/')
        flash('Failed to revoke token for given user')
    return redirect('/')
