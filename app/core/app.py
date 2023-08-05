"""
Blog Api classes
"""
import json
from bson import json_util
from flask_restful import Resource

from app.utils.mongo_connector import MongoConnector


class BlogsDetails(Resource):
    def get(self):
        db_obj = MongoConnector()
        query = {'_id': 0, 'user_id': 1}
        data = db_obj.generic_selection(table_name="reactapp", database_name="test", query=query)
        # return json.loads(data)
        return json.loads(json_util.dumps(data))

    def post(self):
        db_obj = MongoConnector()

    def put(self):
        pass

    def delete(self):
        pass
