
import settings

from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask import jsonify

app = Flask(__name__)
app.secret_key = settings.SECRET

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Category, Base, Item

engine = create_engine(settings.DATABASE)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# API
@app.route('/catalog.json')
def apiAllCatalogJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[r.serialize for r in categories])

@app.route('/<int:category_id>/catalog.json')
def apiCatalogJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    return jsonify(Category=category.serialize)

# Front-End
@app.route('/')
def index():
    categories = session.query(Category).all()
    return render_template('index.html', categories=categories)

# Category
@app.route('/category/<int:category_id>/')
def category_view(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('category/view.html', category=category, items=items)

@app.route('/category/new/', methods=['GET', 'POST'])
def category_new():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = Category(name=name, description=description)
        session.add(category)
        session.commit()
        flash('New Category added!')
        return redirect(url_for('index'))
    return render_template('category/new.html')

@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def category_edit(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category.name = name
        category.description = description
        session.add(category)
        session.commit()
        flash('Category {} updated!'.format(category.name))
        return redirect(url_for('index'))
    return render_template('category/edit.html', category=category)

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def category_delete(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        flash('Category {} deleted!'.format(category.name))
        session.delete(category)
        session.commit()
        return redirect(url_for('index'))
    return render_template('category/delete.html', category=category)

# Item
@app.route('/category/<int:category_id>/item/new/', methods=['GET', 'POST'])
def item_new(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        item = Item(name=name, description=description, category_id=category.id)
        session.add(item)
        session.commit()
        flash('New Item added in {}!'.format(category.name))
        return redirect(url_for('category_view', category_id=category.id))
    return render_template('item/new.html', category=category)

@app.route('/login')
def login():
    categories = session.query(Category).all()
    return render_template('login.html', categories=categories)