from flask import Blueprint, url_for, session, redirect, request
from flask_login import login_user, current_user
from server.models.users import User
from requests import post, get
from urllib import parse
from os import getenv, urandom
from base64 import b64encode
from datetime import datetime, timedelta

auth = Blueprint(__name__, 'auth', url_prefix='/auth')

scopes = [
    'https://www.googleapis.com/auth/userinfo.email',
    'openid', 
    'https://www.googleapis.com/auth/youtube' 
]

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return { 'username': current_user.get_id(), 'redirect': False } 

    params = {
        'client_id': getenv('CLIENT_ID'),
        'redirect_uri': url_for('server.routes.auth.callback', _external=True),
        'scope': ' '.join(scopes),
        'response_type': 'code',
        'access_type': 'offline',
        'include_granted_scopes': 'true',
        'state': b64encode(urandom(16)).decode('utf-8'),
    }

    session['state'] = params['state']
    url = 'https://accounts.google.com/o/oauth2/v2/auth?' + parse.urlencode(params)

    return { 'redirect': True, 'redirect_url': url }

@auth.route('/oauth2callback')
def callback():
    if session.get('error', None):
        return redirect('/')

    if session['state'] != request.args.get('state', None):
        return redirect('/')

    data = {
        'code': request.args['code'],
        'client_id': getenv('CLIENT_ID'),
        'client_secret': getenv('CLIENT_SECRET'),
        'redirect_uri': url_for('server.routes.auth.callback', _external=True),
        'grant_type': 'authorization_code'
    }
    
    info = post('https://oauth2.googleapis.com/token', data=data).json()

    userinfo = get(
        url='https://www.googleapis.com/oauth2/v2/userinfo', 
        headers={ 'Authorization': f'Bearer {info["access_token"]}' },
        params={ 'fields': 'email' }
    ).json()

    user = User.get(userinfo['email'])

    credentials = {
        'access_token': info['access_token'], 
        'refresh_token': info['refresh_token'],
        'expires in': info['expires_in'],
        'scope': info['scope']
    }

    if not user:
        user = User(
            _id=userinfo['email'],
            subscriptions=[],
            collections=[],
            credentials=credentials,
            last_updated=datetime.utcnow()
        )

        user.insert()
    else:
        user.update({'credentials': credentials})
    
    login_user(user, remember=True, duration=timedelta(30))

    return redirect('/')
