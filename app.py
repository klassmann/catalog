
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
def apiCatalogJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[r.serialize for r in categories])

# Front-End
@app.route('/')
def index():
    categories = session.query(Category).all()
    return render_template('index.html', categories=categories)

@app.route('/login')
def login():
    categories = session.query(Category).all()
    return render_template('login.html', categories=categories)