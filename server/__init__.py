from flask import Flask, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_login import LoginManager
from os import getenv, urandom, environ

STATIC_FOLDER = 'dist'

if getenv('FLASK_ENV') == 'development':
    from dotenv import load_dotenv

    STATIC_FOLDER = 'build'
    load_dotenv('.env')
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    

app = Flask(__name__, static_folder=f'../client/{STATIC_FOLDER}', static_url_path='/', template_folder=f'../client/{STATIC_FOLDER}')
app.secret_key = urandom(16)

db = PyMongo(app, uri=getenv('DATABASE_URI')).db

login_manager = LoginManager(app)

from server.models.users import User

@login_manager.user_loader
def load_user(email):
    return User.get(email)

CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

from server.routes.auth import auth

app.register_blueprint(auth, url_prefix='/api/auth')