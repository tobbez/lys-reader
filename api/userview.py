from flask import abort, request, jsonify, make_response, session
from datetime import datetime, timedelta
from api import app
from api.user import *

@require_csrf_token
@app.route('/api/signup/', methods = ['POST'])
def api_user_signup():
    if 'email' in request.json and 'password' in request.json:
        if register_user(request.json['email'], request.json['password']):
            return make_response(jsonify({ 'status': 'OK', 'message': 'User account created'}), 200)
        else:
            return make_response(jsonify({ 'status': 'FAIL', 'message': 'User account not created'}), 200)

    return make_response(jsonify({ 'status': 'BAD REQUEST', 'message': 'Missing parameters'}), 400)

@require_csrf_token
@app.route('/api/login/', methods = ['POST'])
def api_user_login():
    if 'email' in request.json and 'password' in request.json:
        id = check_user_credentials(request.json['email'], request.json['password'])
        if id is not None:
            session = app.open_session(request)
            session['id'] = id
            session['loggedin'] = True
            response = make_response(jsonify({ 'status': 'OK', 'message': 'User logged in successfully'}), 200)
            app.save_session(session, response)
        else:
             response = make_response(jsonify({ 'status': 'FAIL', 'message': 'Email and password combination did not match'}), 200)
        return response
    return make_response(jsonify({ 'status': 'BAD REQUEST', 'message': 'Missing parameters'}), 400)

@require_csrf_token
@require_authentication
@app.route('/api/logout/', methods = ['POST'])
def api_user_logout():
    session.destroy()
    response = make_response(jsonify({ 'status': 'OK', 'message': 'User logged out successfully'}), 200)
    return response

@app.route('/api/')
def api_root():
    generate_csrf_token(session)
    
    status = {'code': 200, 'message': 'Sucess'}
    response = make_response(jsonify({'csrf_token': session['csrf'], 'status': status}), 200)
    return response

