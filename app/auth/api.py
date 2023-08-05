import json

from flask import blueprints, Blueprint
from flask_restful import Resource, Api

from app.auth.app import login_user
from app.core.app import BlogsDetails

admin = Blueprint("fadvance_python_admin", __name__, url_prefix="/admin")

api = Api(admin)

api.add_resource(login_user, "/login", methods=["POST"], endpoint="userh")
