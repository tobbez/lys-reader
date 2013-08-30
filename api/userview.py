from flask import abort, request, jsonify, make_response, session
from api import app
from api.user import *

@app.route('/api/user/register', methods = ['POST'])
def api_user_register():
    if 'email' in request.json and 'password' in request.json:
        if register_user(request.json['email'], request.json['password']):
            return make_response(jsonify({ 'status':'OK', 'message':'User account created'}), 200)
        else:
            return make_response(jsonify({ 'status':'FAIL', 'message':'User account not created'}), 200)

    return make_response(jsonify({ 'status':'BAD REQUEST', 'message':'Missing parameters'}), 400)

@app.route('/api/user/login', methods = ['POST'])
def api_user_login():
    if 'email' in request.json and 'password' in request.json:
        id = check_user_credentials(request.json['email'], request.json['password'])
        if id is not None:
            session = app.open_session(request)
            session['id'] = id
            session['loggedin'] = True
            response = make_response(jsonify({ 'status':'OK', 'message':'User logged in successfully'}), 200)
            app.save_session(session, response)
        else:
             response = make_response(jsonify({ 'status':'FAIL', 'message':'Email and password combination did not match'}), 200)
        return response
    return make_response(jsonify({ 'status':'BAD REQUEST', 'message':'Missing parameters'}), 400)

@app.route('/api/user/logout')
@require_loggedin
def api_user_logout():
    session.destroy()
    response = make_response(jsonify({ 'status':'OK', 'message':'User logged out successfully'}), 200)
    return response

