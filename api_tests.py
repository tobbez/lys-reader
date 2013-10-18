from flask import Flask, g
import unittest
import json
#from simplekv.fs import FilesystemStore
#from flaskext.kvsession import KVSessionExtension
from datetime import datetime, timedelta

from api import app, db
from api.functions import register_user
from common.database import Database

class APITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global db
        #store = FilesystemStore('session')
        #KVSessionExtension(store, app)
        
        # Load the debug config
        app.config.from_pyfile('../config.defaults.py')
        app.config.from_pyfile('../config_debug.py')
        app.secret_key = app.config['SECRET_KEY']
        db = Database(app.config)

        cls._setup_database()
        app.testing = True
        cls.app = app.test_client(use_cookies=True)


    """Setup the database
        by clearing it and loading the schema"""
    @classmethod
    def _setup_database(self):
        con = db.get_connection()
        cur = con.cursor()

        schema = open('schema.sql', 'r')
        cur.execute(schema.read())
        schema.close()
        con.commit()
        
        db.put_away_connection(con)

    # Make the csrf_token test and make it expire in a min
    def _setup_csrf(self):
        with self.app.session_transaction() as sess:
            sess['csrf'] = 'test'
            sess['csrf_expire'] = datetime.now() + timedelta(minutes=1) 

    def _make_logged_in(self):
        with self.app.session_transaction() as sess:
            sess['loggedin'] = True

    # Test /
    def test_1_api_base(self):
        rv = self.app.get('/api/')
        data = json.loads(rv.data.decode('UTF-8'))
        assert data['status']['code'] is 0
        assert data['csrf_token']

    # Test registering a new user
    def test_2a_api_create_user(self):
        self._setup_csrf()
        
        rv = self.app.post('/api/signup/',
                data=json.dumps(dict(
                csrf_token='test',
                email='test@example.com',
                password='test')),
                content_type='application/json')

        data = json.loads(rv.data.decode('UTF-8'))
        assert data['status']['code'] is 0
        assert data['csrf_token']

    # Test that we can't register a user twice
    def test_2b_api_create_user(self):
        self._setup_csrf()
        
        rv = self.app.post('/api/signup/',
                data=json.dumps(dict(
                csrf_token='test',
                email='test@example.com',
                password='test')),
                content_type='application/json')

        data = json.loads(rv.data.decode('UTF-8'))
        assert data['status']['code'] is 5
        assert data['csrf_token']

    # Test missing param
    def test_2c_api_create_user(self):
        self._setup_csrf()
        
        rv = self.app.post('/api/signup/',
                data=json.dumps(dict(
                csrf_token='test',
                email='test@example.com')),
                content_type='application/json')

        data = json.loads(rv.data.decode('UTF-8'))
        assert data['status']['code'] is 3
        assert data['csrf_token']

    # Test login
    def test_3a_api_login(self):
        self._setup_csrf()

        rv = self.app.post('/api/login/',
                data=json.dumps(dict(
                csrf_token='test',
                email='test@example.com',
                password='test')),
                content_type='application/json')

        data = json.loads(rv.data.decode('UTF-8'))
        assert data['status']['code'] is 0
        assert data['csrf_token']

    # Test logout
    def test_4a_api_login(self):
        self._setup_csrf()
        self._make_logged_in()

        rv = self.app.post('/api/logout/',
                data=json.dumps(dict(
                csrf_token='test')),
                content_type='application/json')

        data = json.loads(rv.data.decode('UTF-8'))
        assert data['status']['code'] is 0

if __name__ == '__main__':
    unittest.main()
