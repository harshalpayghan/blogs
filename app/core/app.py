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
        try:
            db_obj = MongoConnector()
            query = {'_id': 0, 'title_name': 1, 'blogs': 1, 'comment': 1}
            data = db_obj.generic_selection(table_name="blogs_details", database_name="blogs", query=query)
            print(data)
            if data:
                return json.loads(json_util.dumps(data))
            else:
                return json.loads(json_util.dumps({'message': 'Data Not Found'}))
        except Exception as e:
            print(str(e))
            return json.loads(json_util.dumps({'message': "Error Occurred While Fetching Data"}))

    @token_required
    def post(self):
        """ Used to create new post payload request
        Input_data = {"user_id" : ""
        "title_name" : ""
        "blogs" : "",
        "description" : "",
        "create_time": "",
        "update_time" : "",
        "comment" : []}
        """
        try:
            data = request.get_json()
            db_obj = MongoConnector()
            if data and "user_id" not in data:
                return json.loads(json_util.dumps({'message': 'User Id Missing'}))
            elif data and "title_name" not in data:
                return json.loads(json_util.dumps({'message': 'Title Name Missing'}))
            elif data and "blogs" not in data:
                return json.loads(json_util.dumps({'message': 'Blogs Details Missing'}))
            else:
                result = db_obj.generic_insert_one(database_name="blogs", table_name="blogs_details", data=data)
                return json.loads(json_util.dumps({'message': 'Blogs Details Successfully Inserted'}))
        except Exception as e:
            print(str(e))
            if e.__getattribute__("details")['errmsg']:
                return json.loads(json_util.dumps({'message': "Duplicate Title Key Error"}))
            return json.loads(json_util.dumps({'message': 'Error Occurred While Inserting Data'}))

    @token_required
    def put(self):
        try:
            data = request.get_json()
            selection_criteria = {}
            update_data = {}
            if data and "commented_user_id" not in data:
                return json.loads(json_util.dumps({'message': 'User Id Missing'}))
            elif data and "comment" not in data:
                return json.loads(json_util.dumps({'message': 'Comment Test Missing'}))
            else:
                selection_criteria = {"user_id": data["user_id"], "title_name": data["title_name"]}
                update_data = {"comment": {
                                   "commented_user_id": data["commented_user_id"],
                                   "comment": data["comment"]
                                   }
                               }
                db_obj = MongoConnector()
                db_obj.generic_update(database_name="blogs", table_name="blogs_details",
                                      selection_criteria=selection_criteria, update_data=update_data)
        except Exception as e:
            print(str(e))
            return json.loads(json_util.dumps({'message': 'Error Occurred While Updating Data'}))

    def delete(self):
        pass
