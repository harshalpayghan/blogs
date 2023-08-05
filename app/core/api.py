import json

from flask import blueprints, Blueprint
from flask_restful import Resource, Api

from app.core.app import BlogsDetails

blog = Blueprint("advance_pythondf", __name__, url_prefix="/blogs")

api = Api(blog)

api.add_resource(BlogsDetails, "/", methods=["GET"], endpoint="user")



