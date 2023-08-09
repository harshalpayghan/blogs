"""
Blog Api classes
"""
import json
from bson import json_util
from flask import request
from flask_restful import Resource

from app.auth.app import token_required
from app.utils.mongo_connector import MongoConnector


class BlogsDetails(Resource):
    @token_required
    def get(self):
        db_obj = MongoConnector()
        query = {'_id': 0, 'title_name': 1, 'blogs': 1}
        data = db_obj.generic_selection(table_name="blogs_details", database_name="blogs", query=query)
        print(data)
        if data:
            return json.loads(json_util.dumps(data))
        else:
            return []

    @token_required
    def post(self):
        data = request.get_json()
        db_obj = MongoConnector()
        db_obj.generic_insert_one(database_name="blogs", table_name="blogs_details", data=data)

    @token_required
    def put(self):
        data = request.get_json()
        selection_criteria = {}
        update_data = {}
        if data:
            selection_criteria = {"user_id": data["user_id"], "title_name": data["title_name"]}
            update_data = {"comment": {
                               "commented_user_id": data["commented_user_id"],
                               "comment": data["comment"]
                               }
                           }
            db_obj = MongoConnector()
            db_obj.generic_update(database_name="blogs", table_name="blogs_details",
                                  selection_criteria=selection_criteria, update_data=update_data)

    def delete(self):
        pass
