import os
from datetime import datetime
from functools import wraps

from flask import Flask, request, blueprints, jsonify, make_response
import jwt
from werkzeug.security import check_password_hash

# import pandas as pd
from app import create_app

config_module = os.environ.get('config_module', 'config')
print(config_module)

app = create_app(config_module)
app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'


@app.route("/")
def app_status():
    return "Blog Service is running", 200


# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#
#         token = None
#
#         if 'x-access-tokens' in request.headers:
#             token = request.headers['x-access-tokens']
#
#         if not token:
#             return jsonify({'message': 'a valid token is missing'})
#
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#             current_user = Users.query.filter_by(public_id=data['public_id']).first()
#         except:
#             return jsonify({'message': 'token is invalid'})
#
#         return f(current_user, *args, **kwargs)
#
#     return decorator


# @app.route('/register', methods=['POST'])
# def signup_user():
#     return jsonify({'message': 'registeration successfully'})



if __name__ == "__main__":
    app.run()



# import os

# from app import create_app
#
# # get the config module from yaml env
# config_module = os.environ.get('config_module', 'config')
#
# # create the app
# flaskapp = create_app(config_module)
#
# if __name__ == '__main__':
#     flaskapp.run(debug=flaskapp.debug)