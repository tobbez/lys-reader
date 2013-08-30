from flask import Flask
from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension

# Use DictStore until the code is ready for production
store = DictStore()
app = Flask(__name__)
app.secret_key = ''

KVSessionExtension(store, app)

import api.userview
