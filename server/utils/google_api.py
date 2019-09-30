from requests import get, post
from urllib import parse
from base64 import b64encode
from os import getenv, urandom

scopes = [
    'https://www.googleapis.com/auth/userinfo.email',
    'openid', 
    'https://www.googleapis.com/auth/youtube' 
]

def create_oauth_url(callback_url: str) -> tuple:
    params = {
        'client_id': getenv('CLIENT_ID'),
        'redirect_uri': callback_url,
        'scope': ' '.join(scopes),
        'response_type': 'code',
        'access_type': 'offline',
        'include_granted_scopes': 'true',
        'state': b64encode(urandom(16)).decode('utf-8'),
    }
    url = 'https://accounts.google.com/o/oauth2/v2/auth?' + parse.urlencode(params)
    return ( params['state'], url )


def get_oauth_tokens(callback_url: str, code: str) -> dict:
    params = {
        'code': code,
        'client_id': getenv('CLIENT_ID'),
        'client_secret': getenv('CLIENT_SECRET'),
        'redirect_uri': callback_url,
        'grant_type': 'authorization_code'
    }
    return post('https://oauth2.googleapis.com/token', data=params).json()


def get_user_email(access_token: str) -> str:
    return get(
        url='https://www.googleapis.com/oauth2/v2/userinfo', 
        headers={ 'Authorization': f'Bearer {access_token}' },
        params={ 'fields': 'email' }
    ).json()['email']


def create_credentials(oauth_response: dict) -> dict:
    return {
        'access_token': oauth_response['access_token'], 
        'refresh_token': oauth_response['refresh_token'],
        'expires in': oauth_response['expires_in'],
        'scope': oauth_response['scope']
    }