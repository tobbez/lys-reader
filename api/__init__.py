from flask import Flask, g
from simplekv.fs import FilesystemStore
from flaskext.kvsession import KVSessionExtension
from functools import wraps

from common import Database

store = FilesystemStore('session')

app = Flask(__name__)

app.config.from_pyfile('../config.defaults.py')
app.config.from_pyfile('../config.py')
app.secret_key = app.config['SECRET_KEY']

KVSessionExtension(store, app)

""" Pass a connection to the function
    and then put it away when the function
    is done """
def database(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """ If flask.g.db is not set yet,
            set it. """
        if not hasattr(g, 'db'):
            g.db = Database(app.config)

        con = g.db.get_connection()
        
        kwargs['connection'] = con
        result = f(*args, **kwargs)
        
        g.db.put_away_connection(con)
        
        return result
    return decorated_function

import api.userview
