"""
    Set up the flask app
"""
from flask import Flask, jsonify, request, current_app, g
from flask_jwt_extended import JWTManager

# Define the WSGI application object
flaskapp = Flask(__name__)
# declare the extensions
jwt = JWTManager()


def create_app(config):
    """
    Function that creates the app.
    """
    # global app object, configure it!
    flaskapp.config.from_object(config)

    configure_extensions(flaskapp)
    configure_error_handlers(flaskapp)
    configure_apis(flaskapp)

    return flaskapp


def configure_extensions(app, socket=False, main=True):
    """
    Configures the extensions being used
    """

    # db.init_app(app)  # flask-sqlalchemy
    # ma.init_app(app)  # flask-marshmallow
    # configure_jwt(app)  # jwt authentication
    return


def configure_jwt(app):
    """
    Configure the jwt extension and its extras
    """

    # initialise the extension
    jwt.init_app(app)

    # the default response dictionary
    resp_dict = {'data': [], 'total': 0, 'success': False}

    @jwt.expired_token_loader
    def jwt_expired_token_callback(expired_token):
        """
        Changing to change 'msg' key to 'message' and adding extra response
        keys

        :param expired_token:
            the expired token info
        """
        resp_dict['message'] = 'The {} token has expired'.format(
            expired_token['type'])
        return jsonify(resp_dict), 401

    @jwt.invalid_token_loader
    def jwt_invalid_token_callback(error_string):
        """
        Changing to change 'msg' key to 'message' and adding extra response
        keys

        :param error_string:
            String indicating why the token is invalid
        """
        resp_dict['message'] = error_string
        return jsonify(resp_dict), 401

    @jwt.unauthorized_loader
    def jwt_unauthorized_callback(error_string):
        """
        Changing to change 'msg' key to 'message' and adding extra response
        keys

        :param error_string:
            String indicating why this request is unauthorized
        """
        resp_dict['message'] = error_string
        return jsonify(resp_dict), 401

    @jwt.needs_fresh_token_loader
    def jwt_needs_fresh_token_callback():
        """
        Changing to change 'msg' key to 'message'
        """
        resp_dict['message'] = 'Fresh token required'
        return jsonify(resp_dict), 401

    @jwt.revoked_token_loader
    def jwt_revoked_token_callback():
        """
        Changing to change 'msg' key to 'message'
        """
        resp_dict['message'] = 'Token has been revoked'
        return jsonify(resp_dict), 401

    @jwt.user_loader_error_loader
    def jwt_user_loader_error_callback(identity):
        """
        Changing to change 'msg' key to 'message'

        :param identity:
            the identity of the user
        """
        resp_dict['message'] = 'Error loading the user {}'.format(identity)
        return jsonify(resp_dict), 401


def configure_error_handlers(app):
    """
    Configures the error handlers used
    """

    @app.errorhandler(404)
    def error_404(error):
        errors_50x(error, dont_send=True)
        if 'api.' in request.url:
            # was supposed to be an api call
            return jsonify({
                'data': [], 'total': 0, 'success': False,
                'message': 'Route not found'}), 404
        return '{}', 404

    @app.errorhandler(500)
    def error_500(error):
        errors_50x(error)
        return '{}', 500

    @app.errorhandler(501)
    def error_501(error):
        errors_50x(error)
        return '{}', 501

    @app.errorhandler(502)
    def error_502(error):
        errors_50x(error)
        return '{}', 502

    @app.errorhandler(503)
    def error_503(error):
        errors_50x(error)
        return '{}', 503


def configure_apis(app):
    """
    Configures the apis exposed
    """

    # blogs details apis
    from app.core.api import blog as blogs_module
    app.register_blueprint(blogs_module)
    from app.auth.app import admin as admin_module
    app.register_blueprint(admin_module)


def errors_50x(error, dont_send=False):
    """
    Logs the error, and sends out error email.
    """
    uid_name = '-1_guest'
    if 'current_user' in g and g.current_user:
        uid_name = str(g.current_user['row_id']) + '_' +\
            str(g.current_user['profile']['first_name'])

    e = 'User= ' + uid_name + ' accessed ' + request.url +\
        ' method= ' + request.method + ' with ip=' +\
        request.environ.get('REMOTE_ADDR', request.remote_addr)

    e += '\nargs = ' + str(request.args) + '\npost = ' + str(request.form) +\
        '\njson = ' + str(request.get_json())

    current_app.logger.exception(e)
    current_app.logger.exception(error)

    if dont_send:  # don't send the error
        return

    track = get_current_traceback(skip=1, show_hidden_frames=True,
                                  ignore_system_exceptions=False)
    e += '\n' + track.plaintext
    # #TODO: send out email?
