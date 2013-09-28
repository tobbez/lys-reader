from flask import abort, request, jsonify, make_response, session
from datetime import datetime, timedelta
from api import app
from api.user import *

@require_csrf_token
@app.route('/api/signup/', methods = ['POST'])
def api_user_signup():
    generate_csrf_token(session)
    status = {}
    httpcode = 200

    if 'email' in request.json and 'password' in request.json:
        if register_user(request.json['email'], request.json['password']):
            status['code'] = 0
            status['message'] = 'Success'
        else:
            status['code'] = 1 
            status['message'] = 'Could not register user, maybe user already exists?'

    else:
        status['code'] = 2
        status['message'] = 'Missing paramter(s)'
        httpcode = 400

    return make_response(jsonify({ 'csrf_token': session['csrf'], 'status': status }), httpcode)

@require_csrf_token
@app.route('/api/login/', methods = ['POST'])
def api_user_login():
    generate_csrf_token(session)
    status = {}
    httpcode = 200

    if 'email' in request.json and 'password' in request.json:
        id = check_user_credentials(request.json['email'], request.json['password'])
        if id is not None:
            session['id'] = id
            session['loggedin'] = True
            status['code'] = 0
            status['message'] = 'Success'
        else:
            status['code'] = 4
            status['message'] = 'Email and password combination did not match'
    else:
        status['code'] = 2
        status['message'] = 'Missing paramter(s)'
        httpcode = 400

    return make_response(jsonify({ 'csrf_token': session['csrf'], 'status': status }), httpcode)

@require_csrf_token
@require_authentication
@app.route('/api/logout/', methods = ['POST'])
def api_user_logout():
    session['loggedin'] = False
    response = make_response(jsonify({ 'status': {'code': '0', 'message': 'User logged out successfully'}}), 200)
    return response

@app.route('/api/')
def api_root():
    generate_csrf_token(session)
    
    status = {'code': 0, 'message': 'Sucess'}
    response = make_response(jsonify({'csrf_token': session['csrf'], 'status': status}), 200)
    return response

