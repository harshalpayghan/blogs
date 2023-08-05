from datetime import datetime
from functools import wraps

import jwt
from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash

from app.utils.mongo_connector import MongoConnector
from main import app


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            db_obj = MongoConnector()
            query = {'user_id': data['user_id']}
            data = db_obj.generic_selection_one(table_name="reactapp", database_name="test", query=query)
        except:
            return jsonify({'message': 'token is invalid'})

        return f(data['user_id'], *args, **kwargs)

    return decorator


@app.route('/register', methods=['POST'])
def signup_user():
    return jsonify({'message': 'registeration successfully'})


# @app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    # user = Users.query.filter_by(name=auth.username).first()
    db_obj = MongoConnector()
    query = {'user_id': auth.username}
    data = db_obj.generic_selection_one(table_name="reactapp", database_name="test", query=query)

    if check_password_hash(data['password'], auth.password):
        token = jwt.encode(
            {'public_id': data.user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            app.config['SECRET_KEY'], "HS256")
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})