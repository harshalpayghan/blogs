from pymongo import MongoClient


class MongoConnector:
    def __init__(self):
        try:
            # self.client = MongoClient()
            self.client = MongoClient('localhost', 27017)
            print("Mongo DB connection created")
        except Exception as e:
            print(e)
            raise Exception(str(e))
    # example:- client = MongoClient(‘localhost’, 27017)

    def generic_selection(self, database_name=None, table_name=None, query=None):
        """
        Use to get data from collection
        :param database_name: str
        :param table_name: str
        :param query: str
        :return:
        """
        try:
            db = self.client[database_name]

            # Created or Switched to collection names
            collection = db[table_name]
            if query:
                collection_obj = collection.find({}, query)
            else:
                collection_obj = collection.find()
            query_result = [row for row in collection_obj]
            return query_result
        except Exception as e:
            print("error occurred while generic_selection")
            print(str(e))
            return None

    def generic_selection_one(self, database_name=None, table_name=None, query=None):
        """
        Use to get data from collection
        :param database_name: str
        :param table_name: str
        :param query: str
        :return:
        """
        try:
            db = self.client[database_name]

            # Created or Switched to collection names
            collection = db[table_name]
            if query:
                collection_obj = collection.find_one(query)
            else:
                collection_obj = collection.find()
            query_result = [row for row in collection_obj]
            return query_result
        except Exception as e:
            print("error occurred while generic_selection")
            print(str(e))
            return None

    def generic_insert_one(self, database_name=None, table_name=None, data=None):
        """
        Used to insert single record into collection
        :param database_name: str
        :param table_name: str
        :param data: dict
        :return: None
        """
        try:
            db = self.client[database_name]
            # Created or Switched to collection names
            collection = db[table_name]
            if isinstance(data, dict):
                collection.insert_one(data)
            return None
        except Exception as e:
            print("error occurred while inserting data")
            print(str(e))
            return None

    def generic_insert_many(self, database_name=None, table_name=None, data=None):
        """
        Use to insert multiple record in collection
        :param database_name: str
        :param table_name: str
        :param data: list
        :return: none
        """
        try:
            db = self.client[database_name]
            # Created or Switched to collection names
            collection = db[table_name]
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                print("error")
            return None
        except Exception as e:
            print("error occurred while inserting data")
            print(str(e))
            return None

    def generic_update(self, database_name=None, table_name=None, selection_data=None, update_data=None):
        """
        Use to insert multiple record in collection
        :param update_data: str
        :param selection_data: str
        :param database_name: str
        :param table_name: str
        :return: none
        """
        try:
            db = self.client[database_name]
            # Created or Switched to collection names
            collection = db[table_name]
            if isinstance(selection_data, dict) and isinstance(update_data, dict):
                collection.update_many(selection_data, {"$set": update_data})
            else:
                print("error")
            return None
        except Exception as e:
            print("error occurred while inserting data")
            print(str(e))
            return None


# abc = MongoConnector()
# rec = [{
#                 "user_id": 'harshp',
#                 "password": 'harshp',
#                 "age": 28
#             }]
# a= {"user_id": "harshalpayghan1"}
# b = {"age": 27, "user_id": "harshalpayghan"}
# abc.generic_update(database_name="test", table_name="reactapp", selection_data=a, update_data=b)
# abc.generic_selection(database_name="test", table_name="reactapp")
# abc.generic_insert_one(database_name="test", table_name="reactapp", data=rec)
# abc.generic_selection(database_name="test", table_name="reactapp")


"""
User collection
    user_id : str
    password : str
    user_firstname : str
    user_lastname : str
    email: str
    mobile_no : int
    address : str
    
blogsDetails collection
    user_id : str
    title : str
    blogs : str
    description : str
    create_time: timestamp
    update_time : timestamp
    comment : {
        commented_user_id : str
        comment : str
    }
"""