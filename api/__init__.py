from flask import Flask, g
from functools import wraps

from common import Database

app = Flask(__name__)

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
