from flask import Blueprint, url_for, session, redirect, request
from flask_login import login_user, current_user
from server.models.users import User
from server.utils.google_api import create_oauth_url, get_oauth_tokens, get_user_email, create_credentials
from datetime import datetime, timedelta

auth = Blueprint(__name__, 'auth')

scopes = [
    'https://www.googleapis.com/auth/userinfo.email',
    'openid', 
    'https://www.googleapis.com/auth/youtube' 
]

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return { 'username': current_user.get_id(), 'redirect': False } 

    session['state'], url = create_oauth_url(url_for('server.routes.auth.callback', _external=True))
    return { 'redirect': True, 'redirect_url': url }

@auth.route('/oauth2callback')
def callback():
    if session.get('error', None):
        return redirect('/')

    if session['state'] != request.args.get('state', None):
        return redirect('/')

    tokens = get_oauth_tokens(url_for('server.routes.auth.callback', _external=True), request.args['code'])
    email = get_user_email(tokens['access_token'])
    user = User.get(email)

    if not user:
        user = User(
            _id=email,
            subscriptions=[],
            collections=[],
            credentials=create_credentials(tokens),
            last_updated=datetime.utcnow()
        )

        user.insert()
    else:
        user.update({'credentials': create_credentials(tokens)})
    
    login_user(user, remember=True, duration=timedelta(30))

    return redirect('/')
