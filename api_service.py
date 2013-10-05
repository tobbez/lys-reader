from api import app
from simplekv.fs import FilesystemStore
from flaskext.kvsession import KVSessionExtension

store = FilesystemStore('session')

app.config.from_pyfile('../config.defaults.py')
app.config.from_pyfile('../config.py')
app.secret_key = app.config['SECRET_KEY']

KVSessionExtension(store, app)

if __name__ == '__main__':
    app.run(debug = True)
