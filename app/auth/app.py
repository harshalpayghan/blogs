from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, jsonify, make_response, current_app, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash

from app.utils.mongo_connector import MongoConnector

admin = Blueprint("fadvance_python_admin", __name__, url_prefix="/admin")


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            db_obj = MongoConnector()
            query = {'user_id': data['public_id']}
            data = db_obj.generic_selection_one(table_name="users", database_name="blogs", query=query)
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs), 200

    return decorator


@admin.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    try:
        db_obj = MongoConnector()
        user_data = {"user_id": data["user_id"],
                     "password": hashed_password,
                     "user_firstname": data["user_firstname"],
                     "user_lastname": data["user_lastname"],
                     "email": data["email"],
                     "mobile_no": data["mobile_no"],
                     "address": data["address"]}
        db_obj.generic_insert_one(database_name="blogs", table_name="users", data=user_data)
        return jsonify({'message': 'registration successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'error occurred while Registration'})


@admin.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    db_obj = MongoConnector()
    query = {'user_id': auth.username}
    data = db_obj.generic_selection_one(table_name="users", database_name="blogs", query=query)

    if check_password_hash(data['password'], auth.password):
        token = jwt.encode(
            {'public_id': data['user_id'], 'exp': datetime.utcnow() + timedelta(minutes=45)},
            current_app.config['SECRET_KEY'], "HS256")
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})