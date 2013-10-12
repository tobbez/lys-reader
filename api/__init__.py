from flask import Flask

# Global database object
db = None
app = Flask(__name__)

import api.views
