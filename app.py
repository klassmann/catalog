
import requests
import random
import string
import httplib2
import json

from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask import jsonify
from flask import session
from flask import make_response

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import settings
from database import Category, Base, Item

CLIENT_ID = json.loads(
    open('client_secret_google.json', 'r').read())['web']['client_id']

MSG_NOT_AUTHORIZED = 'You do not have authorization for {}.'

app = Flask(__name__)
app.secret_key = settings.SECRET
engine = create_engine(settings.DATABASE)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()


def get_state_token():
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32)
    )


# This function guarantee that b is a str
def bytes_to_str(b):
    if type(b) == bytes:
        return b.decode()
    return b


def response_success(msg):
    response = make_response(json.dumps(bytes_to_str(msg)), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


def response_error(msg):
    response = make_response(json.dumps(bytes_to_str(msg)), 401)
    response.headers['Content-Type'] = 'application/json'
    return response


def is_loggedin():
    return 'access_token' in session and 'gplus_id' in session


def get_userid():
    return session.get('gplus_id')

# Cross-Site Request Forgery Token
def update_csrf_token():
    new_csrf_token = get_state_token()
    session['csrf_token'] = new_csrf_token
    return new_csrf_token

# Cross-Site Request Forgery Verification
def correct_csrf():
    if request.form.get('csrf_token') != session.get('csrf_token'):
        flash('Invalid form data.')
        return False
    return True

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
    has_add_permission = is_loggedin()
    categories = dbsession.query(Category).all()
    return render_template(
        'index.html',
        categories=categories,
        has_add_permission=has_add_permission
    )


# Category
@app.route('/category/<int:category_id>/')
def category_view(category_id):
    has_add_permission = is_loggedin()
    category = dbsession.query(Category).filter_by(id=category_id).one()
    items = dbsession.query(Item).filter_by(category_id=category.id).all()
    return render_template(
        'category/view.html',
        category=category,
        items=items,
        has_add_permission=has_add_permission
    )


@app.route('/category/new/', methods=['GET', 'POST'])
def category_new():
    if not is_loggedin():
        flash(MSG_NOT_AUTHORIZED.format('add a new category'))
        return redirect('/')

    if request.method == 'POST':
        # Checking the CSRF token
        if not correct_csrf():
            return redirect(url_for('category_new'))

        name = request.form['name']
        description = request.form['description']
        category = Category(
            name=name,
            description=description,
            gplus_id=get_userid()
        )
        dbsession.add(category)
        dbsession.commit()
        flash('New Category added!')
        return redirect(url_for('index'))
    
    # New CSRF token
    csrf_token = update_csrf_token()
    return render_template('category/new.html', csrf_token=csrf_token)


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def category_edit(category_id):
    category = dbsession.query(Category).filter_by(id=category_id).one()

    if not is_loggedin():
        flash(MSG_NOT_AUTHORIZED.format('update the category'))
        return redirect('/')

    if category.gplus_id != session.get('gplus_id'):
        flash('You do not have authorization for update this category.')
        return redirect('/')

    if request.method == 'POST':

        if not correct_csrf():
            return redirect(url_for('category_edit', category_id=category_id))

        name = request.form['name']
        description = request.form['description']

        category.name = name
        category.description = description
        category.gplus_id = get_userid()

        dbsession.add(category)
        dbsession.commit()

        flash('Category {} updated!'.format(category.name))
        return redirect(url_for('index'))
    
    csrf_token = update_csrf_token()
    return render_template(
        'category/edit.html',
        category=category,
        csrf_token=csrf_token
    )


@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def category_delete(category_id):
    category = dbsession.query(Category).filter_by(id=category_id).one()

    if not is_loggedin():
        flash(MSG_NOT_AUTHORIZED.format('delete the category'))
        return redirect('/')

    if category.gplus_id != session.get('gplus_id'):
        flash(MSG_NOT_AUTHORIZED.format('delete this category'))
        return redirect('/')

    if request.method == 'POST':

        if not correct_csrf():
            return redirect(url_for('category_delete', category_id=category_id))

        message = 'Category {} deleted!'.format(category.name)
        dbsession.delete(category)
        dbsession.commit()
        flash(message)
        return redirect(url_for('index'))
    
    csrf_token = update_csrf_token()
    return render_template(
        'category/delete.html',
        category=category,
        csrf_token=csrf_token
    )


# Item

@app.route('/category/<int:category_id>/item/<int:item_id>/')
def item_view(category_id, item_id):
    category = dbsession.query(Category).filter_by(id=category_id).one()
    item = dbsession.query(Item).filter_by(id=item_id).one()
    return render_template('item/view.html', category=category, item=item)


@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def item_new(category_id):

    if not is_loggedin():
        flash(MSG_NOT_AUTHORIZED.format('add a new item'))
        return redirect('/')

    category = dbsession.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':

        if not correct_csrf():
            return redirect(url_for('item_new', category_id=category_id))

        name = request.form['name']
        description = request.form['description']
        item = Item(
            name=name,
            description=description,
            category_id=category.id,
            gplus_id=get_userid()
        )
        dbsession.add(item)
        dbsession.commit()
        flash('New Item added in {}!'.format(category.name))
        return redirect(url_for('category_view', category_id=category.id))
    
    csrf_token = update_csrf_token()
    return render_template(
        'item/new.html',
        category=category,
        csrf_token=csrf_token
    )


@app.route(
    '/category/<int:category_id>/item/<int:item_id>/edit/',
    methods=['GET', 'POST']
)
def item_edit(category_id, item_id):
    category = dbsession.query(Category).filter_by(id=category_id).one()
    item = dbsession.query(Item).filter_by(id=item_id).one()

    if not is_loggedin():
        flash(MSG_NOT_AUTHORIZED.format('update the item'))
        return redirect('/')

    if item.gplus_id != session.get('gplus_id'):
        flash(MSG_NOT_AUTHORIZED.format('update this item'))
        return redirect('/')

    session['state'] = get_state_token()

    if request.method == 'POST':

        if not correct_csrf():
            url = url_for(
                'item_edit',
                category_id=category_id,
                item_id=item_id
            )
            return redirect(url)

        name = request.form['name']
        description = request.form['description']
        item.name = name
        item.description = description
        item.gplus_id = get_userid()
        dbsession.add(item)
        dbsession.commit()
        flash('Item {} updated!'.format(item.name))
        return redirect(url_for('category_view', category_id=category.id))

    csrf_token = update_csrf_token()
    return render_template(
        'item/edit.html',
        category=category,
        item=item,
        csrf_token=csrf_token
    )


@app.route(
    '/category/<int:category_id>/item/<int:item_id>/delete/',
    methods=['GET', 'POST']
)
def item_delete(category_id, item_id):
    category = dbsession.query(Category).filter_by(id=category_id).one()
    item = dbsession.query(Item).filter_by(id=item_id).one()

    if not is_loggedin():
        flash(MSG_NOT_AUTHORIZED.format('delete the item'))
        return redirect('/')

    if item.gplus_id != session.get('gplus_id'):
        flash(MSG_NOT_AUTHORIZED.format('delete this item'))
        return redirect('/')

    session['state'] = get_state_token()

    if request.method == 'POST':

        if not correct_csrf():
            url = url_for(
                'item_delete',
                category_id=category_id,
                item_id=item_id
            )
            return redirect(url)

        message = 'Item {} deleted!'.format(item.name)
        dbsession.delete(item)
        dbsession.commit()
        flash(message)
        return redirect(url_for('category_view', category_id=category.id))

    csrf_token = update_csrf_token()
    return render_template(
        'item/delete.html',
        category=category,
        item=item,
        csrf_token=csrf_token
    )


# Authentication and Authorization
@app.route('/oauthcallback/google/', methods=['POST'])
def gconnect():
    if request.args.get('state') != session.get('state'):
        return response_error('Invalid state parameter.')

    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'client_secret_google.json',
            scope=''
        )
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return response_error('Failed to upgrade the authorization code.')

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(bytes_to_str(h.request(url, 'GET')[1]))
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
        msg = 'User is not connected.'
        return response_error(msg)

    # Revoke the access from Google
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # I am not expecting only a successful result, because sometimes
    # the browser is not logged and the session in backend still
    # logged in. I am cleaning always the session.
    if result['status'] == '200' or result['status'] == '400':
        del session['username']
        del session['picture']
        del session['email']
        del session['access_token']
        del session['gplus_id']
        flash('User disconnected')
        return redirect('/')

        flash('Failed to revoke token for given user')
    return redirect('/')
