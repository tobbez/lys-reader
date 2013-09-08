from flask import Flask
from simplekv.fs import FilesystemStore
from flaskext.kvsession import KVSessionExtension

from common import Database

store = FilesystemStore('session')

app = Flask(__name__)

app.config.from_pyfile('../config.defaults.py')
app.config.from_pyfile('../config.py')
app.secret_key = app.config['SECRET_KEY']

KVSessionExtension(store, app)

DB = Database(app.config)

import api.userview
