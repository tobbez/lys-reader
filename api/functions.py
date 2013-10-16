from flask import make_response, jsonify, session, request, g
from functools import wraps
from os import urandom
from datetime import datetime, timedelta
from base64 import b64encode

from api import app, db
from common.database import Database

def require_csrf_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'csrf' in session or not 'csrf_token' in request.json \
            or session['csrf'] != request.json['csrf_token'] or datetime.now() > session['csrf_expire']:
            generate_csrf_token(session)
            return make_response(jsonify({ 'status': {'code': 2, 'message':'csrf token invalid'}}), 400)

        generate_csrf_token(session)
        kwargs['csrf'] = session['csrf']

        return f(*args, **kwargs)
    return decorated_function

def require_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'loggedin' in session or not session['loggedin']:
            return make_response(jsonify({ 'status': {'code': 1, 'message':'User not logged in'}}), 400)
        return f(*args, **kwargs)
    return decorated_function

""" Pass a connection to the function
    and then put it away when the function
    is done """
def database(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global db
        """ If db is not set yet,
            set it. """
        if not db:
            db = Database(app.config)

        con = db.get_connection()
        
        kwargs['connection'] = con
        result = f(*args, **kwargs)
        
        db.put_away_connection(con)
        
        return result
    return decorated_function

def generate_csrf_token(session):
    expire_time = datetime.now() + timedelta(minutes=15)
    token = b64encode(urandom(30))
    session['csrf'] = token.decode('UTF-8')
    session['csrf_expire'] = expire_time

@database
def register_user(email, password, connection):

    if not is_user_registered(email):
        cur = connection.cursor()

        cur.execute('INSERT INTO lysr_user (email, password) VALUES (%s, %s)', (email, password))
        connection.commit()

        return True
    return False

@database
def check_user_credentials(email, password, connection):

    if is_user_registered(email):
        cur = connection.cursor()

        cur.execute('SELECT id FROM lysr_user WHERE email = %s and password = %s', (email, password))
        connection.commit()

        if cur.rowcount is 1:
            return cur.fetchone()[0]

        return None

@database
def is_user_registered(email, connection):
    cur = connection.cursor()

    cur.execute('SELECT id FROM lysr_user WHERE email = %s', (email,))
    connection.commit()

    if cur.rowcount is 0:
        return False

    return True

@database
def get_unread(id, connection):
    cur = connection.cursor()

    cur.execute('SELECT COUNT(*) FROM lysr_feed_entry_status WHERE read = FALSE and id = %s;', (id,))
    connection.commit()

    return cur.fetchone()[0]

